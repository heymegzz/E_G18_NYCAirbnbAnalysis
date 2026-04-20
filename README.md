# NST DVA Capstone 2 - Project Repository

> **Newton School of Technology | Data Visualization & Analytics**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

## Before You Start

1. Rename the repository using the format `SectionName_TeamID_ProjectName`.
2. Fill in the project details and team table below.
3. Add the raw dataset to `data/raw/`.
4. Complete the notebooks in order from `01` to `05`.
5. Publish the final dashboard and add the public link in `tableau/dashboard_links.md`.
6. Export the final report and presentation as PDFs into `reports/`.

### Quick Start

If you are working locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

If you are working in Google Colab:

- Upload or sync the notebooks from `notebooks/`
- Keep the final `.ipynb` files committed to GitHub
- Export any cleaned datasets into `data/processed/`

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | _To be filled by team_ |
| **Sector** | _e.g. Retail, Finance, Healthcare, EdTech_ |
| **Team ID** | _e.g. DVA-B1-T3_ |
| **Section** | _To be filled by team_ |
| **Faculty Mentor** | _To be filled by team_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _To be filled by team_ |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | _Name_ | `github-handle` |
| Data Lead | _Name_ | `github-handle` |
| ETL Lead | _Name_ | `github-handle` |
| Analysis Lead | _Name_ | `github-handle` |
| Visualization Lead | _Name_ | `github-handle` |
| Strategy Lead | _Name_ | `github-handle` |
| PPT and Quality Lead | _Name_ | `github-handle` |

---

## Business Problem

_Describe the sector context, the decision-maker this project serves, and the core business challenge being addressed. Keep this to 3-5 sentences written in plain language, as if addressing a senior stakeholder._

**Core Business Question**

> _State the single main question your Tableau dashboard and Python analysis will answer._

**Decision Supported**

> _What action or decision will this analysis enable the stakeholder to take?_

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | _e.g. World Bank, data.gov.in, Kaggle (raw only)_ |
| **Direct Access Link** | _Paste the direct download or access URL_ |
| **Row Count** | _Must be greater than 5,000_ |
| **Column Count** | _Must be greater than 8 meaningful columns_ |
| **Time Period Covered** | _e.g. Jan 2019 to Dec 2023_ |
| **Format** | _e.g. CSV, JSON, Excel_ |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| _column_1_ | _What it means_ | _Used for KPI / filter / segmentation_ |
| _column_2_ | _What it means_ | _Used for KPI / filter / segmentation_ |
| _column_3_ | _What it means_ | _Used for KPI / filter / segmentation_ |
| _column_4_ | _What it means_ | _Used for KPI / filter / segmentation_ |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| _e.g. Monthly Revenue Growth %_ | _What business outcome this tracks_ | _Show the exact formula or notebook reference_ |
| _e.g. Customer Churn Rate_ | _What business outcome this tracks_ | _Show the exact formula or notebook reference_ |
| _e.g. Repeat Purchase Rate_ | _What business outcome this tracks_ | _Show the exact formula or notebook reference_ |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | _Paste Tableau Public link here_ |
| **Executive View** | _Describe the high-level KPI summary view_ |
| **Operational View** | _Describe the detailed drill-down view_ |
| **Main Filters** | _List the interactive filters used_ |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

### Dashboard Architecture

The Tableau workbook consists of **3 interconnected dashboards** built from **22 individual sheets**, providing a complete analytical lens into the NYC Airbnb market.

| Dashboard | Focus | Key Question |
|---|---|---|
| **Dashboard 1 — Market Overview** | Executive summary | _What does the NYC Airbnb market look like at a glance?_ |
| **Dashboard 2 — Pricing & Revenue Analysis** | Revenue deep-dive | _Where is the money and who is making it?_ |
| **Dashboard 3 — Demand & Host Behavior** | Engagement & hosts | _Who are the active players and how engaged is the market?_ |

---

### Dashboard 1 — Market Overview

> **"What does the NYC Airbnb market look like at a glance?"**
>
> The executive summary. High-level numbers, geographic distribution, supply breakdown.

| Sheet | Chart Type | Question Answered |
|---|---|---|
| 4 KPI BAN cards | Big Number tiles | Price, MTV, GMV, Visibility |
| Map (symbol/filled) | Geo map | Where are listings concentrated? |
| Room Type Distribution | Donut chart | What kind of supply exists? |
| Market Concentration | Bar chart | Which borough dominates? |
| Host Portfolio Segmentation | Treemap or stacked bar | Casual vs professional hosts? |

