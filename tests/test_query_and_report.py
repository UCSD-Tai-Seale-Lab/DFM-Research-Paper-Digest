from dfm_research_paper_digest.query_and_report import main


def test_query_and_report_I(username):
    main(
        [
            "Ming Tai-Seale",
            "--year",
            "2025",
            "--output",
            r"C:\Family Medicine\Publication Output\ming_report",
        ]
    )


def test_query_and_report_II(username):
    main(["Gene Kallenberg", "--year", "2024"])
