#!/usr/bin/env python3
"""
Batch Faculty Publications Query
Queries PubMed for publications from multiple faculty members
"""

import sys
from faculty_parser import FacultyNameParser
from pubmed_query import PubMedQuery, export_to_csv
from report_generator import ReportGenerator
import time
import argparse


def export_to_csv_with_faculty(publications, filename):
    """Export publications with faculty information to CSV."""
    import csv
    
    if not publications:
        print("No publications to export.")
        return
    
    try:
        # Add URL field and prepare data for CSV
        for pub in publications:
            if 'url' not in pub:
                pub['url'] = f"https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Don't include authors_list in CSV (it's for HTML report only)
            fieldnames = ['faculty_name', 'faculty_lastname', 'faculty_firstname', 
                         'title', 'authors', 'journal', 'year', 'date', 'pmid', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            writer.writerows(publications)
        
        print(f"✓ Successfully exported {len(publications)} publication(s) to CSV")
        print()
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def query_faculty_batch(faculty_list, year=2025, email=None, output_file=None, 
                       faculty_list_file=None, generate_report=True):
    """
    Query PubMed for multiple faculty members and combine results.
    
    Args:
        faculty_list: List of faculty names in format "Lastname, Firstname, Qualification"
        year: Publication year (default: 2025)
        email: Optional email for NCBI API
        output_file: Optional CSV filename for output
        faculty_list_file: Path to faculty list file (for report generation)
        generate_report: Whether to generate HTML report (default: True)
    
    Returns:
        Dictionary with faculty names as keys and their publications as values
    """
    # Parse faculty names
    parser = FacultyNameParser()
    parsed_faculty = parser.parse_faculty_list(faculty_list)
    
    print("="*80)
    print(f"Querying PubMed for {len(parsed_faculty)} faculty members ({year})")
    print("="*80)
    print()
    
    # Initialize PubMed query
    query = PubMedQuery(email=email)
    
    # Store results
    all_results = []
    faculty_results = {}
    
    # Query each faculty member
    for i, faculty in enumerate(parsed_faculty, 1):
        pubmed_name = faculty['pubmed_format']
        original_name = faculty['original']
        
        print(f"[{i}/{len(parsed_faculty)}] Querying: {original_name}")
        print(f"    PubMed search: {pubmed_name}")
        
        try:
            publications = query.query_author(pubmed_name, year=year)
            
            # Add faculty info to each publication
            for pub in publications:
                pub['faculty_name'] = original_name
                pub['faculty_lastname'] = faculty['lastname']
                pub['faculty_firstname'] = faculty['firstname'] or ''
            
            faculty_results[original_name] = publications
            all_results.extend(publications)
            
            print(f"    Found: {len(publications)} publication(s)")
            
        except Exception as e:
            print(f"    Error: {e}")
            faculty_results[original_name] = []
        
        # Rate limiting: NCBI recommends max 3 requests per second
        if i < len(parsed_faculty):
            time.sleep(0.4)
        
        print()
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total faculty queried: {len(parsed_faculty)}")
    print(f"Total publications found: {len(all_results)}")
    print()
    
    # Faculty with most publications
    if faculty_results:
        sorted_faculty = sorted(faculty_results.items(), key=lambda x: len(x[1]), reverse=True)
        print("Top 10 faculty by publication count:")
        for name, pubs in sorted_faculty[:10]:
            print(f"  {len(pubs):3} - {name}")
        print()
    
    # Export to CSV if requested
    csv_filename = None
    if output_file and all_results:
        if not output_file.endswith('.csv'):
            csv_filename = output_file + '.csv'
        else:
            csv_filename = output_file
        
        print(f"Exporting to CSV: {csv_filename}")
        export_to_csv_with_faculty(all_results, csv_filename)
    
    # Generate HTML report if requested
    if generate_report and all_results and faculty_list_file:
        html_filename = output_file.replace('.csv', '') if output_file else 'faculty_publications_report'
        if html_filename.endswith('.csv'):
            html_filename = html_filename[:-4]
        html_filename += '.html'
        
        print(f"Generating HTML report: {html_filename}")
        report_gen = ReportGenerator(faculty_list_file)
        
        # Get list of queried faculty names
        queried_names = [f['original'] for f in parsed_faculty]
        
        report_gen.generate_html_report(
            publications=all_results,
            output_file=html_filename,
            title=f"DFM Faculty Publications Report ({year})",
            queried_faculty=queried_names
        )
    
    return faculty_results


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(
        description='Batch query PubMed for multiple faculty members',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query from a list
  %(prog)s --year 2025 --output faculty_pubs_2025

  # With email
  %(prog)s --email your@email.com --output results
        """
    )
    
    parser.add_argument(
        '--year', '-y',
        type=int,
        default=2025,
        help='Publication year (default: 2025)'
    )
    
    parser.add_argument(
        '--email', '-e',
        type=str,
        help='Your email (recommended by NCBI)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='faculty_publications',
        help='Output CSV filename (default: faculty_publications)'
    )
    
    parser.add_argument(
        '--faculty-file', '-f',
        type=str,
        help='Text file with faculty names (one per line)'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip HTML report generation'
    )
    
    args = parser.parse_args()
    
    # Get faculty list
    faculty_list = []
    
    if args.faculty_file:
        # Read from file
        try:
            with open(args.faculty_file, 'r') as f:
                faculty_list = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File not found: {args.faculty_file}")
            sys.exit(1)
    else:
        # Use default faculty list (from the images)
        faculty_list = [
            "Tai-Seale, PhD, MPH",
            "Wu, Jennifer, MD",
            "Cheng, Terri, MD",
            "Celebi, Julie, MD",
        ]
        print("No faculty file specified. Using sample faculty list.")
        print()
    
    if not faculty_list:
        print("Error: No faculty names provided")
        sys.exit(1)
    
    # Query faculty
    query_faculty_batch(
        faculty_list=faculty_list,
        year=args.year,
        email=args.email,
        output_file=args.output,
        faculty_list_file=args.faculty_file,
        generate_report=not args.no_report
    )


if __name__ == "__main__":
    main()

