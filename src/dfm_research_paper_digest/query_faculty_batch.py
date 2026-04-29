#!/usr/bin/env python3
"""
Batch Faculty Publications Query
Queries PubMed for publications from multiple faculty members
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from importlib.resources import as_file, files

from faculty import Faculty
from my_logging import setup_logging
from publication import Article
from pubmed_query import PubMedQuery
from report_generator import ReportGenerator


def export_to_csv_with_faculty(publications, filename, log: logging.Logger):
    """Export publications with faculty information to CSV."""
    import csv

    if not publications:
        log.info("No publications to export.")
        return

    try:
        # Add URL field and prepare data for CSV
        for pub in publications:
            if "url" not in pub:
                pub["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/"

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            # Don't include authors_list in CSV (it's for HTML report only)
            fieldnames = [
                "faculty_name",
                "faculty_lastname",
                "faculty_firstname",
                "title",
                "authors",
                "journal",
                "year",
                "date",
                "pmid",
                "url",
            ]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, extrasaction="ignore"
            )

            writer.writeheader()
            writer.writerows(publications)

        log.info(f"✓ Successfully exported {len(publications)} publication(s) to CSV")
    except Exception as e:
        log.info(f"Error exporting to CSV: {e}")


def query_faculty_batch(
    year=datetime.now().year,
    email=None,
    output_file=None,
    faculty_list_file=None,
    generate_report=True,
    log: logging.Logger = None,
):
    """
    Query PubMed for multiple faculty members and combine results.

    Args:
        faculty_list: List of faculty names in format "Lastname, Firstname, Qualification"
        year: Publication year (default: 2025)
        email: Optional email for NCBI API
        output_file: Optional CSV filename for output
        faculty_list_file: Path to faculty list file (for report generation)
        generate_report: Whether to generate HTML report (default: True)
        log: logging.Logger object (default: None, in which case we create our own)

    Returns:
        Dictionary with faculty names as keys and their publications as values
    """
    if not log:
        log = setup_logging(log_filename="query_faculty_batch.log")

    # Parse faculty names.
    faculty: Faculty = Faculty(faculty_list_file, log)

    log.info("=" * 80)
    log.info(f"Querying PubMed for {faculty.num} faculty members ({year})")
    log.info("=" * 80)

    # Initialize PubMed query
    query: PubMedQuery = PubMedQuery(email=email, log=log)

    # Store results
    all_results: list = []
    faculty_results: dict = {}
    i: int = 0

    # Query each faculty member
    for author in faculty.authors:
        i += 1
        log.info(f"[{i}/{faculty.num}] Querying: {author.original}")

        try:
            articles: list[Article] = query.query_author(author.pubmed_style, year=year)
            matching_articles: list[Article] = []

            # Only include articles in which a faculty member is an author.
            for article in articles:
                if author.matches(article.authors_list):
                    matching_articles.append(article)

            faculty_results[author.original] = matching_articles
            all_results.extend(matching_articles)

            log.info(f"    Found: {len(matching_articles)} publication(s)")

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

    # Export to CSV if requested
    if output_file and all_results:
        csv_filename: str = ""

        if not output_file.endswith(".csv"):
            csv_filename = output_file + ".csv"
        else:
            csv_filename = output_file

        log.info(f"Exporting to CSV: {csv_filename}")
        export_to_csv_with_faculty(all_results, csv_filename, log)

    # Generate HTML report if requested
    if generate_report and all_results and faculty_list_file:
        html_filename = (
            output_file.replace(".csv", "")
            if output_file
            else "faculty_publications_report"
        )
        if html_filename.endswith(".csv"):
            html_filename = html_filename[:-4]
        html_filename += ".html"

        log.info(f"Generating HTML report: {html_filename}.")
        report_gen = ReportGenerator(faculty)

        report_gen.generate_html_report(
            publications=all_results,
            output_file=html_filename,
            title=f"DFM Faculty Publications Report ({year})",
        )

    return faculty_results


def main():
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

    log: logging.Logger = setup_logging(log_filename="query_faculty_batch.log")
    resource_path = files("data").joinpath("faculty_list.txt")

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    parser.add_argument(
        "--email", "-e", type=str, help="Your email (recommended by NCBI)"
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

    args = parser.parse_args()

    if not args.faculty_file:
        log.error("Error: No faculty names provided")
        sys.exit(1)

    # Query faculty
    query_faculty_batch(
        year=args.year,
        email=args.email,
        output_file=args.output,
        faculty_list_file=args.faculty_file,
        generate_report=not args.no_report,
        log=log,
    )


if __name__ == "__main__":
    main()
