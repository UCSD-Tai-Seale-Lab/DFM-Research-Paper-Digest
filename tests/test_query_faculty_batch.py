"""
Exercises query_faculty_batch.py
"""

from importlib.resources import as_file, files

from dfm_research_paper_digest.query_faculty_batch import main


def test_query_faculty_batch(username):
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        main(
            [
                "--faculty-file",
                str(faculty_filename),
                "--year",
                "2026",
                "--email",
                f"{username}@ucsd.edu",
                "--output",
                r"C:\Family Medicine\Publication Output\results\test_results",
            ]
        )


# @pytest.mark.skip(reason="Not really a test.")
def test_run_query_faculty_batch(username):
    resource_path = files("data").joinpath("faculty_list.txt")

    with as_file(resource_path) as faculty_filename:
        main(
            [
                "--faculty-file",
                str(faculty_filename),
                "--year",
                "2026",
                "--email",
                f"{username}@ucsd.edu",
                "--output",
                r"C:\Family Medicine\Publication Output\results\batch_results",
            ]
        )
