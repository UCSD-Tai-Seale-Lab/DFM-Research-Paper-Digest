from pathlib import Path
from dfm_research_paper_digest.query_and_report import main


def test_query_and_report_I(username):
    output_file: str = r"C:\Family Medicine\Publication Output\results\ming_report"
    Path(output_file).unlink(missing_ok=True)
    main(
        [
            "Ming Tai-Seale",
            "--year",
            "2025",
            "--output",
            output_file,
        ]
    )

    # Check that the file was created.
    assert Path(output_file).is_file()


def test_query_and_report_II(username):
    main(["Gene Kallenberg", "--year", "2024"])
