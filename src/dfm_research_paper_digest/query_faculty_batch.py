#!/usr/bin/env python3
"""
Batch Faculty Publications Query
Queries PubMed for publications from multiple faculty members
"""
from __future__ import annotations

# pylint: disable=import-error, import-outside-toplevel
import logging
import time
from datetime import datetime
from importlib.resources import as_file, files

import streamlit
from metapub import PubMedArticle

from src.dfm_research_paper_digest import (
    Faculty,
    PubMedQuery,
    setup_logging,
)


def __assemble_article_list(
    query: PubMedQuery,
    faculty: Faculty,
    year: int,
    log: logging.Logger,
    progress_bar: streamlit.progress = None,
) -> list[PubMedArticle]:
    """
        Runs query for each author & assembles list of articles.

    Parameters
    ----------
    query: PubMedQuery object
    faculty: Faculty object
    year: int
    log: logging.Logger
    progress_bar: streamlit.progress object

    Returns
    -------
    articles: list[PubMedArticle]
    """
    i: int = 0
    all_results: list[PubMedArticle] = []
    pct_completion: int = 0

    # Query each faculty member
    for author in faculty.authors:
        if progress_bar:
            pct_completion = int(100.0 * i / faculty.num)
            progress_bar.progress(pct_completion, f"Querying {author.original}")

        i += 1
        log.info(f"[{i}/{faculty.num}] Querying: {author.original}")

        try:
            articles: list[PubMedArticle] = query.query_by_author(
                author.pubmed_style, year=year
            )

            if articles and len(articles) > 0:
                all_results.extend(articles)
                log.info(f"    Found: {len(articles)} publication(s)")

        except Exception as e:
            log.exception(f"    Error: {e}")

        # Rate limiting: NCBI recommends max 3 requests per second
        if i < faculty.num:
            time.sleep(0.33)

    # Summary
    log.info("SUMMARY")
    log.info(f"Total faculty queried: {faculty.num}")
    log.info(f"Total publications found: {len(all_results)}")

    return __eliminate_duplicates(all_results)


def __eliminate_duplicates(articles: list[PubMedArticle]) -> list[PubMedArticle]:
    """
        Remove duplicate entries in article list.

    Parameters
    ----------
    articles: list[PubMedArticle]

    Returns
    -------
    unique_list: list[PubMedArticle]
    """
    seen: set = set()
    unique_list: list = []

    for obj in articles:
        if obj.pmid not in seen:
            unique_list.append(obj)
            seen.add(obj.pmid)

    return unique_list


def run_batch_report(
    contact_email: str = None,
    faculty_list_file: str | list[str] = None,
    log: logging.Logger = None,
    progress_bar: streamlit.progress = None,
    year: int = datetime.now().year,
) -> str:
    """
    Query PubMed for multiple faculty members and combine results.

    Args:
        contact_email: Optional email for NCBI API
        faculty_list_file: webpage OR list of faculty names
        log: logging.Logger object (default: None, in which case we create our own)
        output_file: Optional CSV filename for output
        progress_bar: streamlit progress object
        year: Publication year (default: current year)

    Returns:
        html: str
    """
    from src.dfm_research_paper_digest.report_generator import ReportGenerator

    if not log:
        resource_path = files("logs").joinpath("query_faculty_batch.log")

        with as_file(resource_path) as log_filename:
            log = setup_logging(log_filename=log_filename)

    # Parse faculty names.
    faculty: Faculty = Faculty(faculty_list_file, log)
    log.info("Querying PubMed for %d faculty members (%d)", faculty.num, year)

    # Initialize PubMed query
    query: PubMedQuery = PubMedQuery(faculty=faculty, email=contact_email, log=log)

    # Store results
    all_results: list[PubMedArticle] = __assemble_article_list(
        query, faculty, year, log, progress_bar
    )

    log.info("Generating HTML content.")
    report_gen: ReportGenerator = ReportGenerator(faculty, log)
    html: str = report_gen.generate_html_content(
        publications=all_results,
        title=f"DFM Faculty Publications Report ({year})",
    )
    return html


if __name__ == "__main__":
    pass
