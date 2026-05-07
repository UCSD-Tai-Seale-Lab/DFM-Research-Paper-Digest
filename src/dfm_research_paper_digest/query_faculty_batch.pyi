import logging
from datetime import datetime

from metapub import PubMedArticle

from dfm_research_paper_digest import Faculty, PubMedQuery

def query_faculty_batch(
    contact_email: str = None,
    faculty_list_file: str = None,
    log: logging.Logger = None,
    output_file: str = None,
    year: int = datetime.now().year,
) -> None: ...
def __assemble_article_list__(
    query: PubMedQuery, faculty: Faculty, year: int, log: logging.Logger
) -> list[PubMedArticle]: ...
def main(argv=None) -> None: ...
