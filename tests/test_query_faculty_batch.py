"""
Exercises query_faculty_batch.py
"""

from datetime import datetime
from importlib.resources import as_file, files
from pathlib import Path

import pytest

from dfm_research_paper_digest.query_faculty_batch import main, query_faculty_batch


def test_query_faculty_batch_I(username):
    output_file: str = r"C:\Family Medicine\Publication Output\results\test_results_I"
    Path(output_file).unlink(missing_ok=True)
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        main(
            [
                "--email",
                f"{username}@ucsd.edu",
                "--faculty-file",
                str(faculty_filename),
                "--output",
                output_file,
                "--year",
                "2026",
            ]
        )

    # Check that the file was created.
    assert Path(f"{output_file}.html").is_file()


def test_query_faculty_batch_II(username):
    output_file: str = f"faculty_{datetime.now().year}"
    Path(output_file).unlink(missing_ok=True)
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    # Exercise calling w/o log and w/o output filename.
    with as_file(resource_path) as faculty_filename:
        query_faculty_batch(
            contact_email=f"{username}@ucsd.edu",
            faculty_list_file=str(faculty_filename),
            year=datetime.now().year,
        )

    # Check that the file was created.
    assert Path(f"{output_file}.html").is_file()


# @pytest.mark.skip(reason="Not really a test.")
def test_run_query_faculty_batch(username):
    output_file: str = (
        r"C:\Family Medicine\Publication Output\results\batch_results.html"
    )
    Path(output_file).unlink(missing_ok=True)
    resource_path = files("data").joinpath("faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        main(
            [
                "--email",
                f"{username}@ucsd.edu",
                "--faculty-file",
                str(faculty_filename),
                "--output",
                output_file,
                "--year",
                "2025",
            ]
        )

    # Check that the file was created.
    assert Path(output_file).is_file()
