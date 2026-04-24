#!/usr/bin/env python3
"""
Generate HTML report from existing CSV file
"""

import argparse
import csv

from report_generator import ReportGenerator


def main():
    """Generate HTML report from CSV."""
    parser = argparse.ArgumentParser(
        description='Generate HTML report from publications CSV'
    )
    parser.add_argument('csv_file', help='Input CSV file with publications')
    parser.add_argument('--faculty-file', required=True, help='Faculty list file')
    parser.add_argument('--output', default='report.html', help='Output HTML filename')
    parser.add_argument('--title', default='DFM Faculty Publications Report', help='Report title')
    
    args = parser.parse_args()
    
    # Load publications from CSV
    publications = []
    with open(args.csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert authors string to list
            authors_str = row.get('authors', '')
            if authors_str:
                authors_list = [a.strip() for a in authors_str.split(',')]
                row['authors_list'] = authors_list
            else:
                row['authors_list'] = []
            publications.append(row)
    
    print(f"Loaded {len(publications)} publications from {args.csv_file}")
    
    # Get queried faculty if available in CSV
    queried_faculty = []
    if publications and 'faculty_name' in publications[0]:
        queried_faculty = list(set(pub['faculty_name'] for pub in publications if pub.get('faculty_name')))
    
    # Generate report
    generator = ReportGenerator(args.faculty_file)
    generator.generate_html_report(
        publications, 
        args.output,
        title=args.title,
        queried_faculty=queried_faculty
    )
    
    print(f"\n✅ Report generated successfully!")
    print(f"📄 Open {args.output} in your browser to view the report")


if __name__ == "__main__":
    main()

