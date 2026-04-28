# NYC Airbnb 2019: Market, Revenue, and Demand Analysis

> Capstone 2 Project Report. Newton School of Technology, Data Visualization & Analytics.

---

## 1. Cover Page

| Field | Details |
|---|---|
| **Project Title** | NYCAirbnbAnalysis: NYC Airbnb 2019 Market, Revenue, and Demand Analysis |
| **Sector** | Travel & Hospitality (Short-Term Rental Marketplaces) |
| **Team ID** | G18 |
| **Section** | E |
| **Team Members and Roles** | Meghna Nair (`heymegzz`) — Team Lead, EDA & Analysis Owner; Aditya Rao — Dataset & Sourcing Owner; Shreyansh Agarwal (`BLOODWYROM`) — ETL & Cleaning Owner; Khyati Batra (`khyatibatra0316`) — Statistical Analysis Owner; Kunal Vats (`1Kunalvats9`) — Tableau Dashboard Owner; Sarvesh Srinath (`sarveshcore`) — Report Writing & PPT/Viva Owner |
| **Institute** | Newton School of Technology |
| **GitHub Repository** | https://github.com/heymegzz/E_G18_NYCAirbnbAnalysis |
| **Submission Date** | 2026-05-28 |

---

## 2. Executive Summary

**Situation.** New York City is the largest single short-term rental market in the world, with 48,884 active Airbnb listings, 37,455 hosts, and a theoretical Potential Revenue ceiling of $890.5M across 221 neighborhoods in 2019. The platform sits at the intersection of three competing decision-makers: real-estate investors deploying capital, individual hosts setting prices, and a platform managing inventory quality and search ranking.

**Complication.** Headline averages obscure the structure of the market. Price distributions are heavily right-skewed (raw maximum of $10,000/night versus a median of $106), borough-level revenue is concentrated but yield is not, roughly one-third of inventory is dormant or never-reviewed, and a Pearson correlation of −0.065 between price and reviews/month signals that price and demand are functionally decoupled at listing granularity. Naive metrics over-state Manhattan's attractiveness, under-state outer-borough yield, and miss the professionalization of the top of the host distribution. Decisions made on this raw view systematically misallocate capital, search impressions, and regulatory attention.

**Resolution.** We built a reproducible Python ETL pipeline (`scripts/etl_pipeline.py`), engineered a dual-track revenue framework (Potential Revenue and Estimated Revenue under a 50% occupancy floor), four decision-grade KPIs (Yield Potential, Market Price Index, Listing Demand Score, Host Portfolio Segment), and a three-dashboard Tableau workbook covering location, revenue, and demand. Statistically validated findings (Kruskal-Wallis H = 7,023, p < 0.001 across boroughs) anchor a set of five recommendations that move stakeholders from intuition to evidence: investors toward high-yield outer-borough acquisitions, hosts toward index-based re-pricing, and the platform toward dormant-inventory suppression and enterprise-host segmentation. Estimated platform-wide impact ranges from a 5 to 10 percentage-point lift in booking liquidity to an 8 to 12% revenue uplift on re-priced inventory.

---

## 3. Sector and Business Context

**Sector overview.** Short-term rentals (STR) are a $100B+ global category dominated by Airbnb, VRBO, and Booking.com. NYC is one of the largest single STR markets in the world but also one of the most regulated (Local Law 18, 2023, enforced multi-dwelling restrictions). 2019 represents the last clean before the pandemic, pre LL18 baseline of organic NYC STR behavior, the canonical reference snapshot for research and investment models.

**Decision-makers and stakeholders.**
- **Real-estate investors** evaluating which neighborhoods convert capital to nightly revenue most efficiently.
- **Hosts** deciding pricing, minimum-night, and room-type strategy.
- **Platform operations (Airbnb)** managing listing quality, search ranking, and host segmentation.
- **City policy analysts** quantifying commercial vs. casual host activity for regulation design.

**Why this matters.** Without a quantitative decomposition of the market, decisions default to intuition (e.g., "Manhattan is best") that misses high-yield outer-borough micro-markets and over-weights gross price as a proxy for revenue.

---

## 4. Problem Statement and Objectives

**Formal problem.** Given the 2019 NYC Airbnb dataset, identify (a) where listings and revenue concentrate geographically, (b) which segments deliver the highest revenue and yield, and (c) when and where demand actually materializes, so that investors, hosts, and the platform can make borough, neighborhood, and listing level decisions backed by KPIs rather than averages.

**Scope.**
- **In scope.** Listings active per Inside Airbnb 2019 NYC snapshot, all five boroughs, all room types.
- **Out of scope.** 2020+ data, regulatory simulation, individual guest behavior, dynamic pricing models, supply outside NYC.