#### Sheet 1: BAN — Median Nightly Price

- **Rows:** `MEDIAN([Price (Cleaned)])`
- Change mark type → **Text**
- Format number → Currency, 0 decimal places
- **Title:** Median Nightly Price
- **Font:** Gill Sans, title 11pt `#717171`, number 28pt bold `#FF385C`
- Hide axes, hide gridlines, set background `#F7F7F7`

#### Sheet 2: BAN — Avg Minimum Transaction Value

- **Rows:** `AVG([Minimum Transaction Value])`
- Same formatting as Sheet 1
- **Title:** Avg Min. Transaction Value

#### Sheet 3: BAN — Total Est. Monthly GMV

- **Rows:** `SUM([Est Monthly GMV])`
- Format → Currency, abbreviated (K/M)
- **Title:** Est. Monthly GMV

#### Sheet 4: BAN — Avg Market Visibility Score

- **Rows:** `AVG([Market Visibility Score])`
- Format → Number, 2 decimal places
- **Title:** Avg Visibility Score

#### Sheet 5: Map — Listings by Price

- Change sheet to **Map** view
- Drag `Latitude` → Rows, `Longitude` → Columns
- Tableau will auto-detect as geographic → confirm
- Drag `Price (Cleaned)` → **Color** shelf
- Edit color → Custom Diverging or Sequential:
  - Start: `#FFB3C1` → End: `#C13047`
  - ✅ Check "Use Full Color Range"
- Drag `Name` → Tooltip
- Drag `Neighbourhood Group` → Tooltip
- Drag `Room Type` → Tooltip
- Mark size → set to **3–4** (small dots, dense map)
- Turn off map layers except **Streets & Highways** (Map → Map Layers)
- Background: Tableau default light map; optionally switch to **Light** style

#### Sheet 6: Room Type Distribution — Donut

- Drag `Room Type` → Color
- Drag `CNT(id)` → Rows → change to **Pie** mark type
- Drag `CNT(id)` → **Angle** shelf
- Drag `Room Type` → **Color** shelf
- Set colors manually:
  | Room Type | Color |
  |---|---|
  | Entire home/apt | `#FF385C` |
  | Private room | `#00A699` |
  | Shared room | `#FFB3C1` |
- **To make it a donut:** duplicate the `CNT(id)` pill on rows → dual axis → on the second axis change mark size to very small and color it white `#FFFFFF`
- Add `Room Type` and `CNT(id)` to label on outer pie

#### Sheet 7: Market Concentration — Bar

- **Columns:** `CNT([Id])`
- **Rows:** `Neighbourhood Group`
- Sort bars **descending** by count
- Color all bars `#FF385C`
- Add data labels → `#222222`, Gill Sans 10pt
- Remove gridlines, remove axis line
- **Title:** Listings by Borough

#### Sheet 8: Host Portfolio Segmentation — Treemap

- Drag `Host Portfolio Segment` → **Color** and **Label**
- Drag `CNT([Id])` → **Size**
- Mark type → **Square** (Treemap)
- Colors:
  | Segment | Color |
  |---|---|
  | Enterprise | `#FF385C` |
  | Emerging | `#FF8FA3` |
  | Single | `#FFD6DD` |
- Add `CNT([Id])` to label as well
- **Title:** Host Portfolio Mix

---

### Dashboard 2 — Pricing & Revenue Analysis

> **"Where is the money and who is making it?"**
>
> Deep dive into price patterns, revenue proxies, and what drives high GMV listings.

| Sheet | Chart Type | Question Answered |
|---|---|---|
| Median Price by Borough | Horizontal bar | Which borough is most expensive? |
| Price by Room Type | Box plot or bar | Does room type drive price? |
| Price vs Availability Scatter | Scatter | Do expensive listings stay available? |
| Top 15 Neighbourhoods by GMV | Ranked bar | Which micro-markets earn the most? |
| MTV Distribution | Histogram or bar | Are hosts targeting short or long stays? |

#### Sheet 9: Median Price by Borough — Horizontal Bar

