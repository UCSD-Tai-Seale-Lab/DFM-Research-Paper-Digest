#!/usr/bin/env python3
"""
PubMed Author Publications Query Tool
Queries PubMed for publications by a specific author from 2025.
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import time
import argparse
import sys


class PubMedQuery:
    """Class to handle PubMed API queries."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, email: str = None):
        """
        Initialize PubMed query tool.
        
        Args:
            email: Your email (recommended by NCBI for API usage tracking)
        """
        self.email = email
        
    def search_author_publications(self, author_name: str, year: int = 2025) -> List[str]:
        """
        Search for publication IDs by author and year.
        
        Args:
            author_name: Name of the author (e.g., "Smith J" or "John Smith")
            year: Publication year (default: 2025)
            
        Returns:
            List of PubMed IDs (PMIDs)
        """
        # Construct search query
        search_term = f"{author_name}[Author] AND {year}[pdat]"
        
        # Build search URL
        params = {
            'db': 'pubmed',
            'term': search_term,
            'retmax': 100,  # Maximum number of results
            'retmode': 'xml'
        }
        
        if self.email:
            params['email'] = self.email
            
        url = f"{self.BASE_URL}esearch.fcgi"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            id_list = root.find('IdList')
            
            if id_list is not None:
                pmids = [id_elem.text for id_elem in id_list.findall('Id')]
                return pmids
            else:
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def fetch_publication_details(self, pmids: List[str]) -> List[Dict[str, str]]:
        """
        Fetch publication details for given PMIDs.
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            List of dictionaries containing publication details
        """
        if not pmids:
            return []
        
        # Join PMIDs with comma
        id_string = ','.join(pmids)
        
        params = {
            'db': 'pubmed',
            'id': id_string,
            'retmode': 'xml'
        }
        
        if self.email:
            params['email'] = self.email
            
        url = f"{self.BASE_URL}efetch.fcgi"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            publications = []
            
            for article in root.findall('.//PubmedArticle'):
                pub_info = self._extract_article_info(article)
                if pub_info:
                    publications.append(pub_info)
            
            return publications
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching publication details: {e}")
            return []
    
    def _extract_article_info(self, article) -> Dict[str, str]:
        """
        Extract relevant information from article XML element.
        
        Args:
            article: XML element containing article data
            
        Returns:
            Dictionary with publication details
        """
        try:
            # Extract PMID
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else "N/A"
            
            # Extract title
            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "No title available"
            
            # Extract publication date
            pub_date = article.find('.//PubDate')
            year = "N/A"
            month = ""
            day = ""
            full_date = ""
            
            if pub_date is not None:
                year_elem = pub_date.find('Year')
                month_elem = pub_date.find('Month')
                day_elem = pub_date.find('Day')
                medline_date = pub_date.find('MedlineDate')
                
                if year_elem is not None:
                    year = year_elem.text
                elif medline_date is not None:
                    # MedlineDate might be like "2025 Jan-Feb" or "2025"
                    year = medline_date.text.split()[0] if medline_date.text else "N/A"
                
                if month_elem is not None:
                    month = month_elem.text
                if day_elem is not None:
                    day = day_elem.text
                
                # Build full date string
                if day and month and year != "N/A":
                    full_date = f"{month} {day}, {year}"
                elif month and year != "N/A":
                    full_date = f"{month} {year}"
                else:
                    full_date = year
            
            # Extract journal
            journal_elem = article.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else "N/A"
            
            # Extract authors (ALL authors, not just first 3)
            author_list = article.findall('.//Author')
            authors = []
            for author in author_list:
                last_name = author.find('LastName')
                fore_name = author.find('ForeName')
                initials = author.find('Initials')
                
                if last_name is not None:
                    author_name = last_name.text
                    if fore_name is not None:
                        author_name = f"{fore_name.text} {author_name}"
                    elif initials is not None:
                        author_name = f"{initials.text} {author_name}"
                    authors.append(author_name)
            
            authors_str = ", ".join(authors)
            
            return {
                'pmid': pmid,
                'title': title,
                'year': year,
                'date': full_date,  # Full publication date
                'journal': journal,
                'authors': authors_str,
                'authors_list': authors  # Store as list for matching
            }
            
        except Exception as e:
            print(f"Error extracting article info: {e}")
            return None
    
    def query_author(self, author_name: str, year: int = 2025) -> List[Dict[str, str]]:
        """
        Complete query for author publications.
        
        Args:
            author_name: Name of the author
            year: Publication year (default: 2025)
            
        Returns:
            List of publication details
        """
        print(f"\nSearching PubMed for publications by '{author_name}' from {year}...")
        
        # Step 1: Search for PMIDs
        pmids = self.search_author_publications(author_name, year)
        
        if not pmids:
            print(f"No publications found for '{author_name}' in {year}.")
            return []
        
        print(f"Found {len(pmids)} publication(s).")
        
        # Step 2: Fetch publication details
        # NCBI recommends max 3 requests per second
        time.sleep(0.34)
        
        publications = self.fetch_publication_details(pmids)
        
        return publications


