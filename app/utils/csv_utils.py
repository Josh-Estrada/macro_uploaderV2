import csv
import os
from app.utils.macro_utils import upload_macro

def validate_csv(file_path):
    required_columns = ['ip_address', 'username', 'password', 'macro_file_path']
    errors = []

    if not os.path.exists(file_path):
        errors.append(f"File not found: {file_path}")
        return errors

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames

            # Check for missing required columns
            missing_columns = [column for column in required_columns if column not in headers]
            if missing_columns:
                errors.append(f"Missing required columns: {', '.join(missing_columns)}")
                return errors

            # Check for missing values and file existence
            for row_number, row in enumerate(reader, start=1):
                for column in required_columns:
                    if not row[column]:
                        errors.append(f"Missing value in column '{column}' at row {row_number}")
                    elif column == 'ip_address' and not is_valid_ip(row[column]):
                        errors.append(f"Invalid IP address '{row[column]}' at row {row_number}")
                if not os.path.exists(row['macro_file_path']):
                    errors.append(f"Macro file not found at path '{row['macro_file_path']}' in row {row_number}")

    except csv.Error as e:
        errors.append(f"Error reading CSV file: {e}")

    return errors

def is_valid_ip(ip):
    import re
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def process_csv(file_path):
    errors = validate_csv(file_path)
    if errors:
        raise ValueError('\n'.join(errors))

    successes = 0
    failures = 0

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address = row['ip_address']
            username = row['username']
            password = row['password']
            macro_file_path = row['macro_file_path']
            macro_name = os.path.basename(macro_file_path).split('.')[0]

            try:
                upload_macro(ip_address, username, password, macro_name, macro_file_path)
                successes += 1
            except Exception as e:
                print(f"Error processing row for {ip_address}: {e}")
                failures += 1
                continue  # Proceed with the next row

    return successes, failures
