"""
Tests PubMedQuery class.
"""

from metapub import PubMedArticle

from src.dfm_research_paper_digest.pubmed_query import PubMedQuery


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
