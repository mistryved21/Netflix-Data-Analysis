"""Netflix Catalog Intelligence dashboard for the Auspify Python Data Analysis internship."""
from pathlib import Path
import html
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
CLEAN_PATH = ROOT / "data" / "cleaned_netflix.csv"
RAW_PATH = ROOT / "data" / "Dataset.csv"
RED = "#E50914"
RED_SOFT = "#FF4B55"
WHITE = "#F7F7F7"
MUTED = "#A7A7A7"
PANEL = "#181818"
GRID = "#303030"
MOVIE_COLOR = "#E50914"
TV_COLOR = "#7777FF"

st.set_page_config(
    page_title="Netflix Catalog Intelligence | Auspify",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling keeps the experience consistent whether Streamlit's global theme is light or dark.
st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp {
        background: radial-gradient(ellipse at 50% -20%, #292020 0%, #111111 42%, #0b0b0b 100%);
        color: #f7f7f7;
    }
    [data-testid="stHeader"] { background: rgba(10,10,10,0.35); }
    [data-testid="stAppViewContainer"] > .main .block-container {
        max-width: 1500px; padding-top: 1.7rem; padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171717 0%, #101010 100%);
        border-right: 1px solid #292929;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #d1d1d1; }
    h1, h2, h3 { letter-spacing: -0.035em; }
    h1 { font-weight: 800 !important; }
    h2 { font-weight: 750 !important; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1e1e1e 0%, #151515 100%);
        border: 1px solid #333333; border-radius: 16px;
        padding: 18px 20px 16px; min-height: 122px;
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
    }
    [data-testid="stMetricLabel"] { color: #bdbdbd !important; font-size: .85rem; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.9rem; font-weight: 800; }
    [data-testid="stMetricDelta"] { font-size: .78rem; }
    div[data-testid="stTabs"] button {
        border-radius: 10px 10px 0 0; padding: .7rem 1.15rem;
        font-weight: 650;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff; border-bottom: 3px solid #E50914;
    }
    .hero {
        padding: 1.4rem 1.55rem 1.35rem; margin: .2rem 0 1.25rem;
        background: linear-gradient(115deg, rgba(229,9,20,.15), rgba(25,25,25,.93) 48%, rgba(25,25,25,.76));
        border: 1px solid #3a2729; border-radius: 20px; position: relative; overflow: hidden;
    }
    .hero:after {
        content: "N"; position: absolute; right: 2.2rem; top: -2.6rem;
        color: rgba(229,9,20,.09); font-size: 15rem; line-height: 1; font-weight: 900; pointer-events: none;
    }
    .eyebrow { text-transform: uppercase; letter-spacing: .16em; color: #ff6971; font-size: .72rem; font-weight: 800; margin-bottom: .5rem; }
    .hero-title { font-size: clamp(2rem, 4vw, 3.15rem); font-weight: 850; letter-spacing: -.055em; line-height: 1.05; color: #fff; margin: 0; }
    .hero-title span { color: #E50914; }
    .hero-copy { margin: .7rem 0 1rem; color: #c3c3c3; font-size: 1rem; max-width: 760px; }
    .chip-row { display: flex; flex-wrap: wrap; gap: .5rem; position: relative; z-index: 1; }
    .chip { color: #eeeeee; border: 1px solid #414141; background: rgba(15,15,15,.68); border-radius: 99px; padding: .28rem .7rem; font-size: .74rem; }
    .section-kicker { color: #ff646c; text-transform: uppercase; letter-spacing: .12em; font-weight: 800; font-size: .72rem; margin: .25rem 0 .3rem; }
    .section-intro { color: #b3b3b3; margin-top: -.4rem; margin-bottom: 1rem; font-size: .9rem; }
    .insight-card {
        height: 100%; min-height: 125px; padding: 1rem 1.05rem;
        background: linear-gradient(145deg, #1d1d1d, #141414);
        border: 1px solid #323232; border-radius: 15px;
    }
    .insight-label { color: #a8a8a8; font-size: .76rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 750; }
    .insight-value { color: #fff; font-size: 1.28rem; font-weight: 800; margin-top: .45rem; line-height: 1.25; }
    .insight-detail { color: #a7a7a7; font-size: .81rem; margin-top: .45rem; }
    .note-box { background: #191919; border-left: 3px solid #E50914; border-radius: 0 10px 10px 0; padding: .8rem 1rem; color: #c7c7c7; font-size: .87rem; }
    .stButton > button, .stDownloadButton > button {
        border-radius: 10px; border: 1px solid #484848; font-weight: 700;
    }
    .stDownloadButton > button { background: #E50914; border-color: #E50914; color: white; }
    .stDownloadButton > button:hover { background: #b80710; border-color: #b80710; color: white; }
    [data-testid="stDataFrame"] { border: 1px solid #343434; border-radius: 12px; overflow: hidden; }
    hr { border-color: #303030 !important; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading the Netflix catalog…")
def load_data():
    """Load cleaned data when present; otherwise fall back to the supplied raw file."""
    path = CLEAN_PATH if CLEAN_PATH.exists() else RAW_PATH
    if not path.exists():
        raise FileNotFoundError(path)
    data = pd.read_csv(path)
    for col in ("release_year", "duration_value", "added_year"):
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    for col in ("type", "title", "country", "rating", "director", "listed_in", "duration"):
        if col in data.columns:
            data[col] = data[col].astype("string").str.strip()
    # Treat common placeholders as unavailable values for analysis and filtering.
    placeholders = {"", "unknown", "not given", "n/a", "na", "nan", "none", "null"}
    for col in ("country", "rating", "director", "listed_in"):
        if col in data.columns:
            mask = data[col].str.lower().isin(placeholders)
            data.loc[mask.fillna(False), col] = pd.NA
    # Keep unrated records in the default selection instead of silently filtering them out.
    if "rating" in data.columns:
        data["rating"] = data["rating"].fillna("Unrated")
    return data


def split_assignments(series: pd.Series) -> pd.Series:
    """Explode comma-separated countries/genres and drop placeholder assignments."""
    vals = series.dropna().astype(str).str.split(",").explode().str.strip()
    invalid = {"", "unknown", "not given", "n/a", "na", "nan", "none", "null"}
    return vals[~vals.str.lower().isin(invalid)]


def style_figure(fig, height=390):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, Arial, sans-serif", color="#e8e8e8", size=12),
        title=dict(font=dict(size=16, color="#f7f7f7"), x=0.02, xanchor="left"),
        margin=dict(l=12, r=18, t=58, b=20),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, x=0),
        hoverlabel=dict(bgcolor="#202020", bordercolor="#484848", font_color="#ffffff"),
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, linecolor=GRID, ticks="outside", tickcolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, linecolor=GRID, ticks="outside", tickcolor=GRID)
    return fig


def show_chart(fig, key):
    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        config={"displayModeBar": False, "responsive": True, "displaylogo": False},
        key=key,
    )


def reset_filters():
    """Restore the complete dataset selection for all sidebar widgets."""
    st.session_state["filter_types"] = types
    st.session_state["filter_years"] = (year_min, year_max)
    st.session_state["filter_ratings"] = ratings
    st.session_state["filter_country"] = "All countries"


def insight_card(label, value, detail):
    st.markdown(
        f'<div class="insight-card"><div class="insight-label">{html.escape(str(label))}</div>'
        f'<div class="insight-value">{html.escape(str(value))}</div>'
        f'<div class="insight-detail">{html.escape(str(detail))}</div></div>',
        unsafe_allow_html=True,
    )


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Keep `Dataset.csv` or `cleaned_netflix.csv` inside the project's `data` folder, then run `python src/analysis.py`.")
    st.stop()

# Consistent content type labels, and safe behaviour if a column is absent.
if "type" not in df.columns or "release_year" not in df.columns:
    st.error("The dataset must include at least the `type` and `release_year` columns.")
    st.stop()

types = sorted(df["type"].dropna().unique().tolist())
ratings = sorted(df["rating"].dropna().astype(str).unique().tolist()) if "rating" in df.columns else []
if not types:
    st.error("No content types were found in the dataset.")
    st.stop()

years_valid = df["release_year"].dropna()
if years_valid.empty:
    st.error("No valid release years were found in the dataset.")
    st.stop()
year_min, year_max = int(years_valid.min()), int(years_valid.max())

# ── Sidebar / filters ────────────────────────────────────────────────────────
# Initialize widget state before creating the controls so the reset button works reliably.
if "filter_types" not in st.session_state:
    st.session_state["filter_types"] = types
if "filter_years" not in st.session_state:
    st.session_state["filter_years"] = (year_min, year_max)
if "filter_ratings" not in st.session_state:
    st.session_state["filter_ratings"] = ratings
if "filter_country" not in st.session_state:
    st.session_state["filter_country"] = "All countries"

with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:.65rem;margin:.2rem 0 1rem;">'
        '<div style="background:#E50914;color:white;font-weight:900;font-size:1.35rem;border-radius:8px;padding:.22rem .56rem;">N</div>'
        '<div><div style="font-weight:850;color:white;letter-spacing:.06em;">CATALOG LAB</div>'
        '<div style="font-size:.72rem;color:#929292;">Auspify · Data Analysis</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Refine your view")
    st.caption("Filters update every metric and chart on the page.")
    selected_types = st.multiselect("Content type", options=types, key="filter_types")
    years = st.slider("Release year", min_value=year_min, max_value=year_max, step=1, key="filter_years")
    selected_ratings = st.multiselect("Content rating", options=ratings, key="filter_ratings")

    known_countries = split_assignments(df["country"]) if "country" in df.columns else pd.Series(dtype=str)
    country_options = sorted(known_countries.unique().tolist())
    # Keep the country selection valid if the data changes between runs.
    if st.session_state["filter_country"] not in ["All countries"] + country_options:
        st.session_state["filter_country"] = "All countries"
    chosen_country = st.selectbox("Country", ["All countries"] + country_options, key="filter_country")
    st.divider()
    st.markdown("**Project scope**")
    st.caption("Netflix catalog snapshot · Exploratory analysis · Interactive reporting")
    st.button("Reset all filters", on_click=reset_filters, use_container_width=True)

# ── Apply filters ───────────────────────────────────────────────────────────
filtered = df[df["type"].isin(selected_types)].copy()
filtered = filtered[filtered["release_year"].between(years[0], years[1])]
if "rating" in filtered.columns:
    filtered = filtered[filtered["rating"].astype("string").isin(selected_ratings)]
if chosen_country != "All countries" and "country" in filtered.columns:
    country_match = filtered["country"].fillna("").astype(str).apply(
        lambda value: chosen_country in [part.strip() for part in value.split(",")]
    )
    filtered = filtered[country_match]

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero">'
    '<div class="eyebrow">Auspify Technologies · Python Data Analysis Internship</div>'
    '<h1 class="hero-title">Netflix <span>Catalog Intelligence</span></h1>'
    '<p class="hero-copy">Explore the shape of the catalog, uncover release patterns, compare genres and ratings, and turn raw titles into clear business insights.</p>'
    '<div class="chip-row"><span class="chip">✦ Exploratory data analysis</span>'
    '<span class="chip">◉ Interactive visualizations</span><span class="chip">↗ Filter & export</span></div>'
    '</div>',
    unsafe_allow_html=True,
)

movie_count = int((filtered["type"] == "Movie").sum())
tv_count = int((filtered["type"] == "TV Show").sum())
title_count = int(len(filtered))
movie_share = movie_count / title_count * 100 if title_count else 0
tv_share = tv_count / title_count * 100 if title_count else 0
countries_in_view = split_assignments(filtered["country"]).nunique() if "country" in filtered.columns else 0

k1, k2, k3, k4 = st.columns(4, gap="medium")
k1.metric("Titles in view", f"{title_count:,}", help="Catalog records after applying the selected filters.")
k2.metric("Movies", f"{movie_count:,}", f"{movie_share:.1f}% of view" if title_count else "0% of view")
k3.metric("TV Shows", f"{tv_count:,}", f"{tv_share:.1f}% of view" if title_count else "0% of view")
k4.metric("Countries represented", f"{countries_in_view:,}", help="Distinct country assignments in the filtered selection.")

st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
if filtered.empty:
    st.warning("No records match these filters. Expand the release-year range or select more content types/ratings.")
    st.stop()

# Insight values are derived from the current filtered selection.
counts_by_type = filtered["type"].value_counts()
lead_type = str(counts_by_type.index[0]) if not counts_by_type.empty else "—"
lead_type_pct = (int(counts_by_type.iloc[0]) / len(filtered) * 100) if len(filtered) and not counts_by_type.empty else 0
valid_year_counts = filtered["release_year"].dropna().astype(int).value_counts()
peak_year = int(valid_year_counts.index[0]) if not valid_year_counts.empty else "—"
peak_year_count = int(valid_year_counts.iloc[0]) if not valid_year_counts.empty else 0
rating_counts = filtered["rating"].dropna().value_counts() if "rating" in filtered.columns else pd.Series(dtype=int)
lead_rating = str(rating_counts.index[0]) if not rating_counts.empty else "Not available"
lead_rating_count = int(rating_counts.iloc[0]) if not rating_counts.empty else 0

tab_overview, tab_content, tab_explore, tab_notes = st.tabs(
    ["◈  Overview", "▤  Content insights", "⌕  Explore titles", "ⓘ  Methodology"]
)

with tab_overview:
    st.markdown('<div class="section-kicker">At a glance</div>', unsafe_allow_html=True)
    st.subheader("The catalog, in context")
    st.markdown('<div class="section-intro">A quick read of the current selection. Change filters in the sidebar to explore a different slice.</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3, gap="medium")
    with a:
        insight_card("Largest content type", lead_type, f"{lead_type_pct:.1f}% of the selected titles")
    with b:
        insight_card("Peak release year", peak_year, f"{peak_year_count:,} titles released in this year" if peak_year != "—" else "No release-year data")
    with c:
        insight_card("Most frequent rating", lead_rating, f"{lead_rating_count:,} titles in this selection" if lead_rating != "Not available" else "No rating data")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        type_counts = filtered["type"].value_counts().rename_axis("Content type").reset_index(name="Titles")
        fig = px.pie(
            type_counts, names="Content type", values="Titles", hole=.68,
            color="Content type", color_discrete_map={"Movie": MOVIE_COLOR, "TV Show": TV_COLOR},
            title="Content mix",
        )
        fig.update_traces(textposition="inside", textinfo="percent", insidetextfont=dict(size=13, color="white"),
                          marker=dict(line=dict(color="#151515", width=3)),
                          hovertemplate="%{label}<br>%{value:,} titles · %{percent}<extra></extra>")
        fig.add_annotation(text=f"{len(filtered):,}<br><sup>TITLES</sup>", x=.5, y=.5,
                           showarrow=False, font=dict(size=22, color="white"))
        show_chart(style_figure(fig, 390), "overview_content_mix")
    with right:
        year_counts = filtered.dropna(subset=["release_year"]).groupby("release_year").size().reset_index(name="Titles")
        year_counts = year_counts.sort_values("release_year")
        fig = px.area(year_counts, x="release_year", y="Titles", title="Titles by release year")
        fig.update_traces(line=dict(color=RED, width=2.5), fillcolor="rgba(229,9,20,.18)",
                          hovertemplate="Release year: %{x}<br>Titles: %{y:,}<extra></extra>")
        fig.update_xaxes(title="Release year", tickformat="d")
        fig.update_yaxes(title="Number of titles")
        show_chart(style_figure(fig, 390), "overview_release_year")

    st.markdown(
        '<div class="note-box">Reading the trend correctly: release-year charts describe titles represented in this Netflix catalog snapshot. They do not measure every title produced worldwide in each year.</div>',
        unsafe_allow_html=True,
    )

with tab_content:
    st.markdown('<div class="section-kicker">Content intelligence</div>', unsafe_allow_html=True)
    st.subheader("Where the catalog is concentrated")
    st.markdown('<div class="section-intro">Country and category totals count assignments; one title can appear in multiple countries or genres.</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")
    with left:
        if "country" in filtered.columns:
            country_counts = split_assignments(filtered["country"]).value_counts().head(12).rename_axis("Country").reset_index(name="Title assignments")
        else:
            country_counts = pd.DataFrame(columns=["Country", "Title assignments"])
        fig = px.bar(country_counts.sort_values("Title assignments"), x="Title assignments", y="Country", orientation="h",
                     title="Top countries represented", text="Title assignments", color="Title assignments",
                     color_continuous_scale=[[0, "#5b171c"], [1, RED]])
        fig.update_traces(textposition="outside", cliponaxis=False,
                          hovertemplate="%{y}<br>%{x:,} title assignments<extra></extra>")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(title="Title-country assignments")
        fig.update_yaxes(title="", showgrid=False)
        show_chart(style_figure(fig, 445), "insights_countries")
    with right:
        if "listed_in" in filtered.columns:
            genre_counts = split_assignments(filtered["listed_in"]).value_counts().head(12).rename_axis("Category").reset_index(name="Assignments")
        else:
            genre_counts = pd.DataFrame(columns=["Category", "Assignments"])
        fig = px.bar(genre_counts.sort_values("Assignments"), x="Assignments", y="Category", orientation="h",
                     title="Most common genres / categories", text="Assignments", color="Assignments",
                     color_continuous_scale=[[0, "#35204f"], [1, "#9292ff"]])
        fig.update_traces(textposition="outside", cliponaxis=False,
                          hovertemplate="%{y}<br>%{x:,} category assignments<extra></extra>")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(title="Category assignments")
        fig.update_yaxes(title="", showgrid=False)
        show_chart(style_figure(fig, 445), "insights_genres")

    if "rating" in filtered.columns:
        rating_type = filtered.dropna(subset=["rating"]).groupby(["rating", "type"]).size().reset_index(name="Titles")
        rating_order = filtered["rating"].dropna().value_counts().index.tolist()
        rating_type["rating"] = pd.Categorical(rating_type["rating"], categories=rating_order, ordered=True)
        rating_type = rating_type.sort_values("rating")
        fig = px.bar(rating_type, x="rating", y="Titles", color="type", barmode="group",
                     category_orders={"rating": rating_order}, color_discrete_map={"Movie": MOVIE_COLOR, "TV Show": TV_COLOR},
                     title="Ratings by content type", labels={"rating": "Content rating"})
        fig.update_traces(hovertemplate="Rating: %{x}<br>Titles: %{y:,}<extra></extra>")
        fig.update_xaxes(title="Content rating", tickangle=-20)
        fig.update_yaxes(title="Number of titles")
        show_chart(style_figure(fig, 430), "insights_ratings")

with tab_explore:
    st.markdown('<div class="section-kicker">Catalog search</div>', unsafe_allow_html=True)
    st.subheader("Explore individual titles")
    st.markdown('<div class="section-intro">Search titles or directors, inspect their metadata, then export the rows you found.</div>', unsafe_allow_html=True)

    search_col, info_col = st.columns([2, 1])
    with search_col:
        search = st.text_input("Search title or director", placeholder="e.g. Stranger Things", label_visibility="collapsed")
    with info_col:
        display_limit = st.selectbox("Rows to display", [100, 250, 500, 1000, "All matching"], index=2)
    explore = filtered.copy()
    if search.strip():
        title_series = explore["title"].fillna("") if "title" in explore.columns else pd.Series("", index=explore.index)
        director_series = explore["director"].fillna("") if "director" in explore.columns else pd.Series("", index=explore.index)
        mask = title_series.astype(str).str.contains(search, case=False, regex=False) | director_series.astype(str).str.contains(search, case=False, regex=False)
        explore = explore[mask]
    show_cols = [c for c in ["show_id", "title", "type", "director", "country", "release_year", "rating", "duration", "listed_in"] if c in explore.columns]
    st.caption(f"{len(explore):,} matching title(s) · {len(show_cols)} fields displayed")
    preview = explore[show_cols] if display_limit == "All matching" else explore[show_cols].head(int(display_limit))
    st.dataframe(preview, use_container_width=True, hide_index=True, height=440)
    if len(preview) < len(explore):
        st.caption(f"Showing {len(preview):,} rows. Choose **All matching** to display every matching row. The download contains all rows matching the filters and search.")
    csv_data = explore[show_cols].to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇  Download matching titles as CSV", data=csv_data,
                       file_name="netflix_filtered_titles.csv", mime="text/csv", use_container_width=False)

with tab_notes:
    st.markdown('<div class="section-kicker">How to interpret this dashboard</div>', unsafe_allow_html=True)
    st.subheader("Methodology & data notes")
    st.markdown(
        """
        **Data workflow**

        1. Load the prepared dataset from `data/cleaned_netflix.csv`. If it is not available, fall back to `data/Dataset.csv`.
        2. Convert year/duration fields to numeric values where appropriate and normalize placeholder values.
        3. Apply the sidebar filters to content type, release year, rating and country.
        4. Aggregate the filtered records to build interactive charts, metric cards and the searchable title table.
        5. Export the matching filtered rows to CSV for further analysis.

        **Important interpretation notes**

        - Country and genre/category counts are **assignments**, not unique title counts. A record may name multiple countries or categories.
        - Release-year trends describe this dataset's catalog, not global production volumes.
        - “Countries represented” counts the distinct country names present in the currently selected records.
        - The KPIs and charts always reflect the current filters. Use **Reset all filters** in the sidebar to refresh the selection.

        **Project stack**

        Python · Pandas · Plotly · Streamlit
        """
    )
    st.markdown(
        '<div class="note-box">Internship project: Data Analysis Using Python · Auspify Technologies. Verify chart interpretations and explain the analysis in your own words during the project demonstration.</div>',
        unsafe_allow_html=True,
    )

st.divider()
st.markdown(
    '<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#858585;font-size:.76rem;">'
    '<span>NETFLIX CATALOG INTELLIGENCE · PYTHON DATA ANALYSIS</span>'
    '<span>Built with Pandas · Plotly · Streamlit</span></div>',
    unsafe_allow_html=True,
)
