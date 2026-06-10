#!/usr/bin/env python3
"""
PubMed Author Publications Query Tool
Queries PubMed for publications by a specific author from 2025.
"""
# pylint: disable=import-error, import-outside-toplevel
from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from importlib.resources import as_file, files

import metapub.ncbi_errors
import streamlit
import streamlit.errors
from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher

import src.dfm_research_paper_digest


class PubMedQuery:
    """
        Class to handle PubMed API queries.

    Attributes:
    ----------
    faculty: Faculty object
    email: str
    log: logging.Logger object

    Methods
    -------
    query_by_author()
    """

    UCSD_AFFILIATIONS: str = (
        '((University[ad] AND California[ad]) OR UC[ad]) AND "San Diego"[ad]'
    )

    def __init__(
        self,
        faculty: src.dfm_research_paper_digest.Faculty,
        email: str = None,
        log: logging.Logger = None,
    ):
        """
        Initialize PubMed query tool.

        Args:
            email: Your email (recommended by NCBI for API usage tracking)
        """
        from src.dfm_research_paper_digest import (
            setup_logging,
        )

        self.__log: logging.Logger

        if not log:
            resource_path = files("logs").joinpath("pubmed_query.log")

            with as_file(resource_path) as log_filename:
                self.__log = setup_logging(log_filename=log_filename)

        self.__log = log
        self.__faculty: src.dfm_research_paper_digest.Faculty = faculty

        self.__fetcher: PubMedFetcher
        self.__using_streamlit: bool = False

        # Are we running this under Streamlit or from the command line?
        try:
            self.__fetcher = PubMedFetcher(
                email=email, api_key=streamlit.secrets["api_key"]
            )
            self.__using_streamlit = True
        except streamlit.errors.StreamlitSecretNotFoundError:
            log.info("Did not find Streamlit Secret 'api_key'.")

            # Retrieve from environment variables.
            api_key: str = os.environ.get("NCBI_API_KEY")

            if api_key:
                log.info("Found API key in environment variable.")
                self.__fetcher = PubMedFetcher(email=email, api_key=api_key)
            else:
                log.info("Did not find API key in environment variable.")
                self.__fetcher = PubMedFetcher(email=email)

    def __fetch_publication_details(
        self, pmids: list[str], author_name: str
    ) -> list[PubMedArticle]:
        """
        Fetch publication details for given PMIDs.

        Args:
            pmids: list of PubMed IDs
            author_name: str

        Returns:
            list of PubMedArticle objects
        """
        articles: list[PubMedArticle] = []

        requested_author: src.dfm_research_paper_digest.Author = (
            src.dfm_research_paper_digest.Author(author_name)
        )

        for pmid in pmids:
            try:
                article: PubMedArticle = self.__fetcher.article_by_pmid(pmid)

                if article and len(article.author_list) > 0:
                    # Which PubMedAuthor object matches the author
                    # for whom we requested a list of publications?
                    if requested_author.matches(article.author_list):
                        matching_author: PubMedAuthor = next(
                            a
                            for a in article.author_list
                            if requested_author.matches(a)
                        )

                        if (
                            matching_author
                            and self.__faculty.is_faculty(matching_author)
                            and PubMedQuery.is_ucsd_affiliated(matching_author)
                        ):
                            articles.append(article)
            except metapub.ncbi_errors.NCBIServiceError as e:
                self.__log.error("NCBI Service Error: %s", e.user_message)

                if self.__using_streamlit:
                    streamlit.error(
                        f"**NCBI web service error: {e.user_message}", icon="🚨"
                    )

            # NCBI recommends max 3 requests per second
            time.sleep(0.33)

        return articles

    @staticmethod
    def is_ucsd_affiliated(var: list[str] | PubMedAuthor | str) -> bool:
        """
            Checks to see if affiliation is present
            AND looks like "UCSD" or "University of California San Diego"

        Args:
            var: list[str] or PubMedAuthor or str

        Returns
        -------
        affiliated_with_ucsd: bool
        """
        if isinstance(var, PubMedAuthor):
            return PubMedQuery.is_ucsd_affiliated(var.affiliations)

        affiliations: list[str] = []

        if isinstance(var, list):
            # If NO affliation, then we can't swear they're affiliated.
            if len(var) == 0:
                return False

            if not isinstance(var[0], str):
                raise TypeError(
                    f"Affiliations expected to be a list of str, not {type(var[0])}."
                )

            affiliations = var
        elif isinstance(var, str):
            affiliations = [var]
        else:
            raise TypeError(
                f"Expected either PubMedAuthor object, list[str] or str, but received {type(var)}."
            )

        ucsd_keywords: list[str] = [
            "UCSD",
            "University of California San Diego",
            "University of California, San Diego",
            "UC San Diego",
        ]

        return any(
            keyword in affil for affil in affiliations for keyword in ucsd_keywords
        )

    def query_by_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[PubMedArticle]:
        """
        Complete query for author publications.

        Args:
            author_name: Name of the author
            year: Publication year (default: 2025)

        Returns:
            list of PubMedArticle objects
        """
        self.__log.info(
            "Searching PubMed for publications by '%s' from %d ...", author_name, year
        )

        # Step 1: Search for PMIDs
        pmids: list[str] = self.__search_author_publications(author_name, year)

        if not pmids:
            self.__log.info("No publications found for '%s' in %d.", author_name, year)
            return []

        self.__log.info("Found %d publication(s).", len(pmids))

        # Step 2: Fetch publication details
        publications: list[PubMedArticle] = self.__fetch_publication_details(
            pmids, author_name
        )

        return publications

    def __search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[str]:
        """
        Search for publication IDs by author and year.

        Args:
            author_name: Name of the author (e.g., "Smith J" or "John Smith")
            year: Publication year (default: 2025)

        Returns:
            list of PubMed IDs (PMIDs)
        """
        # Construct search query
        search_term = (
            f"{author_name}[Author] AND {year}[pdat] AND "
            + PubMedQuery.UCSD_AFFILIATIONS
        )

        pmids: list[str] = []

        try:
            pmids = self.__fetcher.pmids_for_query(search_term)
        except metapub.ncbi_errors.NCBIServiceError as e:
            self.__log.error("NCBI Service Error: %s", e.user_message)

            if self.__using_streamlit:
                streamlit.error(
                    f"**NCBI web service error: {e.user_message}", icon="🚨"
                )

        return pmids


if __name__ == "__main__":
    pass
