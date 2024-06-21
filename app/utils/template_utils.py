# /Users/joshestrada/Desktop/Python Projects/macro uploader tkinter/app/utils/template_utils.py
import csv

def download_template(save_path):
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ip_address', 'username', 'password', 'macro_file_path'])
        writer.writerow(['192.168.1.1', 'admin', 'password', '/path/to/macro1.js'])
        writer.writerow(['192.168.1.2', 'admin', 'password', '/path/to/macro2.js'])
    print(f"Template CSV file saved to {save_path}")
