import requests
import json
import time
import subprocess
import os
import base64

class ConnectionDetails:
    '''This is class contains parameter/data for setting time''' 

    intel_proxy = {
        'http': 'http://proxy-dmz.intel.com:911',
        "https": "http://proxy-dmz.intel.com:912"
    }
    
    timezone = 'Asia/Kolkata'
    base_url = 'https://timeapi.io/api/TimeZone/zone?timeZone=' 
    target_url = base_url + timezone


class TimeSyncCMD:
    '''This class has helper methods to set time/timezone'''
    def get_supported_time_format(self, response):
        json_object = json.loads(response.text)
        unformatted_time = json_object["currentLocalTime"]
        splitted_time = unformatted_time.split('.')
        splitted_time = splitted_time[0].replace('T', ' ')
        time_object = time.strptime(splitted_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = time.strftime("%d %b %Y %H:%M:%S", time_object)
        return time_stamp
    
    def execute_time_cmd(self, time_stamp):
        cmd = 'sudo date --set "'+ str(time_stamp) + '"'
        subprocess.call('sudo -S {}'.format(cmd), shell=True)

    def set_timezone_cmd(self, time_zone):
        cmd = ' sudo timedatectl set-timezone "'+ str(time_zone) + '"'
        subprocess.call('sudo -S {}'.format(cmd), shell=True)

    def sync_hw_clock(self):
        cmd = 'sudo hwclock --systohc'
        subprocess.call('sudo -S {}'.format(cmd), shell=True)
    

if __name__=='__main__':
    try:
        obj_conn = ConnectionDetails()
        response = requests.get(obj_conn.target_url, proxies=obj_conn.intel_proxy)
        obj_tsc = TimeSyncCMD()
        obj_tsc.set_timezone_cmd(obj_conn.timezone)
        time_stamp = obj_tsc.get_supported_time_format(response)
        obj_tsc.execute_time_cmd(time_stamp)
        obj_tsc.sync_hw_clock()
        print('Successfully updated system time!')
    except Exception as e:
        print('Failed to update system time!' + e)