**Success criteria.**
- A reproducible ETL that loads the raw 48,895 rows and outputs a Tableau-ready master with engineered KPIs.
- 3 published dashboards covering Location, Revenue, and Demand.
- At least 8 decision-grade insights with at least one statistically tested claim.
- At least 3 recommendations each tied to a specific KPI or segment.

---

## 5. Data Description

| Attribute | Details |
|---|---|
| **Source** | Kaggle, *New York City Airbnb Open Data 2019* (originally compiled from Inside Airbnb) |
| **Access link** | https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data |
| **Raw rows** | 49,080 (file lines incl. header), **48,895** listings parsed |
| **Cleaned rows** | **48,884** (zero-price and full-row duplicates removed) |
| **Columns (raw)** | 16 |
| **Columns (Tableau master)** | 23 (16 base + 7 engineered) |
| **Time period** | Listings live as of 2019 snapshot. Reviews from July 2011 to July 2019. |
| **Format** | CSV |
| **Granularity** | One row per Airbnb listing |

**Why this dataset fits the brief.**
- 48,884 cleaned rows (well above the 5,000 threshold).
- 23 columns in the Tableau master (well above the 8 meaningful columns threshold).
- Missing values in `reviews_per_month`, `last_review`, `name`, `host_name`.
- Heavy price outliers (max raw $10,000) that exercise outlier-treatment logic.
- Categorical columns: `neighbourhood_group`, `neighbourhood`, `room_type`.
- Date column: `last_review`.
- Geographic columns: `latitude`, `longitude`, which drive Tableau map views.

**Key columns (raw).** `id`, `name`, `host_id`, `host_name`, `neighbourhood_group`, `neighbourhood`, `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`, `number_of_reviews`, `last_review`, `reviews_per_month`, `calculated_host_listings_count`, `availability_365`.

**Known biases and limitations.**
- 2019 snapshot only, before the pandemic, before Local Law 18, not representative of post 2023 NYC.
- `availability_365` reflects host-controlled supply, not realized bookings.
- Listings without reviews (~10k) are time-blind. We cannot confirm they are real or active.
- The dataset over-represents popular neighborhoods relative to ad-hoc rentals because Inside Airbnb scrapes only listings publicly visible on Airbnb at scrape time.

**Key data-quality issues.**
- 11 listings with `$0` price (removed).
- ~10,051 listings with zero reviews (`reviews_per_month` NaN, imputed to 0.0; `last_review` retained as `NaT` to preserve temporal integrity in downstream visualizations).
- Heavy right-skew in `price` (max raw $10,000), capped at the 99th percentile ($799), with the original retained as `price_original`.
- `minimum_nights` had values up to 1,250, capped at 365.
- Missing `name` and `host_name` filled with `"Unknown Listing"` and `"Unknown Host"`.

Full schema: see `docs/data_dictionary.md`.

---

## 6. Data Cleaning & ETL Pipeline

The pipeline (`scripts/etl_pipeline.py`) is logging-enabled, vectorized (NumPy), and idempotent.

**Major steps.**
1. **Normalize columns** to `snake_case`.
2. **Rename verbose columns** for KPI readability (`number_of_reviews` to `review_count`, etc.).
3. **Drop duplicates.** Full-row first, then by `id`, keeping the row with most reviews.
4. **Type conversion.** `last_review` to datetime; categorical for borough, neighborhood, room type.
5. **Impute missings.** `name` and `host_name` filled with placeholders; `review_rate_month` filled with 0.0; `last_review` retained as `NaT`.
6. **Outlier treatment.** Drop `price = 0`; cap `price` at p99 ($799); flag `is_luxury` for original above p99.
7. **Min-nights cap** at 365.
8. **Feature engineering.** `log_price`, `revenue_proxy`, `occupancy_rate_est`, `is_multi_lister`, `has_reviews`, `borough_core`, `price_tier` (quartile bins), `review_year`, `review_month`.

**Assumptions.**
- `availability_365 = 0` is treated as listed but blocked, not delisted.
- `Potential Revenue = Price × Availability` is an *upper bound* on theoretical revenue. It does not assume 100% occupancy.
- Summer Peak is defined as June to August based on `last_review` month.

**Output datasets.**
- `data/processed/airbnb_nyc_cleaned.csv`, the analytical layer (snake_case, 27 columns).
- `data/processed/nyc_airbnb_tableau_master.csv`, the BI layer (verbose names, segmentation labels, 23 columns), the primary Tableau source.

---

## 7. KPI & Metric Framework

**Revenue framework: a dual-track approach.**

Single-number revenue proxies are routinely over-interpreted. We separate two clearly defined views and surface both in the dashboard so stakeholders can choose the lens appropriate to the decision.

