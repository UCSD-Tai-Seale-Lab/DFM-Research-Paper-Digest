"""
Tests PubMedQuery class.
"""

from importlib.resources import as_file, files

import pytest
from metapub import PubMedArticle

from dfm_research_paper_digest import Faculty, PubMedQuery, display_publications


def test_pubmed_query(logger, username):
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        faculty: Faculty = Faculty(str(faculty_filename), logger)
        assert isinstance(faculty, Faculty)
        pubmed_query: PubMedQuery = PubMedQuery(
            faculty=faculty, log=logger, email=f"{username}@health.ucsd.com"
        )
        assert isinstance(pubmed_query, PubMedQuery)
        articles: list[PubMedArticle] = pubmed_query.query_by_author(
            author_name="Ming Tai-Seale", year=2025
        )
    assert isinstance(articles, list)
    first_article: PubMedArticle = articles[0]
    assert isinstance(first_article, PubMedArticle)

    display_publications(articles, logger)


def test_pubmed_query_pathological(logger, username):
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        faculty: Faculty = Faculty(str(faculty_filename), logger)
        assert isinstance(faculty, Faculty)
        pubmed_query: PubMedQuery = PubMedQuery(
            faculty=faculty, log=logger, email=f"{username}@health.ucsd.com"
        )
        assert isinstance(pubmed_query, PubMedQuery)

        # Try query that won't return any articles.
        articles = pubmed_query.query_by_author(author_name="Nowhere Nothing")
        assert isinstance(articles, list)
        assert len(articles) == 0


def test_instantiation_without_log(username, logger):
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        faculty: Faculty = Faculty(str(faculty_filename), logger)
        assert isinstance(faculty, Faculty)
        pubmed_query: PubMedQuery = PubMedQuery(faculty=faculty, email=f"{username}@health.ucsd.com")
        assert isinstance(pubmed_query, PubMedQuery)


def test_affiliation():
    assert PubMedQuery.is_ucsd_affiliated(["University of California, San Diego"])
    assert PubMedQuery.is_ucsd_affiliated(["UCSD San Diego", "University of San Diego"])
    assert not PubMedQuery.is_ucsd_affiliated(["San Diego State University"])

    # Exercise str input.
    assert PubMedQuery.is_ucsd_affiliated("University of California, San Diego")

    # Force exceptions.
    with pytest.raises(TypeError):
        PubMedQuery.is_ucsd_affiliated(1979)

    with pytest.raises(TypeError):
        PubMedQuery.is_ucsd_affiliated([1979])
