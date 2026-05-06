# Netflix Movies Data Analysis using Exploratory Data Analysis (EDA)

## Project Overview

This project analyzes Netflix movie data to understand whether movie durations
are decreasing over time and to identify patterns across genres, release years,
countries, and content types.

The analysis is designed as a beginner-friendly but professional data science
portfolio project. It includes data cleaning, feature engineering, exploratory
data analysis, visual storytelling, and business-focused conclusions.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Dataset Description

The project expects a CSV file named `netflix_data.csv`.

Place the dataset here:

```text
data/raw/netflix_data.csv
```

Expected columns:

- `title`: Name of the movie or show
- `type`: Content type, such as Movie or TV Show
- `genre`: Genre or category of the title
- `release_year`: Year the title was released
- `duration`: Movie duration, usually stored like `90 min`
- `country`: Country where the title was produced

The code also supports common Netflix dataset variants where `genre` is named
`listed_in`.

## Project Structure

```text
netflix-movies-eda/
├── analysis.ipynb
├── main.py
├── README.md
├── requirements.txt
├── data/
│   └── raw/
│       └── netflix_data.csv
└── reports/
    └── figures/
```

## Installation Steps

1. Clone or download this project.
2. Open a terminal inside the project folder.
3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Add the dataset:

```text
data/raw/netflix_data.csv
```

## How to Run the Project

Run the complete Python script:

```bash
python main.py
```

Or open the notebook:

```bash
jupyter notebook analysis.ipynb
```

The script saves charts to:

```text
reports/figures/
```

## Analysis Workflow

The project follows a clear data analysis workflow:

1. Load the Netflix CSV dataset.
2. Inspect dataset shape, columns, missing values, and data types.
3. Clean column names and handle missing values.
4. Filter only movie records.
5. Convert movie duration into numeric minutes.
6. Create useful features such as primary genre and decade.
7. Analyze duration trends by release year, genre, and decade.
8. Detect duration outliers.
9. Generate charts and business insights.
10. Summarize final conclusions.

## Visualizations Included

- Scatter plot of movie duration vs release year with trend line
- Histogram of movie durations
- Genre distribution chart
- Movies released each year
- Boxplot of duration by genre
- Correlation heatmap
- Genre-wise trend analysis
- Average duration by decade
- Top 10 longest movies table
- Outlier detection summary

## Key Insights

After running the analysis, the project helps answer:

- Are Netflix movies getting shorter over time?
- Which genres usually have shorter movie durations?
- Which decade produced the longest movies on average?
- How has Netflix movie volume changed over time?
- Which movies are unusually short or unusually long?

The exact answers depend on the contents of your `netflix_data.csv` file. The
notebook and script calculate these insights directly from the dataset.

## Screenshots Placeholder

Add screenshots of your charts here after running the notebook or script.

```markdown
![Duration vs Release Year](reports/figures/duration_vs_release_year.png)
![Genre Distribution](reports/figures/genre_distribution.png)
![Average Duration by Decade](reports/figures/average_duration_by_decade.png)
```

## Future Improvements

- Add interactive charts with Plotly.
- Build a Streamlit dashboard for non-technical users.
- Compare Netflix movies with movies from other streaming platforms.
- Add natural language summaries generated from analysis results.
- Include country-wise duration and genre trends.
- Automate data validation before analysis.

## Git Commands to Push to GitHub

```bash
git init
git add .
git commit -m "Add Netflix movies EDA project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/netflix-movies-eda.git
git push -u origin main
```

If this project is already inside an existing Git repository, use:

```bash
git add netflix-movies-eda
git commit -m "Add Netflix movies EDA project"
git push
```
