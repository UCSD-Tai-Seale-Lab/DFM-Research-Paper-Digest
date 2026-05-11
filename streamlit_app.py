import streamlit
from src.dfm_research_paper_digest.query_faculty_batch import run_batch_report
from datetime import datetime

streamlit.title("Department of Family Medicine Publications Report")
report: str = f"faculty publications {datetime.now().year}.html"
run_batch_report(
    contact_email="kjdelaney@health.ucsd.edu",
    faculty_list_file="https://familymedicine.ucsd.edu/about/faculty.html",
    output_file=report,
    year=datetime.now().year,
)

with open(report, "rb") as file:
    btn = streamlit.download_button(
        label="Download faculty publications report",
        data=file,
        filename=report,
        mime="application/octet-stream",
    )
