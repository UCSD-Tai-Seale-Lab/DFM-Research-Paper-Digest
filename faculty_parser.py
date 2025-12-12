#!/usr/bin/env python3
"""
Faculty Name Parser
Parses faculty names in the format: "Lastname, Firstname, Qualification"
Handles edge case: "Lastname, Qualification" (no firstname)
"""

import re
from typing import List, Dict, Tuple, Optional


class FacultyNameParser:
    """Parse faculty names and convert them to PubMed search format."""
    
    # Common qualifications to identify edge cases (stored in uppercase for comparison)
    QUALIFICATIONS = {
        'MD', 'DO', 'PHD', 'MPH', 'PHARMD', 'DPM', 'DMSC', 'PAC', 'PA-C',
        'LMFT', 'RN', 'NP', 'DDS', 'MS', 'MA', 'MBA', 'MHA', 'DRPH'
    }
    
    def __init__(self):
        self.qualification_pattern = '|'.join(self.QUALIFICATIONS)
    
    def parse_faculty_name(self, faculty_string: str) -> Dict[str, Optional[str]]:
        """
        Parse a faculty name string into components.
        
        Args:
            faculty_string: String in format "Lastname, Firstname, Qualification" 
                           or "Lastname, Qualification"
        
        Returns:
            Dictionary with keys: lastname, firstname, qualification, pubmed_format
        
        Examples:
            "MacDonald, Kaimana, MD" -> {
                'lastname': 'MacDonald',
                'firstname': 'Kaimana',
                'qualification': 'MD',
                'pubmed_format': 'MacDonald K'
            }
            
            "Tai-Seale, PhD, MPH" -> {
                'lastname': 'Tai-Seale',
                'firstname': None,
                'qualification': 'PhD, MPH',
                'pubmed_format': 'Tai-Seale'
            }
        """
        # Remove extra whitespace
        faculty_string = faculty_string.strip()
        
        # Split by comma
        parts = [p.strip() for p in faculty_string.split(',')]
        
        if len(parts) < 2:
            raise ValueError(f"Invalid faculty name format: {faculty_string}")
        
        lastname = parts[0]
        second_part = parts[1]
        
        # Check if second part is a qualification by checking if it's in our list
        # Remove periods and spaces for comparison
        second_part_clean = second_part.replace('.', '').replace(' ', '').upper()
        
        # Check if it exactly matches a qualification
        is_qualification = second_part_clean in self.QUALIFICATIONS
        
        if is_qualification:
            # Edge case: "Lastname, Qualification" (e.g., "Tai-Seale, PhD, MPH")
            firstname = None
            qualification = ', '.join(parts[1:])
            pubmed_format = lastname
        else:
            # Normal case: "Lastname, Firstname, Qualification"
            firstname = second_part
            qualification = ', '.join(parts[2:]) if len(parts) > 2 else ''
            
            # Create PubMed format: "Lastname FirstInitial"
            # Handle names with quotes or special characters
            first_initial = firstname[0] if firstname else ''
            pubmed_format = f"{lastname} {first_initial}" if first_initial else lastname
        
        return {
            'lastname': lastname,
            'firstname': firstname,
            'qualification': qualification,
            'pubmed_format': pubmed_format,
            'original': faculty_string
        }
    
    def parse_faculty_list(self, faculty_list: List[str]) -> List[Dict[str, Optional[str]]]:
        """
        Parse a list of faculty names.
        
        Args:
            faculty_list: List of faculty name strings
        
        Returns:
            List of parsed faculty dictionaries
        """
        parsed_faculty = []
        for faculty in faculty_list:
            try:
                parsed = self.parse_faculty_name(faculty)
                parsed_faculty.append(parsed)
            except ValueError as e:
                print(f"Warning: {e}")
                continue
        
        return parsed_faculty
    
    def get_pubmed_names(self, faculty_list: List[str]) -> List[str]:
        """
        Get list of PubMed-formatted names from faculty list.
        
        Args:
            faculty_list: List of faculty name strings
        
        Returns:
            List of PubMed-formatted names
        """
        parsed = self.parse_faculty_list(faculty_list)
        return [f['pubmed_format'] for f in parsed]


