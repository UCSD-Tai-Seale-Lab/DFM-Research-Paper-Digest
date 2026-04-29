"""
Exercises query_faculty_batch.py
"""

from importlib.resources import as_file, files

from src.dfm_research_paper_digest.query_faculty_batch import \
    query_faculty_batch


def test_query_faculty_batch():
    resource_path = files("src.dfm_research_paper_digest.data").joinpath(
        "faculty_list.txt"
    )

    with as_file(resource_path) as filename:
        query_faculty_batch(
            faculty_list_file=filename,
            year=2026,
            email="kjdelaney@health.ucsd.edu",
            output_file="results",
        )
