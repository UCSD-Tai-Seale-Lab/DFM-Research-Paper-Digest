#!/usr/bin/env python3
"""
Query PubMed and generate HTML report in one command
"""

import argparse
import getpass
from datetime import datetime

from email_sender import EmailSender
from faculty_parser import FacultyNameParser
from pubmed_query import PubMedQuery
from report_generator import ReportGenerator


def parse_author_name(author_string):
    """
    Parse author name and convert to PubMed search format.
    Handles: "Gene Kallenberg" or "Kallenberg G" or "Kallenberg, Gene, MD"
    """
    author_string = author_string.strip()

    # If it already looks like PubMed format (LastName Initial), use as-is
    parts = author_string.split()
    if len(parts) == 2 and len(parts[1]) <= 2 and parts[1][0].isupper():
        # Looks like "Kallenberg G" - use as-is
        return author_string, author_string

    # If it has commas, parse as faculty format
    if "," in author_string:
        parser = FacultyNameParser()
        try:
            parsed = parser.parse_faculty_name(author_string)
            return parsed["pubmed_format"], parsed["original"]
        except:
            return author_string, author_string

    # If it's "FirstName LastName", convert to "LastName F"
    if len(parts) >= 2:
        firstname = parts[0]
        lastname = " ".join(parts[1:])
        pubmed_format = f"{lastname} {firstname[0]}"
        return pubmed_format, author_string

    # Single word - use as-is
    return author_string, author_string


def main():
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

    parser.add_argument(
        "author", help='Author name to search (e.g., "Tai-Seale M", "Kallenberg G")'
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        help="Publication year (default: 2025)",
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

    parser.add_argument(
        "--faculty-file",
        "-f",
        type=str,
        default="faculty_list.txt",
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

    # Parse author name to PubMed format
    pubmed_name, original_name = parse_author_name(args.author)

    # Query PubMed
    print("=" * 80)
    print(f"Querying PubMed for: {original_name}")
    if pubmed_name != original_name:
        print(f"PubMed search format: {pubmed_name}")
    print(f"Year: {args.year}")
    print("=" * 80)
    print()

    query = PubMedQuery(email=args.email)
    publications = query.query_author(pubmed_name, year=args.year)

    if not publications:
        print(f"\n❌ No publications found for '{original_name}' in {args.year}.")
        if pubmed_name != original_name:
            print(f"   (Searched PubMed as: {pubmed_name})")
        return

    print(f"\n✓ Found {len(publications)} publication(s)")
    print()

    # Generate HTML report
    if args.output:
        html_filename = (
            args.output if args.output.endswith(".html") else f"{args.output}.html"
        )
    else:
        # Auto-generate filename from author name
        author_slug = original_name.replace(" ", "_").replace(",", "").replace('"', "")
        html_filename = f"{author_slug}_{args.year}.html"

    generator = ReportGenerator(args.faculty_file)

    # Create title
    title = f"{original_name} Publications ({args.year})"

    # Count DFM faculty
    faculty_count = len(
        set(
            author
            for pub in publications
            for author in pub.get("authors_list", [])
            if generator.is_faculty_member(author)
        )
    )

    generator.generate_html_report(
        publications=publications,
        output_file=html_filename,
        title=title,
        queried_faculty=[original_name],
    )

    print(f"✅ Report generated successfully!")
    print(f"📄 Open {html_filename} in your browser")
    print()

    # Send email if requested
    if args.send_email:
        if not args.email_to or not args.email_from:
            print(
                "❌ Error: --email-to and --email-from are required when using --send-email"
            )
            return

        print("\n" + "=" * 80)
        print("Sending email...")
        print("=" * 80)

        # Get password securely
        password = getpass.getpass(f"Enter password for {args.email_from}: ")

        sender = EmailSender(provider=args.email_provider)

        try:
            if args.email_format == "html":
                sender.send_html_report(
                    html_file=html_filename,
                    to_email=args.email_to,
                    from_email=args.email_from,
                    password=password,
                    author_name=original_name,
                    year=args.year,
                )
            else:  # text
                sender.send_text_summary(
                    publications=publications,
                    to_email=args.email_to,
                    from_email=args.email_from,
                    password=password,
                    author_name=original_name,
                    year=args.year,
                    faculty_count=faculty_count,
                )
        except Exception as e:
            print(f"❌ Error sending email: {e}")


if __name__ == "__main__":
    main()
