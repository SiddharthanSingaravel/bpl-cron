# Cron-Scheduled: Automating Data Updates and Reporting
## Boston Public Library: Daily Footfalls

This project involves analyzing user activity data for the Boston Public Library over the past year. The analysis uses `pandas` for data manipulation and `Plotly` for visualization. The main goal is to generate two types of visualizations:

1. A **heatmap** showing user activity over weeks and days of the week.
2. A **bar chart** showing the daily average user activity.

Additionally, the dataset is processed to calculate **weeks** based on the number of days since the start date, and this logic is used to correctly assign a week number for each date.

`streamlit run streamlitApp.py` should run the Streamlit dashboard. In this project, it is connected to Streamlit Cloud through Github.

### Setting up Cron Scheduling
```yaml
name: Daily Dataset Update

on:
  schedule:
    - cron: "0 7 * * *"  # Runs daily at 7 AM UTC
  workflow_dispatch:  # Allows manual trigger of the workflow

jobs:
  update-dataset:
    runs-on: ubuntu-latest

    steps:
      # Checkout the repository
      - name: Checkout code
        uses: actions/checkout@v3

      # Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      # Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Run the orchestrate script
      - name: Generate Dataset
        run: |
          python orchestrate.py

      # Commit and push changes
      - name: Commit and push changes
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add data/bpl_dataset.csv
          git commit -m "Automated dataset update: $(date)"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Process Overview

### Step 1: Importing Required Libraries
We begin by importing the necessary libraries for the analysis.

```python
import plotly.graph_objects as go
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
```

### Step 2: Loading and Preparing the Dataset
The dataset is loaded into a pandas DataFrame. We ensure that the date column is in the correct datetime format.

```python
# Load the dataset
df = pd.read_csv(r'data/bpl_dataset.csv')
df['date'] = pd.to_datetime(df['date'])  # Ensure date is in datetime format
# Filter for the last year (1 year from the latest date)
latest_date = df['date'].max()
one_year_ago = latest_date - pd.DateOffset(years=1)
df = df[df['date'] >= one_year_ago]

# Ensure ascending order of dates
df = df.sort_values(by='date')

# Set start date (the date of Week 0)
start_date = df['date'].min()

# Calculate days from start (first date of the dataset)
df['days_from_start'] = (df['date'] - start_date).dt.days

# Assign weekdays using pandas' weekday method (0 = Monday, 6 = Sunday)
df['day'] = df['date'].dt.weekday  # 0 = Monday, 6 = Sunday

# Initialize week as 0
df['week'] = 0

# Custom logic for assigning weeks: week 0 starts with the first row, then increments when day = 0 (Monday)
current_week = 0
for i, row in df.iterrows():
    # Check if it's a Monday (day == 0) and it's not the first record
    if row['day'] == 0 and i > 0:
        current_week += 1  # Increment the week
    df.at[i, 'week'] = current_week  # Update the week for the current row

# Group data by week and day, then sum user activity for each (week, day) pair
grid_data = df.groupby(['week', 'day'])['user_count'].sum().reset_index()
```

### Step 3: Heatmap & Bar Chart Showing Daily Activity and Day Averages
Using Plotly, we create a heatmap that shows user activity across weeks and days of the week. Each cell represents the total user activity for a particular week and day.
```python
# Create grid data for heatmap
x = grid_data['week']
y = grid_data['day']
z = grid_data['user_count']

# Hover text showing date and user activity
hover = [f"Date: {date.strftime('%Y-%m-%d')}<br>User Activity: {count}" 
         for date, count in zip(df['date'], df['user_count'])]

# Create Plotly heatmap
fig = go.Figure(
    data=go.Heatmap(
        x=x,
        y=y,
        z=z,
        text=hover,
        hoverinfo="text",
        colorscale=[  # Green color scale for user activity
            [0.0, "#ebedf0"],  # lightest green (lowest user_count)
            [0.25, "#c6e48b"],
            [0.5, "#7bc96f"],
            [0.75, "#239a3b"],
            [1.0, "#196127"],  # darkest green (highest user_count)
        ],
        colorbar=None,  # Removed the color legend
    )
)

# Formatting the layout for the heatmap
fig.update_layout(
    title="Boston Public Library: Daily Activity",
    xaxis=dict(
        title="Weeks",
        tickmode="array",
        tickvals=month_ticks,
        ticktext=month_labels,
        showgrid=False,
    ),
    yaxis=dict(
        title="Days",
        tickvals=list(range(7)),
        ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    ),
    plot_bgcolor="white",
    font=dict(family="Verdana"),
)

# Save the heatmap HTML to file
fig.write_html("data/bpl_heatmap.html")
logging.info('Chart 1: Boston Public Library Heatmap generated.')

# Group by day and calculate the average user_count for each day
daily_avg = df.groupby('day')['user_count'].mean().reset_index()

# Sort by day of the week (Monday to Sunday)
daily_avg = daily_avg.sort_values('day')

# Create the bar chart for daily averages
fig = go.Figure(
    data=go.Bar(
        x=daily_avg['day'],
        y=daily_avg['user_count'],
        text=daily_avg['user_count'].round(2),  # Display the average value on hover
        hoverinfo='text',
        marker=dict(color='royalblue')  # Color for the bars
    )
)

# Formatting the layout for the bar chart
fig.update_layout(
    title="Daily Averages of User Activity",
    xaxis=dict(
        title="Day of the Week",
        tickmode='array',
        tickvals=list(range(7)),
        ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],  # Day names
        showgrid=False
    ),
    yaxis=dict(
        title="Average User Count"
    ),
    plot_bgcolor="white",
    font=dict(family="Verdana"),
)

# Save the bar chart HTML to file
fig.write_html("data/daily_avg_user_activity.html")

# Log that the charts were generated successfully
logging.info('Chart 2: Daily Average User Activity Chart generated.')
```

### Step 4: Streamlit App

```python
# Streamlit layout
st.title("📊 Boston Public Library: User Activity Analysis")

st.header("🟢 Weekly User Activity Heatmap")
st.plotly_chart(heatmap_fig)  # Display the heatmap

st.header("📅 Daily Average User Activity")
st.plotly_chart(bar_chart_fig)  # Display the bar chart
```

