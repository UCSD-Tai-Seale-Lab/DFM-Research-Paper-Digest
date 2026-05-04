import logging
from datetime import datetime
import dfm_research_paper_digest


class Article:
    """
        Contains PUBMED article properties.

    Attributes:
    ----------
    authors_list
    author_names_list
    authors
    journal
    pmid
    publication_date
    title
    year

    Methods
    -------
    is_author_ucsd_affiliated()
    """

    def __init__(self, pubmed_article: dict, log: logging.Logger) -> None:

        if pubmed_article and "MedlineCitation" in pubmed_article:
            medline_citation: dict = pubmed_article["MedlineCitation"]

            if medline_citation and "Article" in medline_citation:
                article: dict = medline_citation["Article"]

                if article and "AuthorList" in article:
                    author_list: dict = article["AuthorList"]

                    if author_list and "Author" in author_list:
                        self.authors_list: list[dfm_research_paper_digest.Author] = []
                        self.author_names_list: list[str] = []

                        for name in author_list["Author"]:
                            try:
                                # Create an Author object.
                                author: dfm_research_paper_digest.Author = (
                                    ArticleAuthor(name, log).as_author()
                                )
                                self.authors_list.append(author)

                                # Also maintain a list of string author names.
                                self.author_names_list.append(author.pubmed_style)

                            except AttributeError:
                                log.exception(
                                    "AttributeError: 'ArticleAuthor' object has no attribute 'name' for object created with {name}."
                                )

                        self.authors: str = ", ".join(
                            [au.original for au in self.authors_list]
                        )

                if article and "Journal" in article:
                    journal: dict = article["Journal"]

                    if journal and "Title" in journal:
                        self.journal: str = journal["Title"]

                if article and "ArticleDate" in article:
                    publication_date: PublicationDate = PublicationDate(
                        article["ArticleDate"], log
                    )
                    self.publication_date: datetime = publication_date.date
                    self.year: int = self.publication_date.year

                if article and "ArticleTitle" in article:
                    self.title: str = article["ArticleTitle"]

            if medline_citation and "PMID" in medline_citation:
                pmid_dict: dict = medline_citation["PMID"]

                if pmid_dict and "#text" in pmid_dict:
                    self.pmid: str = pmid_dict["#text"]

    def is_author_ucsd_affiliated(self, author_name: str) -> bool:
        """
            Checks that the author is affiliated with UCSD (according to the article).

        Args:
            author_name: str

        Returns
        -------
        bool
        """
        matching_Author: dfm_research_paper_digest.Author = next(
            (a for a in self.authors_list if a.matches(author_name)), None
        )
        return matching_Author.is_ucsd()


class ArticleAuthor:
    """
        Extracts info re: one author.

    Attributes:
    ----------
    affiliation
    initials
    first_name
    last_name
    name

    Methods
    -------
    None
    """

    def __init__(self, author_dict: dict, log: logging.Logger) -> None:
        self.affiliation: str = ""
        self.first_name: str = ""
        self.initials: str = ""
        self.last_name: str = ""
        self.name: str = ""

        if author_dict and "LastName" in author_dict:
            self.last_name = author_dict["LastName"]

            if "ForeName" in author_dict:
                self.first_name = author_dict["ForeName"]

                if "Initials" in author_dict:
                    self.initials = author_dict["Initials"]
                    self.name = (
                        self.first_name + " " + self.initials + " " + self.last_name
                    )
                else:
                    self.name = self.first_name + " " + self.last_name

                if "AffiliationInfo" in author_dict:
                    affiliation_dict: dict = author_dict["AffiliationInfo"]

                    if affiliation_dict and "Affiliation" in affiliation_dict:
                        self.affiliation = affiliation_dict["Affiliation"]

    def as_author(self) -> dfm_research_paper_digest.Author:
        """
            Create an Author object.

        Returns
        -------
        author: Author
        """
        author: dfm_research_paper_digest.Author = dfm_research_paper_digest.Author(
            self.name
        )
        author.add_affiliation(self.affiliation)
        return author


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

    def __init__(self, pmid_dict: dict, log: logging.Logger) -> None:
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

    def __init__(self, pub_dict: dict, log: logging.Logger) -> None:
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

    def __init__(self, response: dict, log: logging.Logger):
        self.articles: list[Article] = []

        if response and isinstance(response, dict) and "PubmedArticleSet" in response:
            pubmed_article_set: dict = response["PubmedArticleSet"]

            if pubmed_article_set and "PubmedArticle" in pubmed_article_set:
                pubmed_articles: dict = pubmed_article_set["PubmedArticle"]

                if isinstance(pubmed_articles, list):
                    for pubmed_article in pubmed_articles:
                        self.articles.append(Article(pubmed_article, log))
                else:
                    self.articles.append(Article(pubmed_articles, log))
