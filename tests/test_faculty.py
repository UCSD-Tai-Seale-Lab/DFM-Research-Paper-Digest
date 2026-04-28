"""
Tests Faculty class.
"""

import logging
from importlib.resources import as_file, files

from src.dfm_research_paper_digest.author import Author
from src.dfm_research_paper_digest.faculty import Faculty


def test_faculty(logger: logging.Logger, sample_faculty_list: list[str]):
    resource_path = files("src.dfm_research_paper_digest.data").joinpath(
        "sample_faculty.txt"
    )

    with as_file(resource_path) as filename:
        faculty: Faculty = Faculty(filename, logger)
        assert isinstance(faculty, Faculty)
        assert faculty.num == 3
        author: Author = Author("Tai-Seale, Ming PhD, MPH")
        assert faculty.is_faculty(author)

        faculty_list: list[str] = faculty.names
        assert isinstance(faculty_list, list)
        assert isinstance(faculty_list[0], str)
        assert len(faculty_list) == 3

        # These will be in last, first format.
        assert faculty_list[0] == "Tai-Seale, Ming"
        assert faculty_list[2] == "Cheng, Terri"

        faculty_list_original: list[str] = faculty.original_names
        assert isinstance(faculty_list_original, list)
        assert isinstance(faculty_list_original[0], str)
        assert len(faculty_list_original) == 3

        # These will be in original format.
        assert faculty_list_original[0] == "Tai-Seale, Ming PhD, MPH"
        assert faculty_list_original[2] == "Cheng, Terri, MD"

        # Author objects
        author_list: list[Author] = faculty.authors
        assert isinstance(author_list, list)
        assert isinstance(author_list[0], Author)
        assert len(author_list) == 3
        assert author_list[0].matches(Author("Tai-Seale, Ming PhD, MPH"))

    # Exercise instantiation from a list[str].
    faculty_from_list: Faculty = Faculty(sample_faculty_list, logger)
    assert isinstance(faculty_from_list, Faculty)
    assert faculty_from_list.num == 4
