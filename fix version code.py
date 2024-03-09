import time
import paramiko
import requests
import json
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth(username='lprabha', password='Password@123')

PORTAL_QUERY_URL = "prime-home/portal/query/execute?first=1&count=5"
DEVICE_ACTIONS_URL = "prime-home/api/v1/devices/{id}/actions"
BASE_URL = "https://qadm10.smartrg.com/"
SCRIPT_URL = "prime-home/api/v1/devices/{id}/scriptLog?first=1&count=3"

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

        with open('current_params.json', 'w') as soap_log_file:
            json.dump(get_logs, soap_log_file, indent=2)  # Add indent for formatting
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response. Response content:")
        print(response.content)
        return

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

    return diff

def print_diff(difference, parent_key=''):
    for key, value in difference.items():
        if parent_key:
            nested_key = f"{parent_key}.{key}"
        else:
            nested_key = key

        if isinstance(value, dict):
            print_diff(value, nested_key)
        else:
            print(f"{nested_key}: {value[0]} -> {value[1]}")

# Call the functions
# get_info()
json_diff()
