"""Visualize ADR-0007 training-time data augmentations on 5 real hallway crops."""

from pathlib import Path
import cv2
import numpy as np


def apply_hsv_jitter(img: np.ndarray, h_gain: float = 0.015, s_gain: float = 0.7, v_gain: float = 0.4) -> np.ndarray:
    """Simulate YOLO HSV color jitter."""
    r = np.random.uniform(-1, 1, 3) * [h_gain, s_gain, v_gain] + 1
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    dtype = img.dtype

    x = np.arange(0, 256, dtype=r.dtype)
    lut_hue = ((x * r[0]) % 180).astype(dtype)
    lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
    lut_val = np.clip(x * r[2], 0, 255).astype(dtype)

    im_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val)))
    return cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)


def apply_rotation(img: np.ndarray, degrees: float = 10.0) -> np.ndarray:
    """Simulate stride angle tilt via rotation."""
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    angle = np.random.uniform(-degrees, degrees)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT101)


def apply_erasing(img: np.ndarray, erasing_prob: float = 0.2) -> np.ndarray:
    """Simulate random erasing cutout to mimic leg-over-leg stride occlusion."""
    out = img.copy()
    h, w = out.shape[:2]
    # Erase a rectangle in the lower half (approx shoe level)
    ew = int(w * np.random.uniform(0.15, 0.35))
    eh = int(h * np.random.uniform(0.15, 0.35))
    ex = np.random.randint(0, max(1, w - ew))
    ey = np.random.randint(int(h * 0.3), max(int(h * 0.3) + 1, h - eh))
    out[ey : ey + eh, ex : ex + ew] = np.random.randint(0, 256, (eh, ew, 3), dtype=np.uint8)
    return out


def apply_flip_and_scale(img: np.ndarray, scale: float = 0.5) -> np.ndarray:
    """Simulate horizontal flip and camera distance scaling."""
    out = cv2.flip(img, 1)  # horizontal flip
    s = np.random.uniform(1.0 - scale * 0.3, 1.0 + scale * 0.3)
    h, w = out.shape[:2]
    nw, nh = int(w * s), int(h * s)
    resized = cv2.resize(out, (nw, nh), interpolation=cv2.INTER_LINEAR)
    if s > 1.0:
        # Crop center
        cx, cy = nw // 2, nh // 2
        return resized[cy - h // 2 : cy + h // 2, cx - w // 2 : cx + w // 2]
    else:
        # Pad center
        canvas = np.zeros_like(img)
        y_off = (h - nh) // 2
        x_off = (w - nw) // 2
        canvas[y_off : y_off + nh, x_off : x_off + nw] = resized
        return canvas


def read_yolo_labels(lbl_path: Path, img_shape: tuple[int, int]) -> list[tuple[int, int, int, int]]:
    """Read normalized YOLO labels and convert to pixel (x1, y1, x2, y2)."""
    boxes = []
    if not lbl_path.is_file():
        return boxes
    h, w = img_shape
    with open(lbl_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                _, xc, yc, bw, bh = [float(x) for x in parts[:5]]
                x1 = int((xc - bw / 2) * w)
                y1 = int((yc - bh / 2) * h)
                x2 = int((xc + bw / 2) * w)
                y2 = int((yc + bh / 2) * h)
                boxes.append((x1, y1, x2, y2))
    return boxes


def draw_boxes(img: np.ndarray, boxes: list[tuple[int, int, int, int]], color=(0, 255, 0), label="sneaker") -> np.ndarray:
    """Render bounding boxes on image."""
    canvas = img.copy()
    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
        cv2.putText(canvas, label, (x1, max(15, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    return canvas


def make_comparison_panel(orig: np.ndarray, aug: np.ndarray, title: str, subtitle: str) -> np.ndarray:
    """Create a side-by-side composite comparison image."""
    h, w = orig.shape[:2]
    # Header banner
    banner_h = 50
    composite_w = w * 2 + 10
    composite_h = h + banner_h

    composite = np.zeros((composite_h, composite_w, 3), dtype=np.uint8)
    composite[:banner_h, :] = (30, 30, 30)

    cv2.putText(composite, title, (15, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(composite, subtitle, (15, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

    # Sub-banners
    orig_annotated = orig.copy()
    cv2.putText(orig_annotated, "Original Hallway Crop", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(orig_annotated, "Original Hallway Crop", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 1)

    aug_annotated = aug.copy()
    cv2.putText(aug_annotated, "ADR-0007 Augmented", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(aug_annotated, "ADR-0007 Augmented", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

    composite[banner_h:, :w] = orig_annotated
    composite[banner_h:, w + 10 :] = aug_annotated

    return composite


def generate_samples(output_dir: str | Path = "output/augmentation_samples") -> list[Path]:
    """Generate 5 visual sample images demonstrating Ticket 02 augmentations."""
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    live_dir = Path("datasets/sneakers_live/images/train").resolve()
    image_paths = sorted(list(live_dir.glob("*.jpg")))[:5]
    if len(image_paths) < 5:
        raise RuntimeError(f"Expected at least 5 live hallway crops in {live_dir}, found {len(image_paths)}")

    results = []
    np.random.seed(42)  # Deterministic samples

    scenarios = [
        (
            "Sample 1: HSV Brightness & Saturation Jitter (hsv_v=0.4, hsv_s=0.7)",
            "Robustness against dark footwear silhouettes & bright floor tile auto-exposure glare",
            lambda im: apply_hsv_jitter(im, s_gain=0.7, v_gain=0.4),
        ),
        (
            "Sample 2: Stride Angle Perspective Rotation (degrees=10.0)",
            "Robustness against foot tilt during gait swing phase and directional cornering",
            lambda im: apply_rotation(im, degrees=10.0),
        ),
        (
            "Sample 3: Random Erasing & Depth Cutout (erasing=0.2)",
            "Robustness against leg-over-leg occlusion during forward walking strides",
            lambda im: apply_erasing(im, erasing_prob=0.2),
        ),
        (
            "Sample 4: Directional Horizontal Flip & Distance Scale (fliplr=0.5, scale=0.5)",
            "Robustness to entry direction (A->B / B->A) and variable camera focal distance",
            lambda im: apply_flip_and_scale(im, scale=0.5),
        ),
        (
            "Sample 5: Full Combined ADR-0007 Transformation + Ground-Truth Sneaker Boxes",
            "Synthesized multi-factor indoor corridor condition injected during YOLO11n fine-tuning",
            lambda im: apply_erasing(apply_rotation(apply_hsv_jitter(im, s_gain=0.6, v_gain=0.4), degrees=8.0)),
        ),
    ]

    for idx, (img_file, (title, subtitle, transform_fn)) in enumerate(zip(image_paths, scenarios), start=1):
        orig = cv2.imread(str(img_file))
        if orig is None:
            continue

        lbl_file = img_file.parent.parent.parent / "labels" / "train" / f"{img_file.stem}.txt"
        boxes = read_yolo_labels(lbl_file, orig.shape[:2])

        orig_boxed = draw_boxes(orig, boxes, color=(0, 255, 0), label="sneaker GT")
        aug = transform_fn(orig)
        aug_boxed = draw_boxes(aug, boxes if idx == 5 else [], color=(0, 255, 255), label="sneaker")

        panel = make_comparison_panel(orig_boxed, aug_boxed, title, subtitle)

        out_file = out_path / f"sample_{idx}_adr0007_augmentation.jpg"
        cv2.imwrite(str(out_file), panel)
        results.append(out_file)
        print(f"Generated sample {idx}: {out_file.name}")

    return results


if __name__ == "__main__":
    generate_samples()
