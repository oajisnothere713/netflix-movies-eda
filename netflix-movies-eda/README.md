# Netflix Movies Data Analysis using Exploratory Data Analysis (EDA)

## Project Overview

The project analyzes Netflix movie data to understand whether movie durations
are decreasing over time and to identify patterns across genres, release years,
countries, and content types.


## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Dataset Description

  columns:

- `title`: Name of the movie or show
- `type`: Content type, such as Movie or TV Show
- `genre`: Genre or category of the title
- `release_year`: Year the title was released
- `duration`: Movie duration, usually stored like `90 min`
- `country`: Country where the title was produced


## Project Structure

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


## Installation Steps

1. clone the project.
2. Open a terminal inside the project folder.
3. copy the dataset into the given path ` netflix-movies-eda\data\raw\ `
4. now create a virtual environment:

write in terminal ->
```bash
python -m venv .venv 
```

5. activating the virtual environment:
```bash
.venv\Scripts\activate
```

6. install required libararies:

```bash
pip install -r requirements.txt
```

7. add the dataset - copy the dataset into the required location given in step 3 .

## to Run the Project

Run the python script:
```bash
python main.py
```
script saves charts to:

```text
reports/figures/
```


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

## key insights

after running the analysis it helps answer:

- are Netflix movies getting shorter over time?
- which genres usually have shorter movie durations?
- which decade produced the longest movies on average?
- how has Netflix movie volume changed over time?
- which movies are unusually short or unusually long?

- questions can change according to the dataset , one can use another dataset just check the feilds according to the script or update it.

## future improvements

- Add interactive charts with Plotly.
- Build a Streamlit dashboard for non-technical users.
- Compare Netflix movies with movies from other streaming platforms.
- Add natural language summaries generated from analysis results.
- Include country-wise duration and genre trends.
- Automate data validation before analysis.
