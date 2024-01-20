import requests
import os
from datetime import datetime, timedelta
import logging
import argparse

# Configure logging
logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input():
    try:
        parser = argparse.ArgumentParser(description="Download Excel files for a date range.")
        parser.add_argument("start_date", help="Start date (format: YYYY-MM-DD)")
        parser.add_argument("end_date", help="End date (format: YYYY-MM-DD)")
        args = parser.parse_args()
        return args.start_date, args.end_date
    except Exception as e:
        save_error_to_log("file1", "Error in get_user_input", str(e))
        raise

def construct_file_url(current_date):
    try:
        return f"http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d={current_date.strftime('%Y-%m-%d')}"
    except Exception as e:
        save_error_to_log("file1", "Error in construct_file_url", str(e))
        raise

def save_excel_file(excel_file_url, local_file_path):
    try:
        response = requests.get(excel_file_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        with open(local_file_path, 'wb') as excel_file:
            excel_file.write(response.content)
        logging.info(f"[file1] Excel file '{os.path.basename(local_file_path)}' saved to '{local_file_path}' successfully.")
    except requests.exceptions.RequestException as req_ex:
        save_error_to_log("file1", "Error in save_excel_file", str(req_ex))
        raise
    except Exception as e:
        save_error_to_log("file1", "Error in save_excel_file", str(e))
        raise

def download_excel_files(start_date, end_date):
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        data_folder = 'stage'
        os.makedirs(data_folder, exist_ok=True)

        current_date = start_datetime
        while current_date <= end_datetime:
            excel_file_url = construct_file_url(current_date)
            file_name = f"{current_date.strftime('%Y-%m-%d')}.xlsx"
            local_file_path = os.path.join(data_folder, file_name)
            save_excel_file(excel_file_url, local_file_path)
            current_date += timedelta(days=1)
    except Exception as e:
        save_error_to_log("file1", "Error in download_excel_files", str(e))
        raise

def save_error_to_log(file_name, function_name, error_description):
    logging.error(f"[{file_name}] Function: {function_name}, Error: {error_description}")

if __name__ == "__main__":
    try:
        start_date, end_date = get_user_input()
        download_excel_files(start_date, end_date)
    except Exception as e:
        logging.error(f"[file1] An unexpected error occurred: {str(e)}")
