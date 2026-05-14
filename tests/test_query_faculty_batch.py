"""
Exercises query_faculty_batch.py
"""

from datetime import datetime
from importlib.resources import as_file, files
from pathlib import Path

from dfm_research_paper_digest.query_faculty_batch import main, run_batch_report
from dfm_research_paper_digest.report_generator import ReportGenerator


def test_query_faculty_batch_I(username):
    output_file: str = (
        r"C:\Family Medicine\Publication Output\results\test_results_I.html"
    )
    Path(output_file).resolve().unlink(missing_ok=True)
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
    assert Path(output_file).resolve().is_file()


def test_query_faculty_batch_II(username):
    output_file: str = f"faculty_{datetime.now().year}.html"
    Path(output_file).resolve().unlink(missing_ok=True)
    resource_path = files("data").joinpath("sample_faculty_list.txt")

    # Exercise calling w/o log and w/o output filename.
    with as_file(resource_path) as faculty_filename:
        html: str = run_batch_report(
            contact_email=f"{username}@ucsd.edu",
            faculty_list_file=str(faculty_filename),
            year=datetime.now().year,
        )
        assert isinstance(html, str)
        ReportGenerator.write_html_file(html, output_file)

        # Check that the file was created.
        assert Path(output_file).resolve().is_file()


def test_query_faculty_batch_III(username):
    """Single faculty name"""
    output_file: str = "Tai-Seale_2025.html"
    Path(output_file).resolve().unlink(missing_ok=True)

    # Exercise calling w/ single name.
    html: str = run_batch_report(
        contact_email=f"{username}@ucsd.edu",
        faculty_list_file=["Tai-Seale, Ming PhD, MPH"],
        year=2025,
    )
    assert isinstance(html, str)
    ReportGenerator.write_html_file(html, output_file)

    # Check that the file was created.
    assert Path(output_file).resolve().is_file()


# @pytest.mark.skip(reason="Not really a test.")
# Run using live faculty list from Department of Family Medicine webpage.
def test_run_query_faculty_batch(username, faculty_webpage):
    output_file: str = (
        r"C:\Family Medicine\Publication Output\results\batch_results.html"
    )
    Path(output_file).resolve().unlink(missing_ok=True)

    main(
        [
            "--email",
            f"{username}@ucsd.edu",
            "--faculty-file",
            faculty_webpage,
            "--output",
            output_file,
            "--year",
            str(datetime.now().year),
        ]
    )

    # Check that the file was created.
    assert Path(output_file).resolve().is_file()
