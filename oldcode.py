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
    header = {"content-type": "application/json"}  #x-www-form-urlencoded
    # r = requests.get(url, auth=basic)
    # print(r.json())
    r = requests.get(url, auth=basic, headers=header).json()
    r["scripts"].append(
        {"scriptCode": "tr181_get-all-params", "parameters": []}
    )
    r["applications"].update(
        {"ScriptRunner": {"pendingSync": True, "dataOwner": "SERVER"}}
    )
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, auth=basic, headers=headers, json=r)
    # print(response.json())
    time.sleep(360)
    # trace_url = BASE_URL + TRACE_EVENT_DATA_URL.format(id='17347')
    SCRIPT_LOG = BASE_URL+SCRIPT_URL.format(id='17347')
    print(SCRIPT_LOG)
    get_logs = requests.get(SCRIPT_LOG, auth=basic).json()
    # time.sleep(360)
    print(get_logs)
    # events_logs = list(filter(lambda e: e["durration"] > 1000, get_logs))
    # trace_id = events_logs[0]['traceId']
    # print(trace_id)
    # log_url = BASE_URL + LOG_URL.format(id='17347', trace_id=trace_id)
    # get_soap_details = requests.get(log_url, auth=basic).json()
    # time.sleep(10)  # waiting for logs to load
    # print(get_soap_details)
    # print(type(get_soap_details))
    tr_181_json = json.dumps(str(get_logs))
    time.sleep(15)
    with open('current_params.json', 'w') as soap_log_file:
        soap_log_file.write(tr_181_json)

def json_diff():
    default_params_file = 'default_params.json'
    current_params_file = 'current_params.json'

    with open(default_params_file, 'r') as df_file:
        default_params = json.load(df_file)

    with open(current_params_file, 'r') as cu_file:
        current_params = json.load(cu_file)

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