- **Rows:** `Neighbourhood Group`
- **Columns:** `MEDIAN([Price (Cleaned)])`
- Sort **descending**
- Color: single color `#FF385C`
- Add reference line at overall median → dotted, `#717171`
- Label bars with value
- **Title:** Median Price by Borough

#### Sheet 10: Price by Room Type — Bar

- **Rows:** `Room Type`
- **Columns:** `MEDIAN([Price (Cleaned)])`
- Color by Room Type (use same palette as Sheet 6 donut)
- **Title:** Median Price by Room Type

#### Sheet 11: Price vs Availability Scatter

- **Columns:** `AVG([Availability 365])`
- **Rows:** `AVG([Price (Cleaned)])`
- **Detail:** `Name` (so each dot = one listing)
- **Color:** `Room Type` (same palette)
- Add trend line: Analysis → Trend Lines → Show Trend Lines
- Trend line color `#717171`, dashed
- **Title:** Price vs Availability
- Add reference lines at median price (horizontal) and median availability (vertical) to create **quadrants**

#### Sheet 12: Top 15 Neighbourhoods by GMV — Ranked Bar

- **Rows:** `Neighbourhood` → filter to Top 15 by `SUM([Est Monthly GMV])`
  - Right-click filter → Top → By Field → Top 15 → Sum of Est Monthly GMV
- **Columns:** `SUM([Est Monthly GMV])`
- Sort **descending**
- Color: gradient `#FFB3C1` → `#FF385C` based on value
- **Title:** Top 15 Neighbourhoods by GMV

#### Sheet 13: MTV Distribution — Bar

- Bin `Minimum Transaction Value` into groups:
  - Create a new calculated field:
    ```
    INT([Minimum Transaction Value] / 500) * 500
    ```
    _(creates $500 buckets)_
- **Columns:** MTV bucket
- **Rows:** `CNT([Id])`
- Color: `#FF385C`
- **Title:** Minimum Transaction Value Distribution

#### Sheet 14: BAN — Avg Price (Dashboard 2)

- `MEDIAN([Price (Cleaned)])` — same BAN format as Sheets 1–4

#### Sheet 15: BAN — Avg MTV (Dashboard 2)

- `AVG([Minimum Transaction Value])` — same BAN format as Sheets 1–4

---

### Dashboard 3 — Demand & Host Behavior

> **"Who are the active players and how engaged is the market?"**
>
> Focuses on review activity as a demand proxy, host professionalism, and listing staleness.

| Sheet | Chart Type | Question Answered |
|---|---|---|
| Review Recency Heatmap | Highlight table | Borough × Recency bucket |
| Reviews per Month by Room Type | Bar | Which listing type gets most engagement? |
| Host Segment × Borough | Stacked bar | Where do enterprise hosts operate? |
| Availability vs Reviews Scatter | Scatter | Are highly available listings also reviewed? |
| Top Hosts by GMV | Bar (top 10) | Who are the power hosts? |

#### Sheet 16: Review Recency Heatmap

- **Rows:** `Neighbourhood Group`
- **Columns:** `Review Recency`
- Mark type → **Square**
- **Color:** `CNT([Id])`
  - Color palette: `#FFD6DD` (low) → `#FF385C` (high)
- Sort columns manually using `Recency Sort Order` field: **Active → Aging → Stale → Never**
- Add `CNT([Id])` as label
- **Title:** Review Recency by Borough

#### Sheet 17: Reviews per Month by Room Type — Bar

- **Rows:** `Room Type`
- **Columns:** `AVG([Reviews Per Month])`
- Color: `Room Type` (same categorical palette)
- **Title:** Avg Reviews/Month by Room Type

#### Sheet 18: Host Segment × Borough — Stacked Bar

- **Columns:** `Neighbourhood Group`
- **Rows:** `CNT([Id])`
- **Color:** `Host Portfolio Segment`
  | Segment | Color |
  |---|---|
  | Enterprise | `#FF385C` |
  | Emerging | `#FF8FA3` |
  | Single | `#FFD6DD` |
- Mark type → Bar, **stacked**
- **Title:** Host Mix by Borough

#### Sheet 19: Availability vs Reviews Scatter

- **Columns:** `AVG([Availability 365])`
- **Rows:** `AVG([Number Of Reviews])`
- **Detail:** `Name`
- **Color:** `Host Portfolio Segment` (same palette)
- **Title:** Availability vs Review Volume

