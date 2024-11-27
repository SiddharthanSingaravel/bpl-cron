import streamlit as st
import streamlit.components.v1 as components

# Define the path to the HTML file containing the Plotly chart
html_file_path = "data/bpl_heatmap.html"
st.set_page_config(layout="wide", page_title="Boston Public Library Activity")

# Apply custom CSS styling to improve the layout
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f9;
            font-family: 'Arial', sans-serif;
        }
        .header {
            text-align: center;
            color: #333;
            font-size: 36px;
            margin-top: 20px;
        }
        .subheader {
            text-align: center;
            font-size: 28px;
            color: #555;
            margin-top: 20px;
        }
        .error {
            color: #e74c3c;
        }
        .chart-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 30px 0;
        }
        .chart-container .stMarkdown {
            margin: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main header
st.markdown("<div class='header'>Boston Public Library</div>", unsafe_allow_html=True)

# Chart 1: Activity Heatmap
st.markdown("<div class='subheader'>Daily Activity Heatmap</div>", unsafe_allow_html=True)

# Open the HTML file with utf-8 encoding for Chart 1
try:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Display the Plotly chart inside a container
    if html_content:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            components.html(html_content, height=600)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='error'>The HTML file is empty or not found.</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.markdown(f"<div class='error'>HTML file {html_file_path} not found.</div>", unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"<div class='error'>Error loading HTML file: {e}</div>", unsafe_allow_html=True)

# Chart 2: Day Average User Activity
st.markdown("<div class='subheader'>Day Averages of User Activity</div>", unsafe_allow_html=True)

# Open the HTML file with utf-8 encoding for Chart 2
html_file_path = "data/daily_avg_user_activity.html"
try:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Display the Plotly chart inside a container
    if html_content:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            components.html(html_content, height=600)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='error'>The HTML file is empty or not found.</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.markdown(f"<div class='error'>HTML file {html_file_path} not found.</div>", unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"<div class='error'>Error loading HTML file: {e}</div>", unsafe_allow_html=True)