def display_publications(publications: List[Dict[str, str]]):
    """Display publications in a formatted manner."""
    if not publications:
        print("\nNo publications to display.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(publications)} publication(s):")
    print(f"{'='*80}\n")
    
    for i, pub in enumerate(publications, 1):
        print(f"{i}. {pub['title']}")
        print(f"   Authors: {pub['authors']}")
        print(f"   Journal: {pub['journal']}")
        print(f"   Year: {pub['year']}")
        print(f"   PMID: {pub['pmid']}")
        print(f"   URL: https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/")
        print()


def main():
    """Main function to run the PubMed query tool."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Query PubMed for publications by a specific author from 2025.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Smith J"
  %(prog)s "Ming Tai-Seale" --email your@email.com
  %(prog)s "John Smith" --year 2024
  %(prog)s "Zhang Y" "Li Y" "Xie B"  # Query multiple authors
        """
    )
    
    parser.add_argument(
        'authors',
        nargs='+',
        help='Author name(s) to search for (e.g., "Smith J", "John Smith", or "Ming Tai-Seale")'
    )
    
    parser.add_argument(
        '--email', '-e',
        type=str,
        help='Your email address (optional, recommended by NCBI for API tracking)'
    )
    
    parser.add_argument(
        '--year', '-y',
        type=int,
        default=2025,
        help='Publication year to search (default: 2025)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        choices=['text', 'csv'],
        default='text',
        help='Output format: text or csv (default: text)'
    )
    
    parser.add_argument(
        '--filename', '-f',
        type=str,
        help='Custom output filename for CSV (only used with --output csv)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create query object
    query = PubMedQuery(email=args.email)
    
    # Process each author
    all_results = []
    for author_name in args.authors:
        print("="*80)
        print(f"PubMed Author Publications Query Tool")
        print("="*80)
        
        # Query PubMed
        publications = query.query_author(author_name, year=args.year)
        
        # Display or collect results
        if args.output == 'text':
            display_publications(publications)
        else:
            all_results.extend(publications)
            print(f"Retrieved {len(publications)} publication(s) for '{author_name}'")
        
        # Add delay between queries if multiple authors
        if len(args.authors) > 1 and author_name != args.authors[-1]:
            time.sleep(0.5)
    
    # Export to CSV if requested
    if args.output == 'csv':
        if all_results:
            # Use custom filename or create one based on author(s)
            if args.filename:
                filename = args.filename if args.filename.endswith('.csv') else f"{args.filename}.csv"
            elif len(args.authors) == 1:
                author_slug = args.authors[0].replace(' ', '_').replace(',', '')
                filename = f"{author_slug}_{args.year}.csv"
            else:
                filename = f"multiple_authors_{args.year}.csv"
            export_to_csv(all_results, filename)
        else:
            print("\nNo publications found to export.")
        

def export_to_csv(publications: List[Dict[str, str]], filename: str):
    """Export publications to CSV file."""
    import csv
    
    if not publications:
        print("No publications to export.")
        return
    
    try:
        # Add URL field to each publication
        for pub in publications:
            if 'url' not in pub:
                pub['url'] = f"https://pubmed.ncbi.nlm.nih.gov/{pub['pmid']}/"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'authors', 'journal', 'year', 'date', 'pmid', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            writer.writerows(publications)
        
        print(f"\n{'='*80}")
        print(f"✓ Successfully exported {len(publications)} publication(s) to: {filename}")
        print(f"{'='*80}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


if __name__ == "__main__":
    main()

