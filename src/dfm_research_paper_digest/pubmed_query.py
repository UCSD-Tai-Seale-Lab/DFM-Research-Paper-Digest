#!/usr/bin/env python3
"""
PubMed Author Publications Query Tool
Queries PubMed for publications by a specific author from 2025.
"""
from __future__ import annotations

import argparse
import logging
import time
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher

import dfm_research_paper_digest  # pyline: disable=import-error


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
        from dfm_research_paper_digest import (
            setup_logging,  # pylint: disable=import-error
        )

        self.__log: logging.Logger

        if not log:
            resource_path = files("logs").joinpath("pubmed_query.py")

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

        if not pmids:
            return articles

        requested_author: dfm_research_paper_digest.Author = (
            dfm_research_paper_digest.Author(author_name)
        )

        for pmid in pmids:
            article: PubMedArticle = self.__fetch.article_by_pmid(pmid)
            # NCBI recommends max 3 requests per second
            time.sleep(0.34)

            # Which PubMedAuthor object matches the author
            # for whom we requested a list of publications?
            matching_author: PubMedAuthor = next(
                a for a in article.author_list if requested_author.matches(a)
            )

            if matching_author and PubMedQuery.is_ucsd_affiliated(matching_author):
                articles.append(article)

        return articles

    @staticmethod
    def is_ucsd_affiliated(var: list[str] | PubMedAuthor) -> bool:
        """
            Checks to see if affiliation is present
            AND looks like "UCSD" or "University of California San Diego"

        Args:
            var: list[str] or PubMedAuthor

        Returns
        -------
        affiliated_with_ucsd: bool
        """
        affiliations: list[str]

        if isinstance(var, PubMedAuthor):
            affiliations = var.affiliations
        elif isinstance(var, list) and isinstance(var[0], str):
            affiliations = var
        else:
            raise TypeError(
                f"Expected either PubMedAuthor object or list[str], but received {type(var)}."
            )

        if any("UCSD" in affil for affil in affiliations):
            return True

        if any("University of California San Diego" in affil for affil in affiliations):
            return True

        if any(
            "University of California, San Diego" in affil for affil in affiliations
        ):
            return True

        if any("UC San Diego" in affil for affil in affiliations):
            return True

        return False

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
            f"\nSearching PubMed for publications by '{author_name}' from {year}..."
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

    log.info(f"\n{'='*80}")
    log.info(f"Found {len(publications)} publication(s):")
    log.info(f"{'='*80}\n")

    for i, pub in enumerate(publications, 1):
        log.info(f"{i}. {pub.title}")
        log.info(f"   Authors: {pub.authors_str}")
        log.info(f"   Journal: {pub.journal}")
        log.info(f"   Year: {pub.year}")
        log.info(f"   PMID: {pub.pmid}")
        log.info(f"   URL: https://pubmed.ncbi.nlm.nih.gov/{pub.pmid}/")


def main():
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

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        choices=["text", "csv"],
        default="text",
        help="Output format: text or csv (default: text)",
    )

    parser.add_argument(
        "--filename",
        "-f",
        type=str,
        help="Custom output filename for CSV (only used with --output csv)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Create query object
    query = PubMedQuery(email=args.email, log=log)

    # Process each author
    all_results = []

    for author_name in args.authors:
        log.info("=" * 80)
        log.info("PubMed Author Publications Query Tool")
        log.info("=" * 80)

        # Query PubMed
        publications = query.query_by_author(author_name, year=args.year)

        # Display or collect results
        if args.output == "text":
            display_publications(publications, log)
        else:
            all_results.extend(publications)
            log.info(
                f"Retrieved {len(publications)} publication(s) for '{author_name}'"
            )

        # Add delay between queries if multiple authors
        if len(args.authors) > 1 and author_name != args.authors[-1]:
            time.sleep(0.5)

    # Export to CSV if requested
    if args.output == "csv":
        if all_results:
            # Use custom filename or create one based on author(s)
            if args.filename:
                filename = (
                    args.filename
                    if args.filename.endswith(".csv")
                    else f"{args.filename}.csv"
                )
            elif len(args.authors) == 1:
                author_slug = args.authors[0].replace(" ", "_").replace(",", "")
                filename = f"{author_slug}_{args.year}.csv"
            else:
                filename = f"multiple_authors_{args.year}.csv"
            export_to_csv(all_results, filename, log)
        else:
            log.info("\nNo publications found to export.")


def export_to_csv(
    publications: list[PubMedArticle], filename: str, log: logging.Logger
) -> None:
    """
        Export publications to CSV file.

    Parameters
    ----------
    publications: list[Article]
    filename: str
    log: logging.Logger

    Returns
    -------

    """
    import csv

    if not publications:
        log.info("No publications to export.")
        return

    try:
        # Add URL field to each publication
        for pub in publications:
            if not hasattr(pub, "url"):
                pub.url = f"https://pubmed.ncbi.nlm.nih.gov/{pub.pmid}/"

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "authors", "journal", "year", "date", "pmid", "url"]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, extrasaction="ignore"
            )

            writer.writeheader()

            for publication in publications:
                writer.writerow(vars(publication))

        log.info(f"\n{'='*80}")
        log.info(
            f"✓ Successfully exported {len(publications)} publication(s) to: {filename}"
        )
        log.info(f"{'='*80}")
    except Exception as e:
        log.exception(f"Error exporting to CSV: {e}")


if __name__ == "__main__":
    main()
