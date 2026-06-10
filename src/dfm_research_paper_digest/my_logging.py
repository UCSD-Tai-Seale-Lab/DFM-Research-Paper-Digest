"""
Allows other projects to easily use logging.
"""

from __future__ import annotations

import inspect
import logging
import logging.handlers
import sys
from pathlib import Path

import streamlit


def setup_logging(log_filename: str | Path | None = None) -> logging.Logger:
    """

    Parameters
    ----------
    log_filename : Optional str Desired name of the log file.
                    Can be either a full path or just a filename.

    Returns
    -------
    logger : logging.Logger object to be used in calling routine.

    """
    #       Clear up any old stuff.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if not log_filename:
        #   If user didn't supply a filename, create it with the calling module's name.
        #   (Don't use calling >function<, as it will likely be '__init__', which tells us nothing.
        frame_records = inspect.stack()[1]
        calling_module = inspect.getmodulename(frame_records[1])
        log_filename = f"AoU_{calling_module}.log"

    # Ensure the path to the log file exists.
    file_path: Path

    if isinstance(log_filename, Path):
        file_path = log_filename
    else:
        file_path = Path(log_filename)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    #   Create the logger object named after the filename.
    logger = logging.getLogger(file_path.name)
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter("%(module)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    # New log for every day; discard logs > 30 days old.
    logfile_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(file_path),
        when="D",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        delay=False,
    )
    logfile_format = logging.Formatter(
        fmt="%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    logfile_handler.setFormatter(logfile_format)

    logger.addHandler(console_handler)
    logger.addHandler(logfile_handler)
    logger.setLevel(logging.INFO)
    return logger


@streamlit.cache_resource
def setup_streamlit_logging() -> logging.Logger:
    """
        Setup logging in Streamlit

    Returns
    -------
    log: logging.Logger object
    """
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if not logger.handlers:
        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
