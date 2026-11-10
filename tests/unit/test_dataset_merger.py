"""Unit tests for manifest dataset merger with hallway oversampling."""

from pathlib import Path
import pytest
import yaml
from scripts.merge_datasets import merge_datasets, verify_labels_exist


@pytest.fixture
def dummy_datasets(tmp_path: Path):
    """Create lightweight mock baseline and live datasets with labels."""
    base_dir = tmp_path / "baseline"
    live_dir = tmp_path / "live"

    # Baseline: 3 train, 2 val, 1 test
    for split, count in [("train", 3), ("valid", 2), ("test", 1)]:
        img_dir = base_dir / split / "images"
        lbl_dir = base_dir / split / "labels"
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            img_file = img_dir / f"base_{split}_{i}.jpg"
            img_file.write_bytes(b"fake-image")
            lbl_file = lbl_dir / f"base_{split}_{i}.txt"
            lbl_file.write_text("0 0.5 0.5 0.2 0.2\n")

    base_yaml = base_dir / "data.yaml"
    with open(base_yaml, "w") as f:
        yaml.safe_dump(
            {
                "train": "../train/images",
                "val": "../valid/images",
                "test": "../test/images",
                "nc": 1,
                "names": ["sneaker"],
            },
            f,
        )

    # Live: 2 train, 1 val
    for split, count in [("train", 2), ("val", 1)]:
        img_dir = live_dir / "images" / split
        lbl_dir = live_dir / "labels" / split
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            img_file = img_dir / f"live_{split}_{i}.jpg"
            img_file.write_bytes(b"fake-image")
            lbl_file = lbl_dir / f"live_{split}_{i}.txt"
            lbl_file.write_text("0 0.6 0.6 0.3 0.3\n")

    live_yaml = live_dir / "data.yaml"
    with open(live_yaml, "w") as f:
        yaml.safe_dump(
            {
                "path": str(live_dir),
                "train": "images/train",
                "val": "images/val",
                "names": {0: "sneaker"},
            },
            f,
        )

    return base_yaml, live_yaml


def test_merge_datasets_creates_manifests_and_oversamples(tmp_path: Path, dummy_datasets):
    """Verify manifests are written with correct counts and oversampling multiplier."""
    base_yaml, live_yaml = dummy_datasets
    out_dir = tmp_path / "merged"

    summary = merge_datasets(
        baseline_yaml=base_yaml,
        live_yaml=live_yaml,
        output_dir=out_dir,
        live_oversample_factor=4,
    )

    # 3 baseline train + (2 live train * 4) = 11
    assert summary["train_count"] == 11
    # 2 baseline val + 1 live val = 3
    assert summary["val_count"] == 3
    # 1 baseline test = 1
    assert summary["test_count"] == 1

    train_txt = out_dir / "train.txt"
    val_txt = out_dir / "val.txt"
    test_txt = out_dir / "test.txt"
    data_yaml = out_dir / "data.yaml"

    assert train_txt.is_file()
    assert val_txt.is_file()
    assert test_txt.is_file()
    assert data_yaml.is_file()

    with open(train_txt) as f:
        train_lines = [line.strip() for line in f if line.strip()]
    assert len(train_lines) == 11

    with open(val_txt) as f:
        val_lines = [line.strip() for line in f if line.strip()]
    assert len(val_lines) == 3

    with open(data_yaml) as f:
        cfg = yaml.safe_load(f)
    assert cfg["names"] == {0: "sneaker"}
    assert cfg["train"] == "train.txt"
    assert cfg["val"] == "val.txt"


def test_verify_labels_exist(tmp_path: Path):
    """Verify label file resolution handles missing labels gracefully."""
    img = tmp_path / "images" / "test.jpg"
    img.parent.mkdir(parents=True)
    img.write_bytes(b"data")

    # Missing label
    with pytest.raises(FileNotFoundError, match="Missing label file"):
        verify_labels_exist([img])

    # Created label
    lbl = tmp_path / "labels" / "test.txt"
    lbl.parent.mkdir(parents=True)
    lbl.write_text("0 0.5 0.5 0.1 0.1\n")
    resolved = verify_labels_exist([img])
    assert len(resolved) == 1
