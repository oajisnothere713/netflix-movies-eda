from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "netflix_titles.csv"
FALLBACK_DATA_PATH = PROJECT_ROOT / "netflix_titles.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

IMPORTANT_COLUMNS = [
    "title",
    "type",
    "genre",
    "release_year",
    "duration",
    "country",
]


def find_dataset() -> Path:
    """Return the Netflix CSV path if it exists."""
    if DEFAULT_DATA_PATH.exists():
        return DEFAULT_DATA_PATH
    if FALLBACK_DATA_PATH.exists():
        return FALLBACK_DATA_PATH

    raise FileNotFoundError(
        "Could not find netflix_titles.csv. Place it in data/raw/netflix_titles.csv "
        "or in the project root."
    )


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load the Netflix dataset from a CSV file."""
    return pd.read_csv(csv_path)


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and support common Netflix dataset variants."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Some public Netflix datasets use "listed_in" instead of "genre".
    if "genre" not in cleaned.columns and "listed_in" in cleaned.columns:
        cleaned = cleaned.rename(columns={"listed_in": "genre"})

    return cleaned


def convert_duration_to_minutes(duration: object) -> float:
    """Extract the numeric movie duration from values such as '90 min'."""
    if pd.isna(duration):
        return np.nan

    duration_text = str(duration).strip()
    extracted = pd.Series(duration_text).str.extract(r"(\d+)")[0].iloc[0]

    if pd.isna(extracted):
        return np.nan

    return float(extracted)


def clean_movie_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset and return movie-only records ready for EDA."""
    cleaned = standardize_columns(df)

    missing_columns = [
        column for column in IMPORTANT_COLUMNS if column not in cleaned.columns
    ]
    if missing_columns:
        raise ValueError(
            "The dataset is missing required columns: "
            f"{', '.join(missing_columns)}"
        )

    cleaned = cleaned[IMPORTANT_COLUMNS].copy()

    # Keep only movies because the project question is about movie duration.
    movies = cleaned[cleaned["type"].str.lower().eq("movie")].copy()

    movies["title"] = movies["title"].fillna("Unknown Title")
    movies["genre"] = movies["genre"].fillna("Unknown")
    movies["country"] = movies["country"].fillna("Unknown")
    movies["release_year"] = pd.to_numeric(
        movies["release_year"], errors="coerce"
    )
    movies["duration_minutes"] = movies["duration"].apply(
        convert_duration_to_minutes
    )

    movies = movies.dropna(subset=["release_year", "duration_minutes"])
    movies["release_year"] = movies["release_year"].astype(int)
    movies["duration_minutes"] = movies["duration_minutes"].astype(int)
    movies["decade"] = (movies["release_year"] // 10) * 10

    # Use the first listed genre as the primary genre for grouped charts.
    movies["primary_genre"] = (
        movies["genre"].astype(str).str.split(",").str[0].str.strip()
    )

    return movies


def detect_duration_outliers(movies: pd.DataFrame) -> pd.DataFrame:
    """Detect movie duration outliers using the IQR method."""
    q1 = movies["duration_minutes"].quantile(0.25)
    q3 = movies["duration_minutes"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = movies[
        (movies["duration_minutes"] < lower_bound)
        | (movies["duration_minutes"] > upper_bound)
    ].copy()

    return outliers.sort_values("duration_minutes", ascending=False)


def save_scatter_with_trend(movies: pd.DataFrame) -> None:
    """Save a scatter plot of movie duration versus release year."""
    plt.figure(figsize=(12, 6))
    sns.regplot(
        data=movies,
        x="release_year",
        y="duration_minutes",
        scatter_kws={"alpha": 0.35},
        line_kws={"color": "red", "linewidth": 2},
    )
    plt.title("Netflix Movie Duration vs Release Year")
    plt.xlabel("Release Year")
    plt.ylabel("Duration (Minutes)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "duration_vs_release_year.png", dpi=300)
    plt.close()


def save_duration_histogram(movies: pd.DataFrame) -> None:
    """Save a histogram showing movie duration distribution."""
    plt.figure(figsize=(12, 6))
    sns.histplot(movies["duration_minutes"], bins=30, kde=True, color="#2a9d8f")
    plt.title("Distribution of Netflix Movie Durations")
    plt.xlabel("Duration (Minutes)")
    plt.ylabel("Number of Movies")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "duration_histogram.png", dpi=300)
    plt.close()


def save_genre_distribution(movies: pd.DataFrame) -> None:
    """Save a chart of the top movie genres."""
    top_genres = movies["primary_genre"].value_counts().head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_genres.values, y=top_genres.index, palette="viridis")
    plt.title("Top 10 Netflix Movie Genres")
    plt.xlabel("Number of Movies")
    plt.ylabel("Primary Genre")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "genre_distribution.png", dpi=300)
    plt.close()


def save_movies_per_year(movies: pd.DataFrame) -> None:
    """Save a count plot of movies released by year."""
    yearly_counts = movies["release_year"].value_counts().sort_index()

    plt.figure(figsize=(14, 6))
    sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o")
    plt.title("Netflix Movies Released Each Year")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Movies")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "movies_per_year.png", dpi=300)
    plt.close()


