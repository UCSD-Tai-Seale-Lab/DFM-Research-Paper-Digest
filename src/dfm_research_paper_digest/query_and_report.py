#!/usr/bin/env python3
"""
Query PubMed and generate HTML report in one command
"""
# pylint: disable=import-error, import-outside-toplevel
import argparse
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from importlib.resources import as_file, files

from metapub import PubMedArticle

from dfm_research_paper_digest import (
    Author,
    Faculty,
    PubMedQuery,
    ReportGenerator,
    setup_logging,
)


@dataclass
class DataRequestDetails:
    """
    Package for encapsulating request for PubMedQuery
    """

    author: Author
    faculty_file: str
    year: int = datetime.now().year

    def __init__(
        self, author: Author, faculty_file: str, year: int = datetime.now().year
    ):
        self.author = author
        self.faculty_file = faculty_file
        self.year = year


def query_and_report(
    contact_email: str = None,
    log: logging.Logger = None,
    output_file: str = None,
    data_request: DataRequestDetails = None,
) -> None:
    """
        Lets us generate report for one researcher.

    Parameters
    ----------
    contact_email: str
    log: logging.Logger
    output_file: str
    data_request: DataRequestDetails
        .author: Author
        .faculty_file: str
        ,year: int
    """

    if not log:
        resource_path = files("logs").joinpath("query_and_report.log")

        with as_file(resource_path) as log_filename:
            log = setup_logging(log_filename=log_filename)

    author: Author = data_request.author

    # Query PubMed
    log.info(f"Querying PubMed for: {author.original}")
    if author.pubmed_style != author.original:
        log.info(f"PubMed search format: {author.pubmed_style}")
    log.info(f"Year: {data_request.year}")

    pubmed_query: PubMedQuery = PubMedQuery(log=log, email=contact_email)
    articles: list[PubMedArticle] = pubmed_query.query_by_author(
        author_name=author.pubmed_style, year=data_request.year
    )

    if not articles:
        log.info(
            "\n❌ No publications found for "
            f"'{author.original}' in {data_request.year}."
        )

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
        html_filename = f"{author.slug}_{data_request.year}.html"

    faculty: Faculty = Faculty(data_request.faculty_file, log)
    generator: ReportGenerator = ReportGenerator(faculty, log)

    # Create title
    title: str = f"{author.original} Publications ({data_request.year})"

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

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output HTML filename (default: auto-generated from author name)",
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    args = parser.parse_args(argv)

    # Parse author name to PubMed format.
    author: Author = Author(args.author)
    data_request: DataRequestDetails = DataRequestDetails(
        author, args.faculty_file, args.year
    )
    query_and_report(
        contact_email=args.email,
        log=log,
        output_file=args.output,
        data_request=data_request,
    )


if __name__ == "__main__":
    print("Hello from `query_and_report.py`")  # pragma: no cover
