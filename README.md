# FILE1: Excel File Downloader
This script downloads Excel files for a specified date range from a given URL.

## Prerequisites

first download poetry:
    pip install poetry
    poetry init
    poetry shell

Install the required libraries:
    poetry add requests
    poetry add datetime
    poetry add logging
    poetry add argparse

## Usage

Run the script from the command line, providing the start date and end date as arguments:
    python file1.py <start_date> <end_date>
    Example:
    python file1.py 1402-11-01 1402-11-30

## save
    exel files save in stage folder

## Hint
    i run codes for 1402-10-01 to 1402-10-10
    if you want test change period

#########################################################

## FILE2: Excel to CSV Converter
This Python script converts Excel files in the 'stage' directory to CSV files, considering Persian weekdays
(Thursday and Friday) and deleting empty files.

## Prerequisites

poetry add pandas

## Usage
python script_name.py start_date end_date --output_dir your_desired_directory [--delete_excel]
Options:
    start_date: Start date in the format YYYY-MM-DD.
    end_date: End date in the format YYYY-MM-DD.
    --output_dir: Output directory for CSV files (default: 'stage').
    --delete_excel: (Optional) Delete Excel files after converting to CSV.
Example
python file2.py 1402-11-01 1402-11-30 --output_dir stage --delete_excel

## save
    csv files save in stage folder

#########################################################

## FILE3: CSV Analyzer

## Usage
python file3.py

## save
    csv files save in data folder


