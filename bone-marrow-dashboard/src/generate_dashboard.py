#!/usr/bin/env python3
"""
Dashboard Generator for Bone Marrow Operations Dashboard

Reads case data from CSV, calculates metrics, and generates an HTML dashboard
that can be exported to PDF.
"""

import csv
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import statistics


# Configuration - adjust these targets based on section expectations
CONFIG = {
    "tat_target_days": 3,           # Primary TAT target
    "lag_target_days": 1,           # Service responsiveness target
    "outlier_threshold_days": 7,    # TAT outlier threshold
    "target_met_threshold": 90,     # % for "good" performance
    "near_target_threshold": 75,    # % for "warning" performance
}


def load_data(filepath: str) -> List[Dict[str, Any]]:
    """Load case data from CSV file."""
    cases = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            row['tat_days'] = float(row['tat_days']) if row['tat_days'] else None
            row['flow_tat_days'] = float(row['flow_tat_days']) if row['flow_tat_days'] else None
            row['lag_days'] = float(row['lag_days']) if row['lag_days'] else None
            row['amendment_count'] = int(row['amendment_count']) if row['amendment_count'] else 0
            cases.append(row)
    return cases


def calculate_metrics(cases: List[Dict], category: str) -> Dict[str, Any]:
    """Calculate all metrics for a given category (Adult or Pediatric)."""

    # Filter cases by category
    filtered = [c for c in cases if c['patient_age_category'] == category]

    if not filtered:
        return get_empty_metrics()

    # Volume
    volume = len(filtered)

    # TAT metrics
    tat_values = [c['tat_days'] for c in filtered if c['tat_days'] is not None]
    tat_median = round(statistics.median(tat_values), 1) if tat_values else 0
    tat_p90 = round(percentile(tat_values, 90), 1) if tat_values else 0
    tat_within_target = sum(1 for t in tat_values if t <= CONFIG['tat_target_days'])
    tat_pct = round(tat_within_target / len(tat_values) * 100, 1) if tat_values else 0

    # Flow dependency metrics (only for cases with flow)
    flow_cases = [c for c in filtered if c['flow_ordered'] == 'Y' and c['flow_tat_days'] is not None]
    flow_values = [c['flow_tat_days'] for c in flow_cases]
    flow_median = round(statistics.median(flow_values), 1) if flow_values else 0
    flow_p90 = round(percentile(flow_values, 90), 1) if flow_values else 0

    # Service lag metrics (only for cases with flow)
    lag_cases = [c for c in filtered if c['flow_ordered'] == 'Y' and c['lag_days'] is not None]
    lag_values = [c['lag_days'] for c in lag_cases]
    lag_median = round(statistics.median(lag_values), 1) if lag_values else 0
    lag_p90 = round(percentile(lag_values, 90), 1) if lag_values else 0
    lag_within_target = sum(1 for t in lag_values if t <= CONFIG['lag_target_days'])
    lag_pct = round(lag_within_target / len(lag_values) * 100, 1) if lag_values else 0

    # Quality metrics
    amended = sum(1 for c in filtered if c['amendment_flag'] == 'Y')
    amended_rate = round(amended / volume * 100, 1) if volume else 0
    outliers = sum(1 for c in filtered if c['outlier_flag'] == 'Y')

    # Outlier drivers
    outlier_cases = [c for c in filtered if c['outlier_flag'] == 'Y']
    drivers = {
        'flow': sum(1 for c in outlier_cases if c['outlier_driver'] == 'Flow Delay'),
        'lag': sum(1 for c in outlier_cases if c['outlier_driver'] == 'Internal Lag'),
        'proc': sum(1 for c in outlier_cases if c['outlier_driver'] == 'Processing'),
        'other': sum(1 for c in outlier_cases if c['outlier_driver'] == 'Other'),
    }

    return {
        'volume': volume,
        'tat_median': tat_median,
        'tat_p90': tat_p90,
        'tat_pct': tat_pct,
        'tat_status': get_status(tat_pct),
        'flow_median': flow_median,
        'flow_p90': flow_p90,
        'lag_median': lag_median,
        'lag_p90': lag_p90,
        'lag_pct': lag_pct,
        'lag_status': get_status(lag_pct),
        'amended': amended,
        'amended_rate': amended_rate,
        'outliers': outliers,
        'drivers': drivers,
    }


