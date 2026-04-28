from datetime import datetime


class Article:
    """
        Contains PUBMED article properties.

    Attributes:
    ----------
    authors_list
    journal
    pmid
    publication_date
    title
    year

    Methods
    -------
    None
    """

    def __init__(self, pubmed_article: dict) -> None:

        if pubmed_article and "MedlineCitation" in pubmed_article:
            medline_citation: dict = pubmed_article["MedlineCitation"]

            if medline_citation and "Article" in medline_citation:
                article: dict = medline_citation["Article"]

                if article and "AuthorList" in article:
                    author_list: dict = article["AuthorList"]

                    if author_list and "Author" in author_list:
                        author_names: list[str] = [
                            ArticleAuthor(d).name for d in author_list["Author"]
                        ]

                        self.authors_list: str = ", ".join([a for a in author_names])

                if article and "Journal" in article:
                    journal: dict = article["Journal"]

                    if journal and "Title" in journal:
                        self.journal: str = journal["Title"]

                if article and "ArticleDate" in article:
                    publication_date: PublicationDate = PublicationDate(
                        article["ArticleDate"]
                    )
                    self.publication_date: datetime = publication_date.date
                    self.year: int = self.publication_date.year

                if article and "ArticleTitle" in article:
                    self.title: str = article["ArticleTitle"]

            if medline_citation and "PMID" in medline_citation:
                pmid_dict: dict = medline_citation["PMID"]

                if pmid_dict and "#text" in pmid_dict:
                    self.pmid: str = pmid_dict["#text"]


class ArticleAuthor:
    """
        Extracts info re: one author.

    Attributes:
    ----------
    FirstName
    LastName
    Initials
    name

    Methods
    -------
    None
    """

    def __init__(self, author_dict: dict) -> None:
        if author_dict and "LastName" in author_dict:
            self.LastName: str = author_dict["LastName"]

            if "ForeName" in author_dict:
                self.FirstName: str = author_dict["ForeName"]

                if "Initials" in author_dict:
                    self.Initials: str = author_dict["Initials"]
                    self.name = (
                        self.FirstName + " " + self.Initials + " " + self.LastName
                    )


class PMID:
    """
        Captures the PMID info returned from author query.

    Attributes:
    ----------
    pmids: list[str]

    Methods
    -------
    None
    """

    def __init__(self, pmid_dict: dict) -> None:
        self.pmids: list[str] = []

        if "eSearchResult" in pmid_dict:
            eSearchResult: dict = pmid_dict["eSearchResult"]

            if eSearchResult and "IdList" in eSearchResult:
                idList: dict = eSearchResult["IdList"]

                if idList and "Id" in idList:
                    self.pmids = idList["Id"]


class PublicationDate:
    """
        Assembles the components of the publication date.

    Attributes:
    ----------
    date

    Methods
    -------
    None
    """

    def __init__(self, pub_dict: dict) -> None:
        day: str = pub_dict["Day"]
        month: str = pub_dict["Month"]
        year: str = pub_dict["Year"]
        self.date: datetime = datetime.strptime(
            year + "-" + month + "-" + day, "%Y-%m-%d"
        )


class PubmedArticleSet:
    """
        Holds a list of Articles

    Attributes:
    ----------
    date

    Methods
    -------
    """

    def __init__(self, response: dict):
        self.articles: list[Article] = []

        if response and isinstance(response, dict) and "PubmedArticleSet" in response:
            pubmed_article_set: dict = response["PubmedArticleSet"]

            if pubmed_article_set and "PubmedArticle" in pubmed_article_set:
                pubmed_articles: dict = pubmed_article_set["PubmedArticle"]

                if isinstance(pubmed_articles, list):
                    for pubmed_article in pubmed_articles:
                        self.articles.append(Article(pubmed_article))
                else:
                    self.articles.append(Article(pubmed_articles))
