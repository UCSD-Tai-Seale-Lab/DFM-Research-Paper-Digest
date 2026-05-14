#!/usr/bin/env python3
"""
Report Generator for Faculty Publications
Creates formatted HTML reports with highlighted faculty members
"""
# pylint: disable=import-error, import-outside-toplevel, too-few-public-methods
import logging
from datetime import datetime
from pathlib import Path

from metapub import PubMedArticle, PubMedAuthor

from src.dfm_research_paper_digest import Author, Faculty, PubMedQuery


class ReportGenerator:
    """
        Generate publication reports with faculty highlighting.

    Attributes:
    ----------
    no public attributes

    Methods
    -------
    generate_html_report()
    """

    def __init__(self, faculty: Faculty, log: logging.Logger):
        """
        Initialize report generator.

        Args:
            faculty: Faculty object
        """
        self.__faculty: Faculty = faculty
        self.__log: logging.Logger = log

    def generate_html_content(
        self,
        publications: list[PubMedArticle],
        title: str,
    ) -> str:
        """
            Turn a list of articles into html string.

        Parameters
        ----------
        publications: list[PubMedArticle]
        title: str

        Returns
        -------
        html: str
        """

        # HTML header with styling
        html: str = f"""<!DOCTYPE html>
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
        # Get unique faculty members in publications
        num_faculty_in_pubs: int = self.__count_unique_faculty_members(publications)

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
                <div class="value">{num_faculty_in_pubs}</div>
            </div>
        </div>
    </div>

    <div class="legend">
        <strong>Note:</strong> DFM faculty members are highlighted in <strong>bold with blue background</strong> in the author lists.
    </div>
"""
        # Publications
        for i, pub in enumerate(publications, 1):
            authors_html: str = self.__highlight_faculty_authors(pub.author_list)

            html += f"""
    <div class="publication">
        <span class="publication-number">Publication #{i}</span>
        <div class="publication-title">{pub.title}</div>
        <div class="publication-authors">{authors_html}</div>
        <div class="publication-meta">
            <div class="meta-item">
                <span class="meta-label">Journal:</span>
                <span>{pub.journal}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Publication Date:</span>
                <span>{pub.year}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">PMID:</span>
                <span>{pub.pmid}</span>
            </div>
            <div class="meta-item">
                <a href="{f'https://pubmed.ncbi.nlm.nih.gov/{pub.pmid}/'}"
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

    def generate_html_report(
        self,
        publications: list[PubMedArticle],
        output_file: str,
        title: str = "DFM Faculty Publications Report",
    ):
        """
        Generate HTML report with highlighted faculty members.

        Args:
            publications: list of Article objects
            output_file: Output HTML filename
            title: Report title
        """
        # Generate HTML
        html: str = self.generate_html_content(publications, title)

        # Create file.
        self.write_html_file(html, output_file)

        self.__log.info(f"✓ HTML Report generated: {output_file}")
        self.__log.info(f"  Total publications: {len(publications)}")

    def __highlight_faculty_authors(self, authors_list: list[PubMedAuthor]) -> str:
        """
        Create HTML string with faculty members highlighted.

        Args:
            authors_list: list of PubMedAuthor objects

        Returns:
            HTML string with <strong> tags around faculty members
        """
        highlighted: list = []

        for author in authors_list:
            nice_name: str = f"{author.fore_name} {author.last_name}"

            if self.__faculty.is_faculty(author) and PubMedQuery.is_ucsd_affiliated(
                author
            ):
                highlighted.append(f"<strong>{nice_name}</strong>")
            else:
                highlighted.append(nice_name)

        return ", ".join(highlighted)

    def __count_unique_faculty_members(self, publications: list[PubMedArticle]) -> int:
        """
            Counts the unique faculty members in a list of PubMedArticle objects.

        Parameters
        ----------
        publications: list[PubMedArticle]

        Returns
        -------
        count: int
        """
        faculty_authors_in_pubs: list[Author] = []

        for pub in publications:
            for pubMedAuthor in pub.author_list:
                if self.__faculty.is_faculty(pubMedAuthor):
                    # Build a list of UNIQUE Author objects.
                    this_author: Author = Author(pubMedAuthor)

                    if not this_author.matches(faculty_authors_in_pubs):
                        faculty_authors_in_pubs.append(this_author)

        return len(faculty_authors_in_pubs)

    @staticmethod
    def write_html_file(html: str, output_file: str) -> None:
        """
            Creates .html file

        Parameters
        ----------
        html: str
        output_file: str

        """

        # Ensure directory exists.
        output_dir: Path = Path(output_file).resolve().parent

        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        # Write to file.
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
