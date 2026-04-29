import logging
from email.mime.multipart import MIMEMultipart

from src.dfm_research_paper_digest.publication import Article

class EmailSender:
    SMTP_CONFIGS: dict = {}

    def __init__(
        self,
        smtp_server: str = None,
        smtp_port: int = 587,
        use_tls: bool = True,
        provider: str = None,
        log: logging.Logger = None,
    ):
        self.__log: logging.Logger = None
        self.__smtp_port: int = 0
        self.__smtp_server: str = ""
        self.__use_tls: bool = None

    def __build_text_body(
        self,
        publications: list[Article],
        author_name: str,
        year: int,
        faculty_count: int,
    ) -> str: ...
    def send_text_summary(
        self,
        publications: list[Article],
        to_email: str,
        from_email: str,
        password: str,
        author_name: str,
        year: int,
        faculty_count: int = 0,
    ) -> None: ...
    def send_html_report(
        self,
        html_file: str,
        to_email: str,
        from_email: str,
        password: str,
        author_name: str,
        year: int,
    ) -> None: ...
    def __send_email(
        self, msg: MIMEMultipart, from_email: str, to_email: str, password: str
    ) -> None: ...
