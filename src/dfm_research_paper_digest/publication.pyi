import logging
from datetime import datetime
import dfm_research_paper_digest

class Article:
    def __init__(self, pubmed_article: dict, log: logging.Logger):
        self.authors_list: list[dfm_research_paper_digest.Author] = []
        self.author_names_list: list[str] = []
        self.authors: str = ""
        self.journal: str = ""
        self.pmid: str = ""
        self.publication_date: datetime = datetime.now()
        self.title: str = ""
        self.year: int = 0

    def is_author_ucsd_affiliated(self, author: str) -> bool: ...

class ArticleAuthor:
    def __init__(self, author_dict: dict, log: logging.Logger) -> None:
        self.affiliation: str = ""
        self.first_name: str = ""
        self.last_name: str = ""
        self.initials: str = ""
        self.name: str = ""

    def as_author(self) -> dfm_research_paper_digest.Author: ...

class PMID:
    def __init__(self, pmid_dict: dict, log: logging.Logger) -> None:
        self.pmids: list[str] = []

class PublicationDate:
    def __init__(self, pub_date: dict, log: logging.Logger) -> None:
        self.date: datetime

class PubmedArticleSet:
    def __init__(self, pubmed_article_set: dict, log: logging.Logger):
        self.articles: list[Article] = []
