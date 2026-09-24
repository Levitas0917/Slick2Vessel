# 此代码用于一切csv相关操作，后续可继续添加函数

from pathlib import Path
import pandas as pd

YEAR = "2015"
REPO_ROOT = Path(r"f:/MYR/Research_/ZHANG/Oiling")
TARGET_DIR = REPO_ROOT / "results" / "feature_batch_year" / YEAR

INPUT_FILES = {
    "pos": TARGET_DIR / f"pos_features_{YEAR}_combine.csv",
    "neg": TARGET_DIR / f"neg_features_{YEAR}_combine.csv",
}

# These fields describe the sample, acquisition, geometry, or processing status.
INFO_COLUMNS = {
    "sample_type",
    "label",
    "system:index",
    "BUFF_DIST",
    "Category",
    "Subcategor",
    "CenterX",
    "CenterY",
    "xcoor",
    "ycoor",
    "Date",
    "Year",
    "ORIG_FID",
    "Shape_Area",
    "Shape_Leng",
    "instrument_mode",
    "sar_time",
    "scene_id",
    "scene_ids_used",
    "status",
    "status_34f",
    ".geo",
}


def read_labeled_csv(path: Path, sample_type: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    frame = pd.read_csv(path)
    frame.insert(0, "sample_type", sample_type)
    frame.insert(1, "label", 1 if sample_type == "pos" else 0)
    return frame


def organize_csv_features(target_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    frames = [read_labeled_csv(INPUT_FILES[name], name) for name in ("pos", "neg")]
    all_samples = pd.concat(frames, ignore_index=True, sort=False)

    info_columns = [column for column in all_samples.columns if column in INFO_COLUMNS]
    feature_columns = [column for column in all_samples.columns if column not in INFO_COLUMNS]

    # Keep identifiers and information first, followed by model-ready features.
    all_samples = all_samples[info_columns + feature_columns]
    info_df = all_samples[info_columns].copy()
    feature_df = all_samples[["sample_type", "label"] + feature_columns].copy()

    column_summary = pd.DataFrame(
        {
            "column_name": all_samples.columns,
            "column_group": [
                "information" if column in info_columns else "feature"
                for column in all_samples.columns
            ],
            "dtype": [str(all_samples[column].dtype) for column in all_samples.columns],
            "non_null_count": [all_samples[column].notna().sum() for column in all_samples.columns],
            "missing_count": [all_samples[column].isna().sum() for column in all_samples.columns],
        }
    )

    all_samples.to_csv(target_dir / f"all_samples_{YEAR}_organized.csv", index=False)
    info_df.to_csv(target_dir / f"sample_info_{YEAR}.csv", index=False)
    feature_df.to_csv(target_dir / f"features_{YEAR}.csv", index=False)
    column_summary.to_csv(target_dir / f"columns_summary_{YEAR}.csv", index=False)

    print(f"Rows: {len(all_samples)} (pos={int((all_samples['label'] == 1).sum())}, neg={int((all_samples['label'] == 0).sum())})")
    print(f"Information columns: {len(info_columns)}")
    print(f"Feature columns: {len(feature_columns)}")
    print("Feature columns:")
    print(", ".join(feature_columns))
    print(f"Saved organized files to: {target_dir}")

    return all_samples, info_df, feature_df


if __name__ == "__main__":
    organize_csv_features(TARGET_DIR)