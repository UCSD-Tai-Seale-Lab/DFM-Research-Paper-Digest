import logging
from datetime import datetime

import streamlit
from metapub import PubMedArticle

from dfm_research_paper_digest import Faculty, PubMedQuery

def run_batch_report(
    contact_email: str = "",
    faculty_list_file: str | list[str] = "",
    log: logging.Logger | None = None,
    progress_bar: streamlit.progress = None,
    title: str = "",
    year: int = datetime.now().astimezone().year,
) -> str: ...
def __assemble_article_list(
    query: PubMedQuery,
    faculty: Faculty,
    year: int,
    log: logging.Logger,
    progress_bar: streamlit.progress,
) -> list[PubMedArticle]: ...
def main(argv=None) -> None: ...