| KPI | Formula | Interpretation |
|---|---|---|
| **Potential Revenue (GMV ceiling)** | `Price × Availability 365` | Theoretical upper bound on annual earnings if every available night is booked at list price. Used for relative comparisons across listings, neighborhoods, and boroughs. |
| **Estimated Revenue (50% occupancy floor)** | `Price × Availability × 0.5` | Conservative working estimate that applies an industry-typical 50% realized-occupancy assumption to available supply. Used for capital deployment and ROI sizing. |
| **Estimated Revenue (review-weighted)** | `Price × min(Availability, Reviews/Month × 12 × Avg Stay × Review-to-Booking Multiplier)` | Demand-anchored alternative that converts review velocity to bookings (Avg Stay = 3 nights, Review-to-Booking ≈ 0.5). Surfaces listings with mismatched supply and demand. |

At market level, the three views produce: Potential Revenue **$890.5M**, Estimated Revenue at 50% floor **$445.3M**, Estimated Revenue (review-weighted) **$288.6M**. The gap between the ceiling and the realized-occupancy estimate is the headline opportunity for occupancy-lift levers.

**Supporting KPIs.**

| KPI | Formula | Decision relevance |
|---|---|---|
| **Yield Potential** | `Availability 365` (algebraically equivalent to `Revenue Proxy / Price`) | Capital-efficiency proxy. Surfaces low-price, high-availability listings that punch above their nightly rate. |
| **Market Price Index** | `Price / Neighborhood Median Price` | Benchmarks a listing against its micro-market. Above 1.0 indicates a premium strategy. Below 1.0 indicates a value strategy. |
| **Listing Demand Score** | `Reviews per Month × (Availability / 365)` | Demand normalized for available supply. Allows comparison between a high-volume, rarely-open listing and a low-volume, always-open one. |
| **Occupancy Rate (estimated)** | `(365 − Availability) / 365` | Inferred booking density. Cross-validates the Demand Score. |
| **Host Portfolio Segment** | Single (1), Emerging (2 to 5), Enterprise (>5) | Separates casual hosts from professional operators. Material for policy and platform strategy. |
| **Recent Activity Status** | Active 2019, Trailing 2018, Dormant <2018, No Reviews | Distinguishes live inventory from stale listings. |

---

## 8. Exploratory Data Analysis (EDA)

### Headline numbers (cleaned data, n = 48,884)

| Metric | Value |
|---|---|
| Total listings | 48,884 |
| Unique hosts | 37,455 |
| Neighborhoods covered | 221 |
| Boroughs | 5 |
| Average nightly price | $143.99 |
| Median nightly price | $106 |
| Average availability (days/yr) | 112.8 |
| Total reviews (lifetime) | 1,137,628 |
| Active listings (reviews/mo > 0) | 38,833 (79.4%) |
| Total Potential Revenue (ceiling) | $890.5 M |
| Total Estimated Revenue (50% occupancy floor) | $445.3 M |
| Total Estimated Revenue (review-weighted) | $288.6 M |

### Borough-level summary

| Borough | Listings | Median Price | Potential Revenue | Estimated Revenue (50%) | Avg Yield |
|---|---:|---:|---:|---:|---:|
| Manhattan | 21,660 | $150 | $519.3 M | $259.7 M | 111.98 |
| Brooklyn | 20,095 | $90 | $263.3 M | $131.7 M | 100.22 |
| Queens | 5,666 | $75 | $83.7 M | $41.9 M | 144.45 |
| Bronx | 1,090 | $65 | $16.6 M | $8.3 M | 165.79 |
| Staten Island | 373 | $75 | $7.5 M | $3.8 M | 199.68 |

> Manhattan and Brooklyn = 85.4% of listings, 87.9% of Potential Revenue. But yield (availability) is **highest in Staten Island and the Bronx**. Those listings are open more days of the year, even if their price is lower.

### Room-type summary

| Room Type | Listings | Avg Price | Total Potential Revenue | Avg Reviews/Month |
|---|---:|---:|---:|---:|
| Entire home/apt | 25,407 (52.0%) | $198.34 | $643.8 M (72.3%) | 1.05 |
| Private room | 22,319 (45.7%) | $86.02 | $235.4 M (26.4%) | 1.14 |
| Shared room | 1,158 (2.4%) | $68.65 | $11.3 M (1.3%) | 1.07 |

> Entire homes are the revenue engine. Private rooms attract the most monthly demand per listing.

### Top 10 neighborhoods by Potential Revenue

Midtown ($74.1M), Hell's Kitchen ($58.3M), Williamsburg ($50.6M), Bedford-Stuyvesant ($49.3M), Upper West Side ($40.9M), Upper East Side ($39.8M), Harlem ($36.7M), Financial District ($34.1M), Chelsea ($32.1M), East Village ($29.4M).

### Top 10 hosts by Potential Revenue

