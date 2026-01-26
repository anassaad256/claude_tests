# Bone Marrow Service Operations Dashboard

A PHI-free monthly operations dashboard for monitoring turnaround time and workflow metrics in the Hematopathology Bone Marrow Service, with separate tracking for Adult and Pediatric cases.

## Overview

This project provides tools to generate a 1-page monthly dashboard that tracks:
- **Volume**: Adult and Pediatric bone marrow case counts
- **Primary TAT**: Accession to final sign-out turnaround time
- **Flow Dependency**: Time for external flow cytometry results
- **Service Responsiveness**: Internal lag from flow result to sign-out
- **Quality Indicators**: Amendment rates and TAT outlier analysis

## Project Structure

```
bone-marrow-dashboard/
├── README.md                           # This file
├── docs/
│   └── metric_dictionary_governance.md # Metric definitions & governance
├── templates/
│   └── dashboard.html                  # Dashboard HTML template
├── src/
│   ├── config.py                       # Configuration settings
│   ├── sample_data_generator.py        # Generate test data
│   └── generate_dashboard.py           # Dashboard generation script
├── data/                               # Input data files (CSV)
└── output/                             # Generated dashboards
```

## Quick Start

### 1. Generate Sample Data (for testing)

```bash
cd bone-marrow-dashboard
python src/sample_data_generator.py --year 2024 --month 12 --seed 42
```

This creates `data/bm_cases_2024_12.csv` with synthetic case data.

### 2. Generate Dashboard

```bash
python src/generate_dashboard.py \
  --data data/bm_cases_2024_12.csv \
  --period "December 2024" \
  --reviewer "Dr. Smith" \
  --output output/dashboard_2024_12.html
```

### 3. Export to PDF

Open the generated HTML file in a browser and use Print → Save as PDF, or use a command-line tool:

```bash
# Using wkhtmltopdf (if installed)
wkhtmltopdf output/dashboard_2024_12.html output/dashboard_2024_12.pdf

# Or using Chrome headless
google-chrome --headless --print-to-pdf=output/dashboard_2024_12.pdf output/dashboard_2024_12.html
```

## Using with Real Data

### Data Requirements

Export the following fields from CoPath/LIS (PHI-free):

| Field | Description | Format |
|-------|-------------|--------|
| patient_age_category | Adult or Pediatric | Text |
| specimen_type | Should be "Bone Marrow" | Text |
| accession_datetime | Accession date/time | YYYY-MM-DD HH:MM |
| flow_ordered | Was flow cytometry ordered | Y/N |
| flow_result_datetime | Flow result received | YYYY-MM-DD HH:MM |
| signout_datetime | Final sign-out | YYYY-MM-DD HH:MM |
| amendment_flag | Report amended | Y/N |
| amendment_count | Number of amendments | Integer |

### PHI Handling

1. Use accession numbers only for timestamp linking during data preparation
2. Remove accession numbers before saving final CSV
3. Never include patient name, MRN, DOB, or other identifiers
4. Final output contains only aggregate statistics

## Configuration

Edit `src/config.py` or pass arguments to adjust:

| Setting | Default | Description |
|---------|---------|-------------|
| TAT_TARGET_DAYS | 3 | Primary TAT target |
| LAG_TARGET_DAYS | 1 | Internal responsiveness target |
| OUTLIER_THRESHOLD_DAYS | 7 | Threshold for outlier identification |
| TARGET_MET_THRESHOLD | 90% | Green performance level |
| NEAR_TARGET_THRESHOLD | 75% | Yellow warning level |

## Monthly Workflow

1. **By 5th business day**: Export PHI-free data from CoPath
2. **By 7th business day**: Process data, validate quality
3. **By 10th business day**: Generate dashboard, review with faculty
4. **Monthly meeting**: Present at section QA meeting

## Dashboard Features

- **Side-by-side comparison**: Adult vs Pediatric metrics
- **Color-coded performance**: Green (target met), Yellow (near target), Red (below target)
- **Outlier analysis**: Driver categorization (Flow delay, Internal lag, Processing, Other)
- **Notes section**: Optional action items and commentary
- **Print-ready**: Optimized for 1-page PDF export

## Documentation

See `docs/metric_dictionary_governance.md` for:
- Complete metric definitions
- Calculation methods
- Target rationale
- Governance framework
- Review cadence
- Change control procedures

## Dependencies

- Python 3.7+
- No external packages required (uses only standard library)

## License

Internal use only - DMC/WSU Hematopathology Section
