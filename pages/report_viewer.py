# https://share.google/aimode/tH5mPCGgBxcUfG53l
import streamlit

# 1. Ensure the HTML content exists in session state
if "dynamic_html" in streamlit.session_state:
    html_content = streamlit.session_state["dynamic_html"]
    streamlit.html(html_content)
