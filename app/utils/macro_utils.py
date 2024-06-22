import requests
import logging
from lxml import etree

macro_logger = logging.getLogger('macro')

def upload_macro(endpoint_ip, username, password, macro_name, js_file_path):
    try:
        with open(js_file_path, 'r') as f:
            js_code = f.read()
    except FileNotFoundError as e:
        error_msg = f'Error: File {js_file_path} not found'
        macro_logger.error(error_msg)
        macro_logger.exception(e)
        raise e

    tags = ['Macros', 'Macro', 'Save']
    macro_params = {
        'name': macro_name,
        'body': js_code,
        'overWrite': "True",
        'Transpile': "False",
    }

    xml = root = etree.Element("Command")
    for tag in tags:
        xml = etree.SubElement(xml, tag)
    xml.attrib["command"] = "True"
    for arg, value in macro_params.items():
        arg_xml = etree.SubElement(xml, arg)
        arg_xml.text = str(value)

    data = etree.tostring(root)

    try:
        with requests.post(f'https://{endpoint_ip}/putxml', auth=(username, password), data=data, headers={'Content-Type': 'application/xml'}, verify=False, timeout=10) as response:
            if response.status_code == 200:
                success_msg = f'{macro_name} saved successfully for: {endpoint_ip}'
                macro_logger.info(success_msg)
                enable_otj_macro(endpoint_ip, username, password, macro_name)
            elif response.status_code == 401:
                error_msg = f'401 error. Connection for: {endpoint_ip} unauthorized. Please check your credentials and try again.'
                macro_logger.error(error_msg)
                raise Exception(error_msg)
            else:
                error_msg = f'Error saving {macro_name} to: {endpoint_ip} {response.text}'
                macro_logger.error(error_msg)
                raise Exception(error_msg)
    except requests.exceptions.Timeout:
        error_msg = f'Timed out waiting for a response from {endpoint_ip}.'
        macro_logger.warning(error_msg)
        raise TimeoutError(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f'Error sending request: {e}'
        macro_logger.error(error_msg)
        raise e

def enable_otj_macro(endpoint_ip, username, password, macro_name):
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
        macro_logger.info(f"{macro_name} enabled successfully for {endpoint_ip}")
    else:
        macro_logger.error(f"Error enabling {macro_name} for {endpoint_ip}. Status code: {response.status_code}")

    tags2 = ['Macros', 'Runtime', 'Restart']
    macro_params1 = {"command": "True"}

    root = etree.Element("Command")
    macros = etree.SubElement(root, tags2[0])
    runtime = etree.SubElement(macros, tags2[1])
    etree.SubElement(runtime, tags2[2], **macro_params1)
    payload2 = etree.tostring(root)

    response = requests.post(url, data=payload2, headers=headers, auth=auth, verify=False)
    if response.status_code == 200:
        macro_logger.info(f"Macro runtime restarted successfully for {endpoint_ip}")
    else:
        macro_logger.error(f"Error restarting Macro runtime for {endpoint_ip}. Status code: {response.status_code}")
