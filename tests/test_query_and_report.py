from datetime import datetime
from importlib.resources import as_file, files
from pathlib import Path

from dfm_research_paper_digest import Author
from dfm_research_paper_digest.query_and_report import (
    DataRequestDetails,
    main,
    query_and_report,
)


def test_query_and_report_I(username):
    # Intentionally omit '.html' suffix to exercise code that automatically appends it.
    output_file: str = r"C:\Family Medicine\Publication Output\results\ming_report"
    Path(output_file).unlink(missing_ok=True)
    main(
        [
            "Ming Tai-Seale",
            "--year",
            "2025",
            "--output",
            output_file,
            "--email",
            f"{username}@health.ucsd.edu",
        ]
    )

    # Check that the file was created.
    assert Path(f"{output_file}.html").is_file()


def test_query_and_report_II():
    main(["Gene Kallenberg", "--year", "2024"])


def test_query_and_report_pathological():
    main(["Nowhere Nothing", "--year", "3000"])


def test_query_and_report_III():
    author: Author = Author("Al-Delaimy, Wael MD, PhD")
    output_file: str = r"C:\Family Medicine\Publication Output\results\aldelaimy_report"
    Path(output_file).unlink(missing_ok=True)
    resource_path = files("data").joinpath("faculty_list.txt")

    # Exercise calling routine without log file.
    with as_file(resource_path) as filename:
        data_request = DataRequestDetails(author=author, faculty_file=str(filename))
        query_and_report(
            data_request=data_request,
            output_file=output_file,
        )

    # Check that the file was created.
    assert Path(f"{output_file}.html").is_file()
