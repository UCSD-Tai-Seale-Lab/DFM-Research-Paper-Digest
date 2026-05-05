import logging

from metapub import PubMedArticle, PubMedAuthor

from src.dfm_research_paper_digest.faculty import Faculty

class ReportGenerator:
    def __init__(self, faculty: Faculty = None, log: logging.Logger = None):
        self.__faculty: Faculty = None
        self.__log: logging.Logger = None

    def __generate_html_content(
        self,
        publications: list[PubMedArticle],
        title: str,
        faculty_in_pubs: list[str],
    ) -> str: ...
    def generate_html_report(
        self,
        publications: list[PubMedArticle],
        output_file: str,
        title: str = "DFM Faculty Publications Report",
    ) -> None: ...
    def __highlight_faculty_authors(self, authors_list: list[PubMedAuthor]) -> str: ...
