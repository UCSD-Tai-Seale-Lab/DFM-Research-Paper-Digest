#!/usr/bin/env python3
"""
Example usage of the PubMed Query Tool.
Shows how to query multiple authors programmatically.
"""
import logging
from datetime import datetime

from my_logging import setup_logging
from publication import Article
from pubmed_query import PubMedQuery, display_publications


def query_multiple_authors(log: logging.Logger):
    """Example: Query publications for multiple authors."""

    # List of authors to query
    authors: list[str] = ["Zhang Y", "Li Y", "Xie B"]
    year: int = datetime.now().year

    # Initialize query object (optionally provide email)
    query: PubMedQuery = PubMedQuery(email="your.email@example.com", log=log)

    # Query each author
    for author in authors:
        log.info(f"\n{'='*80}")
        log.info(f"Querying author: {author}")
        log.info(f"{'='*80}")

        publications: list[Article] = query.query_author(author, year=year)
        display_publications(publications, log)


def query_single_author_custom(log: logging.Logger):
    """Example: Query a single author with custom display."""

    author_name: str = "Smith J"

    query: PubMedQuery = PubMedQuery(log=log)
    publications: list[Article] = query.query_author(author_name, year=2025)
    year: int = datetime.now().year

    # Custom display
    if publications:
        log.info(f"\nPublications by {author_name} in {year}:")

        for pub in publications:
            log.info(f"  - {pub.year}: {pub.title}")
    else:
        log.info(f"No publications found for {author_name} in {year}")


def export_to_csv(log: logging.Logger):
    """Example: Export results to CSV format."""
    import csv

    author_name: str = "Zhang Y"

    query: PubMedQuery = PubMedQuery(log=log)
    publications: list[Article] = query.query_author(
        author_name, year=datetime.now().year
    )

    if publications:
        # Export to CSV
        filename = f"{author_name.replace(' ', '_')}_publications_2025.csv"

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "authors", "journal", "year", "pmid"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # Convert list of Article objects to a dictionary with the desired keys.
            publication_list: list = []

            for article in publications:
                new_article_dict: dict = {
                    k: v for k, v in article.__dict__ if k in fieldnames
                }
                publication_list.append(new_article_dict)

            writer.writerows(publication_list)

        log.info(f"\nExported {len(publications)} publications to {filename}")
    else:
        log.info(f"No publications found for {author_name} in 2025")


if __name__ == "__main__":

    log: logging.Logger = setup_logging("example_usage.log")

    # Run the examples
    log.info("Example 1: Query multiple authors")
    query_multiple_authors(log)

    log.info("\n\n" + "=" * 80)
    log.info("Example 2: Query single author with custom display")
    log.info("=" * 80)
    query_single_author_custom(log)

    log.info("\n\n" + "=" * 80)
    log.info("Example 3: Export to CSV")
    log.info("=" * 80)
    export_to_csv(log)
