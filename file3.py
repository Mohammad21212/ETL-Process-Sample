import os
import pandas as pd
import logging

class CSVAnalyzer:
    def __init__(self, stage_directory, data_directory):
        self.stage_directory = stage_directory
        self.data_directory = data_directory
        self.logger = self.setup_logger()

    def setup_logger(self):
        # Set up logging configuration
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Create a file handler and set the logging level
        file_handler = logging.FileHandler('info.log', encoding='utf-8')  # Specify encoding here
        file_handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        return logger

    def analyze_csv(self, input_file_path, criteria_name, output_filename_prefix):
        try:
            # Read CSV data into a pandas DataFrame
            df = pd.read_csv(input_file_path, encoding='utf-8', skiprows=2)

            # Print the first few rows of the DataFrame for inspection
            self.logger.info(f"First few rows of the DataFrame:\n{df.head()}")

            # Identify the column representing values dynamically
            criteria_column = next((col for col in df.columns if criteria_name in col), None)
            if criteria_column is None:
                raise KeyError(f"'{criteria_name}' column not found")

            # Convert the column to numeric (if applicable)
            df[criteria_column] = pd.to_numeric(df[criteria_column], errors='coerce')

            # Identify the top 10 symbols based on the specified criteria
            top_symbols = df.nlargest(10, criteria_column, 'all')[['نماد', criteria_column]]

            # Map criteria names to desired names
            criteria_mapping = {'ارزش': 'value', 'بیشترین': 'most', 'تعداد': 'number'}
            criteria_mapped_name = criteria_mapping.get(criteria_name, criteria_name)

            # Generate the output filename with the desired format
            output_file_name = f"{output_filename_prefix}-{criteria_mapped_name.lower()}-{os.path.basename(input_file_path)}"
            output_file_path = os.path.join(self.data_directory, output_file_name)

            # Save the top symbols to a new CSV file in the data directory
            top_symbols.to_csv(output_file_path, encoding='utf-8', index=False)

            self.logger.info(f"Top 10 symbols based on '{criteria_name}' saved to: {output_file_path}")

            return output_file_path

        except KeyError as e:
            self.logger.error(f"Error: {e}")
            self.logger.error(f"Make sure the column '{criteria_name}' exists in your CSV file.")

    def analyze_top_values(self, input_file_path):
        return self.analyze_csv(input_file_path, 'ارزش', 'top-symbols-values')

    def analyze_top_max(self, input_file_path):
        return self.analyze_csv(input_file_path, 'بیشترین', 'top-symbols-max')

    def analyze_top_quantity(self, input_file_path):
        return self.analyze_csv(input_file_path, 'تعداد', 'top-symbols-quantity')

    def process_files(self):
        # Process all CSV files in the stage directory
        for filename in os.listdir(self.stage_directory):
            if filename.endswith(".csv"):
                input_file_path = os.path.join(self.stage_directory, filename)
                self.analyze_top_values(input_file_path)
                self.analyze_top_max(input_file_path)
                self.analyze_top_quantity(input_file_path)

if __name__ == "__main__":
    # Create an instance of CSVAnalyzer
    csv_analyzer = CSVAnalyzer(stage_directory='stage', data_directory='data')

    # Process CSV files in the stage directory
    csv_analyzer.process_files()
