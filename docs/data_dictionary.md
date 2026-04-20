# NYC Airbnb 2019 Data Dictionary

This document provides a comprehensive overview of the New York City Airbnb Open Data (2019). It includes field definitions, technical specifications, and calculations for advanced KPIs used in the Tableau Dashboard.

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | New York City Airbnb Open Data (2019) |
| Source | Kaggle / Inside Airbnb |
| Volume | 48,884 listings (Post-Cleaning) |
| Granularity | One row per unique Airbnb listing |

## 1. Primary Feature Definitions

| Column Name | Data Type | Description | Cleaning / Preparation |
|---|---|---|---|
| `Listing ID` | `int` | Unique identifier for the listing | Primary Key |
| `Listing Title` | `string` | Name/Title of the property | Trimmed; Nulls filled as "Unknown" |
| `Host ID` | `int` | Unique identifier for the property owner | - |
| `Host Name` | `string` | Name of the host | Trimmed; Nulls filled as "Unknown" |
| `Borough` | `category` | The NYC borough (Neighbourhood Group) | Manhattan, Brooklyn, etc. |
| `Neighborhood` | `category` | The specific local area | 221 unique areas |
| `Latitude` | `float` | GPS Latitude | - |
| `Longitude` | `float` | GPS Longitude | - |
| `Room Type` | `category` | Accommodation category | Entire home, Private room, Shared |
| `Price` | `int` | Nightly rate in USD | Capped at 99th percentile ($799) |
| `Min Nights` | `int` | Minimum stay requirement | Capped at 365 |
| `Total Reviews` | `int` | Lifetime review count | - |
| `Last Review` | `date` | Date of the most recent guest review | NaT for zero-review listings |
| `Reviews per Month` | `float` | Monthly demand frequency | Nulls filled as 0.0 |
| `Host Listings` | `int` | Total listings managed by this host | Used for portfolio segmentation |
| `Availability` | `int` | Days available per year | 0-365 range |

## 2. Advanced Analytical KPIs (Tableau Master Layer)

| Metric | Formula | Business Rationale |
|---|---|---|
| **Listing Demand Score** | `Reviews per Month * (Availability / 365)` | Normalizes booking frequency against annual availability. This is the primary indicator of listing "stickiness" and actual demand throughput. |
| **Price Index** | `Price / Neighborhood Median Price` | Benchmarks a listing against its immediate micro-market. A value > 1.0 indicates a premium pricing strategy; < 1.0 indicates a value strategy. |
| **Revenue Proxy** | `Price * Availability` | Estimates the theoretical maximum annual earnings based on current pricing and supply. |
| **Yield Potential** | `Revenue Proxy / Price` | Measures how efficiently a listing converts its nightly rate into total annual earning potential. |

## 3. Segmentation Dimensions

| Dimension | Logic | Dashboard Use |
|---|---|---|
| **Host Segment** | `Single (1)`, `Emerging (2-5)`, `Enterprise (>5)` | Filters to compare individual hosts vs professional property managers. |
| **Recent Activity** | `Active` (2019), `Trailing` (2018), `Dormant` (<2018) | Helps identify current market sentiment vs legacy data points. |
| **Price Tier** | `Budget`, `Mid-Range`, `Premium`, `Luxury` | Quartile-based price grouping for high-level market summaries. |
| **Seasonality Peak** | `Summer Peak` (Jun-Aug), `Off-Peak` (Other) | Identifies stays originating during NYC's highest tourism period. |

## Data Audit Notes
- **Zero-Price Removal**: 11 records removed during ETL ($0 rates).
- **Physical Bounds**: Listings with > 365 minimum nights were capped to 365 to normalize for annual calculations.
- **Null Ethics**: `last_review` remains as a null date (NaT) to ensure Tableau time-series filters do not include phantom "1900" dates.
