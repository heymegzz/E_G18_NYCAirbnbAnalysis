"""
Airbnb NYC 2019 — ETL Pipeline (Production Grade)

This script provides a standardized, logging-enabled pipeline to transform raw 
Airbnb data into a cleaned, feature-enriched dataset ready for BI and Stats.

Design Standards: 
- Log every transformation step for auditability.
- Use vectorized NumPy operations for performance.
- Maintain NaT for date nulls to preserve BI tool axis integrity.
"""

from __future__ import annotations
import argparse
import warnings
import logging
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Column Helpers
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    logger.info("Step: Normalizing column names to snake_case.")
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
    """Apply project-specific renames for readability and KPI alignment."""
    logger.info("Step: Applying verbose column renames for KPI consistency.")
    return df.rename(columns={
        'calculated_host_listings_count': 'host_listing_count',
        'number_of_reviews'             : 'review_count',
        'reviews_per_month'             : 'review_rate_month',
    })


# ---------------------------------------------------------------------------
# Core Cleaning Steps
# ---------------------------------------------------------------------------

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Identify and remove full-row and ID-level duplicates."""
    logger.info("Step: Handling duplicates.")
    initial_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.sort_values('review_count', ascending=False)
    df = df.drop_duplicates(subset='id', keep='first').reset_index(drop=True)
    removed = initial_rows - len(df)
    if removed > 0:
        logger.info(f"Dropped {removed} duplicate records.")
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to optimal memory/analytical types."""
    logger.info("Step: Converting data types (category/datetime/string).")
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    for col in ['neighbourhood_group', 'neighbourhood', 'room_type']:
        if col in df.columns:
            df[col] = df[col].astype('category')
    for col in ['name', 'host_name']:
        if col in df.columns:
            df[col] = df[col].astype('string').str.strip()
    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values based on business rationale."""
    logger.info("Step: Imputing missing values.")
    # Text placeholders for string nulls
    df['name']      = df['name'].fillna('Unknown Listing')
    df['host_name'] = df['host_name'].fillna('Unknown Host')
    # review_rate_month → 0.0 for zero-review listings
    df['review_rate_month'] = df['review_rate_month'].fillna(0.0)
    logger.info("Handled nulls in 'name', 'host_name', and 'review_rate_month'. 'last_review' kept as NaT.")
    return df


def treat_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Filter $0 prices and cap extreme upper bounds at 99th percentile."""
    logger.info("Step: Treating price outliers.")
    initial_count = len(df)
    df = df[df['price'] > 0].reset_index(drop=True)
    zero_prices = initial_count - len(df)
    if zero_prices > 0:
        logger.warning(f"Removed {zero_prices} records with $0 price.")

    price_arr = df['price'].to_numpy(dtype=np.float64)
    p99 = np.percentile(price_arr, 99)
    df['price_original'] = df['price'].copy()
    df['price']          = np.clip(price_arr, 0, p99).astype(int)
    df['is_luxury']      = (df['price_original'] > p99).astype(int)
    logger.info(f"Price capped at 99th percentile: ${p99:.0f}.")
    return df


def treat_min_nights(df: pd.DataFrame) -> pd.DataFrame:
    """Cap minimum nights at 365 to normalize for annual visibility KPIs."""
    logger.info("Step: Normalizing minimum stay requirements.")
    df['minimum_nights'] = np.clip(
        df['minimum_nights'].to_numpy(dtype=np.float64), 1, 365
    ).astype(int)
    return df


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derivative KPIs using vectorized NumPy operations."""
    logger.info("Step: Engineering analytical features and KPIs.")
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
    """Alias for backward-compatibility with notebook imports."""
    return build_clean_dataset_from_df(df)


def build_clean_dataset_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """Coordinate the full transformation logic on a dataframe."""
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
    """Load raw data and execute the clean dataset build."""
    logger.info(f"Loading raw dataset from {input_path}")
    df = pd.read_csv(input_path, low_memory=False)
    return build_clean_dataset_from_df(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Persist the cleaned and engineered dataset."""
    logger.info(f"Saving processed dataset to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Pipeline Execution: SUCCESS.")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run the NYC Airbnb 2019 cleaning pipeline.'
    )
    parser.add_argument('--input', default='data/raw/AB_NYC_2019.csv', type=Path,
                        help='Path to input CSV')
    parser.add_argument('--output', default='data/processed/airbnb_nyc_cleaned.csv', type=Path,
                        help='Path to output CSV')
    return parser.parse_args()


def main() -> None:
    args        = parse_args()
    cleaned_df  = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)


if __name__ == '__main__':
    main()
