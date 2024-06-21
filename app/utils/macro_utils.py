import logging
import requests
from lxml import etree

macro_logger = logging.getLogger('macro')

def upload_macro(endpoint_ip, username, password, macro_name, js_file_path):
    try:
        with open(js_file_path, 'r') as f:
            js_code = f.read()
    except FileNotFoundError:
        error_message = f"Macro file '{js_file_path}' not found."
        macro_logger.error(error_message)
        raise FileNotFoundError(error_message)
    except Exception as e:
        error_message = f"Error reading macro file '{js_file_path}': {e}"
        macro_logger.error(error_message)
        raise Exception(error_message)

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
        response.raise_for_status()
        success_message = f"{macro_name} saved successfully for: {endpoint_ip}"
        macro_logger.info(success_message)
        print(success_message)
        enable_macro(endpoint_ip, username, password, macro_name)
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_message = f"Unauthorized access to {endpoint_ip}. Please check your credentials."
            macro_logger.error(error_message)
            raise PermissionError(error_message)
        else:
            error_message = f"HTTP error occurred: {e}"
            macro_logger.error(error_message)
            raise ConnectionError(error_message)
    except requests.exceptions.Timeout:
        error_message = f"Request to {endpoint_ip} timed out."
        macro_logger.error(error_message)
        raise TimeoutError(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"Error connecting to {endpoint_ip}: {e}"
        macro_logger.error(error_message)
        raise ConnectionError(error_message)

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

    try:
        response = requests.post(url, auth=auth, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        success_message = f"{macro_name} enabled successfully for {endpoint_ip}"
        macro_logger.info(success_message)
        print(success_message)
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP error occurred while enabling macro: {e}"
        macro_logger.error(error_message)
        raise ConnectionError(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"Error enabling macro: {e}"
        macro_logger.error(error_message)
        raise ConnectionError(error_message)

    root = etree.Element("Command")
    macros = etree.SubElement(root, "Macros")
    runtime = etree.SubElement(macros, "Runtime")
    restart = etree.SubElement(runtime, "Restart")
    restart.attrib["command"] = "True"
    payload2 = etree.tostring(root)

    try:
        response = requests.post(url, data=payload2, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        success_message = f"Macro runtime restarted successfully for {endpoint_ip}"
        macro_logger.info(success_message)
        print(success_message)
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP error occurred while restarting macro runtime: {e}"
        macro_logger.error(error_message)
        raise ConnectionError(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"Error restarting macro runtime: {e}"
        macro_logger.error(error_message)
        raise ConnectionError(error_message)
