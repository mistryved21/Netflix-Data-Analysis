# Netflix Data Analysis & Business Insights Dashboard

**Internship:** Auspify Technologies - Data Analysis Using Python  
**Tasks covered:** All six task themes in the supplied internship brief  
**Tools:** Python, Pandas, Matplotlib, Seaborn, Plotly, Streamlit

## Project objective

Clean and prepare a Netflix titles dataset, explore Movies and TV Shows, compare country representation, review release-year patterns, analyze ratings and genres, and communicate findings through charts, summary CSV files, a written business report, and an interactive dashboard.

## Project structure

```text
netflix_data_analysis_internship/
├── data/
│   ├── Dataset.csv
│   └── cleaned_netflix.csv          # created by the analysis script
├── src/
│   ├── __init__.py
│   └── analysis.py                  # cleaning, EDA, charts, report generation
├── outputs/
│   ├── figures/                    # charts created by the script
│   ├── reports/insights_report.md   # written insights report
│   └── *.csv                       # summary tables
├── Netflix_Data_Analysis.ipynb     # guided notebook walkthrough
├── dashboard.py                    # interactive Streamlit dashboard
├── requirements.txt
└── README.md
```

## Run on Windows (PowerShell)

1. Install Python 3.10 or later from https://www.python.org/downloads/ and enable **Add Python to PATH** during installation.
2. Extract the project ZIP to a folder.
3. Open PowerShell in the extracted `netflix_data_analysis_internship` folder.
4. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Generate the cleaned dataset, charts, summary tables and report:

   ```powershell
   python src/analysis.py
   ```

7. Start the interactive dashboard:

   ```powershell
   streamlit run dashboard.py
   ```

   Streamlit prints a local URL, normally `http://localhost:8501`, which you can open in your browser.

## Internship task mapping

1. **Netflix Data Cleaning & Preparation** - missing and placeholder values (including `Not Given`), whitespace normalization, consistent content type, duplicate ID checks, date parsing, duration extraction, cleaned CSV export.
2. **Content Type Analysis Dashboard** - counts and percentages of Movies and TV Shows.
3. **Country-Wise Content Analysis** - explode multi-country rows, rank and chart top countries.
4. **Trend Analysis by Release Year** - yearly title counts and line chart.
5. **Content Rating & Genre Analysis** - rating distribution, ratings by type, top genre/category assignments.
6. **Netflix Business Insights Report** - generated report and an interactive Streamlit dashboard with filters, charts, searchable title table, and CSV download.

## Data interpretation notes

- The supplied file has 8,790 rows and 10 columns. Initial inspection found no actual null cells and no exact duplicate rows, but placeholder strings such as `Not Given` existed. The cleaning script normalizes these and removes one record whose title was `Unknown`.
- A title can list more than one country or category. Therefore, country and genre/category assignment counts are not mutually exclusive and may sum to more than the number of titles.
- Release-year trends describe titles represented in this catalog dataset. They do not prove the number of titles produced worldwide in each year.
- Always explain results in your own words and verify that each chart matches your interpretation before submitting.

## Submission checklist

- [ ] Run `python src/analysis.py` without errors.
- [ ] Run `streamlit run dashboard.py` and check filters, charts, and download button.
- [ ] Capture screenshots of the dashboard and the generated charts.
- [ ] Read `outputs/reports/insights_report.md` and be ready to explain the findings.
- [ ] Upload the source code, README, report, and selected screenshots to your internship submission portal or GitHub as required.
