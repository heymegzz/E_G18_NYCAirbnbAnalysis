# Presentation Content

Slide-by-slide speaker content for the Capstone 2 deck. Numbers are sourced from `project_report.md` (cleaned dataset, n = 48,884).

---

## Slide 1. Title

**Title:** NYC Airbnb 2019. Market, Revenue, and Demand Analysis
**Sector:** Travel and Hospitality (Short-Term Rental Marketplaces)
**Team ID:** G18, Section E
**Institute:** Newton School of Technology, Data Visualization and Analytics, Capstone 2
**Submission Date:** 2026-05-28

**Team and Roles**
- Meghna Nair (`heymegzz`), Team Lead and EDA Owner
- Aditya Rao, Dataset and Sourcing Owner
- Shreyansh Agarwal (`BLOODWYROM`), ETL and Cleaning Owner
- Khyati Batra (`khyatibatra0316`), Statistical Analysis Owner
- Kunal Vats (`1Kunalvats9`), Tableau Dashboard Owner
- Sarvesh Srinath (`sarveshcore`), Report Writing and PPT Owner

**Faculty Mentor:** [insert mentor name]

---

## Slide 2. Context and Problem Statement

**Sector context.** Short-term rentals are a $100B+ global category. NYC is the largest single STR market in the world. The 2019 snapshot is the last clean pre-pandemic, pre Local Law 18 baseline, the canonical reference for research and investment models.

**Stakeholders.** Three competing decision-makers share one dataset.
- Real-estate investors deciding where capital converts to nightly revenue.
- Hosts setting price, minimum nights, and room type.
- Platform operations managing inventory quality and search ranking.

**Core question.** Where does revenue concentrate, which segments deliver the highest yield, and when does demand actually materialize, so that decisions can be made on KPIs instead of headline averages?

**Objective.** Build a reproducible ETL, a dual-track revenue framework, four decision-grade KPIs, and three Tableau dashboards that deliver at least eight statistically anchored insights and three actionable recommendations.

---

## Slide 3. Data Engineering

**Source.** Kaggle, *New York City Airbnb Open Data 2019* (Inside Airbnb).

**Size and coverage.**
- 48,895 raw rows, 48,884 cleaned rows (zero-price and duplicates removed).
- 16 raw columns, 23 columns in the Tableau master (16 base plus 7 engineered).
- 5 boroughs, 221 neighborhoods, 37,455 unique hosts.
- Listings live as of 2019 snapshot, reviews from July 2011 to July 2019.

**Major cleaning steps (`scripts/etl_pipeline.py`).**
1. Normalize columns to snake_case and rename for KPI readability.
2. Drop full-row duplicates, then by `id` keeping the row with the most reviews.
3. Type conversion: `last_review` to datetime, categorical for borough, neighborhood, room type.
4. Impute missings: `name` and `host_name` placeholders, `review_rate_month` to 0.0, `last_review` retained as NaT.
5. Outlier treatment: remove `price = 0` (11 rows), cap price at p99 ($799), flag `is_luxury`, cap `minimum_nights` at 365.
6. Feature engineering: `log_price`, `revenue_proxy`, `occupancy_rate_est`, `is_multi_lister`, `has_reviews`, `borough_core`, `price_tier`, `review_year`, `review_month`.

**Data dictionary summary.** Geographic (borough, neighborhood, lat/long), categorical (room type, price category, host portfolio segment, recent activity status, seasonality status), numeric (price, availability 365, reviews/month, potential revenue, yield potential, market price index, listing demand score). Full schema in `docs/data_dictionary.md`.

---

## Slide 4. KPI Framework

**Dual-track revenue.** Single-number revenue proxies are routinely over-interpreted. We surface two views and a demand-anchored alternative.

| KPI | Formula | Market-level value |
|---|---|---|
| Potential Revenue (ceiling) | Price × Availability 365 | $890.5 M |
| Estimated Revenue (50% occupancy) | Price × Availability × 0.5 | $445.3 M |
| Estimated Revenue (review-weighted) | Demand-anchored from review velocity | $288.6 M |

**Supporting KPIs.**
- **Yield Potential** = Availability 365. Capital-efficiency proxy. Surfaces low-price, high-availability listings.
- **Market Price Index** = Price / Neighborhood Median Price. Above 1.0 is premium, below 1.0 is value.
- **Listing Demand Score** = Reviews/Month × (Availability / 365). Demand normalized for available supply.
- **Occupancy Rate (estimated)** = (365 − Availability) / 365. Cross-validates the Demand Score.
- **Host Portfolio Segment** = Single (1), Emerging (2 to 5), Enterprise (>5).
- **Recent Activity Status** = Active 2019, Trailing 2018, Dormant <2018, No Reviews.

