from dfm_research_paper_digest.query_and_report import main


def test_query_and_report(username):
    main(
        [
            "Ming Tai-Seale",
            "--year",
            "2025",
            "--output",
            r"C:\Family Medicine\Publication Output\ming_report",
        ]
    )
    main(["Wu J", "--year", "2024"])
    main(
        [
            "Gene Kallenberg",
            "--send-email",
            "--email-to",
            f"{username}@ucsd.edu",
            "--email-from",
            f"{username}@ucsd.edu",
        ]
    )
