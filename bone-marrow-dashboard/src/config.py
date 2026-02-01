"""
Configuration settings for Bone Marrow Dashboard

Adjust these values based on section expectations and operational targets.
"""

# Turnaround Time Targets
TAT_TARGET_DAYS = 3          # Primary TAT target (accession to sign-out)
LAG_TARGET_DAYS = 1          # Service responsiveness target (flow result to sign-out)
OUTLIER_THRESHOLD_DAYS = 7   # Threshold for TAT outlier identification

# Performance Thresholds (percentage)
TARGET_MET_THRESHOLD = 90    # >= this value = "good" (green)
NEAR_TARGET_THRESHOLD = 75   # >= this value = "warning" (yellow), below = "alert" (red)

# Data Export Fields (for reference when setting up CoPath export)
REQUIRED_FIELDS = [
    "patient_age_category",   # Adult or Pediatric
    "specimen_type",          # Should be "Bone Marrow"
    "accession_datetime",     # Date/time of case accession
    "flow_ordered",           # Y/N - was flow cytometry ordered
    "flow_result_datetime",   # Date/time flow result received (if applicable)
    "signout_datetime",       # Date/time of final sign-out
    "amendment_flag",         # Y/N - was report amended
    "amendment_count",        # Number of amendments
]

# Optional fields for enhanced analysis
OPTIONAL_FIELDS = [
    "signing_pathologist_id", # For workload distribution analysis
    "outlier_driver",         # Manual categorization of delay drivers
]

# Age threshold for Adult vs Pediatric
ADULT_AGE_THRESHOLD = 18     # >= this age = Adult

# Report Distribution
DEFAULT_REPORT_RECIPIENTS = [
    "Hematopathology Section Faculty",
    "AP Lab Manager",
    "Quality Committee (quarterly)",
]