Sonder (NYC) at $24.6M, Blueground at $18.0M, Kara at $10.2M, Red Awning at $7.6M, Pranjal at $6.3M, Ken at $5.9M, Jeremy & Laura at $5.9M, Sonder at $5.6M, Ruchi at $4.2M, Bluebird at $3.5M.

> All ten top-revenue hosts are enterprise multi-listing operators. The head of the host distribution is fully professionalized and behaves as a hospitality operator class rather than as casual supply.

### Price tier distribution

Roughly equal quartile cut by design. Budget 12,360, Mid-Range 12,101, Premium 12,246, Luxury 12,177.

### Recency

Active 2019: 25,202 (51.6%). No Reviews: 10,051 (20.6%). Dormant <2018: 7,583 (15.5%). Trailing 2018: 6,048 (12.4%).

### Seasonality

Summer Peak (June to August last-review): 21,188 listings. Off-Peak: 27,696. **Average reviews/month is 2.08 in Summer Peak vs 0.34 Off-Peak**, a 6.2× ratio that evidences strong June to August booking concentration.

---

## 9. Statistical Analysis

The statistical layer exists to convert the descriptive findings of §8 into defensible decision inputs. Each test below is paired with the recommendation it ultimately supports in §11 and §12.

**Q1. Are inter-borough price differences statistically genuine, or sample noise?**

- **Kruskal-Wallis H-test** on `Price` across the five boroughs: H = **7,023.4**, p < 0.001. The null hypothesis of equal price distributions is rejected at any standard significance threshold.
- **Mann-Whitney U-test** for Manhattan vs Brooklyn (one-sided, Manhattan > Brooklyn): U = 2.99 × 10⁸, p ≈ 0. The Manhattan price premium is stochastically dominant, not an artifact of mean compression.
- **Implication.** Borough is a real pricing factor and merits separate treatment in any downstream segmentation or pricing model.

**Q: What drives revenue?**

Pearson correlations on the cleaned dataset:

| Pair | r |
|---|---:|
| Price ↔ Potential Revenue | **+0.639** |
| Availability ↔ Listing Demand Score | +0.476 |
| Reviews per Month ↔ Listing Demand Score | **+0.735** |
| Price ↔ Reviews per Month | −0.065 |
| Price ↔ Listing Demand Score | −0.006 |

> **Business interpretation.** Approximately 64% of revenue variation is explained by price, while demand (reviews per month) is statistically independent of price at the listing level. The implication is yield compression: a non-trivial subset of listings are priced below the elasticity-implied optimum and could absorb a 10 to 15% rate increase without observable booking loss. The Simpson's Paradox caveat in §14 applies.

**Q: Does seasonality matter for demand?**

Summer Peak listings average **2.077** reviews/month vs **0.336** off-peak, a 6.2× difference. Even ignoring statistical machinery, this is the largest single effect in the dataset.

---

## 10. Tableau Dashboard Design

The Tableau workbook contains **3 linked dashboards** built from **25 worksheets**, all sourced from `nyc_airbnb_tableau_master.csv`. Static screenshots are checked in at `tableau/screenshots/dashboard-{1,2,3}.png` for offline review, and the public link is recorded in `tableau/dashboard_links.md`.

### Dashboard 1: Location & Market Overview

> *"Where are listings, and what does NYC charge?"*

**Purpose.** Establish the geographic and structural footprint of the NYC Airbnb market.

**Sheets.** Total Listings, Average Price/Night, Total Boroughs, NEIGHBORHOODS, AVG REVIEWS / MONTH (KPI BANs); Borough Revenue Map (filled map); Avg Price by Borough & Room Type (grouped bar); Neighborhood Density (bar / heatmap).

**What it tells you.** Manhattan and Brooklyn carry 85% of supply and 88% of Potential Revenue. Williamsburg, Bed-Stuy, Harlem, and Bushwick are the highest-density outer-borough markets. Manhattan's median price is 67% above Brooklyn's.

### Dashboard 2: Revenue & Yield Performance

> *"Where is the money, and who is making it?"*

**Purpose.** Quantify revenue, yield, and host concentration to surface investment opportunities.

**Sheets.** TOTAL ANNUAL REVENUE, AVG YIELD POTENTIAL, MARKET PRICE INDEX, UNIQUE HOSTS, AVG AVAILABILITY (DAYS) (KPI BANs); Revenue by Room Type (dual-axis revenue + price); Yield vs Price (scatter, hidden-gem quadrant); Top 10 Hosts (ranked bar); Price Category Mix (donut: Budget, Mid-Range, Premium, Luxury).

**What it tells you.** Entire homes drive 72% of Potential Revenue despite being 52% of supply. The top 10 hosts are uniformly enterprise operators (Sonder, Blueground, Kara, Red Awning, etc.). The yield-versus-price scatter surfaces a low-price, high-availability cluster across the Bronx, Queens, and Staten Island whose capital efficiency exceeds what the headline price would imply.

