from datetime import datetime
import logging
import streamlit

from src.dfm_research_paper_digest.faculty import Faculty
from src.dfm_research_paper_digest.query_faculty_batch import run_batch_report
from src.dfm_research_paper_digest.my_logging import setup_logging

streamlit.title("UCSD Health")
streamlit.header(" Department of Family Medicine")
streamlit.subheader("Publications Report")

log: logging.Logger = setup_logging()
faculty: Faculty = Faculty("https://familymedicine.ucsd.edu/about/faculty.html", log)
faculty_names: list[str] = faculty.names
faculty_names.insert(0, "All")
streamlit.write(f"Received {len(faculty_names)} names.")
# selection: streamlit.selectbox = streamlit.selectbox(
#    "Select faculty members for report.", faculty_names
# )
# streamlit.write(f"Selection: {selection}")

progress_text: str = "Pulling data from PubMed..."
my_bar: streamlit.progress = streamlit.progress(0, progress_text)

if streamlit.button("Create report"):
    streamlit.write("Ok!")
    my_bar.progress(100, text=progress_text)
else:
    streamlit.write("Why am I here?")
# report: str = f"faculty publications {datetime.now().year}.html"
# run_batch_report(
#    contact_email="kjdelaney@health.ucsd.edu",
#    faculty_list_file="https://familymedicine.ucsd.edu/about/faculty.html",
#    output_file=report,
#    year=datetime.now().year,
# )

# with open(report, "rb") as file:
#    btn = streamlit.download_button(
#        label="Download faculty publications report",
#        data=file,
#        filename=report,
#        mime="application/octet-stream",
#    )
