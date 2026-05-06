#!/usr/bin/env python3
"""
Batch Faculty Publications Query
Queries PubMed for publications from multiple faculty members
"""
# pylint: disable=import-error, import-outside-toplevel
import argparse
import logging
import os
import sys
import time
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle


def query_faculty_batch(
    year=datetime.now().year,
    contact_email=None,
    output_file=None,
    faculty_list_file=None,
    log: logging.Logger = None,
):
    """
    Query PubMed for multiple faculty members and combine results.

    Args:
        contact_email: Optional email for NCBI API
        faculty_list_file: Path to faculty list file (for report generation)
        log: logging.Logger object (default: None, in which case we create our own)
        output_file: Optional CSV filename for output
        year: Publication year (default: current year)

    Returns:
        Dictionary with faculty names as keys and their publications as values
    """
    from dfm_research_paper_digest import (
        Faculty,
        PubMedQuery,
        ReportGenerator,
        setup_logging,
    )

    if not log:
        resource_path = files("logs").joinpath("query_faculty_batch.log")

        with as_file(resource_path) as log_filename:
            log = setup_logging(log_filename=log_filename)

    # Parse faculty names.
    faculty: Faculty = Faculty(faculty_list_file, log)

    log.info("=" * 80)
    log.info(f"Querying PubMed for {faculty.num} faculty members ({year})")
    log.info("=" * 80)

    # Initialize PubMed query
    query: PubMedQuery = PubMedQuery(email=contact_email, log=log)

    # Store results
    all_results: list = []
    faculty_results: dict = {}
    i: int = 0

    # Query each faculty member
    for author in faculty.authors:
        i += 1
        log.info(f"[{i}/{faculty.num}] Querying: {author.original}")

        try:
            articles: list[PubMedArticle] = query.query_by_author(
                author.pubmed_style, year=year
            )
            faculty_results[author.original] = articles
            all_results.extend(articles)
            log.info(f"    Found: {len(articles)} publication(s)")

        except Exception as e:
            log.exception(f"    Error: {e}")
            faculty_results[author.original] = []

        # Rate limiting: NCBI recommends max 3 requests per second
        if i < faculty.num:
            time.sleep(1.0)

    # Summary
    log.info("=" * 80)
    log.info("SUMMARY")
    log.info("=" * 80)
    log.info(f"Total faculty queried: {faculty.num}")
    log.info(f"Total publications found: {len(all_results)}")

    # Faculty with most publications
    if faculty_results:
        sorted_faculty = sorted(
            faculty_results.items(), key=lambda x: len(x[1]), reverse=True
        )
        log.info("Top 10 faculty by publication count:")

        for name, pubs in sorted_faculty[:10]:
            log.info(f"  {len(pubs):3} - {name}")

    # Generate HTML report if requested
    if all_results and faculty_list_file:
        html_filename = (
            output_file.replace(".csv", "")
            if output_file
            else "faculty_publications_report"
        )
        if html_filename.endswith(".csv"):
            html_filename = html_filename[:-4]
        html_filename += ".html"

        log.info(f"Generating HTML report: {html_filename}.")
        report_gen = ReportGenerator(faculty, log)

        report_gen.generate_html_report(
            publications=all_results,
            output_file=html_filename,
            title=f"DFM Faculty Publications Report ({year})",
        )

    return faculty_results


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
    from dfm_research_paper_digest import setup_logging

    resource_path_log = files("logs").joinpath("query_faculty_batch.log")
    log: logging.Logger

    with as_file(resource_path_log) as log_filename:
        log = setup_logging(log_filename=log_filename)

    resource_path = files("data").joinpath("faculty_list.txt")

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    parser.add_argument(
        "--email",
        "-e",
        type=str,
        default=f"{os.getlogin()}@health.ucsd.edu",
        help="Your email (recommended by NCBI)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="faculty_publications",
        help="Output CSV filename (default: faculty_publications)",
    )

    with as_file(resource_path) as faculty_filename:
        parser.add_argument(
            "--faculty-file",
            "-f",
            type=str,
            default=faculty_filename,
            help="Text file with faculty names (one per line)",
        )

    parser.add_argument(
        "--no-report", action="store_true", help="Skip HTML report generation"
    )

    args = parser.parse_args(argv)

    if not args.faculty_file:
        log.error("Error: No faculty names provided")
        sys.exit(1)

    # Query faculty
    query_faculty_batch(
        year=args.year,
        contact_email=args.email,
        output_file=args.output,
        faculty_list_file=args.faculty_file,
        log=log,
    )


if __name__ == "__main__":
    main()