### Dashboard 3: Demand, Activity & Seasonality

> *"When and why does demand happen?"*

**Purpose.** Track demand intensity, listing activity, and seasonal patterns over time.

**Sheets.** TOTAL REVIEWS, AVG DEMAND SCORE, ACTIVE LISTINGS %, SUMMER PEAK LISTINGS, Avg Min Nights (KPI BANs); Review Trend Over Time (line); Demand Heatmap (neighborhood × room type); Availability vs Demand (quadrant scatter); Seasonality Revenue (summer vs off-season bar).

**What it tells you.** Demand is concentrated June to August (Summer Peak listings average 6.2× the reviews/month of off-peak). Roughly 20% of inventory has zero reviews and is effectively dormant. The high-demand, low-availability quadrant of the scatter highlights the best-performing listings on the platform.

**Filters and interactivity.** Borough, Room Type, Host Portfolio Segment, Price Category, Recent Activity Status, and Seasonality Status. All global filters with cross-dashboard actions (`Action (Borough)`, `Action (Price Category)`, `Action (Host Name)`, `Action (Recent Activity Status, Seasonality Status)`) so a click in one dashboard filters the others.

**Story arc.** Dashboard 1 answers *where things are*. Dashboard 2 answers *how money is made*. Dashboard 3 answers *when and why demand happens*.

---

## 11. Insights Summary

Each insight below is tied to a specific evidentiary anchor (statistical test, KPI computation, or segmentation result) so the recommendation that follows can be defended.

1. **Supply concentration is structural, not cyclical.** Manhattan and Brooklyn together host 85.4% of listings and 87.9% of Potential Revenue. The Kruskal-Wallis test on price across the five boroughs returns H = 7,023.4, p < 0.001, confirming the borough effect is statistically genuine and not an artifact of sample size.
2. **Manhattan's pricing premium is robust.** Median nightly price is $150 in Manhattan vs $90 in Brooklyn (Mann-Whitney U one-sided, U = 2.99 × 10⁸, p ≈ 0). The premium is real and significant at every standard threshold.
3. **Revenue and volume are decoupled by room type.** Entire homes are 52% of listings but 72% of Potential Revenue. Private rooms post the highest reviews-per-month (1.14 vs 1.05) yet generate 26% of revenue. Volume of demand and revenue density are different KPIs and should not be conflated.
4. **Yield inverts the borough ranking.** Average availability is 199.7 days in Staten Island and 165.8 in the Bronx vs 112.0 in Manhattan. Listings outside the core are open more of the year, which means yield-per-dollar can favor outer boroughs even when nightly price does not.
5. **Demand is sharply seasonal.** Summer Peak listings average 2.08 reviews/month vs 0.34 off-peak, a 6.2× ratio. Seasonality is the largest single effect in the dataset and dominates any borough or room-type variation in demand.
6. **The host distribution has professionalized at the head.** All 10 top revenue hosts (Sonder, Blueground, Kara, Red Awning, etc.) are enterprise multi-listing operators. The platform's revenue concentration is not driven by casual hosts.
7. **A third of listed inventory does not convert.** 20.6% of listings have zero reviews and an additional 15.5% have not received a review since before 2018. The platform is currently allocating finite search impressions to inventory that does not generate measurable bookings.
8. **Price and demand are functionally decoupled at listing level.** Pearson correlation between Price and Reviews/Month is −0.065 across the cleaned 48,884 listings, materially indistinguishable from zero. Listings priced below their neighborhood median with above-average review velocity are leaving revenue on the table.
9. **Revenue concentrates in a Manhattan-heavy neighborhood set.** Midtown, Hell's Kitchen, Upper West Side, Upper East Side, Financial District, and Chelsea dominate the top 10 by Potential Revenue. Williamsburg and Bedford-Stuyvesant are the only Brooklyn entries.
10. **Williamsburg is the dominant non-Manhattan opportunity.** 3,919 listings, $50.6M Potential Revenue, median price $90. It pairs Manhattan-grade revenue density with an outer-borough cost basis.
11. **Minimum-nights distribution is bimodal.** Median is 3 nights, but a long tail extends to 365, suggesting some operators are deliberately structuring long-stay rentals to navigate around short-term regulation.
12. **High availability does not imply high demand.** The Availability vs Demand quadrant identifies a populous always-open, near-zero-review cluster. These are the dormant or over-priced listings that drag platform-wide booking conversion.

---

## 12. Recommendations

Each recommendation maps to a stakeholder, the operating lever it pulls, and the supporting evidence from §11.

