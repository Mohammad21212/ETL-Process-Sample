import os
import pandas as pd
from datetime import datetime, timedelta
import logging
import argparse

# Configure logging
logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input():
    try:
        parser = argparse.ArgumentParser(description="Convert Excel files in the 'stage' directory to CSV and delete empty files.")
        parser.add_argument("--output_dir", default='stage', help="Output directory for CSV files (default: 'stage')")
        parser.add_argument("start_date", help="Start date (format: YYYY-MM-DD)")
        parser.add_argument("end_date", help="End date (format: YYYY-MM-DD)")
        parser.add_argument("--delete_excel", action="store_true", help="Delete Excel files after converting to CSV")
        args = parser.parse_args()
        return args.start_date, args.end_date, args.output_dir, args.delete_excel
    except Exception as e:
        save_error_to_log("file_converter", "Error in get_user_input", str(e))
        raise

def construct_file_path(file_date, output_dir):
    return os.path.join(output_dir, f"{file_date}.xlsx")

def save_csv_file(excel_file_path, output_dir):
    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(excel_file_path)

        # Check if the DataFrame is empty
        if df.empty:
            logging.warning(f"Empty file: {excel_file_path}. Deleting.")
            os.remove(excel_file_path)
        else:
            # Save DataFrame to CSV file
            csv_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(excel_file_path))[0]}.csv")
            df.to_csv(csv_file_path, index=False)
            logging.info(f"CSV file '{os.path.basename(csv_file_path)}' saved successfully.")
    except Exception as e:
        save_error_to_log("file_converter", "Error in save_csv_file", str(e))
        raise

def convert_excel_files_to_csv(start_date, end_date, output_dir, delete_excel):
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        while start_datetime <= end_datetime:
            file_date_str = start_datetime.strftime("%Y-%m-%d")

            try:
                # Convert file_date_str to a datetime object
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            except ValueError:
                logging.warning(f"Invalid file name format: {file_date_str}. Skipping.")
                continue

            excel_file_path = construct_file_path(file_date_str, output_dir)

            if not os.path.exists(excel_file_path):
                logging.error(f"File not found: {excel_file_path}")
                continue

            # Always delete Excel files for weekends
            persian_weekend_days = [3, 4]  # Thursday and Friday

            # Check if the file_date is on a weekend
            if file_date.weekday() in persian_weekend_days:
                os.remove(excel_file_path)
            else:
                # Save CSV for non-weekend days
                save_csv_file(excel_file_path, output_dir)

                # Delete Excel file if specified
                if delete_excel:
                    os.remove(excel_file_path)

            start_datetime += timedelta(days=1)
    except Exception as e:
        save_error_to_log("file_converter", "Error in convert_excel_files_to_csv", str(e))
        raise




def save_error_to_log(file_name, function_name, error_description):
    logging.error(f"[{file_name}] Function: {function_name}, Error: {error_description}")

if __name__ == "__main__":
    try:
        start_date, end_date, output_dir, delete_excel = get_user_input()
        
        # Create the 'stage' directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)
        
        convert_excel_files_to_csv(start_date, end_date, output_dir, delete_excel)
    except Exception as e:
        logging.error(f"[file_converter] An unexpected error occurred: {str(e)}")
