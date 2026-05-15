# PubMed Author Publications Query Tool
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Coverage Status](./.github/badges/coverage-badge.svg?dummy=8484744)
![Pylint](./.github/badges/pylint-badge.svg?dummy=8484744)](https://github.com/psf/black)
![GitHub last commit](https://img.shields.io/github/last-commit/UCSD-Tai-Seale-Lab/DFM-Research-Paper-Digest)

A Python tool to query [PubMed](https://pubmed.ncbi.nlm.nih.gov/) for publications by specific authors--or all Department of Family Medicine faculty.

![image info](./pictures/result.png) 

## Features
  - Easy web interface
  - ✨ DFM faculty members **highlighted in bold with blue background**
  - 📊 Summary statistics and visualizations
  - 🔗 Clickable links to PubMed
  - 📱 Responsive design for any device
  - 🖨️ Print-friendly formatting

## Usage

Go to https://dfm-publications-report.streamlit.app/ and select the faculty names and years, then click "Create report"

![image info](./pictures/app.png) 


## Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## API Information

This tool uses the Python [metapub](https://metapub.org/) library to handle PubMed interface.


## License

See the [LICENSE](LICENSE) file for details.

