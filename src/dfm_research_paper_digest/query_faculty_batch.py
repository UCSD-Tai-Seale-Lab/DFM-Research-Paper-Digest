#!/usr/bin/env python3
"""
Batch Faculty Publications Query
Queries PubMed for publications from multiple faculty members
"""
# pylint: disable=import-error, import-outside-toplevel
import argparse
import logging
import os
import time
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle

from dfm_research_paper_digest import (
    Faculty,
    PubMedQuery,
    ReportGenerator,
    setup_logging,
)


def query_faculty_batch(
    contact_email: str = None,
    faculty_list_file: str = None,
    log: logging.Logger = None,
    output_file: str = None,
    year: int = datetime.now().year,
):
    """
    Query PubMed for multiple faculty members and combine results.

    Args:
        contact_email: Optional email for NCBI API
        faculty_list_file: Path to faculty list file OR webpate (for report generation)
        log: logging.Logger object (default: None, in which case we create our own)
        output_file: Optional CSV filename for output
        year: Publication year (default: current year)

    Returns:
        Dictionary with faculty names as keys and their publications as values
    """
    if not log:
        resource_path = files("logs").joinpath("query_faculty_batch.log")

        with as_file(resource_path) as log_filename:
            log = setup_logging(log_filename=log_filename)

    # Parse faculty names.
    faculty: Faculty = Faculty(faculty_list_file, log)

    log.info(f"Querying PubMed for {faculty.num} faculty members ({year})")

    # Initialize PubMed query
    query: PubMedQuery = PubMedQuery(email=contact_email, log=log)

    # Store results
    all_results: list[PubMedArticle] = __assemble_article_list(
        query, faculty, year, log
    )

    # Generate HTML report.
    if output_file:
        html_filename: str = (
            output_file if output_file.endswith(".html") else f"{output_file}.html"
        )
    else:
        # Auto-generate filename.
        html_filename = f"faculty_{year}.html"

    log.info(f"Generating HTML report: {html_filename}.")
    report_gen: ReportGenerator = ReportGenerator(faculty, log)
    report_gen.generate_html_report(
        publications=all_results,
        output_file=html_filename,
        title=f"DFM Faculty Publications Report ({year})",
    )


def __assemble_article_list(
    query: PubMedQuery, faculty: Faculty, year: int, log: logging.Logger
) -> list[PubMedArticle]:
    """
        Runs query for each author & assembles list of articles.

    Parameters
    ----------
    query: PubMedQuery object
    faculty: Faculty object
    year: int
    log: logging.Logger

    Returns
    -------
    articles: list[PubMedArticle]
    """
    i: int = 0
    all_results: list[PubMedArticle] = []

    # Query each faculty member
    for author in faculty.authors:
        i += 1
        log.info(f"[{i}/{faculty.num}] Querying: {author.original}")

        try:
            articles: list[PubMedArticle] = query.query_by_author(
                author.pubmed_style, year=year
            )

            if articles and len(articles) > 0:
                all_results.extend(articles)
                log.info(f"    Found: {len(articles)} publication(s)")

        except Exception as e:
            log.exception(f"    Error: {e}")

        # Rate limiting: NCBI recommends max 3 requests per second
        if i < faculty.num:
            time.sleep(1.0)

    # Summary
    log.info("SUMMARY")
    log.info(f"Total faculty queried: {faculty.num}")
    log.info(f"Total publications found: {len(all_results)}")

    return __eliminate_duplicates(all_results)


def __eliminate_duplicates(articles: list[PubMedArticle]) -> list[PubMedArticle]:
    """
        Remove duplicate entries in article list.

    Parameters
    ----------
    articles: list[PubMedArticle]

    Returns
    -------
    unique_list: list[PubMedArticle]
    """
    seen: set = set()
    unique_list: list = []

    for obj in articles:
        if obj.pmid not in seen:
            unique_list.append(obj)
            seen.add(obj.pmid)

    return unique_list


def main(argv=None):
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Batch query PubMed for multiple faculty members",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query from a list
  %(prog)s --year 2025 --output faculty_pubs_2025

  # With email
  %(prog)s --email your@email.com --output results
        """,
    )
    resource_path_log = files("logs").joinpath("query_faculty_batch.log")
    log: logging.Logger

    with as_file(resource_path_log) as log_filename:
        log = setup_logging(log_filename=log_filename)

    parser.add_argument(
        "--email",
        "-e",
        type=str,
        default=f"{os.getlogin()}@health.ucsd.edu",
        help="Your email (recommended by NCBI)",
    )

    resource_path = files("data").joinpath("faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        parser.add_argument(
            "--faculty-file",
            "-f",
            type=str,
            default=faculty_filename,
            help="Text file with faculty names (one per line)",
        )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="faculty_publications.html",
        help="Output filename (default: faculty_publications.html)",
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    args = parser.parse_args(argv)

    # Query faculty
    query_faculty_batch(
        contact_email=args.email,
        faculty_list_file=args.faculty_file,
        log=log,
        output_file=args.output,
        year=args.year,
    )


if __name__ == "__main__":
    main()  # pragma: no cover
