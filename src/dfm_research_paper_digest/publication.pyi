from datetime import datetime
import logging

class Article:
    def __init__(self, pubmed_article: dict, log: logging.Logger):
        self.authors_list: list[str] = []
        self.authors: str = ""
        self.journal: str = ""
        self.pmid: str = ""
        self.publication_date: datetime = datetime.now()
        self.title: str = ""
        self.year: int = 0

class ArticleAuthor:
    def __init__(self, author_dict: dict, log: logging.Logger) -> None:
        self.FirstName: str = ""
        self.LastName: str = ""
        self.Initials: str = ""
        self.name: str = ""

class PMID:
    def __init__(self, pmid_dict: dict, log: logging.Logger) -> None:
        self.pmids: list[str] = []

class PublicationDate:
    def __init__(self, pub_date: dict, log: logging.Logger) -> None:
        self.date: datetime

class PubmedArticleSet:
    def __init__(self, pubmed_article_set: dict, log: logging.Logger):
        self.articles: list[Article] = []
