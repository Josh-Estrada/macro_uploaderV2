# /Users/joshestrada/Desktop/Python Projects/macro uploader tkinter/app/utils/macro_utils.py
import requests
from lxml import etree

def upload_macro(endpoint_ip, username, password, macro_name, js_file_path):
    try:
        with open(js_file_path, 'r') as f:
            js_code = f.read()
    except FileNotFoundError as e:
        print(f"Error: File {js_file_path} not found")
        return

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

    root = etree.Element("Command")
    macros = etree.SubElement(root, "Macros")
    macro = etree.SubElement(macros, "Macro")
    activate = etree.SubElement(macro, "Activate")
    name = etree.SubElement(activate, "Name")
    name.text = macro_name
    payload = etree.tostring(root, encoding='unicode')

    response = requests.post(url, auth=auth, headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        print(f"{macro_name} enabled successfully for {endpoint_ip}")
    else:
        print(f"Error enabling {macro_name} for {endpoint_ip}. Status code: {response.status_code}")

    root = etree.Element("Command")
    macros = etree.SubElement(root, "Macros")
    runtime = etree.SubElement(macros, "Runtime")
    restart = etree.SubElement(runtime, "Restart")
    restart.attrib["command"] = "True"
    payload2 = etree.tostring(root)

    response = requests.post(url, data=payload2, headers=headers, auth=auth, verify=False)
    if response.status_code == 200:
        print(f"Macro runtime restarted successfully for {endpoint_ip}")
    else:
        print(f"Error restarting Macro runtime for {endpoint_ip}. Status code: {response.status_code}")
