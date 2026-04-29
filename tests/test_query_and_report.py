from dfm_research_paper_digest.query_and_report import main


def test_query_and_report(user):
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
            f"--email-to {user}@ucsd.edu",
            f"--email-from {user}@ucsd.edu",
        ]
    )
