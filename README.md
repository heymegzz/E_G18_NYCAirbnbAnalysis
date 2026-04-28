# E_G18_NYCAirbnbAnalysis

> Capstone 2, Newton School of Technology, Data Visualization and Analytics.
> NYC Airbnb 2019 market, revenue, and demand analysis. Section E, Team G18.

This repository contains the ETL pipeline, analysis notebooks, Tableau workbook artifacts, and final deliverables. For the project narrative, methodology, KPIs, insights, and recommendations, see [`project_report.md`](project_report.md).

---

## Repository Layout

```text
E_G18_NYCAirbnbAnalysis/
|
|-- README.md                          # This file. Repo guide and setup.
|-- project_report.md                  # Full Capstone 2 report (the source of truth).
|-- requirements.txt                   # Python dependencies.
|
|-- data/
|   |-- raw/
|   |   `-- AB_NYC_2019.csv            # Original Kaggle dataset (never edited).
|   `-- processed/
|       |-- airbnb_nyc_cleaned.csv     # Analytical layer (snake_case, 27 cols).
|       `-- nyc_airbnb_tableau_master.csv  # BI layer, 23 cols. Tableau source.
|
|-- notebooks/
|   |-- 01_extraction.ipynb            # Load raw, profile schema.
|   |-- 02_cleaning.ipynb              # Cleaning logic, mirrors etl_pipeline.py.
|   |-- 03_eda.ipynb                   # EDA, headline numbers, segment cuts.
|   |-- 04_statistical_analysis.ipynb  # Kruskal-Wallis, Mann-Whitney, correlations.
|   `-- 05_final_load_prep.ipynb       # Build the Tableau master CSV.
|
|-- scripts/
|   |-- __init__.py
|   `-- etl_pipeline.py                # Reproducible end-to-end ETL (run this).
|
|-- tableau/
|   |-- dashboard_links.md             # Public Tableau URLs.
|   `-- screenshots/
|       |-- dashboard-1.png            # Location and Market Overview.
|       |-- dashboard-2.png            # Revenue and Yield Performance.
|       `-- dashboard-3.png            # Demand, Activity, and Seasonality.
|
|-- reports/
|   |-- README.md                      # Notes on report deliverables.
|   |-- NYC Airbnb Report.pdf          # Final report PDF.
|   |-- NYCAirbnb Presentation.pdf     # Final presentation PDF.
|   |-- presentation_outline.md        # Slide-by-slide outline.
|   `-- presentation_content.md        # Slide-by-slide speaker content.
|
|-- docs/
|   `-- data_dictionary.md             # Full column schema (raw and engineered).
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Quick Start

```bash
git clone https://github.com/heymegzz/E_G18_NYCAirbnbAnalysis.git
cd E_G18_NYCAirbnbAnalysis

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option A. Run the full ETL end-to-end.
python scripts/etl_pipeline.py

# Option B. Open the notebooks.
jupyter notebook
```

Running `scripts/etl_pipeline.py` consumes `data/raw/AB_NYC_2019.csv` and writes both processed CSVs into `data/processed/`. The pipeline is logging-enabled and idempotent.

**Dependencies** (`requirements.txt`): pandas, numpy, matplotlib, seaborn, scipy, statsmodels, jupyter.

---

## Where to Find What

| You want… | Look at… |
|---|---|
| The full project narrative, KPIs, statistical results, insights, recommendations | [`project_report.md`](project_report.md) |
| The exported report PDF | [`reports/NYC Airbnb Report.pdf`](reports/) |
| The exported presentation PDF | [`reports/NYCAirbnb Presentation.pdf`](reports/) |
| Slide outline and speaker content | [`reports/presentation_outline.md`](reports/presentation_outline.md), [`reports/presentation_content.md`](reports/presentation_content.md) |
| The cleaning and feature-engineering code | [`scripts/etl_pipeline.py`](scripts/etl_pipeline.py) |
| Statistical tests (Kruskal-Wallis, Mann-Whitney, correlations) | [`notebooks/04_statistical_analysis.ipynb`](notebooks/04_statistical_analysis.ipynb) |
| The Tableau-ready master dataset | [`data/processed/nyc_airbnb_tableau_master.csv`](data/processed/) |
| Column definitions for raw and engineered fields | [`docs/data_dictionary.md`](docs/data_dictionary.md) |
| Tableau dashboard public links | [`tableau/dashboard_links.md`](tableau/dashboard_links.md) |
| Dashboard screenshots for offline review | [`tableau/screenshots/`](tableau/screenshots/) |

---

## Notebook Order

The notebooks are designed to run sequentially and can be executed independently of `scripts/etl_pipeline.py` (the pipeline consolidates `01` to `05`).

1. **`01_extraction.ipynb`** loads the raw CSV and profiles the schema.
2. **`02_cleaning.ipynb`** applies cleaning rules: drop zero-price rows, cap price at p99, cap minimum nights at 365, impute missings, normalize columns.
3. **`03_eda.ipynb`** produces headline numbers and segment cuts (borough, room type, neighborhood, host).
4. **`04_statistical_analysis.ipynb`** runs Kruskal-Wallis on price across boroughs, Mann-Whitney for Manhattan vs Brooklyn, and Pearson correlations on the KPI set.
5. **`05_final_load_prep.ipynb`** assembles `nyc_airbnb_tableau_master.csv` with verbose column names and segmentation labels.

---

## Data

| Field | Value |
|---|---|
| Source | Kaggle, *New York City Airbnb Open Data 2019* (Inside Airbnb) |
| Link | https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data |
| Raw rows | 48,895 |
| Cleaned rows | 48,884 |
| Columns (Tableau master) | 23 (16 base, 7 engineered) |
| Time period | Listings live as of 2019 snapshot, reviews July 2011 to July 2019 |

The raw file is committed to `data/raw/` so the pipeline runs without external downloads.

---

## Team

| Member | GitHub | Role Owner |
|---|---|---|
| Meghna Nair | `heymegzz` | Team Lead, EDA and Analysis |
| Aditya Rao | | Dataset and Sourcing |
| Shreyansh Agarwal | `BLOODWYROM` | ETL and Cleaning |
| Khyati Batra | `khyatibatra0316` | Statistical Analysis |
| Kunal Vats | `1Kunalvats9` | Tableau Dashboard |
| Sarvesh Srinath | `sarveshcore` | Report Writing, PPT and Viva |

Full contribution matrix in `project_report.md` §18.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 with Jupyter | ETL, cleaning, EDA, statistical tests |
| pandas, numpy | Vectorized data manipulation |
| scipy, statsmodels | Statistical tests |
| matplotlib, seaborn | Notebook charts |
| Tableau Public | Three published dashboards |
| GitHub | Version control and contribution audit |

---

*Newton School of Technology. Data Visualization and Analytics, Capstone 2.*