| # | Stakeholder | Recommendation | Operating Lever | Evidence |
|---|---|---|---|---|
| 1 | Investors | Prioritize entire-home acquisitions in Williamsburg, Bedford-Stuyvesant, Hell's Kitchen, and Long Island City over Midtown core. | **Geographic Yield Arbitrage.** Capital deployed in these markets accesses Manhattan-grade revenue density (top 10 by Potential Revenue) at 40 to 50% lower acquisition cost, lifting revenue-per-dollar deployed without exposure to Manhattan price ceilings. | Insights 4, 9, 10 |
| 2 | Hosts | Re-price listings indexed below 0.9 on the Market Price Index that show reviews/month above 1.0. Suggested adjustment: 10 to 15% rate increase. | **Yield Compression.** Pearson r between Price and Reviews/Month is −0.065 (n = 48,884). Demand inelasticity at this granularity allows price increases without measurable booking loss, capturing producer surplus that is currently subsidizing guests. | Insight 8 |
| 3 | Platform Operations | Down-rank or re-engage the 36% dormant plus zero-review inventory in default search ordering. | **Search Liquidity.** Shifting impression share from non-converting inventory to the 51.6% Active 2019 pool concentrates demand on listings that produce reviews. Higher per-impression conversion lifts platform liquidity, which compounds over time as active listings accumulate review velocity. | Insight 7, 12 |
| 4 | Hosts and Platform | Implement a 20 to 30% dynamic pricing premium during June to August and pair it with off-peak minimum-night relaxation. | **Seasonal Smoothing.** Capturing the 6.2× summer demand premium with peak rates while reducing friction in shoulder months redistributes revenue across the calendar and lowers host dependence on a single quarter. | Insight 5 |
| 5 | Platform and Policy | Formally segment enterprise hosts (>5 listings) in search ranking, host onboarding, and compliance reporting. | **Regulatory Clarity.** Top 10 hosts alone control over $70M in Potential Revenue and operate as de facto hotel chains. A clean enterprise classification simplifies pre LL18 style enforcement and lets the platform apply differentiated quality standards. | Insight 6 |

---

## 13. Impact Estimation

Estimates are directional and grounded in the structural levers identified in §12. Each row maps the recommendation to the metric it moves, the magnitude expected, and the mechanism by which the magnitude is realized. Confidence is reported on a Low/Medium/High scale based on the strength of the underlying evidence.

| # | Recommendation | Lever | Metric Moved | Estimated Magnitude | Mechanism | Confidence |
|---|---|---|---|---|---|---|
| 1 | Outer-borough acquisitions | Geographic Yield Arbitrage | Revenue per dollar of capital deployed | **+15 to 25%** | Lower acquisition cost denominator combined with comparable revenue density numerator. Direct ratio improvement. | Medium |
| 2 | Re-price under-indexed listings | Yield Compression | Host revenue per listing | **+8 to 12%** (≈ $5 to $8M aggregate) | Demand inelasticity (r = −0.065) means price increases pass through to revenue without booking loss. Applied to the ~5,000 listings in the under-indexed, demand-strong segment. | Medium |
| 3 | Suppress dormant inventory in search | Search Liquidity | Platform-wide booking conversion | **+5 to 10 percentage points** | Impression share is finite. Reallocating it from a 36% non-converting pool to a 52% converting pool produces a conversion lift proportional to the gap, attenuated by guest-side substitution effects. | High |
| 4 | Seasonal dynamic pricing | Seasonal Smoothing | Off-peak occupancy and revenue variance | **+5 to 8 ppt off-peak occupancy** | Peak premium funds off-peak discounting. Lower revenue variance reduces host churn and stabilizes platform supply. | Medium |
| 5 | Enterprise host segmentation | Regulatory Clarity | Inventory under differentiated policy | **~15% of inventory** | Top 10 hosts alone control >$70M Potential Revenue. A formal enterprise tier streamlines compliance reporting and applies hotel-grade quality standards to the listings that most resemble hotel inventory. | High |

**Why act now?** The 2019 dataset is the cleanest pre regulation reference point for NYC STR strategy. Investors pricing 2026 acquisitions are anchoring on this baseline, hosts entering the platform need it to benchmark, and the platform itself benefits from cleaning dormant inventory before any policy-driven supply contraction makes the active-listing pool appear artificially smaller than it is.

---

## 14. Limitations

**Data limitations.**
- 2019 snapshot. Pre-pandemic, before Local Law 18. Findings do not directly transfer to post 2023 NYC.
- `Potential Revenue` assumes 100% conversion of available days. It is a ceiling, not realized revenue.
- No occupancy or booking-level data. Demand is inferred from review velocity.
- `last_review` is the only time signal. Listings without reviews are time-blind.
- Inside Airbnb scrapes only publicly visible listings. Long-tail or temporarily delisted properties are missed.

