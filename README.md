# PubMed Author Publications Query Tool
![GitHub last commit](https://img.shields.io/github/last-commit/UCSD-Tai-Seale-Lab/DFM-Research-Paper-Digest)

A Python tool to query [PubMed](https://pubmed.ncbi.nlm.nih.gov/) for publications by specific authors.

## Features

- **Single Author Queries**: Search PubMed for publications by individual authors
- **Batch Faculty Queries**: Query multiple faculty members at once from a file
- **Faculty Name Parser**: Handles various name formats including edge cases
  - Standard: "Lastname, Firstname, Qualification" (e.g., "MacDonald, Kaimana, MD")
  - Edge case: "Lastname, Qualification" (e.g., "Tai-Seale, PhD, MPH")
- **Complete Author Lists**: Retrieves ALL authors (no "et al." truncation)
- **HTML Report Generation**: Creates beautiful, formatted reports with:
  - ✨ DFM faculty members **highlighted in bold with blue background**
  - 📊 Summary statistics and visualizations
  - 🔗 Clickable links to PubMed
  - 📱 Responsive design for any device
  - 🖨️ Print-friendly formatting
- **Flexible Output**: Export to both CSV and HTML formats
- **Filter by Year**: Defaults to 2025, customizable to any year
- **Publication Details**: Retrieve:
  - Publication title
  - Year of publication
  - Journal name
  - Complete author list (all authors, not truncated)
  - PubMed ID (PMID)
  - Direct link to PubMed article
  - Faculty information (in batch mode)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the script with author name(s) as arguments:

```bash
# Activate virtual environment first
source venv/bin/activate

# Query single author
python pubmed_query.py "Ming Tai-Seale"

# Query with email (recommended by NCBI)
python pubmed_query.py "Smith J" --email your.email@example.com

# Query multiple authors
python pubmed_query.py "Zhang Y" "Li Y" "Xie B"

# Query different year
python pubmed_query.py "Smith J" --year 2024

# Export to CSV (auto-generated filename)
python pubmed_query.py "Ming Tai-Seale" --output csv

# Export to CSV with custom filename
python pubmed_query.py "Ming Tai-Seale" --output csv --filename my_results
```

### Command Line Options

```
usage: pubmed_query.py [-h] [--email EMAIL] [--year YEAR] [--output {text,csv}]
                       [--filename FILENAME] authors [authors ...]

positional arguments:
  authors               Author name(s) to search for

optional arguments:
  -h, --help           Show help message and exit
  --email, -e EMAIL    Your email address (optional, recommended by NCBI)
  --year, -y YEAR      Publication year to search (default: 2025)
  --output, -o {text,csv}
                       Output format: text or csv (default: text)
  --filename, -f FILENAME
                       Custom output filename for CSV
```

### CSV Export Format

When using `--output csv`, the file will contain the following columns:
- **title**: Publication title
- **authors**: List of authors (first 3 + "et al." if more)
- **journal**: Journal name
- **year**: Publication year
- **pmid**: PubMed ID
- **url**: Direct link to the PubMed article

The CSV file can be opened in Excel, Google Sheets, or any spreadsheet application.

### Example Output

```bash
$ python pubmed_query.py "Ming Tai-Seale"

================================================================================
PubMed Author Publications Query Tool
================================================================================

Searching PubMed for publications by 'Ming Tai-Seale' from 2025...
Found 5 publication(s).

================================================================================
Found 5 publication(s):
================================================================================

1. Telehealth Emergency Department Transition-of-care Program: A Value-based Innovation.
   Authors: Allyson Kreshak, Itzik Fadlon, Karna Malaviya, et al.
   Journal: The western journal of emergency medicine
   Year: 2025
   PMID: 41193006
   URL: https://pubmed.ncbi.nlm.nih.gov/41193006/
...
```

## Batch Faculty Queries

Query multiple faculty members at once using a text file.

### Prepare Faculty List File

Create a text file (`faculty_list.txt`) with one faculty name per line in the format:
```
Lastname, Firstname, Qualification
```

Example `faculty_list.txt`:
```
MacDonald, Kaimana, MD
Tai-Seale, PhD, MPH
Wu, Jennifer, MD
Cheng, Terri, MD
```

**Note**: The parser handles the edge case where only lastname and qualification are present (like "Tai-Seale, PhD, MPH").

### Run Batch Query

```bash
# Activate virtual environment
source venv/bin/activate

# Query all faculty from file
python query_faculty_batch.py --faculty-file faculty_list.txt --year 2025 --output results

# With email (recommended)
python query_faculty_batch.py --faculty-file faculty_list.txt --email your@email.com --output faculty_2025
```

### Batch Query Output

Running batch queries generates **TWO output files**:

#### 1. CSV File (`output_name.csv`)
Includes columns for faculty tracking:
- `faculty_name`: Original faculty name from input file
- `faculty_lastname`: Parsed last name
- `faculty_firstname`: Parsed first name (empty for edge cases like Tai-Seale)
- `title`: Publication title
- `authors`: Complete list of ALL authors (no truncation)
- `journal`: Journal name
- `year`: Publication year
- `pmid`: PubMed ID
- `url`: Direct PubMed link

#### 2. HTML Report (`output_name.html`)
Beautiful, formatted report featuring:
- **✨ Highlighted DFM Faculty**: Authors who are DFM faculty members appear in **bold with blue background**
- **Complete Author Lists**: ALL authors displayed (no "et al.")
- **Summary Dashboard**: Total publications, unique faculty count, etc.
- **Clickable PubMed Links**: Direct links to each publication
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Print-Friendly**: Optimized formatting for printing

### Generate Report from Existing CSV

If you already have a CSV file and want to generate just the HTML report:

```bash
python generate_report_from_csv.py your_file.csv \
  --faculty-file faculty_list.txt \
  --output report.html \
  --title "My Custom Report Title"
```

### Programmatic Usage

You can also use the `PubMedQuery` class in your own Python scripts:

```python
from pubmed_query import PubMedQuery

# Initialize the query object
query = PubMedQuery(email="your.email@example.com")

# Query for author publications from 2025
publications = query.query_author("Smith J", year=2025)

# Access publication details
for pub in publications:
    print(f"Title: {pub['title']}")
    print(f"Year: {pub['year']}")
    print(f"PMID: {pub['pmid']}")
```

## API Information

This tool uses the [NCBI E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/) to query PubMed:
- **ESearch**: Search and retrieve PubMed IDs (PMIDs)
- **EFetch**: Fetch detailed publication information

### Rate Limits

- NCBI recommends no more than 3 requests per second
- Providing an email address helps NCBI contact you if there are issues
- The script automatically handles rate limiting

## Author Name Formats

The tool accepts various author name formats:
- Last name with initial: `"Smith J"`
- Full name: `"John Smith"`
- Last name only: `"Smith"`

## Customization

To search for different years, modify the `year` parameter:

```python
publications = query.query_author("Smith J", year=2024)
```

## Notes

- Results are limited to 100 publications per query
- The tool only retrieves publications from the specified year (default: 2025)
- All results include direct links to the PubMed website

## License

This tool is provided as-is for research purposes.

