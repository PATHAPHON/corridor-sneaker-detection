"""Evaluate fine-tuned YOLO sneaker detector, benchmark FPS, enforce dual-gate, and export weights."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
import cv2
import numpy as np
import torch
from ultralytics import YOLO


def resolve_device(requested_device: str | None = None) -> str:
    """Resolve the optimal compute device (MPS -> CUDA -> CPU)."""
    if requested_device:
        return requested_device
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def benchmark_inference(
    model: YOLO,
    device: str,
    imgsz: int = 640,
    iterations: int = 100,
    warmup: int = 10,
) -> dict[str, float]:
    """Benchmark pure forward-pass inference latency and FPS throughput."""
    dummy_input = np.zeros((imgsz, imgsz, 3), dtype=np.uint8)

    for _ in range(warmup):
        _ = model(dummy_input, device=device, verbose=False)

    if device == "mps":
        torch.mps.synchronize()
    elif device == "cuda":
        torch.cuda.synchronize()

    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = model(dummy_input, device=device, verbose=False)
        if device == "mps":
            torch.mps.synchronize()
        elif device == "cuda":
            torch.cuda.synchronize()
    total_time = time.perf_counter() - start_time

    mean_latency_ms = (total_time / iterations) * 1000.0
    fps = 1000.0 / mean_latency_ms if mean_latency_ms > 0 else 0.0

    return {
        "iterations": iterations,
        "mean_latency_ms": round(mean_latency_ms, 2),
        "fps": round(fps, 1),
    }


def compute_iou(box1: list[float], box2: list[float]) -> float:
    """Compute IoU between two (x1, y1, x2, y2) boxes."""
    xa = max(box1[0], box2[0])
    ya = max(box1[1], box2[1])
    xb = min(box1[2], box2[2])
    yb = min(box1[3], box2[3])

    inter = max(0.0, xb - xa) * max(0.0, yb - ya)
    area1 = max(0.0, box1[2] - box1[0]) * max(0.0, box1[3] - box1[1])
    area2 = max(0.0, box2[2] - box2[0]) * max(0.0, box2[3] - box2[1])
    union = area1 + area2 - inter

    return inter / union if union > 0 else 0.0


def read_gt_boxes(label_file: Path, img_shape: tuple[int, int]) -> list[list[float]]:
    """Read normalized YOLO labels and return pixel coordinates [x1, y1, x2, y2]."""
    boxes = []
    if not label_file.is_file():
        return boxes
    h, w = img_shape
    with open(label_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                _, xc, yc, bw, bh = [float(x) for x in parts[:5]]
                x1 = (xc - bw / 2) * w
                y1 = (yc - bh / 2) * h
                x2 = (xc + bw / 2) * w
                y2 = (yc + bh / 2) * h
                boxes.append([x1, y1, x2, y2])
    return boxes


def evaluate_hallway_crops(
    model: YOLO,
    hallway_dir: str | Path = "datasets/sneakers_live",
    device: str = "cpu",
    conf: float = 0.40,
    iou_thresh: float = 0.50,
) -> dict:
    """Evaluate detection recall on all curated hallway crops."""
    hallway_path = Path(hallway_dir).resolve()
    image_files = sorted(list(hallway_path.glob("images/**/*.jpg")))

    total_gt = 0
    matched_gt = 0
    all_confs = []

    for img_path in image_files:
        lbl_path = Path(str(img_path).replace("/images/", "/labels/")).with_suffix(".txt")
        orig_img = cv2.imread(str(img_path))
        if orig_img is None:
            continue
        h, w = orig_img.shape[:2]
        gt_boxes = read_gt_boxes(lbl_path, (h, w))
        total_gt += len(gt_boxes)

        res = model(str(img_path), device=device, conf=conf, verbose=False)
        pred_boxes = []
        if res and len(res) > 0 and len(res[0].boxes) > 0:
            for b in res[0].boxes:
                coords = b.xyxy[0].tolist() if hasattr(b.xyxy[0], "tolist") else list(b.xyxy[0])
                c = float(b.conf[0])
                pred_boxes.append((coords, c))
                all_confs.append(c)

        # Match GT to pred
        for gt in gt_boxes:
            for pred_b, _ in pred_boxes:
                if compute_iou(gt, pred_b) >= iou_thresh:
                    matched_gt += 1
                    break

    recall = matched_gt / total_gt if total_gt > 0 else 0.0
    mean_conf = float(np.mean(all_confs)) if all_confs else 0.0

    return {
        "total_images": len(image_files),
        "total_gt_boxes": total_gt,
        "detected_boxes": matched_gt,
        "recall": round(recall, 4),
        "mean_conf": round(mean_conf, 4),
    }


def render_before_after_comparisons(
    before_model: YOLO,
    after_model: YOLO,
    hallway_dir: str | Path = "datasets/sneakers_live",
    output_dir: str | Path = "runs/detect/eval/comparisons",
    device: str = "cpu",
    conf: float = 0.40,
) -> list[str]:
    """Generate side-by-side Before vs After visual panels across all hallway crops."""
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    hallway_path = Path(hallway_dir).resolve()
    image_files = sorted(list(hallway_path.glob("images/**/*.jpg")))
    saved_paths = []

    for img_path in image_files:
        orig = cv2.imread(str(img_path))
        if orig is None:
            continue
        h, w = orig.shape[:2]

        lbl_path = Path(str(img_path).replace("/images/", "/labels/")).with_suffix(".txt")
        gt_boxes = read_gt_boxes(lbl_path, (h, w))

        # Before inference
        res_before = before_model(str(img_path), device=device, conf=conf, verbose=False)
        before_img = orig.copy()
        before_boxes = res_before[0].boxes if res_before and len(res_before) > 0 else []
        for b in before_boxes:
            x1, y1, x2, y2 = [int(v) for v in b.xyxy[0]]
            c = float(b.conf[0])
            cv2.rectangle(before_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(before_img, f"sneaker {c:.2f}", (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

        # After inference
        res_after = after_model(str(img_path), device=device, conf=conf, verbose=False)
        after_img = orig.copy()
        after_boxes = res_after[0].boxes if res_after and len(res_after) > 0 else []
        for b in after_boxes:
            x1, y1, x2, y2 = [int(v) for v in b.xyxy[0]]
            c = float(b.conf[0])
            cv2.rectangle(after_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(after_img, f"sneaker {c:.2f}", (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

        # Composite
        banner_h = 45
        panel = np.zeros((h + banner_h, w * 2 + 10, 3), dtype=np.uint8)
        panel[:banner_h, :] = (25, 25, 25)

        title = f"Crop: {img_path.name} | GT: {len(gt_boxes)} sneakers"
        cv2.putText(panel, title, (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        status_sub = f"Before: {len(before_boxes)} detected  -->  After: {len(after_boxes)} detected"
        cv2.putText(panel, status_sub, (15, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(before_img, f"BEFORE (detected: {len(before_boxes)})", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(after_img, f"AFTER (detected: {len(after_boxes)})", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        panel[banner_h:, :w] = before_img
        panel[banner_h:, w + 10 :] = after_img

        out_file = out_dir / f"before_vs_after_{img_path.stem}.jpg"
        cv2.imwrite(str(out_file), panel)
        saved_paths.append(str(out_file))

    return saved_paths


def evaluate_and_export(
    weights_path: str | Path = "runs/detect/sneaker_yolo11n_merged/weights/best.pt",
    data_yaml: str | Path = "datasets/sneakers_merged/data.yaml",
    export_dest: str | Path = "models/yolo-sneaker.pt",
    hallway_dir: str | Path = "datasets/sneakers_live",
    split: str = "val",
    min_map50: float = 0.80,
    min_hallway_recall: float = 0.90,
    device: str | None = None,
    output_evidence_dir: str | Path = "runs/detect/eval",
) -> dict:
    """Run dual-gate model validation, benchmark FPS, auto-backup, export weights, and save evidence."""
    weights = Path(weights_path).resolve()
    if not weights.is_file():
        raise FileNotFoundError(f"Trained weights not found: {weights}")

    data_file = Path(data_yaml).resolve()
    if not data_file.is_file():
        raise FileNotFoundError(f"Data config not found: {data_file}")

    target_device = resolve_device(device)
    export_path = Path(export_dest).resolve()
    evidence_dir = Path(output_evidence_dir).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading candidate model '{weights}' on device: {target_device}...")
    model = YOLO(str(weights))

    # 1. Validation on split (Gate 1)
    print(f"\n--- 1. Evaluating on '{split}' split (Gate 1: mAP50 >= {min_map50}) ---")
    val_results = model.val(
        data=str(data_file),
        split=split,
        device=target_device,
        verbose=True,
    )

    box = val_results.box
    map50 = float(box.map50)
    map50_95 = float(box.map)
    precision = float(box.p[0]) if len(box.p) > 0 else float(box.mp)
    recall = float(box.r[0]) if len(box.r) > 0 else float(box.mr)

    print(f"Metrics ({split} set):")
    print(f"  mAP50:     {map50:.4f}")
    print(f"  mAP50-95:  {map50_95:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")

    # 2. Hallway recall evaluation (Gate 2)
    print(f"\n--- 2. Evaluating on Hallway Crops (Gate 2: Recall >= {min_hallway_recall}) ---")
    hallway_metrics = evaluate_hallway_crops(model, hallway_dir=hallway_dir, device=target_device, conf=0.40)
    hallway_recall = hallway_metrics["recall"]
    print(f"  Hallway Images:   {hallway_metrics['total_images']}")
    print(f"  Ground-Truth:     {hallway_metrics['total_gt_boxes']}")
    print(f"  Detected Sneakers: {hallway_metrics['detected_boxes']}")
    print(f"  Hallway Recall:   {hallway_recall:.4f}")
    print(f"  Mean Confidence:  {hallway_metrics['mean_conf']:.4f}")

    gate1_passed = map50 >= min_map50
    gate2_passed = hallway_recall >= min_hallway_recall
    all_gates_passed = gate1_passed and gate2_passed

    print(f"\n--- Dual-Gate Verification Status ---")
    print(f"  Gate 1 (Overall mAP50 >= {min_map50}): {'PASSED' if gate1_passed else 'FAILED'} ({map50:.4f})")
    print(f"  Gate 2 (Hallway Recall >= {min_hallway_recall}): {'PASSED' if gate2_passed else 'FAILED'} ({hallway_recall:.4f})")

    # 3. Benchmark throughput
    print("\n--- 3. Benchmarking Inference Throughput ---")
    benchmark_res = benchmark_inference(model, device=target_device, iterations=100)
    print(f"  Mean Latency: {benchmark_res['mean_latency_ms']} ms")
    print(f"  Throughput:   {benchmark_res['fps']} FPS")

    # Check promotion
    backup_file = None
    if not all_gates_passed:
        summary = {
            "candidate_weights": str(weights),
            "gates": {
                "passed": False,
                "gate1_map50": {"required": min_map50, "actual": round(map50, 4), "passed": gate1_passed},
                "gate2_hallway_recall": {"required": min_hallway_recall, "actual": round(hallway_recall, 4), "passed": gate2_passed},
            },
            "metrics": {
                "mAP50": round(map50, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
            },
            "hallway": hallway_metrics,
            "benchmark": benchmark_res,
        }
        summary_path = evidence_dir / "eval_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        raise RuntimeError(
            f"Dual-gate benchmark check failed: Gate 1 (mAP50 {map50:.4f} >= {min_map50}) = {gate1_passed}, "
            f"Gate 2 (Hallway Recall {hallway_recall:.4f} >= {min_hallway_recall}) = {gate2_passed}. Promotion aborted."
        )

    # 4. Backup existing weights and promote
    export_path.parent.mkdir(parents=True, exist_ok=True)
    if export_path.is_file():
        backup_path = export_path.with_name(f"{export_path.stem}.backup.pt")
        shutil.copy2(export_path, backup_path)
        backup_file = str(backup_path)
        print(f"\n--- 4. Safe Backup & Model Promotion ---")
        print(f"  Backed up existing model to: {backup_path}")
    else:
        print(f"\n--- 4. Model Promotion ---")

    shutil.copy2(weights, export_path)
    print(f"  Promoted candidate weights to: {export_path}")

    # 5. Render Before vs After visual comparisons
    print("\n--- 5. Generating Before vs After Visual Comparisons ---")
    before_model_weights = backup_file if backup_file else str(export_path)
    before_model = YOLO(before_model_weights)
    comparison_files = render_before_after_comparisons(
        before_model=before_model,
        after_model=model,
        hallway_dir=hallway_dir,
        output_dir=evidence_dir / "comparisons",
        device=target_device,
        conf=0.40,
    )
    print(f"  Generated {len(comparison_files)} comparison panels in {evidence_dir / 'comparisons'}")

    summary = {
        "model_weights": str(export_path),
        "backup_weights": backup_file,
        "gates": {
            "passed": True,
            "gate1_map50": {"required": min_map50, "actual": round(map50, 4), "passed": True},
            "gate2_hallway_recall": {"required": min_hallway_recall, "actual": round(hallway_recall, 4), "passed": True},
        },
        "metrics": {
            "mAP50": round(map50, 4),
            "mAP50_95": round(map50_95, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
        },
        "hallway": hallway_metrics,
        "benchmark": benchmark_res,
        "comparison_panels": comparison_files,
    }

    summary_path = evidence_dir / "eval_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nEvaluation summary written to: {summary_path}")

    return summary


def main() -> None:
    """CLI entry point for evaluation and export."""
    parser = argparse.ArgumentParser(description="Evaluate and export trained sneaker model with dual gates")
    parser.add_argument("--weights", type=str, default="runs/detect/sneaker_yolo11n_merged/weights/best.pt")
    parser.add_argument("--data", type=str, default="datasets/sneakers_merged/data.yaml")
    parser.add_argument("--export", type=str, default="models/yolo-sneaker.pt")
    parser.add_argument("--hallway-dir", type=str, default="datasets/sneakers_live")
    parser.add_argument("--split", type=str, default="val")
    parser.add_argument("--min-map50", type=float, default=0.80)
    parser.add_argument("--min-hallway-recall", type=float, default=0.90)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default="runs/detect/eval")

    args = parser.parse_args()

    try:
        evaluate_and_export(
            weights_path=args.weights,
            data_yaml=args.data,
            export_dest=args.export,
            hallway_dir=args.hallway_dir,
            split=args.split,
            min_map50=args.min_map50,
            min_hallway_recall=args.min_hallway_recall,
            device=args.device,
            output_evidence_dir=args.output_dir,
        )
    except Exception as e:
        print(f"Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