**Why they matter.** The gap between the $890.5M ceiling and the $445.3M realized estimate is the headline opportunity for occupancy-lift levers. The Market Price Index lets hosts re-price within their micro-market without confounding from borough effects. Host Portfolio Segment isolates enterprise operators that behave like hotel chains.

---

## Slide 5. Key EDA Insights

1. **Supply concentration.** Manhattan and Brooklyn together hold 85.4% of listings and 87.9% of Potential Revenue. Manhattan alone accounts for $519.3M of the $890.5M ceiling.
2. **Yield inverts the ranking.** Average availability is 199.7 days in Staten Island and 165.8 in the Bronx, versus 112.0 in Manhattan. Outer-borough listings are open more of the year.
3. **Room-type revenue gap.** Entire homes are 52% of inventory but 72.3% of Potential Revenue ($643.8M). Private rooms post higher reviews/month (1.14 vs 1.05) yet generate only 26.4% of revenue.
4. **Seasonality dominates demand.** Summer Peak (June to August) listings average 2.08 reviews/month versus 0.34 off-peak, a 6.2× ratio. The largest single effect in the dataset.
5. **Dormant inventory.** 20.6% of listings have zero reviews. Another 15.5% have not been reviewed since before 2018. Roughly one-third of inventory does not convert.
6. **Professionalized head.** All ten top-revenue hosts are enterprise multi-listing operators (Sonder NYC at $24.6M, Blueground at $18.0M, Kara at $10.2M).

---

## Slide 6. Advanced Analysis

**Statistical tests.**
- **Kruskal-Wallis** on Price across five boroughs: H = 7,023.4, p < 0.001. Borough price differences are statistically genuine.
- **Mann-Whitney U** for Manhattan vs Brooklyn (one-sided): U = 2.99 × 10⁸, p ≈ 0. The Manhattan premium is stochastically dominant, not mean compression.

**Correlation findings (Pearson, n = 48,884).**
| Pair | r |
|---|---:|
| Price vs Potential Revenue | +0.639 |
| Reviews/Month vs Listing Demand Score | +0.735 |
| Availability vs Listing Demand Score | +0.476 |
| Price vs Reviews/Month | −0.065 |
| Price vs Listing Demand Score | −0.006 |

**Business interpretation.** Roughly 64% of revenue variation is explained by price, while demand is statistically independent of price at the listing level. This is yield compression: a non-trivial subset of listings sit below their elasticity-implied optimum and could absorb a 10 to 15% rate increase without measurable booking loss. Simpson's Paradox caveat applies (see Slide 11).

**Segmentation output.** Host Portfolio Segments isolate enterprise operators (>5 listings) controlling >$70M of Potential Revenue. Recent Activity Status separates the 51.6% Active 2019 pool from the 36.1% dormant or never-reviewed pool.

---

## Slide 7. Dashboard Overview

Three linked Tableau dashboards, 25 worksheets, sourced from `nyc_airbnb_tableau_master.csv`.

**Executive view (Dashboard 1, Location and Market Overview).** Where are listings and what does NYC charge? KPI BANs for total listings, average price, boroughs, neighborhoods, average reviews/month. Borough revenue map, average price by borough and room type, neighborhood density.

**Operational view (Dashboard 2, Revenue and Yield Performance).** Where is the money and who is making it? KPI BANs for total annual revenue, average yield potential, market price index, unique hosts, average availability. Revenue by room type (dual-axis), yield-vs-price scatter with a hidden-gem quadrant, top 10 hosts ranked, price category mix.

**Demand view (Dashboard 3, Demand, Activity, and Seasonality).** When and why does demand happen? KPI BANs for total reviews, average demand score, active listings %, summer peak listings, average minimum nights. Review trend over time, neighborhood × room-type demand heatmap, availability-vs-demand quadrant, seasonality revenue split.

**Filters and drilldowns.** Borough, Room Type, Host Portfolio Segment, Price Category, Recent Activity Status, Seasonality Status. Cross-dashboard actions on Borough, Price Category, Host Name, and Activity × Seasonality so a click in one dashboard filters the others.

---

## Slide 8. Top Insights

1. **Williamsburg is the dominant non-Manhattan opportunity.** 3,919 listings, $50.6M Potential Revenue, median price $90. Manhattan-grade revenue density at an outer-borough cost basis.
2. **Price and demand are functionally decoupled.** Pearson r = −0.065 between Price and Reviews/Month across 48,884 listings. Listings priced below neighborhood median with above-average review velocity are leaving revenue on the table.
3. **A third of inventory does not convert.** 36.1% of listings are dormant or never-reviewed yet still consume search impressions that could go to the 51.6% Active 2019 pool.
4. **Enterprise operators run the head.** Top 10 hosts alone control over $70M of Potential Revenue. The platform's revenue is not driven by casual supply.

