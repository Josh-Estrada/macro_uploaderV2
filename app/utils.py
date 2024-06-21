import csv
import os

def validate_csv(file_path):
    required_columns = ['ip_address', 'username', 'password', 'macro_file_path']
    errors = []

    # Check if file exists
    if not os.path.exists(file_path):
        errors.append(f"File not found: {file_path}")
        return errors

    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        # Check for missing columns
        for column in required_columns:
            if column not in headers:
                errors.append(f"Missing required column: {column}")

        # Check for missing values and file existence
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

    # Process the CSV file (placeholder for actual upload logic)
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address = row['ip_address']
            username = row['username']
            password = row['password']
            macro_file_path = row['macro_file_path']
            # Simulate uploading the macro file to the endpoint
            print(f"Uploading {macro_file_path} to {ip_address} with username {username} and password {password}")

def download_template(save_path):
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ip_address', 'username', 'password', 'macro_file_path'])
        writer.writerow(['192.168.1.1', 'admin', 'password', '/path/to/macro1.js'])
        writer.writerow(['192.168.1.2', 'admin', 'password', '/path/to/macro2.js'])
    print(f"Template CSV file saved to {save_path}")
