import logging

from metapub import PubMedArticle, PubMedAuthor
from enum import Enum
from src.dfm_research_paper_digest.faculty import Faculty

class HighlightStyle(Enum):
    BOLD = 1
    LINK = 2
    PLAIN = 3

class ReportGenerator:
    def __init__(self, faculty: Faculty = None, log: logging.Logger = None):
        self.__faculty: Faculty = None
        self.__log: logging.Logger = None
        self.__highlight_style: HighlightStyle = None

    def __format_authors(
        self, nice_name: str, is_faculty: bool, plain: bool
    ) -> str: ...
    def generate_html_content(
        self,
        publications: list[PubMedArticle],
        title: str,
    ) -> str: ...
    def generate_html_report(
        self,
        publications: list[PubMedArticle],
        output_file: str,
        title: str = "DFM Faculty Publications Report",
    ) -> None: ...
    def __count_unique_faculty_members(
        self, publications: list[PubMedArticle]
    ) -> int: ...
    def __list_faculty_authors(
        self, authors_list: list[PubMedAuthor], plain: bool
    ) -> str: ...
    @staticmethod
    def send_email(html_body: str, log: logging.Logger) -> None: ...
    @staticmethod
    def send_email_attachment(report_name: str, log: logging.Logger) -> None: ...
    @staticmethod
    def write_html_file(html: str, output_file: str) -> None: ...
