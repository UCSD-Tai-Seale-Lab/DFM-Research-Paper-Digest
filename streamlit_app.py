from __future__ import annotations

import logging
from datetime import datetime

import streamlit
import streamlit.components.v1 as components
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
    report: str = f"faculty publications {year_selection}.html"

    if name_selection != "All":
        faculty_source = [name_selection]
        report = f"{name_selection.replace(', ', '_')} {year_selection}.html"

    html: str = run_batch_report(
        contact_email="kjdelaney@health.ucsd.edu",
        faculty_list_file=faculty_source,
        log=log,
        progress_bar=my_bar,
        year=year_selection,
    )
    my_bar.progress(100, text="Complete")

    # Display report in new tab.
    if streamlit.button("Display report"):
        log.info("Clicked 'display report' button.")

        # JavaScript to open a new window and write HTML to it
        js_code = f"""
        <script>
            function openInNewTab() {{
                var newWindow = window.open();
                newWindow.document.write(`{html}`);
                newWindow.document.close();
            }}
            openInNewTab();
        </script>
        """
        components.html(js_code, height=0)

        streamlit.download_button(
            label="Download report",
            data=html,
            file_name=report,
            mime="text/html",
            icon=":material/download:",
        )
