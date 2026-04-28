#!/usr/bin/env python3
"""
Faculty Name Parser
Parses faculty names in the format: "Lastname, Firstname, Qualification"
Handles edge case: "Lastname, Qualification" (no firstname)
"""

import re
from typing import Dict, List, Optional, Tuple

from nameparser import HumanName


class FacultyNameParser:
    """Parse faculty names and convert them to PubMed search format."""

    @staticmethod
    def check_middle_name_match(authors: list[str], faculty: dict) -> bool:
        """
        Not all publications will list an author's middle name/initial.
        But if it IS listed, does it match our faculty member?

        For example, if our faculty member is Dr. Ima A. Provider and
        one of the listed authors is "Provider, Ima", (no middle name given),
        or "Provider, Ima A" (with matching middle initial) then it's a match.
        But if it's "Provider, Ima Z." then it's NOT a match.

        It's OK if the author's middle initial isn't listed,
        but if it IS listed, it has to match.

        Parameters
        ----------
        authors: list[str]
        faculty: dict with keys 'first', 'last', 'middle'

        Returns
        -------
        match: bool
        """

        for author in authors:
            author_struct: HumanName = HumanName(author.strip())

            if (
                (author_struct.first == faculty["firstname"])
                and (author_struct.last == faculty["lastname"])
                and FacultyNameParser.__middle_names_match_where_present(
                    author_struct.middle, faculty["middle"]
                )
            ):
                return True

        return False

    @staticmethod
    def __middle_names_match_where_present(
        middle_name_A: str, middle_name_B: str
    ) -> bool:
        """
        Returns True if:
            * middle_name_A is empty
            * middle_name_B is empty
            * middle_name_A == middle_name_B
            * middle_name_A is only one char and matches first char of middle_name_B
            * middle_name_B is only one char and matches first char of middle_name_A

        Examples:
                middle_name_A       middle_name_B       result
            *       ''                  'Juan'            True
            *       'Juan'              ''                True
            *       'Juan'              'Juan'            True
            *       'J'                 'Juan'            True
            *       'Juan'              'J'               True
            *       'J'                 'J'               True
            *       ''                  ''                True
            *       'X'                 'J'              False
            *       'X'                 'Juan'           False
            *       'Juan'              'Z'              False

        Parameters
        ----------
        middle_name_A: str
        middle_name_B: str

        Returns
        -------
        match: bool
        """
        if middle_name_A:
            if middle_name_B:
                if middle_name_A == middle_name_B:
                    return True
                elif len(middle_name_A) == 1 and middle_name_A == middle_name_B[0]:
                    return True
                elif len(middle_name_B) == 1 and middle_name_A[0] == middle_name_B:
                    return True
            else:
                return True
        else:
            return True

        return False

    @staticmethod
    def names_match(
        name_A: dict[str, Optional[str]], name_B: dict[str, Optional[str]]
    ) -> bool:
        """
        Tests first, last and (if present) middle names.

        Parameters
        ----------
        name_A: dict (output of "parse_faculty_name"
        name_B: dict (output of "parse_faculty_name"

        Returns
        -------
        match: bool
        """
        return (
            name_A["firstname"] == name_B["firstname"]
            and name_A["lastname"] == name_B["lastname"]
            and FacultyNameParser.__middle_names_match_where_present(
                name_A["middle"], name_B["middle"]
            )
        )

    def parse_faculty_name(self, faculty_string: str) -> dict[str, Optional[str]]:
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
        name: HumanName = HumanName(faculty_string)

        # The default--just a last name.
        pubmed_format: str = f"{name.last}"
        pubmed_long_format: str = f"{name.last}"

        if name.first:
            pubmed_format = f"{name.last} {name.first[0]}"
            pubmed_long_format = f"{name.last} {name.first}"

        return {
            "lastname": name.last,
            "firstname": name.first,
            # Turn 'A.' into just 'A'
            "middle": name.middle.rstrip("."),
            "qualification": name.suffix,
            "pubmed_format": pubmed_format,
            "pubmed_long_format": pubmed_long_format,
            "original": faculty_string,
        }

    def parse_faculty_list(
        self, faculty_list: List[str]
    ) -> List[Dict[str, Optional[str]]]:
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
        return [f["pubmed_format"] for f in parsed]


def main():
    """Demo usage of faculty name parser."""

    # Example faculty list from the images
    faculty_list = [
        "Achar, Suraj, MD",
        "Ajayi, Toluwalase, MD",
        "Al-Delaimy, Wael MD, PhD",
        "Allison, Matthew MD, MPH",
        "Andrew, William, DO",
        'Araneta, Maria "Happy" Rosario, PhD, MPH',
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
        "Wang, Mary, MD",
    ]

    # Initialize parser
    parser = FacultyNameParser()

    # Parse faculty list
    print("=" * 80)
    print("Faculty Name Parser - Demo")
    print("=" * 80)
    print()

    parsed_faculty = parser.parse_faculty_list(faculty_list)

    # Display results
    print(f"Parsed {len(parsed_faculty)} faculty members:\n")

    # Show some examples including the edge case
    examples = [
        "MacDonald, Kaimana, MD",
        "Tai-Seale, PhD, MPH",
        "Wu, Jennifer, MD",
        'Araneta, Maria "Happy" Rosario, PhD, MPH',
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

    print("\n" + "=" * 80)
    print("All PubMed-formatted names:")
    print("=" * 80)

    pubmed_names = parser.get_pubmed_names(faculty_list)
    for i, name in enumerate(pubmed_names, 1):
        print(f"{i:3}. {name}")

    print(f"\nTotal: {len(pubmed_names)} names ready for PubMed queries")

    return parsed_faculty, pubmed_names


if __name__ == "__main__":
    parsed_faculty, pubmed_names = main()
