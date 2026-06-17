from __future__ import annotations

import logging
from datetime import datetime
import base64
import streamlit
from PIL import Image

from src.dfm_research_paper_digest.faculty import Faculty
from src.dfm_research_paper_digest.my_logging import setup_streamlit_logging
from src.dfm_research_paper_digest.query_faculty_batch import run_batch_report

# Headline
image: Image = Image.open("logos-clinicalHealth-full.png")
streamlit.image(image)
streamlit.header(" Department of Family Medicine")
streamlit.subheader("Publications Report")

# Setup logging
log: logging.Logger = setup_streamlit_logging()

# Specific faculty member? Or ALL?
dfm_webpage: str = "https://familymedicine.ucsd.edu/about/faculty.html"
faculty: Faculty = Faculty(dfm_webpage, log)
faculty_names: list[str] = faculty.names
faculty_names.insert(0, "All")
name_selection: streamlit.selectbox = streamlit.selectbox(
    "Select faculty members for report.", options=faculty_names, index=0
)
streamlit.write(f"Report on: {name_selection}")

# What year?
recent_years: list[int] = [datetime.now().year - delta for delta in [0, 1, 2, 3]]
year_selection: streamlit.selectbox = streamlit.selectbox(
    "Select year of publication.", options=recent_years, index=0
)
streamlit.write(f"Report year: {year_selection}")

# Keep track of progress.
my_bar: streamlit.progress = streamlit.progress(0)
html: str = ""
report_name: str = ""

# Initialize session_state.
if "report_is_ready" not in streamlit.session_state:
    streamlit.session_state.report_is_ready = False

if streamlit.button("Create report"):
    streamlit.session_state.report_is_ready = False
    faculty_source: str | list[str] = dfm_webpage
    streamlit.session_state.report_name = f"faculty publications {year_selection}.html"

    if name_selection != "All":
        faculty_source = [name_selection]
        streamlit.session_state.report_name = (
            f"{name_selection.replace(', ', '_')} {year_selection}.html"
        )

    html_content = run_batch_report(
        contact_email="kjdelaney@health.ucsd.edu",
        faculty_list_file=faculty_source,
        log=log,
        progress_bar=my_bar,
        year=year_selection,
    )
    my_bar.progress(100, text="Complete")

    # Store it in session state so the new tab can read it
    streamlit.session_state.html_content = html_content
    streamlit.session_state.report_is_ready = True

if streamlit.session_state.report_is_ready:
    # Create a button that targets the secondary page.
    streamlit.page_link("pages/report_viewer.py", label="View report")

    if (
        "html_content" in streamlit.session_state
        and "report_name" in streamlit.session_state
    ):
        streamlit.download_button(
            label="Download report",
            data=streamlit.session_state.html_content,
            file_name=streamlit.session_state.report_name,
            mime="text/html",
            icon=":material/download:",
        )

streamlit.link_button(
    "Go to Help Page", "https://github.com/UCSD-Tai-Seale-Lab/DFM-Research-Paper-Digest"
)
