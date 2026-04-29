#!/usr/bin/env python3
"""
Query PubMed and generate HTML report in one command
"""

import argparse
import getpass
import logging
from datetime import datetime
from importlib.resources import as_file, files

from author import Author
from email_sender import EmailSender
from faculty import Faculty
from my_logging import setup_logging
from publication import Article
from pubmed_query import PubMedQuery
from report_generator import ReportGenerator


def main(argv=None):
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
  
  # Send via email (text summary in body)
  %(prog)s "Gene Kallenberg" --send-email --email-to recipient@email.com --email-from your@gmail.com
  
  # Send with HTML attachment
  %(prog)s "Ming Tai-Seale" --send-email --email-to recipient@email.com --email-from your@gmail.com --email-format html
        """,
    )

    log: logging.Logger = setup_logging(log_filename="query_and_report.log")
    resource_path = files("data").joinpath("faculty_list.txt")

    parser.add_argument(
        "author", help='Author name to search (e.g., "Tai-Seale M", "Kallenberg G")'
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: current year)",
    )

    parser.add_argument(
        "--email", "-e", type=str, help="Your email (optional, recommended by NCBI)"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output HTML filename (default: auto-generated from author name)",
    )

    with as_file(resource_path) as faculty_filename:
        parser.add_argument(
            "--faculty-file",
            "-f",
            type=str,
            default=faculty_filename,
            help="Faculty list file for highlighting (default: faculty_list.txt)",
        )

    # Email options
    parser.add_argument(
        "--send-email", action="store_true", help="Send report via email"
    )

    parser.add_argument("--email-to", type=str, help="Recipient email address")

    parser.add_argument("--email-from", type=str, help="Your email address")

    parser.add_argument(
        "--email-format",
        choices=["text", "html"],
        default="text",
        help="Email format: text (summary in body) or html (attached report) - default: text",
    )

    parser.add_argument(
        "--email-provider",
        choices=["gmail", "outlook", "yahoo", "ucsd"],
        default="gmail",
        help="Email provider (default: gmail)",
    )

    args = parser.parse_args()

    # Parse author name to PubMed format.
    author: Author = Author(args.author)

    # Query PubMed
    log.info("=" * 80)
    log.info(f"Querying PubMed for: {author.original}")
    if author.pubmed_style != author.original:
        log.info(f"PubMed search format: {author.pubmed_style}")
    log.info(f"Year: {args.year}")
    log.info("=" * 80)

    query: PubMedQuery = PubMedQuery(email=args.email, log=log)
    publications: list[Article] = query.query_author(
        author.pubmed_style, year=args.year
    )

    if not publications:
        log.info(f"\n❌ No publications found for '{author.original}' in {args.year}.")
        if author.pubmed_style != author.original:
            log.info(f"   (Searched PubMed as: {author.pubmed_style})")
        return

    log.info(f"\n✓ Found {len(publications)} publication(s)")

    # Generate HTML report
    if args.output:
        html_filename = (
            args.output if args.output.endswith(".html") else f"{args.output}.html"
        )
    else:
        # Auto-generate filename from author name
        html_filename = f"{author.slug}_{args.year}.html"

    faculty: Faculty = Faculty(args.faculty_file, log)
    generator: ReportGenerator = ReportGenerator(faculty, log)

    # Create title
    title: str = f"{author.original} Publications ({args.year})"

    # Count DFM faculty
    faculty_count = len(
        set(
            author
            for pub in publications
            for author in pub.authors_list
            if faculty.is_faculty(author)
        )
    )

    generator.generate_html_report(
        publications=publications,
        output_file=html_filename,
        title=title,
    )

    log.info(f"✅ Report generated successfully!")
    log.info(f"📄 Open {html_filename} in your browser")

    # Send email if requested
    if args.send_email:
        if not args.email_to or not args.email_from:
            log.error(
                "❌ Error: --email-to and --email-from are required when using --send-email"
            )
            return

        log.info("\n" + "=" * 80)
        log.info("Sending email...")
        log.info("=" * 80)

        # Get password securely
        password: str = getpass.getpass(f"Enter password for {args.email_from}: ")

        sender: EmailSender = EmailSender(provider=args.email_provider, log=log)

        try:
            if args.email_format == "html":
                sender.send_html_report(
                    html_file=html_filename,
                    to_email=args.email_to,
                    from_email=args.email_from,
                    password=password,
                    author_name=author.original,
                    year=args.year,
                )
            else:  # text
                sender.send_text_summary(
                    publications=publications,
                    to_email=args.email_to,
                    from_email=args.email_from,
                    password=password,
                    author_name=author.original,
                    year=args.year,
                    faculty_count=faculty_count,
                )
        except Exception as e:
            log.exception(f"❌ Error sending email: {e}")


if __name__ == "__main__":
    main()
