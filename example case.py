import time
import paramiko
import requests
import json
import jsondiff

# from scrapli.driver import GenericDriver
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth(username='lprabha', password='Password@123')

PORTAL_QUERY_URL = "prime-home/portal/query/execute?first=1&count=5"
DEVICE_ACTIONS_URL = "prime-home/api/v1/devices/{id}/actions"
DEVICE_DATA_URL = "prime-home/api/v1/devices/{id}/data"
DEVICE_FIRMWARES_URL = "prime-home/portal/devices/types/*/firmware?deviceId={id}"
ADD_FIRMWARE_URL = "prime-home/portal/devices/types/*/firmware"
REMOVE_FIRMWARE_URL = "prime-home/portal/devices/types/*/firmware/{id}"
GET_ACTIVITY = "prime-home/portal/devices/{id}/activity"
BASE_URL = "https://qadm10.smartrg.com/"
TRACE_EVENT_DATA_URL = "prime-home/portal/devices/{id}/trace?first=1&count=10"
LOG_URL = "prime-home/portal/devices/{id}/trace/{trace_id}/log"
SCRIPT_URL = "prime-home/api/v1/devices/{id}/scriptLog?first=1&count=3"

# data ={
#     'username': 'lprabha',
#     'password': 'Password@123'
# }

def get_info():
    url = BASE_URL + DEVICE_ACTIONS_URL.format(id='17347')
    print(url)
    header = {"content-type": "application/json"}
    r = requests.get(url, auth=basic, headers=header).json()
    r["scripts"].append(
        {"scriptCode": "tr181_get-all-params", "parameters": []}
    )
    r["applications"].update(
        {"ScriptRunner": {"pendingSync": True, "dataOwner": "SERVER"}}
    )
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, auth=basic, headers=headers, json=r)
    time.sleep(360)

    SCRIPT_LOG = BASE_URL + SCRIPT_URL.format(id='17347')

    try:
        response = requests.get(SCRIPT_LOG, auth=basic)
        get_logs = response.json()
        print(f"Type of get_logs: {type(get_logs)}")
        print(f"Content of get_logs: {get_logs}")
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response. Response content:")
        print(response.content)
        return

    with open('current_params.json', 'w') as soap_log_file:
        json.dump(get_logs, soap_log_file)

# Specify the path to your log file
log_file_path = 'default_params.json'

# Read the log file
with open(log_file_path, 'r') as file:
    log_entries = file.readlines()

# Process each log entry
for log_entry in log_entries:
    # Remove extra characters and backslashes
    cleaned_log_entry = log_entry.replace("\\", "").replace("(", "").replace(")", "")

    # Convert the cleaned log entry to a Python dictionary
    try:
        parsed_data = json.loads(cleaned_log_entry)
        print(json.dumps(parsed_data, indent=2))  # Print the formatted JSON
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def json_diff():
    default_params_file = 'default_params.json'
    current_params_file = 'current_params.json'

    with open(default_params_file, 'r') as df_file:
        default_params = json.load(df_file)

    with open(current_params_file, 'r') as cu_file:
        current_params = json.load(cu_file)

    # Print the types of both variables
    print(f"Type of default_params: {type(default_params)}")
    print(f"Type of current_params: {type(current_params)}")

    # Find the differences between the two dictionaries
    difference = find_dict_differences(default_params, current_params)

    # Print the differences
    if difference:
        print("Differences found:")
        print_diff(difference)
    else:
        print("No differences found.")


def find_dict_differences(dict1, dict2):
    # Helper function to recursively find differences between dictionaries
    diff = {}
    for key in set(dict1.keys()) | set(dict2.keys()):
        if isinstance(dict1.get(key), dict) and isinstance(dict2.get(key), dict):
            nested_diff = find_dict_differences(dict1[key], dict2[key])
            if nested_diff:
                diff[key] = nested_diff
        elif dict1.get(key) != dict2.get(key):
            diff[key] = (dict1.get(key), dict2.get(key))

    # Add debugging information
    if not isinstance(dict1, dict):
        print(f"dict1 is not a dictionary. Type: {type(dict1)}")
#     if not isinstance(dict2, dict):
#         print(f"dict2 is not a dictionary. Type: {type(dict2)}")
#
#     return diff
#
# def print_diff(difference, parent_key=''):
#     for key, value in difference.items():
#         if parent_key:
#             nested_key = f"{parent_key}.{key}"
#         else:
#             nested_key = key
#
#         if isinstance(value, dict):
#             print_diff(value, nested_key)
#         else:
#             print(f"{nested_key}: {value[0]} -> {value[1]}")

# Call the function
json_diff()
# def json_diff(default_params, current_params):
#     with open('default_params.json', 'r') as df_file:
#         default_params = json.load(df_file)
#     with open('current_params.json', 'r') as cu_file:
#         current_params = json.load(cu_file)
#     difference = jsondiff.diff(default_params, current_params)
#     print(difference)

    # for k, v in difference.items():
    #     print(k, v)

get_info()
# json_diff(default_params='default_params.json', current_params='current_params.json')



# def json_file():
#     file = 'tr_parameters.json'
#     with open('tr_parameters.json', 'r') as file:
#         # fj = json.load(file)
#         fs = filter(lambda x: x[0]['type'] == 'script custom',file)
#         print(list(fs))
#
# json_file()


get_info()

# my_device = {
#     "hostname": "192.168.1.1",
#     "username": "admin",
#     "password": "admin123",
#     # "auth_strict_key": False,
#     # "channel_log": True
# }
# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(**my_device)
# channel = ssh_client.invoke_shell()
# channel.send("show mfg\n")
# time.sleep(2)
# out = channel.recv(9999)
# # print(out.decode())
#
# out1 = out.decode()
# print(out1.split('\n')[3].lstrip().split('=')[1])