from datetime import datetime

class Article:
    def __init__(self, pubmed_article: dict):
        self.authors_list: list[str] = []
        self.journal: str = ""
        self.pmid: str = ""
        self.publication_date: datetime = datetime.now()
        self.title: str = ""
        self.year: int = 0

class ArticleAuthor:
    def __init__(self, author_dict: dict) -> None:
        self.FirstName: str = ""
        self.LastName: str = ""
        self.Initials: str = ""
        self.name: str = ""

class PMID:
    def __init__(self, pmid_dict: dict) -> None:
        self.pmids: list[str] = []

class PublicationDate:
    def __init__(self, pub_date: dict) -> None:
        self.date: datetime

class PubmedArticleSet:
    def __init__(self, pubmed_article_set: dict):
        self.articles: list[Article] = []
