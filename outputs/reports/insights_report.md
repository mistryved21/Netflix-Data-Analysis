# Netflix Data Analysis - Business Insights Report

## 1. Project overview
This project cleans and analyzes the Netflix titles dataset using Python, Pandas, Matplotlib and Seaborn. It completes the six task themes in the Auspify Technologies Data Analysis Using Python internship brief.

## 2. Dataset and data quality
- Rows in supplied dataset: **8,790**
- Columns in supplied dataset: **10**
- Rows after cleaning: **8,789**
- Missing or placeholder cells before cleaning: **2,876**
- Exact duplicate rows before cleaning: **0**
- Duplicate show IDs before cleaning: **0**
- Placeholder cells detected before cleaning: **2,876**
- Missing cells after cleaning: **0**

The supplied dataset had no actual null cells or exact duplicate rows on initial inspection, but it used text placeholders such as `Not Given` and `Unknown`. The pipeline standardizes these placeholders, normalizes text fields, checks duplicate IDs, standardizes content-type labels, validates date and numeric fields, separates duration into a numeric value and unit, fills missing categorical descriptors with `Unknown`, and removes the record with no usable title.

## 3. Task 2 - Content type analysis
The dataset contains **8,789 titles**.
- **Movie:** 6,125 titles (69.69%)
- **TV Show:** 2,664 titles (30.31%)

![Content type distribution](../figures/content_type_distribution.png)

## 4. Task 3 - Country-wise analysis
Country values are split because a title may be associated with more than one country. Counts represent title-country assignments, so they can exceed the number of unique titles across all countries.

The leading country is **United States** with 3,240 title-country assignments.

![Top countries](../figures/top_15_countries.png)

## 5. Task 4 - Release-year trend
The release years represented range from **1925** to **2021**. This chart reflects release years of titles present in this Netflix catalog dataset, not total worldwide film/TV production.

![Release year trend](../figures/release_year_trend.png)

## 6. Task 5 - Ratings and genres
The most common rating category is **TV-MA** (3,205 titles).
The most frequent genre/category assignment is **International Movies** (2,752 assignments).

![Ratings by content type](../figures/rating_by_type.png)

![Top genres](../figures/top_15_genres.png)

## 7. Business insights and recommendations
1. **Catalog mix:** Movies represent **69.69%** of titles, compared with **30.31%** for TV Shows. The catalog is movie-heavy, so compare engagement and retention by format before making content investment decisions.
2. **Country representation:** **United States** leads with **3,240** title-country assignments, followed by India (1,057). Multi-country titles are counted for every listed country, so these are assignments rather than unique-title totals per exclusive market.
3. **Release-year pattern:** The highest represented release year is **2018** with **1,146** titles in this dataset. This describes this catalog only; the dataset cannot establish global production volumes or explain why a year has more titles.
4. **Ratings and categories:** **TV-MA** is the most common rating (3,205 titles, about 36.5% of the cleaned catalog). **International Movies** is the most frequent genre/category assignment (2,752). Ratings are classifications, not direct audience demographics.
5. **Data quality:** The source includes **2,876** placeholder cells, mainly in director and country values. Standardize these placeholders and keep the cleaning steps repeatable before using this data for decision-making.

## 8. Deliverables
- `data/Dataset.csv` - supplied dataset
- `data/cleaned_netflix.csv` - cleaned dataset with derived duration/date fields
- `outputs/figures/` - visualizations for tasks 2-5
- `outputs/*.csv` - summary tables
- `outputs/reports/insights_report.md` - this report
- `dashboard.py` - optional interactive Streamlit dashboard

## 9. How to run
From the project root:

```bash
python -m pip install -r requirements.txt
python src/analysis.py
streamlit run dashboard.py
```
