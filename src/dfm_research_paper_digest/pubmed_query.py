#!/usr/bin/env python3
"""
PubMed Author Publications Query Tool
Queries PubMed for publications by a specific author from 2025.
"""
# pylint: disable=import-error, import-outside-toplevel
from __future__ import annotations

import argparse
import logging
import time
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher

import dfm_research_paper_digest


class PubMedQuery:
    """
        Class to handle PubMed API queries.

    Attributes:
    ----------
    email: str

    Methods
    -------
    query_by_author()
    """

    def __init__(self, email: str = None, log: logging.Logger = None):
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
        self.__fetch: PubMedFetcher = PubMedFetcher(email=email)

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

        requested_author: dfm_research_paper_digest.Author = (
            dfm_research_paper_digest.Author(author_name)
        )

        for pmid in pmids:
            article: PubMedArticle = self.__fetch.article_by_pmid(pmid)

            if article and len(article.author_list) > 0:
                # Which PubMedAuthor object matches the author
                # for whom we requested a list of publications?
                if requested_author.matches(article.author_list):
                    matching_author: PubMedAuthor = next(
                        a for a in article.author_list if requested_author.matches(a)
                    )

                    if matching_author and PubMedQuery.is_ucsd_affiliated(
                        matching_author
                    ):
                        articles.append(article)

            # NCBI recommends max 3 requests per second
            time.sleep(0.34)

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
            f"Searching PubMed for publications by '{author_name}' from {year}..."
        )

        # Step 1: Search for PMIDs
        pmids: list[str] = self.__search_author_publications(author_name, year)

        if not pmids:
            self.__log.info(f"No publications found for '{author_name}' in {year}.")
            return []

        self.__log.info(f"Found {len(pmids)} publication(s).")

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
        search_term = f"{author_name}[Author] AND {year}[pdat]"
        pmids: list[str] = self.__fetch.pmids_for_query(search_term)
        return pmids


def display_publications(
    publications: list[PubMedArticle], log: logging.Logger
) -> None:
    """
        Display publications in a formatted manner.

    Parameters
    ----------
    publications: list[Article]
    log: logging.Loggre object

    Returns
    -------

    """
    if not publications:
        log.info("\nNo publications to display.")
        return

    log.info(f"Found {len(publications)} publication(s):")

    for i, pub in enumerate(publications, 1):
        log.info(f"{i}. {pub.title}")
        log.info(f"   Authors: {pub.authors_str}")
        log.info(f"   Journal: {pub.journal}")
        log.info(f"   Year: {pub.year}")
        log.info(f"   PMID: {pub.pmid}")
        log.info(f"   URL: https://pubmed.ncbi.nlm.nih.gov/{pub.pmid}/")


def main(argv=None):
    """Main function to run the PubMed query tool."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Query PubMed for publications by a specific author from 2025.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Smith J"
  %(prog)s "Ming Tai-Seale" --email your@email.com
  %(prog)s "John Smith" --year 2024
  %(prog)s "Zhang Y" "Li Y" "Xie B"  # Query multiple authors
        """,
    )
    log = dfm_research_paper_digest.setup_logging(log_filename="pubmed_query.log")

    parser.add_argument(
        "authors",
        nargs="+",
        help='Author name(s) to search for (e.g., "Smith J", "John Smith", or "Ming Tai-Seale")',
    )

    parser.add_argument(
        "--email",
        "-e",
        type=str,
        help="Your email address (optional, recommended by NCBI for API tracking)",
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year to search (default: 2025)",
    )

    # Parse arguments
    args = parser.parse_args(argv)

    # Create query object
    query = PubMedQuery(email=args.email, log=log)

    # Process each author
    for author_name in args.authors:
        log.info("=" * 80)
        log.info("PubMed Author Publications Query Tool")
        log.info("=" * 80)

        # Query PubMed
        publications = query.query_by_author(author_name, year=args.year)

        # Display or collect results
        display_publications(publications, log)

        # Add delay between queries if multiple authors
        if len(args.authors) > 1 and author_name != args.authors[-1]:
            time.sleep(0.5)


if __name__ == "__main__":
    main()  # pragma: no cover
