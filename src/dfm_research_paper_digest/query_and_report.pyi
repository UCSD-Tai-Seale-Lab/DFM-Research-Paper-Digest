import logging
from dataclasses import dataclass
from datetime import datetime

from dfm_research_paper_digest import Author

@dataclass
class DataRequestDetails:
    author: Author
    faculty_file: str
    year: int

    def __init__(
        self, author: Author, faculty_file: str, year: int = datetime.now().year
    ) -> None: ...

def query_and_report(
    contact_email: str = None,
    log: logging.Logger = None,
    output_file: str = None,
    data_request: DataRequestDetails = None,
) -> None: ...
def main(argv=None) -> None: ...
