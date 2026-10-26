# Netflix Data Analysis & Business Insights Dashboard

An end-to-end data analysis project using Python, Pandas, Matplotlib, Seaborn, Plotly, and Streamlit to explore Netflix Movies and TV Shows, identify content trends, and present business insights through an interactive dashboard.

**Internship:** Auspify Technologies — Data Analysis Using Python  
**Tools:** Python, Pandas, Matplotlib, Seaborn, Plotly, Streamlit

## Project Objective

Clean and prepare a Netflix titles dataset, explore Movies and TV Shows, compare country representation, analyze release-year patterns, ratings, and genres, and communicate findings through charts, summary CSV files, a written business report, and an interactive dashboard.

## Project Structure

```text
netflix_data_analysis_internship/
├── data/
├── src/
│   ├── __init__.py
│   └── analysis.py
├── outputs/
│   ├── figures/
│   └── reports/
├── Netflix_Data_Analysis.ipynb
├── dashboard.py
├── requirements.txt
└── README.md
```

## Technologies Used

- **Python:** Data analysis and processing
- **Pandas:** Data cleaning and manipulation
- **Matplotlib & Seaborn:** Statistical visualization
- **Plotly:** Interactive charts
- **Streamlit:** Interactive dashboard development
- **Jupyter Notebook:** Exploratory analysis and documentation

## Key Analysis Tasks

1. **Data Cleaning & Preparation:** Handle missing and placeholder values, normalize text, check duplicate IDs, parse dates, and extract duration information.
2. **Content Type Analysis:** Compare the distribution of Movies and TV Shows.
3. **Country-Wise Analysis:** Explore country representation and identify leading countries.
4. **Release-Year Trends:** Analyze title counts by release year.
5. **Ratings & Genre Analysis:** Explore rating distributions and popular genres.
6. **Business Insights Dashboard:** Present interactive charts, filters, searchable titles, and CSV downloads.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/mistryved21/Netflix-Data-Analysis.git
cd Netflix-Data-Analysis
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the analysis

```powershell
python src/analysis.py
```

### 5. Launch the Streamlit dashboard

```powershell
streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Data Interpretation Notes

- The dataset contains Netflix catalog information; trends describe titles represented in the dataset, not all content produced worldwide.
- A title may list multiple countries or genres, so category counts may overlap.
- Review the generated charts and reports before drawing conclusions.

## Project Outcomes

- A cleaned dataset for analysis
- Exploratory data analysis and visualizations
- Summary CSV files and a business insights report
- An interactive Streamlit dashboard for exploring Netflix content

## Author

**Mistry Ved**

GitHub: [mistryved21](https://github.com/mistryved21)

---

*This project was developed for data analytics practice and internship learning.*