"""
Tests PubMedQuery class.
"""

from metapub import PubMedArticle

from dfm_research_paper_digest import PubMedQuery


def test_pubmed_query(logger, username):
    pubmed_query: PubMedQuery = PubMedQuery(
        log=logger, email=f"{username}@health.ucsd.com"
    )
    assert isinstance(pubmed_query, PubMedQuery)
    articles: list[PubMedArticle] = pubmed_query.query_by_author(
        author_name="Ming Tai-Seale", year=2025
    )
    assert isinstance(articles, list)
    first_article: PubMedArticle = articles[0]
    assert isinstance(first_article, PubMedArticle)


def test_affiliation():
    assert PubMedQuery.is_ucsd_affiliated(["University of California, San Diego"])
    assert PubMedQuery.is_ucsd_affiliated(["UCSD San Diego", "University of San Diego"])
    assert not PubMedQuery.is_ucsd_affiliated(["San Diego State University"])
