# /Users/joshestrada/Desktop/Python Projects/macro uploader tkinter/app/utils/csv_utils.py
import csv
import os
from app.utils.macro_utils import upload_macro

def validate_csv(file_path):
    required_columns = ['ip_address', 'username', 'password', 'macro_file_path']
    errors = []

    if not os.path.exists(file_path):
        errors.append(f"File not found: {file_path}")
        return errors

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for column in required_columns:
            if column not in headers:
                errors.append(f"Missing required column: {column}")

        for row_number, row in enumerate(reader, start=1):
            for column in required_columns:
                if not row[column]:
                    errors.append(f"Missing value in column '{column}' at row {row_number}")
            if not os.path.exists(row['macro_file_path']):
                errors.append(f"Macro file not found at path '{row['macro_file_path']}' in row {row_number}")

    return errors

def process_csv(file_path):
    errors = validate_csv(file_path)
    if errors:
        raise ValueError('\n'.join(errors))

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address = row['ip_address']
            username = row['username']
            password = row['password']
            macro_file_path = row['macro_file_path']
            macro_name = os.path.basename(macro_file_path).split('.')[0]

            upload_macro(ip_address, username, password, macro_name, macro_file_path)
