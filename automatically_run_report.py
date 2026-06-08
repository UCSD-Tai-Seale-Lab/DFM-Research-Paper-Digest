import logging
from datetime import datetime

from src.dfm_research_paper_digest.my_logging import setup_logging
from src.dfm_research_paper_digest.query_faculty_batch import run_batch_report
from src.dfm_research_paper_digest.report_generator import ReportGenerator

# Setup logging
log: logging.Logger = setup_logging()

# Mark report with today's date.
now: datetime = datetime.now()
year_selection: int = now.year

# Faculty list.
dfm_webpage: str = "https://familymedicine.ucsd.edu/about/faculty.html"
html: str = run_batch_report(
    contact_email="kjdelaney@health.ucsd.edu",
    # faculty_list_file=dfm_webpage,
    faculty_list_file=["Tai-Seale, Ming PhD, MPH"],
    log=log,
    year=year_selection,
)
report_name: str = f"{now.strftime("%Y-%m-%d")} DFM report for {year_selection}.html"
ReportGenerator.write_html_file(html, report_name)
ReportGenerator.send_email_attachment(report_name, log)
