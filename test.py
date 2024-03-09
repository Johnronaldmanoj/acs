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
    print(response.json())
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
    # tr_181_json = json.dumps(str(get_logs))
    time.sleep(15)
    with open('default_params.json', 'w') as soap_log_file:
        json.dump(get_logs, soap_log_file)

# def json_diff():
#     default_params = 'default_params.json'
#     with open(default_params, 'r') as df_file:
#         default_params = json.load(df_file)
#     with open('current_params.json', 'r') as cu_file:
#         current_params = json.load(cu_file)
#     print(current_params[1]['log'])


import json

def compare_logs(logs1, logs2):
    for i, (log1, log2) in enumerate(zip(logs1, logs2)):
        message1 = log1.get("message", "")
        message2 = log2.get("message", "")

        if message1 != message2:
            print(f"Difference in message at logs[{i}]: {message1} (first) vs {message2} (second)")

# Replace 'file1.json' and 'file2.json' with your actual file paths
file_path1 = 'default_params.json'
file_path2 = 'current_params.json'

try:
    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

        # Assuming the logs are in a list at the top level of the JSON structure
        logs1 = data1
        logs2 = data2

        # Call the function with your logs
        compare_logs(logs1, logs2)

except FileNotFoundError:
    print("One or both files not found. Please provide valid file paths.")
except json.JSONDecodeError:
    print("Error decoding JSON. Please check the format of your JSON files.")
except Exception as e:
    print(f"An error occurred: {e}")

# json_diff()







#     difference = jsondiff.diff(default_params, current_params)[1]['log'][0]
#     # print(f'difference in parameters are: {difference}')
#     # print(difference)
#     print(type(difference))
#     # tr181 = json.loads(difference)
#     # print(type(tr181))
#     tr181 = {}
#     p = {}
#     for k, v in difference.items():
#         # print(f'key:{k}, Value: {v}')
#         tr181.update({k: v})
#         # print(type(tr181))
#     # jsondiff.diff(___, tr181)
#     m = tr181['message']
#     md = m.strip('()').split(' ')
#     # print(f'my_list = {md}')
#     # print(type(md))
#     # print(type(tr181['message']))
#     # return
#
#     parameters= {}
#     for i in md:
#         # if not i.endswith('}'):
#         #     i += '}'
#         # print(type(i))
#         print(i)
#         try:
#             message = eval(i)
#         except SyntaxError:
#             continue
#
#         # for k, v in message.items():
#         #     value = v['value']
#         #     p[k] = value
#         #     print(p)
#
# # get_info()
# json_diff()
#
# # def json_file():
# #     file = 'tr_parameters.json'
# #     with open('tr_parameters.json', 'r') as file:
# #         # fj = json.load(file)
# #         fs = filter(lambda x: x[0]['type'] == 'script custom',file)
# #         print(list(fs))
# #
# # json_file()
#
#
# #get_info()
#
# # my_device = {
# #     "hostname": "192.168.1.1",
# #     "username": "admin",
# #     "password": "admin123",
# #     # "auth_strict_key": False,
# #     # "channel_log": True
# # }
# # ssh_client = paramiko.SSHClient()
# # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # ssh_client.connect(**my_device)
# # channel = ssh_client.invoke_shell()
# # channel.send("show mfg\n")
# # time.sleep(2)
# # out = channel.recv(9999)
# # # print(out.decode())
# #
# # out1 = out.decode()
# # print(out1.split('\n')[3].lstrip().split('=')[1])