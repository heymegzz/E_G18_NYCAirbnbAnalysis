# NYC Airbnb 2019 Data Dictionary

This document provides a comprehensive overview of the New York City Airbnb Open Data (2019). It includes field definitions, technical specifications, and calculations for key performance indicators (KPIs) used in the analysis and dashboard.

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | New York City Airbnb Open Data (2019) |
| Source | Kaggle / Inside Airbnb |
| Raw file name | `AB_NYC_2019.csv` |
| Last updated | 2019-08-12 (Snapshot) |
| Volume | 48,895 listings |
| Granularity | One row per unique Airbnb listing |

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `id` | `int` | Unique listing identifier | `2539` | Joins / ID | Primary Key. No duplicates. |
| `name` | `string` | Name of the listing | `Clean & quiet apt home` | Search / Text Analysis | 16 missing values. |
| `host_id` | `int` | Unique identifier for the host | `2787` | Aggregations | Used for grouping by host. |
| `host_name` | `string` | Name of the host | `John` | Identification | 21 missing values. |
| `neighbourhood_group` | `string` | The borough where the listing is located | `Brooklyn` | Filters / Drill-down | 5 unique values (Manhattan, Brooklyn, etc.) |
| `neighbourhood` | `string` | The specific neighborhood area | `Kensington` | Geo Analysis | 221 unique values. |
| `latitude` | `float` | Geographic coordinate (North-South) | `40.64749` | Maps | Ready for GIS visualization. |
| `longitude` | `float` | Geographic coordinate (East-West) | `-73.97237` | Maps | Ready for GIS visualization. |
| `room_type` | `string` | Type of accommodation offered | `Private room` | Segment Analysis | Entire home/apt, Private room, Shared room. |
| `price` | `int` | Price per night in USD | `149` | KPIs / Price Analysis | Contains 11 records with `$0` price. |
| `minimum_nights` | `int` | Minimum number of nights for stay | `1` | Booking Analysis | Outliers exist (max: 1,250). |
| `number_of_reviews` | `int` | Total lifetime reviews for the listing | `9` | Demand Analysis | Ranges from 0 to 629. |
| `last_review` | `date` | Date of the latest review received | `2018-10-19` | Recency Analysis | 10,052 nulls (listings with 0 reviews). |
| `reviews_per_month` | `float` | Average reviews per month | `0.21` | KPI / Demand | 10,052 nulls. Impute with 0 if needed. |
| `calculated_host_listings_count` | `int` | Total listings managed by this host | `6` | Professionalism | Measure of host scale. |
| `availability_365` | `int` | Available days in a year (out of 365) | `365` | KPI / Supply | Values range from 0 to 365. |

## Analytical Framework & KPI Definitions

This section defines the metrics used to measure market performance, host behavior, and demand patterns in the NYC Airbnb ecosystem.

### 1. Pricing & Revenue Metrics
| Metric Name | Logic/Calculation | Business Rationale |
|---|---|---|
| **Median Nightly Price** | `Median(price)` | Preferred over average price to mitigate the skewness caused by extreme luxury listings and potential data entry errors ($0 listings). |
| **Minimum Transaction Value (MTV)** | `price * minimum_nights` | Represents the lowest financial commitment required for a stay. Higher MTVs indicate long-term rental patterns or high-barrier luxury stays. |
| **Estimated Monthly GMV (Revenue Proxy)** | `price * (reviews_per_month * 1.5)` | Estimates monthly listing performance based on a review-to-stay conversion factor (Industry proxy: 1 review per 1.5 stays). |

### 2. Demand & Engagement Metrics
| Metric Name | Logic/Calculation | Business Rationale |
|---|---|---|
| **Market Visibility Score** | `reviews_per_month * (availability_365 / 365)` | Normalizes review frequency against the listing's annual availability. Identifies high-performing active listings versus seasonal or inactive ones. |
| **Review Recency Index** | Categorization of `last_review` | Distinguishes between active market participants and "stale" listings that may no longer be operational. |

### 3. Supply & Host Portfolio Metrics
| Metric Name | Logic/Calculation | Business Rationale |
|---|---|---|
| **Host Portfolio Segmentation** | `CASE WHEN host_listings == 1 THEN 'Single' WHEN host_listings <= 5 THEN 'Emerging' ELSE 'Enterprise' END` | Profiles the supply side to understand the ratio of casual home-sharers to professional management entities. |
| **Market Concentration Index** | `Count(id)` by `neighbourhood_group` | Measures supply density across boroughs to identify saturated markets versus underserved niche areas. |

## Data Integrity & Pre-processing Considerations

The following observations are critical for ensuring the validity of analysis and dashboard visualizations:

- **Review Signal Sparsity**: Approximately **20.5% (10,052)** of listings have zero reviews. In demand modeling, these records should be categorized as 'Unverified' or 'New Market Entries' to avoid dragging down monthly averages.
- **Price Anomaly Handling**: Records with a price of **$0 (11 total)** are considered data integrity issues and must be excluded from all pricing aggregations.
- **Supply Logic (Availability)**: An `availability_365` value of `0` does not always indicate 100% occupancy; it may represent blocked calendars or inactive IDs. Cross-referencing with `last_review` is required to confirm listing status.
- **Regulatory Outliers**: Listings with `minimum_nights > 30` often fall under different NYC housing regulations (long-term leases). Analysts should segment these from "short-term" vacation rental data.
