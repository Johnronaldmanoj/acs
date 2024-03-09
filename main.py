
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
SCRIPT_URL = "prime-home/api/v1/devices/{id}/scriptLog?first=1&count=2"

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
    trace_url = BASE_URL + TRACE_EVENT_DATA_URL.format(id='17347')
    get_logs = requests.get(trace_url, auth=basic ).json()
    # events_logs = list(filter(lambda e: e["duration"] > 1000, get_logs))
    # trace_id = events_logs[0]['traceId']
    # print(trace_id)
    # log_url = BASE_URL + LOG_URL.format(id='17347', trace_id=trace_id)
    # get_soap_details = requests.get(log_url, auth=basic).json()
    # time.sleep(10)  # waiting for logs to load
    # print(get_soap_details)
    tr_181_json = json.dumps(str(get_logs))
    time.sleep(15)
    with open('default_parameters.json', 'w') as soap_log_file:
        soap_log_file.writelines(get_soap_details)


# def json_diff(default_config, current_config):
#     default_config = json.load('default_config.json')
#     current_config = json.load('tr_181.json')
#     difference = jsondiff.diff(default_config, current_config)
#     print(difference)


get_info()
# json_diff(default_config=, current_config=)

my_device = {
    "hostname": "192.168.1.1",
    "username": "admin",
    "password": "admin123",
    # "auth_strict_key": False,
    # "channel_log": True
}
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**my_device)
channel = ssh_client.invoke_shell()
channel.send("show mfg\n")
time.sleep(2)
out = channel.recv(9999)
# print(out.decode())

out1 = out.decode()
print(out1.split('\n')[3].lstrip().split('=')[1])

