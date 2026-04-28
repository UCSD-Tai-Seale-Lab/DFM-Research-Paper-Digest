"""
Tests Publication class.
"""

from datetime import datetime
from src.dfm_research_paper_digest.publication import Article, PMID, PubmedArticleSet


def test_pmid(fake_pmid_dict: dict):
    pmid: PMID = PMID(fake_pmid_dict)
    assert isinstance(pmid, PMID)
    assert isinstance(pmid.pmids, list)
    assert len(pmid.pmids) == 3
    assert isinstance(pmid.pmids[0], str)
    assert pmid.pmids[0] == "41651011"
    assert pmid.pmids[2] == "41351263"


def test_publication_one_article(fake_pubmed_dict_one_article: dict):
    pubmed_articleset: PubmedArticleSet = PubmedArticleSet(fake_pubmed_dict_one_article)
    assert isinstance(pubmed_articleset, PubmedArticleSet)
    articles: list[Article] = pubmed_articleset.articles
    assert isinstance(articles, list)
    assert len(articles) == 1
    first_article: Article = articles[0]
    assert isinstance(first_article, Article)
    assert isinstance(first_article.authors_list, str)
    assert first_article.authors_list.startswith("Kelly K Nielsen")
    assert isinstance(first_article.publication_date, datetime)
    assert first_article.publication_date == datetime(2026, 4, 8)
    assert first_article.journal == "GeoHealth"
    assert (
        first_article.title
        == "Building Youth Capacity for Climate-Health Science: Lessons From Implementing The DataJam in Jordan."
    )


def test_publication_two_articles(fake_pubmed_dict_two_articles: dict):
    pubmed_articleset: PubmedArticleSet = PubmedArticleSet(
        fake_pubmed_dict_two_articles
    )
    assert isinstance(pubmed_articleset, PubmedArticleSet)
    articles: list[Article] = pubmed_articleset.articles
    assert isinstance(articles, list)
    assert len(articles) == 2
    first_article: Article = articles[0]
    assert isinstance(first_article, Article)
    assert isinstance(first_article.authors_list, str)
    assert first_article.authors_list.startswith("Kelly K Nielsen")
    assert isinstance(first_article.publication_date, datetime)
    assert first_article.publication_date == datetime(2026, 4, 8)
    assert first_article.journal == "GeoHealth"
    assert (
        first_article.title
        == "Building Youth Capacity for Climate-Health Science: Lessons From Implementing The DataJam in Jordan."
    )
