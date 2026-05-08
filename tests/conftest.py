import logging
import os
import sys

import pytest


@pytest.fixture(name="pmid_with_corporate_author")
def pmid_with_corporate_author() -> str:
    return "40465838"


@pytest.fixture(name="logger")
def logger(tmp_path) -> logging.Logger:
    """
    Synthesizes a log object for testing.

    Returns
    -------
    log: logging.Logger
    """
    log_filename: str = os.path.join(tmp_path, "testing.log")
    logger = logging.getLogger(log_filename)

    # Logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(module)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Logging to a file
    logfile_format = logging.Formatter(
        fmt="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logfile_handler = logging.FileHandler(log_filename)
    logfile_handler.setFormatter(logfile_format)
    logger.addHandler(logfile_handler)

    logger.setLevel(logging.DEBUG)
    return logger


@pytest.fixture(name="sample_faculty_list")
def sample_faculty_list() -> list[str]:
    return [
        "Tai-Seale, PhD, MPH",
        "Wu, Jennifer, MD",
        "Cheng, Terri, MD",
        "Celebi, Julie, MD",
    ]


@pytest.fixture(name="username")
def user() -> str:
    return os.getlogin()
