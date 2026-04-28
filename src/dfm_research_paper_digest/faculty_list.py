from typing import Optional

from src.dfm_research_paper_digest.faculty_parser import FacultyNameParser


class FacultyList:
    """
    Loads & handles list of faculty members
    """

    def __init__(self, filename: str) -> None:
        """
        Build FacultyList object from file.

        Parameters
        ----------
        filename: str
        """
        self.__parser: FacultyNameParser = FacultyNameParser()
        self.__list: list[dict[str, Optional[str]]]

        try:
            faculty_lines: list[str]

            with open(filename, "r") as f:
                faculty_lines = [line.strip() for line in f if line.strip()]

            self.__list: list[dict[str, Optional[str]]] = (
                self.__parser.parse_faculty_list(faculty_lines)
            )
            print(f"Loaded {len(self.__list)} faculty members for highlighting")

        except FileNotFoundError:
            print(f"Warning: Faculty list file not found: {filename}")
        except Exception as e:
            print(f"Error loading faculty list: {e}")

    def is_faculty_member(self, author_name: str) -> bool:
        """
        Check if an author is a DFM faculty member.

        Args:
            author_name: Author name to check

        Returns:
            True if author is faculty member
        """
        author_name_parsed: dict[str, Optional[str]] = self.__parser.parse_faculty_name(
            author_name
        )

        for faculty_member in self.__list:
            if self.__parser.names_match(author_name_parsed, faculty_member):
                return True

        return False