def main():
    """Demo usage of faculty name parser."""
    
    # Example faculty list from the images
    faculty_list = [
        "Achar, Suraj, MD",
        "Ajayi, Toluwalase, MD",
        "Al-Delaimy, Wael MD, PhD",
        "Allison, Matthew MD, MPH",
        "Andrew, William, DO",
        "Araneta, Maria \"Happy\" Rosario, PhD, MPH",
        "Beck, Ellen, MD",
        "Brady, Patricia, MD",
        "Buckholz, Gary, MD",
        "Cederquist, Lynette, MD",
        "Celebi, Julie, MD",
        "Chen, Alice, DO",
        "Cheng, Terri, MD",
        "Criqui, Michael, MD, MPH",
        "Dang, Laurel, MD",
        "Eastman, Amelia, DO, MPH",
        "Edi, Rina, MD",
        "Fiorella, Melanie, MD",
        "Folsom, David P., MD, MPH",
        "Fraser, Kevin, MD",
        "Galloway, Sam, MD",
        "Gin, Geneen, DO",
        "Gutierrez, Cecilia, MD",
        "Hatamy, Esmatullah, MD",
        "Huffman, Jared, DO",
        "Jain, Shamini, PhD",
        "Johnson, Michelle, MD",
        "Jolicoeur, Megan, DO",
        "Kallenberg, Gene, MD",
        "Le, Julie, DO",
        "Lebensohn-Chialvo, Florencia, PhD",
        "Leu, Amy, DO",
        "Lillie, Dustin, MD",
        "Lindeman, Kurt, MD",
        "Lynch, Allison, MD",
        "MacMillen, Caitlin, DO",
        "Mandvi, Ammar, MD",
        "McPherson, Julia, MD",
        "Mercer, Anna, DO",
        "Merrill, Sarah, MD",
        "Morn, Cassandra, MD",
        "Morris, Sheldon, MD, MPH",
        "Osborne, Chad, MD",
        "Portera, Ariel, DO",
        "Rahman, Akbar, MD, MPH",
        "Reddy, Divya, MD",
        "Rodriguez, Natalie, MD",
        "Romero, Jairo, MD",
        "Rosen, Rebecca, MD",
        "Rosenblum, Elizabeth, MD",
        "Sannidhi, Deepa, MD",
        "Searles, Robert (Chris), MD",
        "Shahtaji, Alan, DO",
        "Sieber, Wiliam J., PhD",
        "Silverstein, Donna, PhD",
        "Slater, Daniel, M.D.",
        "Sudano, Laura, PhD, LMFT",
        "Tai-Seale, PhD, MPH",  # Edge case - no firstname
        "Taylor, Kenneth S., M.D.",
        "Thorne, Christine, MD, MPH",
        "Vieten, Cassandra, PhD",
        "Villarreal, Elias, PA-C, DMSc",
        "Wang, Regina, MD",
        "Wilkinson, Lesley, MD",
        "Wu, Jennifer, MD",
        "Yeung, Heidi, MD",
        "MacDonald, Kaimana, MD",
        "Martinez, Brianna, MD",
        "Miller, Stephen, MD",
        "Nasar, Aboo, MD, MPH",
        "Wang, Mary, MD"
    ]
    
    # Initialize parser
    parser = FacultyNameParser()
    
    # Parse faculty list
    print("="*80)
    print("Faculty Name Parser - Demo")
    print("="*80)
    print()
    
    parsed_faculty = parser.parse_faculty_list(faculty_list)
    
    # Display results
    print(f"Parsed {len(parsed_faculty)} faculty members:\n")
    
    # Show some examples including the edge case
    examples = [
        "MacDonald, Kaimana, MD",
        "Tai-Seale, PhD, MPH",
        "Wu, Jennifer, MD",
        "Araneta, Maria \"Happy\" Rosario, PhD, MPH"
    ]
    
    print("Example Parsing:")
    print("-" * 80)
    for example in examples:
        parsed = parser.parse_faculty_name(example)
        print(f"\nOriginal: {example}")
        print(f"  Lastname:       {parsed['lastname']}")
        print(f"  Firstname:      {parsed['firstname'] or '(None)'}")
        print(f"  Qualification:  {parsed['qualification']}")
        print(f"  PubMed Format:  {parsed['pubmed_format']}")
    
    print("\n" + "="*80)
    print("All PubMed-formatted names:")
    print("="*80)
    
    pubmed_names = parser.get_pubmed_names(faculty_list)
    for i, name in enumerate(pubmed_names, 1):
        print(f"{i:3}. {name}")
    
    print(f"\nTotal: {len(pubmed_names)} names ready for PubMed queries")
    
    return parsed_faculty, pubmed_names


if __name__ == "__main__":
    parsed_faculty, pubmed_names = main()

