#!/usr/bin/env python3
"""
PubMed Author Publications Query Tool
Queries PubMed for publications by a specific author from 2025.
"""

import argparse
import logging
import time
from datetime import datetime
from typing import Dict, List

import requests
import xmltodict
from my_logging import setup_logging
from publication import PMID, Article, PubmedArticleSet


class PubMedQuery:
    """
        Class to handle PubMed API queries.

    Attributes:
    ----------
    email: str

    Methods
    -------
    fetch_publication_details()
    search_author_publications()
    """

    BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    CHUNK_SIZE: int = 100

    def __init__(self, email: str = None, log: logging.Logger = None):
        """
        Initialize PubMed query tool.

        Args:
            email: Your email (recommended by NCBI for API usage tracking)
        """
        self.email: str = email
        self.__log: logging.Logger

        if log:
            self.__log = log
        else:
            self.__log = setup_logging(log_filename="pubmed_query.py")

    def search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> List[str]:
        """
        Search for publication IDs by author and year.

        Args:
            author_name: Name of the author (e.g., "Smith J" or "John Smith")
            year: Publication year (default: 2025)

        Returns:
            List of PubMed IDs (PMIDs)
        """
        # Construct search query
        search_term = f"{author_name}[Author] AND {year}[pdat]"

        # Initialize search parameters
        params = {
            "db": "pubmed",
            "term": search_term,
            "retmax": PubMedQuery.CHUNK_SIZE,  # Maximum number of results
            "retstart": 1,  # Starting index
            "retmode": "xml",
        }

        if self.email:
            params["email"] = self.email

        url = f"{self.BASE_URL}esearch.fcgi"
        pmids: List[str] = []
        num_pubs_retrieved: int = 0

        # Request publications in chunks.
        while True:
            params["retstart"] = num_pubs_retrieved + 1

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data_dict: dict = xmltodict.parse(response.content)
                new_pmids: list[str] = PMID(data_dict, self.__log).pmids

                # Did we get them all?
                if len(new_pmids) == 0:
                    break

                num_pubs_retrieved += len(new_pmids)
                pmids.extend(new_pmids)

            except requests.exceptions.RequestException as e:
                self.__log.error(f"Error searching PubMed: {e}")
                break

        return pmids

    def fetch_publication_details(self, pmids: List[str]) -> List[Article]:
        """
        Fetch publication details for given PMIDs.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of Article objects
        """
        publications: List[Article] = []

        if not pmids:
            return publications

        # Initialize parameters.
        params = {"db": "pubmed", "id": [], "retmode": "xml"}

        if self.email:
            params["email"] = self.email

        url = f"{self.BASE_URL}efetch.fcgi"

        # Make the request in chunks.
        num_pubs_total: int = len(pmids)
        num_pubs_received_so_far: int = 0

        while True:
            # Establish start/stop indices for this slice.
            index_start: int = num_pubs_received_so_far  # zero-based
            index_end: int = min(num_pubs_total, index_start + PubMedQuery.CHUNK_SIZE)

            # Join PMIDs with comma
            id_string = ",".join(pmids[index_start:index_end])
            params["id"] = id_string

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()

                data_dict: dict = xmltodict.parse(response.content)
                pubmed_articleset: PubmedArticleSet = PubmedArticleSet(data_dict)
                articles: list[Article] = pubmed_articleset.articles

                for article in articles:
                    publications.append(article)
                    num_pubs_received_so_far += 1

            except requests.exceptions.RequestException as e:
                self.__log.exception(f"Error fetching publication details: {e}")
                break

        return publications

    def query_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> List[Article]:
        """
        Complete query for author publications.

        Args:
            author_name: Name of the author
            year: Publication year (default: 2025)

        Returns:
            List of Article objects
        """
        self.__log.info(
            f"\nSearching PubMed for publications by '{author_name}' from {year}..."
        )

        # Step 1: Search for PMIDs
        pmids = self.search_author_publications(author_name, year)

        if not pmids:
            self.__log.info(f"No publications found for '{author_name}' in {year}.")
            return []

        self.__log.info(f"Found {len(pmids)} publication(s).")

        # Step 2: Fetch publication details
        # NCBI recommends max 3 requests per second
        time.sleep(0.34)

        publications = self.fetch_publication_details(pmids)

        return publications


def display_publications(publications: list[Article], log: logging.Logger) -> None:
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
        log.info(f"   Authors: {pub.authors_list}")
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
    log = setup_logging(log_filename="pubmed_query.log")

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
        log.info(f"PubMed Author Publications Query Tool")
        log.info("=" * 80)

        # Query PubMed
        publications = query.query_author(author_name, year=args.year)

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
    publications: List[Article], filename: str, log: logging.Logger
) -> None:
    """
        Export publications to CSV file.

    Parameters
    ----------
    publications: List[Article]
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
