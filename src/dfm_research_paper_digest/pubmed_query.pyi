import logging
from datetime import datetime

from src.dfm_research_paper_digest.publication import Article

def display_publications(publications: list[Article], log: logging.Logger) -> None: ...
def export_to_csv(
    publications: list[Article], filename: str, log: logging.Logger
) -> None: ...

class PubMedQuery:
    BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    CHUNK_SIZE: int = 100

    def __init__(self, email: str = None, log: logging.Logger = None):
        self.email: str = None
        self.__log: logging.Logger = None

    def display_publications(publications: list[Article], log: logging.Logger): ...
    def fetch_publication_details(
        self, pmids: list[str], author_name: str
    ) -> list[Article]: ...
    def query_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[Article]: ...
    def search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[str]: ...
