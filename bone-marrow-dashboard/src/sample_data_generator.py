#!/usr/bin/env python3
"""
Sample Data Generator for Bone Marrow Dashboard
Generates PHI-free synthetic data for testing and demonstration purposes.

This script creates realistic sample data that mirrors the structure of
CoPath exports without any actual patient information.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
import argparse


def generate_sample_data(
    year: int,
    month: int,
    adult_count: int = 45,
    peds_count: int = 12,
    output_dir: str = "data"
) -> str:
    """
    Generate synthetic bone marrow case data for a given month.

    Args:
        year: Report year
        month: Report month (1-12)
        adult_count: Number of adult cases to generate
        peds_count: Number of pediatric cases to generate
        output_dir: Directory for output file

    Returns:
        Path to generated CSV file
    """

    # Determine month boundaries
    if month == 12:
        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    days_in_month = (end_date - start_date).days + 1

    cases = []

    # Generate adult cases
    for i in range(adult_count):
        case = generate_case(
            case_num=i + 1,
            category="Adult",
            start_date=start_date,
            days_in_month=days_in_month
        )
        cases.append(case)

    # Generate pediatric cases
    for i in range(peds_count):
        case = generate_case(
            case_num=adult_count + i + 1,
            category="Pediatric",
            start_date=start_date,
            days_in_month=days_in_month
        )
        cases.append(case)

    # Shuffle cases to mix adult and pediatric
    random.shuffle(cases)

    # Create output directory if needed
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write to CSV
    filename = output_path / f"bm_cases_{year}_{month:02d}.csv"

    fieldnames = [
        "patient_age_category",
        "specimen_type",
        "accession_datetime",
        "flow_ordered",
        "flow_result_datetime",
        "signout_datetime",
        "tat_days",
        "flow_tat_days",
        "lag_days",
        "amendment_flag",
        "amendment_count",
        "outlier_flag",
        "outlier_driver"
    ]

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)

    print(f"Generated {len(cases)} cases ({adult_count} adult, {peds_count} pediatric)")
    print(f"Output: {filename}")

    return str(filename)


def generate_case(
    case_num: int,
    category: str,
    start_date: datetime,
    days_in_month: int
) -> dict:
    """Generate a single synthetic case with realistic timing patterns."""

    # Random accession date within the month (weighted toward earlier in month)
    accession_day = min(
        int(random.triangular(1, days_in_month, days_in_month * 0.4)),
        days_in_month - 5  # Ensure enough time for sign-out within month
    )
    accession_hour = random.randint(7, 17)
    accession_minute = random.randint(0, 59)

    accession_dt = start_date + timedelta(
        days=accession_day - 1,
        hours=accession_hour,
        minutes=accession_minute
    )

    # Determine if flow cytometry was ordered (most cases have flow)
    flow_ordered = random.random() < 0.85

    if flow_ordered:
        # Flow result timing: typically 1-3 days, occasionally longer
        # Simulating send-out lab variability
        if random.random() < 0.10:  # 10% chance of significant delay
            flow_days = random.uniform(4, 7)
        elif random.random() < 0.20:  # 20% chance of moderate delay
            flow_days = random.uniform(2.5, 4)
        else:  # Normal timing
            flow_days = random.uniform(1, 2.5)

        flow_result_dt = accession_dt + timedelta(days=flow_days)

        # Service lag: time from flow result to sign-out
        # Typically same day or next day, occasionally longer
        if random.random() < 0.08:  # 8% internal delay
            lag_days = random.uniform(2, 4)
        elif random.random() < 0.15:
            lag_days = random.uniform(1, 2)
        else:
            lag_days = random.uniform(0.1, 1)

        signout_dt = flow_result_dt + timedelta(days=lag_days)

    else:
        # No flow - faster sign-out typically
        flow_result_dt = None
        flow_days = None
        lag_days = None

        tat_days = random.uniform(1, 3)
        signout_dt = accession_dt + timedelta(days=tat_days)

    # Calculate total TAT
    total_tat = (signout_dt - accession_dt).total_seconds() / 86400

    # Amendment tracking
    if random.random() < 0.03:  # 3% amendment rate
        amendment_flag = "Y"
        amendment_count = random.choices([1, 2], weights=[0.9, 0.1])[0]
    else:
        amendment_flag = "N"
        amendment_count = 0

    # Determine outlier status and driver
    outlier_threshold = 7  # days
    outlier_flag = "Y" if total_tat > outlier_threshold else "N"

    outlier_driver = ""
    if outlier_flag == "Y":
        if flow_ordered and flow_days and flow_days > 4:
            outlier_driver = "Flow Delay"
        elif flow_ordered and lag_days and lag_days > 2:
            outlier_driver = "Internal Lag"
        elif random.random() < 0.3:
            outlier_driver = "Processing"
        else:
            outlier_driver = "Other"

    return {
        "patient_age_category": category,
        "specimen_type": "Bone Marrow",
        "accession_datetime": accession_dt.strftime("%Y-%m-%d %H:%M"),
        "flow_ordered": "Y" if flow_ordered else "N",
        "flow_result_datetime": flow_result_dt.strftime("%Y-%m-%d %H:%M") if flow_result_dt else "",
        "signout_datetime": signout_dt.strftime("%Y-%m-%d %H:%M"),
        "tat_days": round(total_tat, 2),
        "flow_tat_days": round(flow_days, 2) if flow_days else "",
        "lag_days": round(lag_days, 2) if lag_days else "",
        "amendment_flag": amendment_flag,
        "amendment_count": amendment_count,
        "outlier_flag": outlier_flag,
        "outlier_driver": outlier_driver
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample bone marrow case data for dashboard testing"
    )
    parser.add_argument(
        "--year", "-y",
        type=int,
        default=datetime.now().year,
        help="Report year (default: current year)"
    )
    parser.add_argument(
        "--month", "-m",
        type=int,
        default=datetime.now().month - 1 or 12,
        help="Report month (default: previous month)"
    )
    parser.add_argument(
        "--adult-count", "-a",
        type=int,
        default=45,
        help="Number of adult cases (default: 45)"
    )
    parser.add_argument(
        "--peds-count", "-p",
        type=int,
        default=12,
        help="Number of pediatric cases (default: 12)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="data",
        help="Output directory (default: data)"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    generate_sample_data(
        year=args.year,
        month=args.month,
        adult_count=args.adult_count,
        peds_count=args.peds_count,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
