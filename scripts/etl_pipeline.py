"""Airbnb NYC 2019 — ETL Pipeline (E_G18_NYCAirbnbAnalysis)

Stand-alone script that mirrors the notebook cleaning logic so the pipeline
can be re-run from the command line without Jupyter.

Usage:
    python scripts/etl_pipeline.py \\
        --input  data/raw/AB_NYC_2019.csv \\
        --output data/processed/airbnb_nyc_cleaned.csv
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------------
# Column Helpers
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[^a-z0-9]+', '_', regex=True)
        .str.strip('_')
    )
    result = df.copy()
    result.columns = cleaned
    return result


def rename_verbose_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply project-specific renames for readability."""
    return df.rename(columns={
        'calculated_host_listings_count': 'host_listing_count',
        'number_of_reviews'             : 'review_count',
        'reviews_per_month'             : 'review_rate_month',
    })


# ---------------------------------------------------------------------------
# Core Cleaning Steps
# ---------------------------------------------------------------------------

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.sort_values('review_count', ascending=False)
    df = df.drop_duplicates(subset='id', keep='first').reset_index(drop=True)
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    for col in ['neighbourhood_group', 'neighbourhood', 'room_type']:
        df[col] = df[col].astype('category')
    for col in ['name', 'host_name']:
        df[col] = df[col].astype('string').str.strip()
    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    # Text placeholders for the two minor string nulls
    df['name']      = df['name'].fillna('Unknown Listing')
    df['host_name'] = df['host_name'].fillna('Unknown Host')
    # review_rate_month → 0.0: listings with 0 reviews genuinely have 0 reviews/month
    df['review_rate_month'] = df['review_rate_month'].fillna(0.0)
    # last_review → LEFT AS NaT (do NOT fill with a sentinel date).
    # Tableau and pandas exclude NaT from date axes, filters, and trend lines
    # automatically. A sentinel like 1900-01-01 would corrupt date visuals.
    return df


def treat_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['price'] > 0].reset_index(drop=True)
    price_arr = df['price'].to_numpy(dtype=np.float64)
    p99 = np.percentile(price_arr, 99)
    df['price_original'] = df['price'].copy()
    df['price']          = np.clip(price_arr, 0, p99).astype(int)
    df['is_luxury']      = (df['price_original'] > p99).astype(int)
    return df


def treat_min_nights(df: pd.DataFrame) -> pd.DataFrame:
    df['minimum_nights'] = np.clip(
        df['minimum_nights'].to_numpy(dtype=np.float64), 1, 365
    ).astype(int)
    return df


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    price_v     = df['price'].to_numpy(dtype=np.float64)
    avail_v     = df['availability_365'].to_numpy(dtype=np.float64)
    rev_count_v = df['review_count'].to_numpy(dtype=np.float64)
    host_cnt_v  = df['host_listing_count'].to_numpy(dtype=np.float64)

    df['log_price']          = np.log1p(price_v)
    df['revenue_proxy']      = (price_v * avail_v).astype(int)
    df['occupancy_rate_est'] = np.clip((365 - avail_v) / 365, 0, 1).round(4)
    df['is_multi_lister']    = (host_cnt_v > 1).astype(int)
    df['has_reviews']        = (rev_count_v > 0).astype(int)
    df['borough_core']       = df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn']).astype(int)

    q1, q2, q3 = np.percentile(price_v, [25, 50, 75])
    df['price_tier'] = pd.cut(
        df['price'],
        bins=[0, q1, q2, q3, df['price'].max() + 1],
        labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'],
        include_lowest=True
    ).astype('category')

    # review_year / review_month: NaT rows propagate as NaN automatically
    df['review_year']  = df['last_review'].dt.year
    df['review_month'] = df['last_review'].dt.month

    return df


# ---------------------------------------------------------------------------
# Full Pipeline
# ---------------------------------------------------------------------------

FINAL_COLUMNS = [
    'id', 'name', 'host_id', 'host_name',
    'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude',
    'room_type', 'price', 'price_original', 'log_price', 'price_tier',
    'minimum_nights', 'review_count', 'last_review',
    'review_rate_month', 'review_year', 'review_month',
    'host_listing_count', 'availability_365',
    'revenue_proxy', 'occupancy_rate_est',
    'is_multi_lister', 'has_reviews', 'is_luxury', 'borough_core'
]


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Alias kept for backward-compatibility with notebook imports."""
    return build_clean_dataset_from_df(df)


def build_clean_dataset_from_df(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    df = rename_verbose_columns(df)
    df = drop_duplicates(df)
    df = convert_types(df)
    df = fill_missing(df)
    df = treat_price_outliers(df)
    df = treat_min_nights(df)
    df = engineer_features(df)
    df = df[[c for c in FINAL_COLUMNS if c in df.columns]].copy()
    return df.reset_index(drop=True)


def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path, low_memory=False)
    return build_clean_dataset_from_df(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run the NYC Airbnb 2019 cleaning pipeline.'
    )
    parser.add_argument('--input', required=True, type=Path,
                        help='Path to data/raw/AB_NYC_2019.csv')
    parser.add_argument('--output', required=True, type=Path,
                        help='Path to data/processed/airbnb_nyc_cleaned.csv')
    return parser.parse_args()


def main() -> None:
    args        = parse_args()
    cleaned_df  = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f'Processed dataset saved to : {args.output}')
    print(f'Rows    : {len(cleaned_df):,}')
    print(f'Columns : {len(cleaned_df.columns)}')
    print(f'Nulls   : {int(cleaned_df.isna().sum().sum())}')


if __name__ == '__main__':
    main()
