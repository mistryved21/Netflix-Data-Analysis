"""Netflix data-cleaning and analysis pipeline for the Auspify internship tasks."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Dataset.csv"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
REPORT_DIR = OUTPUT_DIR / "reports"

sns.set_theme(style="whitegrid", palette="Set2")


def ensure_folders() -> None:
    for folder in (OUTPUT_DIR, FIGURE_DIR, REPORT_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def clean_text(value: object) -> object:
    """Strip outer spaces and collapse repeated internal whitespace."""
    if not isinstance(value, str):
        return value
    return re.sub(r"\s+", " ", value).strip()


def clean_dataset(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    """Clean dataset and return it with a data-quality summary."""
    df = raw.copy()
    original_rows, original_columns = df.shape
    df.columns = [re.sub(r"[^a-z0-9]+", "_", str(c).strip().lower()).strip("_") for c in df.columns]

    text_columns = df.select_dtypes(include="object").columns
    for col in text_columns:
        df[col] = df[col].map(clean_text)
        df[col] = df[col].replace("", pd.NA)

    # Count both real nulls and common text placeholders as data-quality gaps.
    placeholder_pattern = r"(?i)^(not given|n/?a|null|none|nan|)$"
    placeholder_cells_before = int(df.select_dtypes(include="object").apply(
        lambda col: col.astype("string").str.strip().str.match(placeholder_pattern, na=False)
    ).sum().sum())
    if "title" in df.columns:
        placeholder_cells_before += int(df["title"].astype("string").str.casefold().eq("unknown").sum())
    missing_before = int(df.isna().sum().sum()) + placeholder_cells_before
    duplicates_before = int(df.duplicated().sum())
    show_id_duplicates_before = int(df["show_id"].duplicated().sum()) if "show_id" in df.columns else 0

    # Replace common textual placeholders with actual nulls before applying field-specific rules.
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].replace(to_replace=placeholder_pattern, value=pd.NA, regex=True)
    if "title" in df.columns:
        df.loc[df["title"].astype("string").str.casefold().eq("unknown"), "title"] = pd.NA

    # Normalize labels to a consistent format.
    if "type" in df.columns:
        df["type"] = df["type"].astype("string").str.strip().str.casefold().map(
            {"movie": "Movie", "tv show": "TV Show"}
        ).fillna(df["type"])
    for col in ("country", "rating", "listed_in", "director"):
        if col in df.columns:
            df[col] = df[col].replace({"": pd.NA})
            df[col] = df[col].fillna("Unknown")

    if "title" in df.columns:
        df = df[df["title"].notna()].copy()
    if "show_id" in df.columns:
        df = df.drop_duplicates(subset=["show_id"], keep="first")
    else:
        df = df.drop_duplicates(keep="first")

    if "release_year" in df.columns:
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    if "duration" in df.columns:
        duration_parts = df["duration"].astype("string").str.extract(r"(?P<duration_value>\d+)?\s*(?P<duration_unit>min|Season|Seasons)?", expand=True)
        df["duration_value"] = pd.to_numeric(duration_parts["duration_value"], errors="coerce").astype("Int64")
        df["duration_unit"] = duration_parts["duration_unit"].str.lower().replace({"seasons": "season"})
    if "date_added" in df.columns:
        df["added_year"] = df["date_added"].dt.year.astype("Int64")
        df["added_month"] = df["date_added"].dt.month_name()

    # Keep date_added as an unambiguous ISO-style date in the export.
    if "date_added" in df.columns:
        df["date_added"] = df["date_added"].dt.strftime("%Y-%m-%d")

    summary = {
        "original_rows": original_rows,
        "original_columns": original_columns,
        "rows_after_cleaning": int(len(df)),
        "columns_after_cleaning": int(len(df.columns)),
        "missing_or_placeholder_cells_before_cleaning": missing_before,
        "placeholder_cells_before_cleaning": placeholder_cells_before,
        "exact_duplicate_rows_before_cleaning": duplicates_before,
        "duplicate_show_ids_before_cleaning": show_id_duplicates_before,
        "missing_cells_after_cleaning": int(df.isna().sum().sum()),
        "duplicate_show_ids_after_cleaning": int(df["show_id"].duplicated().sum()) if "show_id" in df.columns else int(df.duplicated().sum()),
    }
    return df.reset_index(drop=True), summary


def split_multi_value(series: pd.Series) -> pd.Series:
    """Split comma-separated values, trim spaces and return one value per row."""
    return series.fillna("Unknown").astype(str).str.split(",").explode().map(clean_text).dropna()


def save_chart(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=180, bbox_inches="tight")
    plt.close()


def make_content_type_chart(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["type"].value_counts().rename_axis("content_type").reset_index(name="title_count")
    counts["percentage"] = (counts["title_count"] / counts["title_count"].sum() * 100).round(2)
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=counts, x="content_type", y="title_count", color="steelblue")
    ax.set(title="Netflix Catalog: Movies vs TV Shows", xlabel="Content type", ylabel="Number of titles")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f")
    save_chart("content_type_distribution.png")
    counts.to_csv(OUTPUT_DIR / "content_type_summary.csv", index=False)
    return counts


def make_country_chart(df: pd.DataFrame) -> pd.DataFrame:
    countries = split_multi_value(df["country"])
    counts = countries[countries.ne("Unknown")].value_counts().head(15).rename_axis("country").reset_index(name="title_count")
    counts.to_csv(OUTPUT_DIR / "top_countries.csv", index=False)
    plt.figure(figsize=(10, 7))
    ax = sns.barplot(data=counts, y="country", x="title_count", color="steelblue")
    ax.set(title="Top 15 Countries by Netflix Catalog Titles", xlabel="Number of titles (a title can list multiple countries)", ylabel="Country")
    save_chart("top_15_countries.png")
    return counts


def make_release_year_chart(df: pd.DataFrame) -> pd.DataFrame:
    years = df.dropna(subset=["release_year"]).groupby("release_year").size().rename("title_count").reset_index()
    years.to_csv(OUTPUT_DIR / "releases_by_year.csv", index=False)
    recent = years[years["release_year"] >= 2000]
    plt.figure(figsize=(11, 5))
    sns.lineplot(data=recent, x="release_year", y="title_count", marker="o")
    plt.title("Netflix Catalog Titles by Release Year (2000 onward)")
    plt.xlabel("Release year")
    plt.ylabel("Number of titles in dataset")
    save_chart("release_year_trend.png")
    return years


def make_rating_genre_charts(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ratings = df.groupby(["rating", "type"]).size().rename("title_count").reset_index()
    rating_totals = df["rating"].value_counts().rename_axis("rating").reset_index(name="title_count")
    rating_totals.to_csv(OUTPUT_DIR / "rating_summary.csv", index=False)
    plt.figure(figsize=(10, 6))
    top_ratings = rating_totals.head(12)["rating"]
    rating_plot = ratings[ratings["rating"].isin(top_ratings)]
    sns.barplot(data=rating_plot, x="rating", y="title_count", hue="type")
    plt.title("Content Ratings by Type (Top 12 Ratings)")
    plt.xlabel("Rating")
    plt.ylabel("Number of titles")
    plt.xticks(rotation=35, ha="right")
    save_chart("rating_by_type.png")

    genre_counts = split_multi_value(df["listed_in"])
    genre_counts = genre_counts[genre_counts.ne("Unknown")].value_counts().head(15).rename_axis("genre").reset_index(name="title_count")
    genre_counts.to_csv(OUTPUT_DIR / "top_genres.csv", index=False)
    plt.figure(figsize=(10, 7))
    sns.barplot(data=genre_counts, y="genre", x="title_count", color="steelblue")
    plt.title("Top 15 Genres / Categories")
    plt.xlabel("Number of title-category assignments")
    plt.ylabel("Genre / category")
    save_chart("top_15_genres.png")

    rating_by_type = pd.crosstab(df["rating"], df["type"])
    rating_by_type.to_csv(OUTPUT_DIR / "rating_by_content_type.csv")
    return rating_totals, genre_counts, ratings


def create_report(df: pd.DataFrame, quality: dict[str, object], content: pd.DataFrame,
                  countries: pd.DataFrame, years: pd.DataFrame, ratings: pd.DataFrame,
                  genres: pd.DataFrame) -> None:
    type_lines = "\n".join(f"- **{r.content_type}:** {r.title_count:,} titles ({r.percentage:.2f}%)" for r in content.itertuples())
    top_country = countries.iloc[0] if not countries.empty else None
    top_genre = genres.iloc[0] if not genres.empty else None
    top_rating = ratings.iloc[0] if not ratings.empty else None
    valid_years = years["release_year"].dropna()
    latest_release_year = int(valid_years.max()) if not valid_years.empty else "N/A"
    earliest_release_year = int(valid_years.min()) if not valid_years.empty else "N/A"
    peak_year_row = years.loc[years["title_count"].idxmax()] if not years.empty else None
    top_rating_percent = (int(top_rating["title_count"]) / len(df) * 100) if top_rating is not None and len(df) else 0
    second_country = countries.iloc[1] if len(countries) > 1 else None
    report = f'''# Netflix Data Analysis - Business Insights Report

## 1. Project overview
This project cleans and analyzes the Netflix titles dataset using Python, Pandas, Matplotlib and Seaborn. It completes the six task themes in the Auspify Technologies Data Analysis Using Python internship brief.

## 2. Dataset and data quality
- Rows in supplied dataset: **{quality['original_rows']:,}**
- Columns in supplied dataset: **{quality['original_columns']}**
- Rows after cleaning: **{quality['rows_after_cleaning']:,}**
- Missing or placeholder cells before cleaning: **{quality['missing_or_placeholder_cells_before_cleaning']:,}**
- Exact duplicate rows before cleaning: **{quality['exact_duplicate_rows_before_cleaning']:,}**
- Duplicate show IDs before cleaning: **{quality['duplicate_show_ids_before_cleaning']:,}**
- Placeholder cells detected before cleaning: **{quality['placeholder_cells_before_cleaning']:,}**
- Missing cells after cleaning: **{quality['missing_cells_after_cleaning']:,}**

The supplied dataset had no actual null cells or exact duplicate rows on initial inspection, but it used text placeholders such as `Not Given` and `Unknown`. The pipeline standardizes these placeholders, normalizes text fields, checks duplicate IDs, standardizes content-type labels, validates date and numeric fields, separates duration into a numeric value and unit, fills missing categorical descriptors with `Unknown`, and removes the record with no usable title.

## 3. Task 2 - Content type analysis
The dataset contains **{len(df):,} titles**.
{type_lines}

![Content type distribution](../figures/content_type_distribution.png)

## 4. Task 3 - Country-wise analysis
Country values are split because a title may be associated with more than one country. Counts represent title-country assignments, so they can exceed the number of unique titles across all countries.

{f"The leading country is **{top_country['country']}** with {int(top_country['title_count']):,} title-country assignments." if top_country is not None else "Country information was not available."}

![Top countries](../figures/top_15_countries.png)

## 5. Task 4 - Release-year trend
The release years represented range from **{earliest_release_year}** to **{latest_release_year}**. This chart reflects release years of titles present in this Netflix catalog dataset, not total worldwide film/TV production.

![Release year trend](../figures/release_year_trend.png)

## 6. Task 5 - Ratings and genres
{f"The most common rating category is **{top_rating['rating']}** ({int(top_rating['title_count']):,} titles)." if top_rating is not None else "Rating data was not available."}
{f"The most frequent genre/category assignment is **{top_genre['genre']}** ({int(top_genre['title_count']):,} assignments)." if top_genre is not None else "Genre data was not available."}

![Ratings by content type](../figures/rating_by_type.png)

![Top genres](../figures/top_15_genres.png)

## 7. Business insights and recommendations
1. **Catalog mix:** Movies represent **{content.iloc[0]['percentage']:.2f}%** of titles, compared with **{content.iloc[1]['percentage']:.2f}%** for TV Shows. The catalog is movie-heavy, so compare engagement and retention by format before making content investment decisions.
2. **Country representation:** **{top_country['country']}** leads with **{int(top_country['title_count']):,}** title-country assignments{f", followed by {second_country['country']} ({int(second_country['title_count']):,})" if second_country is not None else ""}. Multi-country titles are counted for every listed country, so these are assignments rather than unique-title totals per exclusive market.
3. **Release-year pattern:** The highest represented release year is **{int(peak_year_row['release_year'])}** with **{int(peak_year_row['title_count']):,}** titles in this dataset. This describes this catalog only; the dataset cannot establish global production volumes or explain why a year has more titles.
4. **Ratings and categories:** **{top_rating['rating']}** is the most common rating ({int(top_rating['title_count']):,} titles, about {top_rating_percent:.1f}% of the cleaned catalog). **{top_genre['genre']}** is the most frequent genre/category assignment ({int(top_genre['title_count']):,}). Ratings are classifications, not direct audience demographics.
5. **Data quality:** The source includes **{quality['placeholder_cells_before_cleaning']:,}** placeholder cells, mainly in director and country values. Standardize these placeholders and keep the cleaning steps repeatable before using this data for decision-making.

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
'''
    (REPORT_DIR / "insights_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    ensure_folders()
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Place Dataset.csv in the data folder.")
    raw = pd.read_csv(DATA_PATH)
    cleaned, quality = clean_dataset(raw)
    cleaned.to_csv(ROOT / "data" / "cleaned_netflix.csv", index=False)
    content = make_content_type_chart(cleaned)
    countries = make_country_chart(cleaned)
    years = make_release_year_chart(cleaned)
    rating_totals, genres, _ = make_rating_genre_charts(cleaned)
    create_report(cleaned, quality, content, countries, years, rating_totals, genres)
    pd.DataFrame([quality]).to_csv(OUTPUT_DIR / "data_quality_summary.csv", index=False)
    print("\nNetflix analysis completed successfully.")
    print(f"Cleaned dataset: {ROOT / 'data' / 'cleaned_netflix.csv'}")
    print(f"Charts: {FIGURE_DIR}")
    print(f"Business report: {REPORT_DIR / 'insights_report.md'}")
    print("\nContent type summary:")
    print(content.to_string(index=False))
    print("\nTop 5 countries:")
    print(countries.head().to_string(index=False))
    print("\nTop 5 genres:")
    print(genres.head().to_string(index=False))


if __name__ == "__main__":
    main()