---

## Slide 9. Recommendations

| # | Stakeholder | Recommendation | Lever |
|---|---|---|---|
| 1 | Investors | Prioritize entire-home acquisitions in Williamsburg, Bedford-Stuyvesant, Hell's Kitchen, and Long Island City over Midtown core. | Geographic Yield Arbitrage |
| 2 | Hosts | Re-price listings indexed below 0.9 on Market Price Index with reviews/month above 1.0. Suggested 10 to 15% rate increase. | Yield Compression |
| 3 | Platform Operations | Down-rank or re-engage the 36% dormant plus zero-review inventory in default search ordering. | Search Liquidity |
| 4 | Hosts and Platform | Apply a 20 to 30% peak premium June to August, paired with off-peak minimum-night relaxation. | Seasonal Smoothing |
| 5 | Platform and Policy | Formally segment enterprise hosts (>5 listings) in search ranking, onboarding, and compliance reporting. | Regulatory Clarity |

---

## Slide 10. Impact

| # | Metric Moved | Estimated Magnitude | Confidence | Priority |
|---|---|---|---|---|
| 1 | Revenue per dollar of capital deployed | +15 to 25% | Medium | High |
| 2 | Host revenue per listing | +8 to 12% (≈ $5 to $8M aggregate) | Medium | High |
| 3 | Platform-wide booking conversion | +5 to 10 percentage points | High | Highest |
| 4 | Off-peak occupancy and revenue variance | +5 to 8 ppt off-peak occupancy | Medium | Medium |
| 5 | Inventory under differentiated policy | ~15% of inventory | High | Medium |

**Feasibility.** Recommendations 2, 3, and 5 are platform-side configuration changes (search ranking, host classification, host-facing pricing nudges) and can be deployed without new infrastructure. Recommendation 1 is an investor-facing memo. Recommendation 4 requires a seasonal pricing module but reuses existing availability fields. **Why act now:** the 2019 dataset is the cleanest pre regulation reference point; investors pricing 2026 acquisitions are anchoring on this baseline.

---

## Slide 11. Limitations

**Data constraints.**
- 2019 snapshot only. Pre-pandemic, before Local Law 18. Findings do not directly transfer to post 2023 NYC.
- Potential Revenue is a 100% conversion ceiling, not realized revenue.
- No occupancy or booking-level data. Demand is inferred from review velocity.
- Listings without reviews (~10k) are time-blind.
- Inside Airbnb scrapes only publicly visible listings, missing temporarily delisted properties.

**Method constraints.**
- All correlations reported are pairwise. No multivariate or causal model has been fit.
- Quartile-based price tiers are coarse. A finite-mixture clustering would yield finer segmentation.
- Yield Potential is algebraically equivalent to Availability and should not be treated as an independent input downstream.

**Simpson's Paradox risk.** The aggregate r = −0.065 between Price and Reviews/Month is the load-bearing premise behind Recommendation 2. Within-stratum effects (borough × room type) may differ. Mitigated in current scope by stating the recommendation in within-neighborhood terms via the Market Price Index. Formal mitigation deferred to a multivariate regression in Future Scope.

---

## Slide 12. Next Steps

**Future extensions.**
1. **2019 vs 2024 comparison.** Re-run the pipeline on the latest Inside Airbnb NYC snapshot to quantify post-pandemic and post-LL18 shifts.
2. **Multivariate regression.** Fit `log(price) ~ borough + room_type + availability + host_segment + min_nights + neighborhood_fe` to disentangle confounded premiums.
3. **Listing-level revenue forecast.** Build a seasonal index per neighborhood × room type for 12-month revenue ranges.
4. **Spatial enrichment.** Layer subway-stop distance, POI density, crime stats, and median household income for spatial-autocorrelation regression.
5. **Host scoring model.** Revenue × consistency × recency score for platform ranking experiments.
6. **Live dashboard.** Pipe a monthly Inside Airbnb scrape into the workbook via Tableau Server refresh.

**Closing summary.** The 2019 NYC Airbnb market is geographically concentrated, segmented by host professionalism, and seasonally compressed. Manhattan and Brooklyn hold 85% of supply and 88% of Potential Revenue, entire homes generate 72% of revenue against 52% of inventory, the top 10 hosts are uniformly enterprise operators, and summer demand is 6.2× off-peak. The dual-track revenue framework, four decision-grade KPIs, and three Tableau dashboards turn that structure into a defensible basis for capital deployment, pricing strategy, and platform policy through the next NYC STR cycle.
