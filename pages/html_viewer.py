# https://share.google/aimode/tH5mPCGgBxcUfG53l
import streamlit

# 1. Ensure the HTML content exists in session state
if "dynamic_html" in streamlit.session_state:
    html_content = streamlit.session_state["dynamic_html"]

    # 2. Render the dynamic HTML using st.html (modern replacement for v1)
    streamlit.html(html_content)
else:
    streamlit.error("No HTML content found. Please navigate from the main page.")
