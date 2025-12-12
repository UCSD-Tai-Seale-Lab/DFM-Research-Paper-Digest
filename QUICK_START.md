# Quick Start Guide

## Setup (One Time)

```bash
# Navigate to project directory
cd "/Users/mihirjagtap/Documents/Ming DFM Research"

# Activate virtual environment
source venv/bin/activate
```

## Single Author Queries (One Command!)

### Basic Query - Generates HTML Report
```bash
# Query and generate report in one command!
python query_and_report.py "Tai-Seale M"

# Different year
python query_and_report.py "Kallenberg G" --year 2024

# Custom output filename
python query_and_report.py "Wu J" --output jennifer_wu

# With email (recommended by NCBI)
python query_and_report.py "Ming Tai-Seale" --email your@email.com
```

**That's it!** Opens HTML report with:
- ✨ **All authors listed** (no "et al.")
- 🔍 **DFM faculty highlighted** in bold with blue background
- 📅 **Publication dates**
- 🔗 **Clickable PubMed links**

## Batch Faculty Queries

### Query Multiple Faculty from File
```bash
# Use the provided faculty_list.txt (94 faculty members)
# This generates BOTH CSV and HTML report
python query_faculty_batch.py --faculty-file faculty_list.txt --year 2025 --output all_faculty_2025

# Use a custom/smaller list
python query_faculty_batch.py --faculty-file sample_faculty.txt --year 2025 --output sample_results

# With email (recommended by NCBI)
python query_faculty_batch.py --faculty-file faculty_list.txt --email your@email.com --output results
```

**Output:** This generates:
- `output_name.csv` - CSV with all publication data  
- `output_name.html` - **Beautiful HTML report with DFM faculty highlighted!**

### Faculty List Format
Create a text file with one faculty member per line:
```
MacDonald, Kaimana, MD
Tai-Seale, PhD, MPH
Wu, Jennifer, MD
```

**Important**: The system handles the edge case where only lastname + qualification is present (like "Tai-Seale, PhD, MPH")

## Email Reports

### Send Text Summary (No Attachment)
```bash
# Sends publication list directly in email body
python query_and_report.py "Gene Kallenberg" \
  --send-email \
  --email-to recipient@email.com \
  --email-from your@gmail.com

# Will prompt for password securely
```

### Send HTML Report as Attachment
```bash
# Sends formatted HTML report as attachment
python query_and_report.py "Ming Tai-Seale" \
  --send-email \
  --email-to recipient@email.com \
  --email-from your@gmail.com \
  --email-format html
```

### Email Providers
```bash
# Gmail (default)
--email-provider gmail

# Outlook
--email-provider outlook

# Yahoo
--email-provider yahoo

# UCSD email
--email-provider ucsd
```

**📧 Email Authentication:**
- Most providers: Use your regular email password
- Gmail: Regular password works (or app-specific password if 2FA is enabled)
- Outlook/Yahoo/UCSD: Regular password works fine

## HTML Report Features

The HTML report includes:
- ✨ **ALL authors listed** (no more "et al.")
- 🔍 **DFM faculty members highlighted in bold with blue background**
- 📊 Summary statistics (total pubs, unique faculty, etc.)
- 🔗 Direct clickable links to PubMed
- 📱 Responsive design (works on mobile/tablet)
- 🖨️ Print-friendly formatting

## Quick Examples

```bash
# All these name formats work!
python query_and_report.py "Kallenberg G"           # PubMed format
python query_and_report.py "Gene Kallenberg"        # Natural format (auto-converts)
python query_and_report.py "Kallenberg, Gene, MD"   # Faculty list format (auto-converts)

# More examples
python query_and_report.py "Ming Tai-Seale"
python query_and_report.py "Jennifer Wu"
python query_and_report.py "Terri Cheng"

# Different year
python query_and_report.py "Gene Kallenberg" --year 2024

# With email (recommended)
python query_and_report.py "Ming Tai-Seale" --email your@email.com
```

## Output Files

HTML reports include:
- ✨ Complete author lists (no truncation)
- 🎯 DFM faculty highlighted in **bold with blue background**
- 📅 Publication dates
- 📊 Summary statistics
- 🔗 Clickable PubMed links

## Tips

1. **Always use quotes** around author names: `"Gene Kallenberg"`
2. **Any name format works!** The tool auto-converts:
   - `"Gene Kallenberg"` → `"Kallenberg G"`
   - `"Kallenberg, Gene, MD"` → `"Kallenberg G"`
   - `"Kallenberg G"` → works as-is
3. The tool limits results to 100 publications per author
4. NCBI recommends providing your email for API tracking

## Troubleshooting

If you get module errors, make sure the virtual environment is activated:
```bash
source venv/bin/activate
```

If you need to reinstall dependencies:
```bash
pip install -r requirements.txt
```

