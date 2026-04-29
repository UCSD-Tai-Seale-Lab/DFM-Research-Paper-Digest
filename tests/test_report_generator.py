from importlib.resources import as_file, files
from pathlib import Path

from src.dfm_research_paper_digest.faculty import Faculty
from src.dfm_research_paper_digest.publication import Article, PubmedArticleSet
from src.dfm_research_paper_digest.report_generator import ReportGenerator


def test_report_generator(fake_pubmed_dict_two_articles, logger):
    resource_path = files("src.dfm_research_paper_digest.data").joinpath(
        "faculty_list.txt"
    )

    with as_file(resource_path) as filename:
        faculty: Faculty = Faculty(filename, logger)
        report_gen = ReportGenerator(faculty, logger)
        assert isinstance(report_gen, ReportGenerator)

        pubmed_articleset: PubmedArticleSet = PubmedArticleSet(
            fake_pubmed_dict_two_articles
        )
        assert isinstance(pubmed_articleset, PubmedArticleSet)
        articles: list[Article] = pubmed_articleset.articles

        # Delete proposed output file if it already exists.
        output_file: str = r"C:\Family Medicine\Publication Output\test.html"
        Path(output_file).unlink(missing_ok=True)

        report_gen.generate_html_report(
            publications=articles,
            output_file=output_file,
            title=f"Test Report ({2026})",
        )

        # Check that the file was created.
        assert Path(output_file).is_file()