def get_empty_metrics() -> Dict[str, Any]:
    """Return empty metrics structure for categories with no cases."""
    return {
        'volume': 0,
        'tat_median': 0,
        'tat_p90': 0,
        'tat_pct': 0,
        'tat_status': 'good',
        'flow_median': 0,
        'flow_p90': 0,
        'lag_median': 0,
        'lag_p90': 0,
        'lag_pct': 0,
        'lag_status': 'good',
        'amended': 0,
        'amended_rate': 0,
        'outliers': 0,
        'drivers': {'flow': 0, 'lag': 0, 'proc': 0, 'other': 0},
    }


def percentile(data: List[float], pct: float) -> float:
    """Calculate percentile of a list of values."""
    if not data:
        return 0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * pct / 100
    f = int(k)
    c = f + 1 if f + 1 < len(sorted_data) else f
    return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)


def get_status(pct: float) -> str:
    """Determine status based on percentage meeting target."""
    if pct >= CONFIG['target_met_threshold']:
        return 'good'
    elif pct >= CONFIG['near_target_threshold']:
        return 'warning'
    else:
        return 'alert'


def generate_dashboard(
    data_file: str,
    template_file: str,
    output_file: str,
    report_period: str,
    reviewer: str = "[Reviewer Name]",
    notes: str = ""
) -> str:
    """Generate the dashboard HTML from template and data."""

    # Load data
    cases = load_data(data_file)

    # Calculate metrics for each category
    adult = calculate_metrics(cases, 'Adult')
    peds = calculate_metrics(cases, 'Pediatric')

    # Load template
    with open(template_file, 'r') as f:
        template = f.read()

    # Prepare replacements
    replacements = {
        # Header
        '{{REPORT_PERIOD}}': report_period,
        '{{PREPARED_DATE}}': datetime.now().strftime('%Y-%m-%d'),
        '{{REVIEWER}}': reviewer,

        # Targets
        '{{TAT_TARGET}}': str(CONFIG['tat_target_days']),
        '{{LAG_TARGET}}': str(CONFIG['lag_target_days']),
        '{{OUTLIER_THRESHOLD}}': str(CONFIG['outlier_threshold_days']),

        # Adult metrics
        '{{ADULT_VOLUME}}': str(adult['volume']),
        '{{ADULT_TAT_MEDIAN}}': str(adult['tat_median']),
        '{{ADULT_TAT_P90}}': str(adult['tat_p90']),
        '{{ADULT_TAT_PCT}}': str(adult['tat_pct']),
        '{{ADULT_TAT_STATUS}}': adult['tat_status'],
        '{{ADULT_FLOW_MEDIAN}}': str(adult['flow_median']),
        '{{ADULT_FLOW_P90}}': str(adult['flow_p90']),
        '{{ADULT_LAG_MEDIAN}}': str(adult['lag_median']),
        '{{ADULT_LAG_P90}}': str(adult['lag_p90']),
        '{{ADULT_LAG_PCT}}': str(adult['lag_pct']),
        '{{ADULT_LAG_STATUS}}': adult['lag_status'],
        '{{ADULT_AMENDED}}': str(adult['amended']),
        '{{ADULT_AMENDED_RATE}}': str(adult['amended_rate']),
        '{{ADULT_OUTLIERS}}': str(adult['outliers']),

        # Adult drivers
        '{{ADULT_DRIVER_FLOW}}': str(adult['drivers']['flow']),
        '{{ADULT_DRIVER_LAG}}': str(adult['drivers']['lag']),
        '{{ADULT_DRIVER_PROC}}': str(adult['drivers']['proc']),
        '{{ADULT_DRIVER_OTHER}}': str(adult['drivers']['other']),

        # Pediatric metrics
        '{{PEDS_VOLUME}}': str(peds['volume']),
        '{{PEDS_TAT_MEDIAN}}': str(peds['tat_median']),
        '{{PEDS_TAT_P90}}': str(peds['tat_p90']),
        '{{PEDS_TAT_PCT}}': str(peds['tat_pct']),
        '{{PEDS_TAT_STATUS}}': peds['tat_status'],
        '{{PEDS_FLOW_MEDIAN}}': str(peds['flow_median']),
        '{{PEDS_FLOW_P90}}': str(peds['flow_p90']),
        '{{PEDS_LAG_MEDIAN}}': str(peds['lag_median']),
        '{{PEDS_LAG_P90}}': str(peds['lag_p90']),
        '{{PEDS_LAG_PCT}}': str(peds['lag_pct']),
        '{{PEDS_LAG_STATUS}}': peds['lag_status'],
        '{{PEDS_AMENDED}}': str(peds['amended']),
        '{{PEDS_AMENDED_RATE}}': str(peds['amended_rate']),
        '{{PEDS_OUTLIERS}}': str(peds['outliers']),

        # Pediatric drivers
        '{{PEDS_DRIVER_FLOW}}': str(peds['drivers']['flow']),
        '{{PEDS_DRIVER_LAG}}': str(peds['drivers']['lag']),
        '{{PEDS_DRIVER_PROC}}': str(peds['drivers']['proc']),
        '{{PEDS_DRIVER_OTHER}}': str(peds['drivers']['other']),

        # Combined drivers
        '{{TOTAL_DRIVER_FLOW}}': str(adult['drivers']['flow'] + peds['drivers']['flow']),
        '{{TOTAL_DRIVER_LAG}}': str(adult['drivers']['lag'] + peds['drivers']['lag']),
        '{{TOTAL_DRIVER_PROC}}': str(adult['drivers']['proc'] + peds['drivers']['proc']),
        '{{TOTAL_DRIVER_OTHER}}': str(adult['drivers']['other'] + peds['drivers']['other']),

        # Notes
        '{{NOTES_DISPLAY}}': 'block' if notes else 'none',
        '{{NOTES_CONTENT}}': notes or '',
    }

    # Apply replacements
    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)

    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"Dashboard generated: {output_path}")
    print(f"  Adult cases: {adult['volume']}, Pediatric cases: {peds['volume']}")
    print(f"  Adult TAT: {adult['tat_median']}d median, {adult['tat_pct']}% within target")
    print(f"  Peds TAT: {peds['tat_median']}d median, {peds['tat_pct']}% within target")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Bone Marrow Operations Dashboard"
    )
    parser.add_argument(
        "--data", "-d",
        type=str,
        required=True,
        help="Path to CSV data file"
    )
    parser.add_argument(
        "--template", "-t",
        type=str,
        default="templates/dashboard.html",
        help="Path to HTML template (default: templates/dashboard.html)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output/dashboard.html",
        help="Output file path (default: output/dashboard.html)"
    )
    parser.add_argument(
        "--period", "-p",
        type=str,
        default=None,
        help="Report period label (e.g., 'December 2024')"
    )
    parser.add_argument(
        "--reviewer", "-r",
        type=str,
        default="[Reviewer Name]",
        help="Reviewer name for dashboard footer"
    )
    parser.add_argument(
        "--notes", "-n",
        type=str,
        default="",
        help="Notes/action items to include on dashboard"
    )

    args = parser.parse_args()

    # Default period if not specified
    if args.period is None:
        today = datetime.now()
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1
        args.period = datetime(prev_year, prev_month, 1).strftime('%B %Y')

    generate_dashboard(
        data_file=args.data,
        template_file=args.template,
        output_file=args.output,
        report_period=args.period,
        reviewer=args.reviewer,
        notes=args.notes
    )


if __name__ == "__main__":
    main()
