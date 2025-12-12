#!/usr/bin/env python3
"""
Example usage of the PubMed Query Tool.
Shows how to query multiple authors programmatically.
"""

from pubmed_query import PubMedQuery, display_publications


def query_multiple_authors():
    """Example: Query publications for multiple authors."""
    
    # List of authors to query
    authors = [
        "Zhang Y",
        "Li Y",
        "Xie B"
    ]
    
    # Initialize query object (optionally provide email)
    query = PubMedQuery(email="your.email@example.com")
    
    # Query each author
    for author in authors:
        print(f"\n{'='*80}")
        print(f"Querying author: {author}")
        print(f"{'='*80}")
        
        publications = query.query_author(author, year=2025)
        display_publications(publications)


def query_single_author_custom():
    """Example: Query a single author with custom display."""
    
    author_name = "Smith J"
    
    query = PubMedQuery()
    publications = query.query_author(author_name, year=2025)
    
    # Custom display
    if publications:
        print(f"\nPublications by {author_name} in 2025:")
        for pub in publications:
            print(f"  - {pub['year']}: {pub['title']}")
    else:
        print(f"No publications found for {author_name} in 2025")


def export_to_csv():
    """Example: Export results to CSV format."""
    import csv
    
    author_name = "Zhang Y"
    
    query = PubMedQuery()
    publications = query.query_author(author_name, year=2025)
    
    if publications:
        # Export to CSV
        filename = f"{author_name.replace(' ', '_')}_publications_2025.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'authors', 'journal', 'year', 'pmid']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(publications)
        
        print(f"\nExported {len(publications)} publications to {filename}")
    else:
        print(f"No publications found for {author_name} in 2025")


if __name__ == "__main__":
    # Run the examples
    print("Example 1: Query multiple authors")
    query_multiple_authors()
    
    print("\n\n" + "="*80)
    print("Example 2: Query single author with custom display")
    print("="*80)
    query_single_author_custom()
    
    print("\n\n" + "="*80)
    print("Example 3: Export to CSV")
    print("="*80)
    export_to_csv()

