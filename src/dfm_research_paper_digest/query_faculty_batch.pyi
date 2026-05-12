import logging
from datetime import datetime

from metapub import PubMedArticle
import streamlit
from dfm_research_paper_digest import Faculty, PubMedQuery

def run_batch_report(
    contact_email: str = None,
    faculty_list_file: str = None,
    log: logging.Logger = None,
    progress_bar: streamlit.progress = None,
    year: int = datetime.now().year,
) -> str: ...
def __assemble_article_list(
    query: PubMedQuery,
    faculty: Faculty,
    year: int,
    log: logging.Logger,
    progress_bar: streamlit.progress,
) -> list[PubMedArticle]: ...
def main(argv=None) -> None: ...