def save_boxplot_by_genre(movies: pd.DataFrame) -> None:
    """Save a duration boxplot for the most common genres."""
    top_genres = movies["primary_genre"].value_counts().head(10).index
    genre_subset = movies[movies["primary_genre"].isin(top_genres)]

    plt.figure(figsize=(14, 7))
    sns.boxplot(
        data=genre_subset,
        x="duration_minutes",
        y="primary_genre",
        palette="Set2",
    )
    plt.title("Movie Duration by Top Genres")
    plt.xlabel("Duration (Minutes)")
    plt.ylabel("Primary Genre")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "duration_by_genre_boxplot.png", dpi=300)
    plt.close()


def save_correlation_heatmap(movies: pd.DataFrame) -> None:
    """Save a heatmap for numeric column correlations."""
    numeric_data = movies[["release_year", "duration_minutes", "decade"]]

    plt.figure(figsize=(8, 5))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()


def save_genre_trend_analysis(movies: pd.DataFrame) -> None:
    """Save genre-wise average duration trends over time."""
    top_genres = movies["primary_genre"].value_counts().head(5).index
    trend_data = movies[movies["primary_genre"].isin(top_genres)]
    trend_data = (
        trend_data.groupby(["release_year", "primary_genre"])["duration_minutes"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=trend_data,
        x="release_year",
        y="duration_minutes",
        hue="primary_genre",
        marker="o",
    )
    plt.title("Genre-Wise Average Movie Duration Trend")
    plt.xlabel("Release Year")
    plt.ylabel("Average Duration (Minutes)")
    plt.legend(title="Primary Genre")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "genre_duration_trends.png", dpi=300)
    plt.close()


def save_average_duration_by_decade(movies: pd.DataFrame) -> None:
    """Save a bar chart of average duration by decade."""
    decade_duration = (
        movies.groupby("decade")["duration_minutes"].mean().reset_index()
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=decade_duration,
        x="decade",
        y="duration_minutes",
        palette="magma",
    )
    plt.title("Average Netflix Movie Duration by Decade")
    plt.xlabel("Decade")
    plt.ylabel("Average Duration (Minutes)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "average_duration_by_decade.png", dpi=300)
    plt.close()


def create_visualizations(movies: pd.DataFrame) -> None:
    """Create and save all EDA visualizations."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    save_scatter_with_trend(movies)
    save_duration_histogram(movies)
    save_genre_distribution(movies)
    save_movies_per_year(movies)
    save_boxplot_by_genre(movies)
    save_correlation_heatmap(movies)
    save_genre_trend_analysis(movies)
    save_average_duration_by_decade(movies)


def print_insights(movies: pd.DataFrame) -> None:
    """Print concise business insights from the cleaned movie data."""
    correlation = movies["release_year"].corr(movies["duration_minutes"])
    yearly_average = movies.groupby("release_year")["duration_minutes"].mean()
    decade_average = movies.groupby("decade")["duration_minutes"].mean()
    genre_average = (
        movies.groupby("primary_genre")["duration_minutes"]
        .mean()
        .sort_values()
    )

    longest_decade = decade_average.idxmax()
    shortest_genres = genre_average.head(5)
    longest_movies = movies.nlargest(10, "duration_minutes")[
        ["title", "release_year", "primary_genre", "duration_minutes"]
    ]
    outliers = detect_duration_outliers(movies)

    print("\nNetflix Movies EDA Summary")
    print("=" * 30)
    print(f"Total cleaned movie records: {len(movies):,}")
    print(f"Release year range: {movies['release_year'].min()}-"
          f"{movies['release_year'].max()}")
    print(f"Average movie duration: {movies['duration_minutes'].mean():.1f} min")
    print(f"Correlation between release year and duration: {correlation:.3f}")

    if correlation < -0.1:
        print("Insight: Movie durations show a decreasing trend over time.")
    elif correlation > 0.1:
        print("Insight: Movie durations show an increasing trend over time.")
    else:
        print("Insight: Movie durations are mostly stable over time.")

    print(f"\nDecade with longest average movies: {longest_decade}s")
    print("\nAverage duration by decade:")
    print(decade_average.round(1).to_string())

    print("\nFive genres with shortest average durations:")
    print(shortest_genres.round(1).to_string())

    print("\nTop 10 longest movies:")
    print(longest_movies.to_string(index=False))

    print(f"\nDuration outliers detected: {len(outliers):,}")
    if not outliers.empty:
        print(outliers[["title", "duration_minutes"]].head(10).to_string(index=False))

    print(f"\nCharts saved to: {FIGURES_DIR}")
    print(f"Recent yearly average duration sample:\n{yearly_average.tail().round(1)}")


def main() -> None:
    """Run the complete Netflix movies EDA workflow."""
    sns.set_theme(style="whitegrid", palette="deep")

    csv_path = find_dataset()
    raw_data = load_data(csv_path)
    movies = clean_movie_data(raw_data)

    create_visualizations(movies)
    print_insights(movies)


if __name__ == "__main__":
    main()
