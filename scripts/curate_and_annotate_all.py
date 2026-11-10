"""Generate accurate ground-truth sneaker bounding boxes for the 15 live camera crops."""
import glob
import os
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np
from ultralytics import YOLO

from src.footwear.roi import extract_lower_body_roi


def segment_feet_boxes(crop: np.ndarray, known_boxes: List[List[float]]) -> List[List[float]]:
    """Segment and refine accurate sneaker bounding boxes in lower-body crop.

    Rules:
    - Shoes sit in lower 55% of crop.
    - Single shoe aspect ratio is roughly 1.3 to 2.5.
    - Thin shadows (height < 30 or aspect > 3.5) are discarded.
    - Overlapping feet in a wide blob are split.
    - Never split a single normal shoe.
    """
    h, w = crop.shape[:2]

    # Filter known detections: keep confident boxes on the floor
    valid_known = []
    for b in known_boxes:
        bx1, by1, bx2, by2 = b
        bw = bx2 - bx1
        bh = by2 - by1
        if by2 > h * 0.50 and bw > 40 and bh > 35 and (bw / bh) < 3.2:
            valid_known.append([max(0, bx1), max(0, by1), min(w, bx2), min(h, by2)])

    # Dark foot mask for dark sneakers on light tile
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    shoe_mask = ((gray < 85) & (crop[:, :, 0] < 95)).astype(np.uint8) * 255
    shoe_mask[:int(h * 0.45), :] = 0  # Ignore upper legs/pants

    # Morphological closing
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    shoe_mask = cv2.morphologyEx(shoe_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(shoe_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1200:
            cx, cy, cw, ch = cv2.boundingRect(c)
            aspect = cw / float(ch)
            # Discard thin horizontal baseboard or floor reflections
            if ch >= 35 and aspect < 3.5 and (cy + ch) > h * 0.60:
                clean_contours.append([cx, cy, cx + cw, cy + ch])

    # If model found 2 separate valid shoes with good confidence
    if len(valid_known) == 2:
        return sorted(valid_known, key=lambda b: b[0])

    # If model found 1 valid shoe
    if len(valid_known) == 1:
        k = valid_known[0]
        kx1, ky1, kx2, ky2 = k
        second_box = None
        for cb in clean_contours:
            cx1, cy1, cx2, cy2 = cb
            # Non-overlapping distinct contour
            if cx2 < (kx1 - 20) or cx1 > (kx2 + 20):
                second_box = cb
                break
        if second_box:
            return sorted([k, second_box], key=lambda b: b[0])
        return [k]

    # If model found 0 valid shoes, use clean contours
    if len(clean_contours) == 2:
        return sorted(clean_contours, key=lambda b: b[0])
    elif len(clean_contours) == 1:
        cx1, cy1, cx2, cy2 = clean_contours[0]
        cw = cx2 - cx1
        ch = cy2 - cy1
        # If very wide (> 250px) where both feet are overlapping side by side
        if cw > 250 and (cw / float(ch)) > 1.6:
            mid_x = cx1 + int(cw * 0.48)
            box1 = [cx1, cy1, mid_x + 15, cy2]
            box2 = [mid_x - 15, cy1, cx2, cy2]
            return [box1, box2]
        return [[cx1, cy1, cx2, cy2]]

    # If more than 2, pick top 2 by area
    clean_contours.sort(key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
    return sorted(clean_contours[:2], key=lambda b: b[0])


def main() -> None:
    full_imgs = sorted(glob.glob("output/captures/1970-01-01/*_full.jpg"))
    p_model = YOLO("yolo11n.pt")
    s_model = YOLO("models/yolo-sneaker.pt")

    verified_dir = Path("output/verified_labels")
    verified_dir.mkdir(parents=True, exist_ok=True)

    train_img_dir = Path("datasets/sneakers_live/images/train")
    train_lbl_dir = Path("datasets/sneakers_live/labels/train")
    train_img_dir.mkdir(parents=True, exist_ok=True)
    train_lbl_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing {len(full_imgs)} images...")

    for idx, img_path in enumerate(full_imgs, 1):
        full_img = cv2.imread(img_path)
        stem = Path(img_path).stem.replace("_full", "")

        # 1. Detect person
        res_p = p_model(full_img, classes=[0], conf=0.4, verbose=False)[0]
        if len(res_p.boxes) == 0:
            print(f"[{idx}/15] No person in {stem}")
            continue

        p_box = res_p.boxes[0].xyxy[0].cpu().numpy()
        roi = extract_lower_body_roi(full_img, p_box)
        clean_crop = roi.crop
        h, w = clean_crop.shape[:2]

        # 2. Candidate boxes from sneaker model
        res_s = s_model(clean_crop, conf=0.15, verbose=False)[0]
        known_boxes = [b.xyxy[0].cpu().numpy().tolist() for b in res_s.boxes]

        # 3. Refine to obtain both feet
        final_boxes = segment_feet_boxes(clean_crop, known_boxes)

        # 4. Save clean crop
        clean_dest = train_img_dir / f"{stem}_crop.jpg"
        cv2.imwrite(str(clean_dest), clean_crop)

        # 5. Write YOLO label
        yolo_lines = []
        for box in final_boxes:
            bx1, by1, bx2, by2 = box
            cx = (bx1 + bx2) / (2.0 * w)
            cy = (by1 + by2) / (2.0 * h)
            bw = (bx2 - bx1) / w
            bh = (by2 - by1) / h
            yolo_lines.append(f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

        lbl_dest = train_lbl_dir / f"{stem}_crop.txt"
        lbl_dest.write_text("\n".join(yolo_lines) + "\n")

        # 6. Render verification preview
        preview = clean_crop.copy()
        colors = [(0, 255, 0), (255, 255, 0)]  # Green and Cyan
        for b_idx, box in enumerate(final_boxes):
            bx1, by1, bx2, by2 = map(int, box)
            color = colors[b_idx % len(colors)]
            cv2.rectangle(preview, (bx1, by1), (bx2, by2), color, 2)
            cv2.putText(
                preview,
                f"sneaker #{b_idx+1}",
                (bx1, max(14, by1 - 6)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
                cv2.LINE_AA,
            )

        ver_path = verified_dir / f"{stem}_verified.jpg"
        cv2.imwrite(str(ver_path), preview)
        print(f"[{idx}/15] {stem}: {len(final_boxes)} sneakers annotated -> {ver_path.name}")

    print("\nAnnotation complete! Verification images saved in output/verified_labels/")


if __name__ == "__main__":
    main()
