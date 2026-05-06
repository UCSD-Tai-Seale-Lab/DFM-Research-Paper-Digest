"""
Exercises my_logging.py
"""

from logging import Logger

from dfm_research_paper_digest import setup_logging


def test_my_logging_no_file():
    my_log: Logger = setup_logging()

    assert isinstance(my_log, Logger)
