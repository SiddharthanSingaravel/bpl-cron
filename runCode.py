import plotly.graph_objects as go
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

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

# Create grid data for heatmap
x = grid_data['week']
y = grid_data['day']
z = grid_data['user_count']

# Hover text showing date and user activity
hover = [f"Date: {date.strftime('%Y-%m-%d')}<br>User Activity: {count}" 
         for date, count in zip(df['date'], df['user_count'])]

# Determine x-ticks for month labels
month_starts = pd.date_range(df['date'].min(), df['date'].max(), freq='MS')
month_ticks = [(month_start - df['date'].min()).days // 7 for month_start in month_starts]
month_labels = [month_start.strftime("%b") for month_start in month_starts]

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