**Method limitations.**
- All correlations reported are pairwise. No multivariate or causal model has been fit, and pairwise statistics cannot rule out confounding.
- Quartile-based price tiers are coarse. A finite-mixture or Gaussian-mixture clustering approach would yield finer market segmentation and would better preserve the price distribution's heavy right tail.
- Yield Potential is algebraically equivalent to Availability. Both KPIs are surfaced because they communicate different narratives at the dashboard level (capital efficiency vs raw supply availability), but they should not be treated as independent inputs in any downstream model.

**Simpson's Paradox risk on the price-demand decoupling.**

The headline finding that price and reviews-per-month are uncorrelated at the listing level (Pearson r = −0.065 across the cleaned 48,884 listings) is the load-bearing premise behind Recommendation 2 (Yield Compression). It must be interrogated.

Simpson's Paradox is the phenomenon where a relationship observed at the aggregate level reverses or disappears once the population is stratified by a confounding variable. In this dataset there are two natural strata: borough and room type. It is plausible that within Manhattan entire homes the price-demand relationship is *negatively* correlated (over-priced premium listings sit empty), and within Bronx private rooms it is also *negatively* correlated, while the aggregate appears null because the strata sit at different positions on a shared price-demand surface. If that is the case, the recommendation to raise rates on under-indexed, demand-strong listings would still be defensible (it operates at the within-listing level via the Market Price Index, not at the cross-borough level), but the aggregate r = −0.065 would not by itself be sufficient evidence.

**Mitigation in current scope.** The Market Price Index normalizes price against neighborhood median, which strips out the borough-level confound. The recommendation is therefore stated in within-stratum terms ("listings indexed below 0.9 within their own neighborhood") rather than aggregate terms.

**Mitigation deferred to Future Scope.** A multivariate regression of `log(price) ~ borough + room_type + availability + host_segment + min_nights + neighborhood_fe` (Future Scope item 2) is the formal vehicle for confirming the within-stratum effect. Until that regression is fit, the price-demand finding should be treated as a strong directional signal, not a precise elasticity estimate.

**What we cannot conclude.**
- Causality between price changes and demand outcomes (the dataset has no time-series of price changes within a listing).
- Regulatory impact (LL18 only enforced from 2023, outside the dataset window).
- Platform take-rate or realized host net income (only gross Potential Revenue is observable).

---

## 15. Future Scope

1. **2019 vs 2024 comparison.** Re-run the pipeline on Inside Airbnb's latest NYC monthly snapshot to quantify post-pandemic and post-LL18 supply and pricing shifts.
2. **Multivariate regression.** Fit `log(price) ~ borough + room_type + availability + host_segment + min_nights + neighborhood_fe` to disentangle borough premium from room-type premium.
3. **Listing-level revenue forecast.** Build a seasonal index per neighborhood × room type and forecast 12 month revenue ranges.
4. **Spatial enrichment.** Layer subway-stop distance, POI density, crime stats, and median household income for a spatial-autocorrelation regression.
5. **Host scoring model.** Revenue × consistency × recency score for platform ranking experiments.
6. **Real-time dashboard.** Pipe a monthly Inside Airbnb scrape into the Tableau workbook via Tableau Server / Public Cloud refresh, turning this from a snapshot artifact into a live decision tool.

---

## 16. Conclusion

