#!/usr/bin/env python3
"""
Query PubMed and generate HTML report in one command
"""

import argparse
import logging
import os
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle

from dfm_research_paper_digest import Author, Faculty, PubMedQuery, ReportGenerator


def query_and_report(
    author: Author,
    contact_email: str,
    faculty_list_file: str = None,
    log: logging.Logger = None,
    output_file: str = None,
    year: int = datetime.now().year,
) -> None:
    """
        Lets us generate report for one researcher.

    Parameters
    ----------
    author: Author
    contact_email: str
    faculty_list_file: str
    log: logging.Logger
    output_file: str
    year: int
    """

    # Query PubMed
    log.info("=" * 80)
    log.info(f"Querying PubMed for: {author.original}")
    if author.pubmed_style != author.original:
        log.info(f"PubMed search format: {author.pubmed_style}")
    log.info(f"Year: {year}")
    log.info("=" * 80)

    pubmed_query: PubMedQuery = PubMedQuery(log=log, email=contact_email)
    articles: list[PubMedArticle] = pubmed_query.query_by_author(
        author_name=author.pubmed_style, year=year
    )

    if not articles:
        log.info(f"\n❌ No publications found for '{author.original}' in {year}.")

        if author.pubmed_style != author.original:
            log.info(f"   (Searched PubMed as: {author.pubmed_style})")
        return

    log.info(f"\n✓ Found {len(articles)} publication(s)")

    # Generate HTML report
    if output_file:
        html_filename = (
            output_file if output_file.endswith(".html") else f"{output_file}.html"
        )
    else:
        # Auto-generate filename from author name
        html_filename = f"{author.slug}_{year}.html"

    faculty: Faculty = Faculty(faculty_list_file, log)
    generator: ReportGenerator = ReportGenerator(faculty, log)

    # Create title
    title: str = f"{author.original} Publications ({year})"

    generator.generate_html_report(
        publications=articles,
        output_file=html_filename,
        title=title,
    )

    log.info("✅ Report generated successfully!")
    log.info(f"📄 Open {html_filename} in your browser")


def main(argv=None):
    """
        Callable from command line.

    Parameters
    ----------
    argv

    Returns
    -------

    """
    parser = argparse.ArgumentParser(
        description="Query PubMed and generate HTML report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic query
  %(prog)s "Tai-Seale M"
  %(prog)s "Gene Kallenberg"          # Automatically converts to "Kallenberg G"
  %(prog)s "Kallenberg, Gene, MD"     # Also works with faculty list format
  
  # With options
  %(prog)s "Wu J" --year 2024
  %(prog)s "Ming Tai-Seale" --output ming_report
        """,
    )
    from dfm_research_paper_digest import Author, setup_logging

    resource_path_log = files("logs").joinpath("query_and_report.log")
    log: logging.Logger

    with as_file(resource_path_log) as log_filename:
        log = setup_logging(log_filename=log_filename)

    resource_path = files("data").joinpath("faculty_list.txt")

    parser.add_argument(
        "author",
        type=str,
        help='Author name to search (e.g., "Tai-Seale M", "Kallenberg G")',
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output HTML filename (default: auto-generated from author name)",
    )

    parser.add_argument(
        "--email",
        "-e",
        type=str,
        default=f"{os.getlogin()}@health.ucsd.edu",
        help="Your email (recommended by NCBI)",
    )

    with as_file(resource_path) as faculty_filename:
        parser.add_argument(
            "--faculty-file",
            "-f",
            type=str,
            default=faculty_filename,
            help="Faculty list file for highlighting (default: faculty_list.txt)",
        )

    args = parser.parse_args(argv)

    # Parse author name to PubMed format.
    author: Author = Author(args.author)

    query_and_report(
        author=author,
        contact_email=args.email,
        faculty_list_file=args.faculty_file,
        log=log,
        output_file=args.output,
        year=args.year,
    )


if __name__ == "__main__":
    main()
