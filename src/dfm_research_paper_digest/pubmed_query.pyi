import logging
from datetime import datetime
from typing import Dict, List

from src.dfm_research_paper_digest.publication import Article

def display_publications(publications: list[Article], log: logging.Logger) -> None: ...
def export_to_csv(
    publications: List[Article], filename: str, log: logging.Logger
) -> None: ...

class PubMedQuery:
    BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    CHUNK_SIZE: int = 100

    def __init__(self, email: str = None, log: logging.Logger = None):
        self.email: str = None
        self.__log: logging.Logger = None

    def display_publications(publications: List[Article], log: logging.Logger): ...
    def _extract_article_info(self, article) -> Dict[str, str]: ...
    def fetch_publication_details(self, pmids: List[str]) -> List[Article]: ...
    def query_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> List[Article]: ...
    def search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> List[str]: ...
