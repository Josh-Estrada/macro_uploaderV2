import csv
import os
import requests
from lxml import etree

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

    # Process the CSV file and upload macros
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address = row['ip_address']
            username = row['username']
            password = row['password']
            macro_file_path = row['macro_file_path']
            macro_name = os.path.basename(macro_file_path).split('.')[0]  # Use file name without extension as macro name

            # Upload the macro to the endpoint
            upload_macro(ip_address, username, password, macro_name, macro_file_path)

def upload_macro(endpoint_ip, username, password, macro_name, js_file_path):
    try:
        with open(js_file_path, 'r') as f:
            js_code = f.read()
    except FileNotFoundError as e:
        print(f"Error: File {js_file_path} not found")
        return

    # Create the payload for saving the macro
    tags = ['Macros', 'Macro', 'Save']
    macro_params = {'name': macro_name,
                    'body': js_code,
                    'overWrite': "True",
                    'Transpile': "False"}

    xml = root = etree.Element("Command")
    for tag in tags:
        xml = etree.SubElement(xml, tag)
    xml.attrib["command"] = "True"
    for (arg, value) in macro_params.items():
        arg_xml = etree.SubElement(xml, arg)
        arg_xml.text = str(value)

    data = etree.tostring(root)

    # Send the xAPI command to the endpoint
    try:
        response = requests.post(f'https://{endpoint_ip}/putxml', auth=(username, password), data=data, headers={'Content-Type': 'application/xml'}, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"{macro_name} saved successfully for: {endpoint_ip}")
            enable_macro(endpoint_ip, username, password, macro_name)
        elif response.status_code == 401:
            print(f"401 error. Connection for: {endpoint_ip} unauthorized. Please check your credentials and try again.")
        else:
            print(f"Error saving {macro_name} to: {endpoint_ip} {response.text}")
    except requests.exceptions.Timeout:
        print(f"Timed out waiting for a response from {endpoint_ip}.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

def enable_macro(endpoint_ip, username, password, macro_name):
    url = f"https://{endpoint_ip}/putxml"
    headers = {'Content-Type': 'application/xml'}
    auth = (username, password)

    # Set the payload for enabling the macro
    root = etree.Element("Command")
    macros = etree.SubElement(root, "Macros")
    macro = etree.SubElement(macros, "Macro")
    activate = etree.SubElement(macro, "Activate")
    name = etree.SubElement(activate, "Name")
    name.text = macro_name
    payload = etree.tostring(root, encoding='unicode')

    # Send the POST request to the endpoint to enable the macro
    response = requests.post(url, auth=auth, headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        print(f"{macro_name} enabled successfully for {endpoint_ip}")
    else:
        print(f"Error enabling {macro_name} for {endpoint_ip}. Status code: {response.status_code}")

    # Set the payload for restarting the Macro runtime
    root = etree.Element("Command")
    macros = etree.SubElement(root, "Macros")
    runtime = etree.SubElement(macros, "Runtime")
    restart = etree.SubElement(runtime, "Restart")
    restart.attrib["command"] = "True"
    payload2 = etree.tostring(root)

    # Send the POST request to restart the Macro runtime
    response = requests.post(url, data=payload2, headers=headers, auth=auth, verify=False)
    if response.status_code == 200:
        print(f"Macro runtime restarted successfully for {endpoint_ip}")
    else:
        print(f"Error restarting Macro runtime for {endpoint_ip}. Status code: {response.status_code}")

def download_template(save_path):
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ip_address', 'username', 'password', 'macro_file_path'])
        writer.writerow(['192.168.1.1', 'admin', 'password', '/path/to/macro1.js'])
        writer.writerow(['192.168.1.2', 'admin', 'password', '/path/to/macro2.js'])
    print(f"Template CSV file saved to {save_path}")
