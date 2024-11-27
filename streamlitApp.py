import streamlit as st
import streamlit.components.v1 as components

# Define the path to the HTML file containing the Plotly chart
html_file_path = "data/bpl_heatmap.html"
st.set_page_config(layout="wide")
st.header("Boston Public Library")

# Set background to white
# st.markdown(
#     """
#     <style>
#         body {
#             background-color: white;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# Chart 1
# Open the HTML file with utf-8 encoding
try:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Ensure that the file contains the necessary HTML for Plotly
    if html_content:
        # Display the Plotly chart using Streamlit components
        components.html(html_content, height=600)
    else:
        st.subheader("Daily Activity")
        st.error("The HTML file is empty or not found.")

except FileNotFoundError:
    st.error(f"HTML file {html_file_path} not found.")
except Exception as e:
    st.error(f"Error loading HTML file: {e}")

# Chart 2
# Open the HTML file with utf-8 encoding
html_file_path = "data/daily_avg_user_activity.html"
try:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Ensure that the file contains the necessary HTML for Plotly
    if html_content:
        # Display the Plotly chart using Streamlit components
        st.subheader("Day Averages")
        components.html(html_content, height=600)
    else:
        st.error("The HTML file is empty or not found.")

except FileNotFoundError:
    st.error(f"HTML file {html_file_path} not found.")
except Exception as e:
    st.error(f"Error loading HTML file: {e}")

    