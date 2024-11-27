import plotly.graph_objects as go
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

# Load the dataset
df = pd.read_csv(r'data/bpl_dataset.csv')
df['date'] = pd.to_datetime(df['date'])

# Filter for the last year (1 year from the latest date)
latest_date = df['date'].max()
one_year_ago = latest_date - pd.DateOffset(years=1)
df = df[df['date'] >= one_year_ago]

# Set the start and end dates based on the dataset
start_date = df['date'].min()  # Earliest date
end_date = df['date'].max()    # Latest date

# Filter the dataset for the last year (1 year from the latest date)
one_year_ago = end_date - pd.DateOffset(years = 1)
df = df[df['date'] >= one_year_ago]

# Ensure ascending order of dates
df = df.sort_values(by='date')

# Initialize week and day columns
df['week'] = 0
df['day'] = 0

# Loop through the rows and set week and day values
current_week = 0
current_day = 6  # Start on Sunday for the first row

for i, row in df.iterrows():
    # Set the day of the week for the current row (0 = Monday, 6 = Sunday)
    df.at[i, 'day'] = current_day
    # Set the week number
    df.at[i, 'week'] = current_week
    
    # Update the day and week for the next row
    current_day += 1  # Move to the next day
    if current_day > 6:  # If it's past Sunday, increment the week and reset the day to Monday
        current_day = 0
        current_week += 1

grid_data = df.groupby(['week', 'day'])['user_count'].sum().reset_index()

# Create grid data for heatmap
x = grid_data['week']
y = grid_data['day']
z = grid_data['user_count']

# Hover text (showing the week, day, and user activity)
# hover = [f"Week: {week}<br>Day: {day}<br>User Activity: {count}" 
#          for week, day, count in zip(grid_data['week'], grid_data['day'], grid_data['user_count'])]

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
        colorscale=[
            [0.0, "#ebedf0"],  # lightest green (lowest user_count)
            [0.25, "#c6e48b"],
            [0.5, "#7bc96f"],
            [0.75, "#239a3b"],
            [1.0, "#196127"],  # darkest green (highest user_count)
        ],
        colorbar=None,  # Removed the color legend
    )
)

# Formatting
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

fig.write_html("data/bpl_heatmap.html")

# Group by day and calculate the average user_count for each day
daily_avg = df.groupby('day')['user_count'].mean().reset_index()

# Sort by day of the week (Monday to Sunday)
daily_avg = daily_avg.sort_values('day')

# Create the bar chart
fig = go.Figure(
    data=go.Bar(
        x=daily_avg['day'],
        y=daily_avg['user_count'],
        text=daily_avg['user_count'].round(2),  # Display the average value on hover
        hoverinfo='text',
        marker=dict(color='royalblue')  # Color for the bars
    )
)

# Formatting the layout
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
fig.write_html("data/daily_avg_user_activity.html")
logging.info('Daily Average User Activity Chart generated.')