#### Sheet 20: Top 10 Hosts by GMV — Bar

- **Rows:** `Host Name`
- **Filter:** Top 10 by `SUM([Est Monthly GMV])`
- **Columns:** `SUM([Est Monthly GMV])`
- **Color:** `Host Portfolio Segment`
- Sort **descending**
- **Title:** Top 10 Hosts by Revenue

#### Sheet 21: BAN — Avg Visibility Score (Dashboard 3)

- `AVG([Market Visibility Score])` — same BAN format as Sheets 1–4

#### Sheet 22: BAN — Total Reviews (Dashboard 3)

- `SUM([Number Of Reviews])` — same BAN format as Sheets 1–4

---

### 🏗️ Dashboard Assembly (Phase 5)

> Complete all 22 sheets before assembling dashboards.

**For each dashboard, follow these steps:**

1. **Canvas Setup**
   - New Dashboard → set size to **Fixed, 1200 × 900 px**

2. **Header Strip**
   - Drag a **Blank** object as header strip (height **60 px**)
   - Fill: `#FF385C`
   - Add **Text** object with dashboard title in **white, Gill Sans Bold**

3. **KPI Row**
   - Drop BAN sheets in a **horizontal container** row (equal width)
   - Background: `#F7F7F7`

4. **Chart Layout**
   - Drop chart sheets into **tiled layout** below the KPI row

5. **Filter Controls**
   - Add filter controls for `Neighbourhood Group` and `Room Type`
   - Position as **floating pills**, top-right
   - Style with border `#DDDDDD`

6. **Navigation Buttons**
   - Insert → Button → set link to target dashboard sheet
   - Style with `#FF385C` background for inter-dashboard navigation

---

## Key Insights

_List 8-12 major findings from the analysis, written in decision language. Each insight should tell the reader what to think or act upon, not merely describe a chart._

1. _Insight 1_
2. _Insight 2_
3. _Insight 3_
4. _Insight 4_
5. _Insight 5_
6. _Insight 6_
7. _Insight 7_
8. _Insight 8_

---

## Recommendations

_Provide 3-5 specific, actionable business recommendations, each linked directly to an insight above._

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 2 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 3 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |

---

## Repository Structure

```text
SectionName_TeamID_ProjectName/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   |-- 04_statistical_analysis.ipynb
|   `-- 05_final_load_prep.ipynb
|
|-- scripts/
|   `-- etl_pipeline.py
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- README.md
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Recommended Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Is the business question clear and well-scoped? |
| Data Quality and ETL | 15 | Is the cleaning pipeline thorough and documented? |
| Analysis Depth | 25 | Are statistical methods applied correctly with insight? |
| Dashboard and Visualization | 20 | Is the Tableau dashboard interactive and decision-relevant? |
| Business Recommendations | 20 | Are insights actionable and well-reasoned? |
| Storytelling and Clarity | 10 | Is the presentation professional and coherent? |
| **Total** | **100** | |

> Marks are awarded for analytical thinking and decision relevance, not chart quantity, visual decoration, or code length.

---

## Submission Checklist

**GitHub Repository**

- [ ] Public repository created with the correct naming convention (`SectionName_TeamID_ProjectName`)
- [ ] All notebooks committed in `.ipynb` format
- [ ] `data/raw/` contains the original, unedited dataset
- [ ] `data/processed/` contains the cleaned pipeline output
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains the Tableau Public URL
- [ ] `docs/data_dictionary.md` is complete
- [ ] `README.md` explains the project, dataset, and team
- [ ] All members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] Cover page, executive summary, sector context, problem statement
- [ ] Data description, cleaning methodology, KPI framework
- [ ] EDA with written insights, statistical analysis results
- [ ] Dashboard screenshots and explanation
- [ ] 8-12 key insights in decision language
- [ ] 3-5 actionable recommendations with impact estimates
- [ ] Contribution matrix matches GitHub history

**Presentation Deck**

- [ ] Final presentation exported as PDF into `reports/`
- [ ] Title slide through recommendations, impact, limitations, and next steps

**Individual Assets**

- [ ] DVA-oriented resume updated to include this capstone
- [ ] Portfolio link or project case study added

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| _Member 1_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 2_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 3_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 4_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 5_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 6_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** _____________________________

**Date:** _______________

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*



## Color Theme

Pink accent foreground color: #FF385C
Background color: #fff 
