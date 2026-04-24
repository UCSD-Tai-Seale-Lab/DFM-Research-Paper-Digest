#!/usr/bin/env python3
"""
Report Generator for Faculty Publications
Creates formatted HTML reports with highlighted faculty members
"""

import re
import sys
from datetime import datetime
from typing import Dict, List, Set

from faculty_parser import FacultyNameParser
from faculty_list import FacultyList


class ReportGenerator:
    """Generate publication reports with faculty highlighting."""

    def __init__(self, faculty_list_file: str = None):
        """
        Initialize report generator.

        Args:
            faculty_list_file: Path to faculty list file (optional)
        """
        self.__parser: FacultyNameParser = FacultyNameParser()
        self.__faculty_names: FacultyList

        if faculty_list_file:
            self.__faculty_names = FacultyList(faculty_list_file)

    def is_faculty_member(self, author_name: str) -> bool:
        """
        Check if an author is a DFM faculty member.

        Args:
            author_name: Author name to check

        Returns:
            True if author is faculty member
        """
        if self.__faculty_names:
            return self.__faculty_names.is_faculty_member(author_name)

        return False

    def highlight_faculty_authors(self, authors_list: List[str]) -> str:
        """
        Create HTML string with faculty members highlighted.

        Args:
            authors_list: List of author names

        Returns:
            HTML string with <strong> tags around faculty members
        """
        highlighted = []

        for author in authors_list:
            if self.is_faculty_member(author):
                highlighted.append(f"<strong>{author}</strong>")
            else:
                highlighted.append(author)

        return ", ".join(highlighted)

    def generate_html_report(
        self,
        publications: List[Dict],
        output_file: str,
        title: str = "DFM Faculty Publications Report",
        queried_faculty: List[str] = None,
    ):
        """
        Generate HTML report with highlighted faculty members.

        Args:
            publications: List of publication dictionaries
            output_file: Output HTML filename
            title: Report title
            queried_faculty: List of faculty names that were queried
        """
        if not output_file.endswith(".html"):
            output_file += ".html"

        # Get unique faculty members in publications
        faculty_in_pubs = set()

        for pub in publications:
            authors_list = pub.get("authors_list", [])

            for author in authors_list:
                if self.is_faculty_member(author):
                    faculty_in_pubs.add(author)

        # Generate HTML
        html = self._generate_html_content(
            publications, title, queried_faculty, faculty_in_pubs
        )

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\n{'='*80}")
        print(f"✓ HTML Report generated: {output_file}")
        print(f"  Total publications: {len(publications)}")
        print(f"  Unique DFM faculty found: {len(faculty_in_pubs)}")
        print(f"{'='*80}\n")

    def _generate_html_content(
        self,
        publications: List[Dict],
        title: str,
        queried_faculty: List[str],
        faculty_in_pubs: Set[str],
    ) -> str:
        """Generate HTML content for report."""

        # HTML header with styling
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2em;
        }}
        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary h2 {{
            margin-top: 0;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .summary-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        .summary-item .label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        .summary-item .value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}
        .publication {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .publication:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .publication-number {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .publication-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
            line-height: 1.4;
        }}
        .publication-authors {{
            color: #555;
            margin: 15px 0;
            line-height: 1.6;
            font-size: 1em;
        }}
        .publication-authors strong {{
            color: #667eea;
            font-weight: bold;
            background: #f0f4ff;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .publication-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            font-size: 0.95em;
        }}
        .meta-label {{
            font-weight: bold;
            color: #444;
        }}
        .pmid-link {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.2s;
        }}
        .pmid-link:hover {{
            background: #218838;
        }}
        .faculty-list {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}
        .faculty-list h3 {{
            margin-top: 0;
            color: #667eea;
            font-size: 1.1em;
        }}
        .faculty-list ul {{
            columns: 3;
            column-gap: 20px;
            margin: 10px 0;
        }}
        .faculty-list li {{
            margin-bottom: 5px;
            color: #555;
        }}
        .legend {{
            background: #fff9e6;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .legend strong {{
            color: #667eea;
            background: #f0f4ff;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        @media print {{
            body {{
                background: white;
            }}
            .publication {{
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
    </div>
"""

        # Summary section
        html += f"""
    <div class="summary">
        <h2>Report Summary</h2>
        <div class="summary-grid">
            <div class="summary-item">
                <div class="label">Total Publications</div>
                <div class="value">{len(publications)}</div>
            </div>
            <div class="summary-item">
                <div class="label">DFM Faculty Authors</div>
                <div class="value">{len(faculty_in_pubs)}</div>
            </div>
        </div>
    </div>
    
    <div class="legend">
        <strong>Note:</strong> DFM faculty members are highlighted in <strong>bold with blue background</strong> in the author lists.
    </div>
"""

        # Publications
        for i, pub in enumerate(publications, 1):
            authors_html = self.highlight_faculty_authors(pub.get("authors_list", []))

            html += f"""
    <div class="publication">
        <span class="publication-number">Publication #{i}</span>
        <div class="publication-title">{pub['title']}</div>
        <div class="publication-authors">{authors_html}</div>
        <div class="publication-meta">
            <div class="meta-item">
                <span class="meta-label">Journal:</span>
                <span>{pub['journal']}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Publication Date:</span>
                <span>{pub.get('date', pub.get('year', 'N/A'))}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">PMID:</span>
                <span>{pub['pmid']}</span>
            </div>
            <div class="meta-item">
                <a href="{pub.get('url', f'https://pubmed.ncbi.nlm.nih.gov/{pub["pmid"]}/')}" 
                   class="pmid-link" target="_blank">View on PubMed</a>
            </div>
        </div>
    </div>
"""

        # Footer
        html += """
</body>
</html>
"""

        return html


def main():
    """Demo/test function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate publication report with faculty highlighting"
    )
    parser.add_argument("--faculty-file", required=True, help="Faculty list file")
    parser.add_argument("--csv-file", required=True, help="Publications CSV file")
    parser.add_argument("--output", default="report.html", help="Output HTML file")
    parser.add_argument(
        "--title", default="DFM Faculty Publications Report", help="Report title"
    )

    args = parser.parse_args()

    # Load publications from CSV
    import csv

    publications = []
    with open(args.csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert authors string to list
            authors_str = row.get("authors", "")
            authors_list = [a.strip() for a in authors_str.split(",")]
            row["authors_list"] = authors_list
            publications.append(row)

    # Generate report
    generator = ReportGenerator(args.faculty_file)
    generator.generate_html_report(publications, args.output, title=args.title)


if __name__ == "__main__":
    main()
