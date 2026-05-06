"""
Tests PubMedQuery class.
"""

from pathlib import Path

import pytest
from metapub import PubMedArticle

from dfm_research_paper_digest import PubMedQuery, display_publications
from dfm_research_paper_digest.pubmed_query import main


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

    display_publications(articles, logger)


def test_pubmed_query_main(username):
    main(
        [
            "Ming Tai-Seale",
            "Wael Al-Delaimy",
            "--email",
            f"{username}@health.ucsd.edu",
            "--year",
            "2026",
        ]
    )


def test_pubmed_query_main_no_articles(username):
    main(
        [
            "Nowhere Nothing",
            "--email",
            f"{username}@health.ucsd.edu",
            "--year",
            "3000",
        ]
    )


def test_pubmed_query_pathological(logger, username):
    pubmed_query: PubMedQuery = PubMedQuery(
        log=logger, email=f"{username}@health.ucsd.com"
    )
    assert isinstance(pubmed_query, PubMedQuery)

    # Try query that won't return any articles.
    articles = pubmed_query.query_by_author(author_name="Nowhere Nothing")
    assert isinstance(articles, list)
    assert len(articles) == 0


def test_instantiation_without_log(username):
    pubmed_query: PubMedQuery = PubMedQuery(email=f"{username}@health.ucsd.com")
    assert isinstance(pubmed_query, PubMedQuery)


def test_affiliation():
    assert PubMedQuery.is_ucsd_affiliated(["University of California, San Diego"])
    assert PubMedQuery.is_ucsd_affiliated(["UCSD San Diego", "University of San Diego"])
    assert not PubMedQuery.is_ucsd_affiliated(["San Diego State University"])

    # Exercise str input.
    assert PubMedQuery.is_ucsd_affiliated("University of California, San Diego")

    # Force exception.
    with pytest.raises(TypeError):
        PubMedQuery.is_ucsd_affiliated(1979)
