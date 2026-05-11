from __future__ import annotations

import logging
from datetime import datetime

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

if streamlit.button("Create report"):
    faculty_source: str | list[str] = dfm_webpage
    report: str = f"/app/static/faculty publications {year_selection}.html"

    if name_selection != "All":
        faculty_source = [name_selection]
        report = f"/app/static/{name_selection} {year_selection}.html"

    run_batch_report(
        contact_email="kjdelaney@health.ucsd.edu",
        faculty_list_file=dfm_webpage,
        log=log,
        output_file=report,
        progress_bar=my_bar,
        year=year_selection,
    )
    my_bar.progress(100, text="Complete")
    streamlit.download_button(label="Download report", file_name=report, mime="html")
    #    streamlit.write("Ok!")
