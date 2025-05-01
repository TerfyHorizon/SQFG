"""
Structured Quarterly Folder Generator (SQFG)
Version 1.0.0 -- CLI

Generates a folder structure for the year, organized by quarter, week, and day based on
the calendar year defined in config.toml.

This script will create a folder hierarchy for each quarter (Q1, Q2, Q3, Q4), with folders
for each week, and inside those, folders for each day. The names will be based on the month,
day, and day of the week (e.g., "01-01_Monday").

Usage:
    python3 sqfg-cli.py [--verbose]

Requires:
    - Python 3.11+ (uses `tomllib` for TOML file parsing)
    - `config.toml` file should be present in the same directory

"""
import os
import tomllib
import argparse
from datetime import date, timedelta
from collections import defaultdict

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Structured Quarterly Folder Generator")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
verbose = args.verbose

# Load config from file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

settings = config["settings"]
year = settings["year"]
output_folder = settings["output_folder"]
week_prefix = settings["week_prefix"]
# day_folder_names = settings["day_folder_names"] # [Deprecated]

def get_quarter(d):
    return (d.month - 1) // 3 + 1

# Group days by custom week number (based on calendar, not ISO)
weeks = defaultdict(list)

start_date = date(year, 1, 1)
end_date = date(year, 12, 31)
current = start_date

while current <= end_date:
    # Week 1 starts Jan 1, every 7 days is a new week
    week_number = ((current - start_date).days // 7) + 1
    weeks[week_number].append(current)
    current += timedelta(days=1)

# Track last printed quarter for concise debug output
last_quarter = None

# Process each week
for week_number, days in weeks.items():
    # Use the first day in the week (within this year) to determine quarter
    quarter = get_quarter(days[0])

    if quarter != last_quarter:
        print(f"[+] Creating folders for Q{quarter}")
        last_quarter = quarter
    print(f"    - Week {week_number:02d}")

    for day in days:
        day_name = f"{day.strftime('%m-%d')}_{day.strftime('%A')}"
        path = os.path.join(
                output_folder,
                f"Q{quarter}",
                f"{week_prefix}{week_number:02d}",
                day_name
        )
        os.makedirs(path, exist_ok=True)

        if verbose:
            print(f"        * {day.isoformat()} -> {path}")