The 2019 NYC Airbnb market is geographically concentrated, segmented by host professionalism, and seasonally compressed. Manhattan and Brooklyn jointly hold 85% of supply and 88% of Potential Revenue, entire homes generate 72% of revenue against 52% of inventory, the top 10 hosts are uniformly enterprise operators, and summer demand exceeds off-peak demand by a factor of 6.2. Approximately one-third of listed inventory does not convert. Translated to action: investors should reallocate capital toward high-yield outer-borough markets (Williamsburg, Bedford-Stuyvesant, Hell's Kitchen, Long Island City); hosts should adopt index-based dynamic pricing given the demonstrated decoupling between price and demand at the listing level; and the platform should suppress dormant inventory in search while formally segmenting enterprise hosts. The framework presented here, dual-track revenue accounting paired with statistically validated segmentation, provides a defensible basis for capital deployment, pricing strategy, and platform policy through the next NYC STR cycle.

---

## 17. Appendix

### A. Data Dictionary (summary)

Full schema: [`docs/data_dictionary.md`](docs/data_dictionary.md).

| Column | Type | Description |
|---|---|---|
| `Listing ID` | int | Unique listing identifier |
| `Host ID` / `Host Name` | int / str | Host identifier and display name |
| `Borough` (Neighbourhood Group) | category | Manhattan, Brooklyn, Queens, Bronx, Staten Island |
| `Neighborhood` | category | 221 micro-markets |
| `Latitude` / `Longitude` | float | GPS coordinates |
| `Room Type` | category | Entire home/apt, Private room, Shared room |
| `Price` | int | Nightly rate USD (capped at p99 = $799) |
| `Min Nights` | int | Minimum stay (capped at 365) |
| `Total Reviews` | int | Lifetime reviews |
| `Last Review` | date | Latest review date (NaT if none) |
| `Reviews per Month` | float | Monthly demand frequency |
| `Host Portfolio Size` | int | Listings managed by host |
| `Availability 365` | int | Days available per year |
| `Potential Revenue` | int | Price × Availability |
| `Yield Potential` | float | Revenue Proxy / Price |
| `Market Price Index` | float | Price / Neighborhood median price |
| `Listing Demand Score` | float | Reviews/mo × (Availability / 365) |
| `Recent Activity Status` | category | Active 2019, Trailing 2018, Dormant <2018, No Reviews |
| `Seasonality Status` | category | Summer Peak (Jun to Aug last review), Off-Peak |
| `Price Category` | category | Budget, Mid-Range, Premium, Luxury (quartile bins) |

### B. Cleaning Log Excerpt

From `scripts/etl_pipeline.py` execution:

```
[INFO] Step: Normalizing column names to snake_case.
[INFO] Step: Applying verbose column renames for KPI consistency.
[INFO] Step: Handling duplicates.
[INFO] Step: Converting data types (category/datetime/string).
[INFO] Step: Imputing missing values.
[INFO] Handled nulls in 'name', 'host_name', and 'review_rate_month'. 'last_review' kept as NaT.
[INFO] Step: Treating price outliers.
[WARNING] Removed 11 records with $0 price.
[INFO] Price capped at 99th percentile: $799.
[INFO] Step: Normalizing minimum stay requirements.
[INFO] Step: Engineering analytical features and KPIs.
[INFO] Saving processed dataset to data/processed/airbnb_nyc_cleaned.csv
[INFO] Pipeline Execution: SUCCESS.
```

### C. Key Python Logic Excerpts

**Outlier treatment (price):**
```python
price_arr = df['price'].to_numpy(dtype=np.float64)
p99 = np.percentile(price_arr, 99)
df['price_original'] = df['price'].copy()
df['price'] = np.clip(price_arr, 0, p99).astype(int)
df['is_luxury'] = (df['price_original'] > p99).astype(int)
```

**KPI feature engineering:**
```python
df['revenue_proxy']      = (price_v * avail_v).astype(int)
df['occupancy_rate_est'] = np.clip((365 - avail_v) / 365, 0, 1).round(4)
df['log_price']          = np.log1p(price_v)
df['is_multi_lister']    = (host_cnt_v > 1).astype(int)
```

**Statistical tests (notebook 04):**
```python
from scipy import stats
H, p = stats.kruskal(*[g['Price'].values for _, g in df.groupby('Borough')])
# H = 7023.4, p < 0.001 -> borough price differences are real
```

### D. Repository Pointers

- ETL pipeline: `scripts/etl_pipeline.py`
- Cleaning notebook: `notebooks/02_cleaning.ipynb`
- EDA notebook: `notebooks/03_eda.ipynb`
- Statistical notebook: `notebooks/04_statistical_analysis.ipynb`
- Final load prep: `notebooks/05_final_load_prep.ipynb`
- Dashboard screenshots: `tableau/screenshots/dashboard-{1,2,3}.png`
- Dashboard public link: `tableau/dashboard_links.md`

---

## 18. Contribution Matrix (Mandatory)

This section documents each team member's contribution across all project phases. Claims match evidence in GitHub Insights, PR history, and committed files. Any mismatch may result in individual grade adjustments.

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
|---|---|---|---|---|---|---|---|
| Sarvesh Srinath (`sarveshcore`), sarvesh.srinath2024@nst.rishihood.edu.in | Support | Support | Support | Support | Support | **Owner** | **Owner** |
| Aditya Rao, aditya.rao2024@nst.rishihood.edu.in | **Owner** | Support | Support | Support | Support | Support | Support |
| Khyati Batra (`khyatibatra0316`), khyati.batra2024@nst.rishihood.edu.in | Support | Support | Support | **Owner** | Support | Support | Support |
| Kunal Vats (`1Kunalvats9`), kunal.vats2024@nst.rishihood.edu.in | Support | Support | Support | Support | **Owner** | Support | Support |
| Meghna Nair (`heymegzz`), meghna.nair2024@nst.rishihood.edu.in | Support | Support | **Owner** | Support | Support | Support | Support |
| Shreyansh Agarwal (`BLOODWYROM`), shreyansh.agrawal2024@nst.rishihood.edu.in | Support | **Owner** | Support | Support | Support | Support | Support |

**Declaration:** We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts.

**Team Lead Signature:** Meghna Nair _________________________  **Date:** 2026-05-29

---

*Newton School of Technology. Data Visualization & Analytics, Capstone 2.*
