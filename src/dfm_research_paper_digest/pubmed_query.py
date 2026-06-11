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

        if log:
            self.__log = log
        else:
            resource_path = files("logs").joinpath("pubmed_query.log")

            with as_file(resource_path) as log_filename:
                self.__log = setup_logging(log_filename=log_filename)

        self.__log.info("Instantiating PubMedQuery object.")
        self.__faculty: src.dfm_research_paper_digest.Faculty = faculty
        self.__fetcher: PubMedFetcher
        self.__using_streamlit: bool = False

        api_key: str

        # Are we running this under Streamlit or from the command line?
        try:
            api_key = streamlit.secrets["api_key"]
            self.__fetcher = PubMedFetcher(email=email, api_key=api_key)
            self.__using_streamlit = True
            self.__log.info("Found API key in Streamlit secrets.")
        except streamlit.errors.StreamlitSecretNotFoundError:
            self.__log.info("Did not find Streamlit Secret 'api_key'.")

            # Retrieve from environment variables.
            api_key = os.environ.get("NCBI_API_KEY")

            if api_key:
                self.__log.info("Found API key in environment variable.")
                self.__fetcher = PubMedFetcher(email=email, api_key=api_key)
            else:
                self.__log.info("Did not find API key in environment variable.")
                self.__fetcher = PubMedFetcher(email=email)

    def __fetch_publication_details(
        self, pmids: list[str], requested_author: src.dfm_research_paper_digest.Author
    ) -> list[PubMedArticle]:
        """
        Fetch publication details for given PMIDs.

        Args:
            pmids: list of PubMed IDs
            requested_author: Author object

        Returns:
            list of PubMedArticle objects
        """
        articles: list[PubMedArticle] = []

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

                        if matching_author:
                            self.__log.debug(
                                f"Matching author is {str(matching_author)}."
                            )

                            if self.__faculty.is_faculty(matching_author):
                                self.__log.debug(f"{str(matching_author)} is faculty.")

                                if PubMedQuery.is_ucsd_affiliated(matching_author):
                                    self.__log.debug(
                                        f"{str(matching_author)} is UCSD affiliated."
                                    )
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
            AND NOT like "Emergency Medicine" or "Mechanical Engineering"

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
            # If NO affiliation, then we can't swear they're affiliated.
            if len(var) == 0:
                return False

            if not isinstance(var[0], str):
                raise TypeError(
                    "Affiliations expected to be a list of str, not %s.", type(var[0])
                )

            affiliations = var
        elif isinstance(var, str):
            affiliations = [var]
        else:
            raise TypeError(
                "Expected either PubMedAuthor object, list[str] or str, but received %s.",
                type(var),
            )

        ucsd_keywords: list[str] = [
            "UCSD",
            "University of California San Diego",
            "University of California, San Diego",
            "UC San Diego",
        ]

        distraction_keywords: list[str] = [
            "Emergency Medicine",
            "Mechanical Engineering",
        ]

        return any(
            keyword in affil for affil in affiliations for keyword in ucsd_keywords
        ) and not any(
            keyword in affil
            for affil in affiliations
            for keyword in distraction_keywords
        )

    def query_by_author(
        self,
        author: src.dfm_research_paper_digest.Author,
        year: int = datetime.now().year,
    ) -> list[PubMedArticle]:
        """
        Complete query for author publications.

        Args:
            author: Author object
            year: Publication year (default: current year)

        Returns:
            list of PubMedArticle objects
        """
        self.__log.info(
            "Searching PubMed for publications by '%s' from %d ...",
            author.original,
            year,
        )

        # Step 1: Search for PMIDs
        pmids: list[str] = self.__search_author_publications(author, year)

        if not pmids:
            self.__log.info(
                "No publications found for '%s' in %d.", author.original, year
            )
            return []

        self.__log.info("Found %d publication(s).", len(pmids))

        # Step 2: Fetch publication details
        publications: list[PubMedArticle] = self.__fetch_publication_details(
            pmids, author
        )

        return publications

    def __search_author_publications(
        self,
        author: src.dfm_research_paper_digest.Author,
        year: int = datetime.now().year,
    ) -> list[str]:
        """
        Search for publication IDs by author, year and UCSD affiliation.

        Args:
            author_name: Name of the author (e.g., "Smith J" or "John Smith")
            year: Publication year (default: current year)

        Returns:
            list of PubMed IDs (PMIDs)
        """
        # Construct search query
        search_term = (
            f"{author.pubmed_style}[Author] AND {year}[pdat] AND "
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
