"""
Tests PubMedQuery class.
"""

from src.dfm_research_paper_digest.pubmed_query import PubMedQuery
from src.dfm_research_paper_digest.publication import Article
import requests_mock


def test_author_publications(logger, fake_pmid_response, empty_pmid_response):
    pubmed_query: PubMedQuery = PubMedQuery(log=logger, email="notreal@email.com")
    assert isinstance(pubmed_query, PubMedQuery)

    # Need to mock TWO responses:
    # 1) first response giving three IDs for this author
    # 2) next response has zero IDs, prompting the loop to break out & return.
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            [
                {"text": fake_pmid_response, "status_code": 200},
                {"text": empty_pmid_response, "status_code": 200},
            ],
        )

        pubmed_ids: list[str] = pubmed_query.search_author_publications(
            author_name="Allison, Matthew A", year=2026
        )
        assert isinstance(pubmed_ids, list)
        assert len(pubmed_ids) == 3
        assert pubmed_ids[0] == "41651011"
        assert pubmed_ids[2] == "41351263"


def test_publication_details(
    logger, fake_pubmed_response_one_article, fake_pubmed_response_two_articles
):
    pubmed_query: PubMedQuery = PubMedQuery(log=logger, email="notreal@email.com")
    assert isinstance(pubmed_query, PubMedQuery)
    #
    #   ONE ARTICLE
    #
    # Need to mock TWO responses:
    # 1) first response giving info for this publication
    # 2) next response has zero articles, prompting the loop to break out & return.
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            [
                {"text": fake_pubmed_response_one_article, "status_code": 200},
                {"text": fake_pubmed_response_one_article, "status_code": 404},
            ],
        )

        pubs: list[Article] = pubmed_query.fetch_publication_details(pmids=["41960023"])
        assert isinstance(pubs, list)
        assert len(pubs) == 1
        assert isinstance(pubs[0], Article)
    #
    #   TWO ARTICLES
    #
    # Need to mock TWO responses:
    # 1) first response giving info for this publication
    # 2) next response has zero articles, prompting the loop to break out & return.
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            [
                {"text": fake_pubmed_response_two_articles, "status_code": 200},
                {"text": fake_pubmed_response_two_articles, "status_code": 404},
            ],
        )

        pubs: list[Article] = pubmed_query.fetch_publication_details(
            pmids=["41960023,41873419"]
        )
        assert isinstance(pubs, list)
        assert len(pubs) == 2
        assert isinstance(pubs[0], Article)
        assert isinstance(pubs[1], Article)
