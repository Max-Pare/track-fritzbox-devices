# import socket
# def guard(*args, **kwargs):
#     raise Exception("I told_hosts you not to use the Internet!")
# socket.socket = guard
import time
import copy
import telegram_send
from fritzconnection.lib.fritzhosts import FritzHosts
#-----------------------------------------------------

print("Script running!")
check_interval = 15
timeout_interval = 60

connection_try = 0
found_host = False
while(not found_host):
    try:
        hostInstance = FritzHosts(address="192.168.178.1", password="PASSWORD") #connect to router
        print("Host found, now running!")
    except:
        print("No internet connection, retrying...")
        pass
    else:
        found_host = True
        break
    time.sleep(5)

#-----------------------------------------------------
def Loop():
    current_hosts = GetActiveHosts()
    old_hosts = copy.deepcopy(current_hosts)
    print("Running!")
    while(True):
        try:
            current_hosts = GetActiveHosts()
        except NoDeviceGet("No devices available"):
            return
        new_hosts = []
        for i, key in enumerate(current_hosts):
            if current_hosts[i] not in old_hosts:
                new_hosts.append(current_hosts[i])
        for item in new_hosts:
            msg = str(f"{item['name']} is now online!")
            print(msg)
            SendTelegramNotification(msg)
        old_hosts = copy.deepcopy(current_hosts)
        time.sleep(check_interval)

def SendTelegramNotification(message):
    telegram_send.send(messages=[message]) #this needs to be configured before you run the script

def GetActiveHosts(session:FritzHosts):
    if not session == None:
        session.get_active_hosts()
    else:
        raise Exception("Fritz session is None.")

def GetActiveHosts():
    hosts = hostInstance.get_active_hosts()
    for key in hosts:
        key.pop('interface_type')
        key.pop('lease_time_remaining')
        key.pop('address_source')
        key.pop('ip')
    return hosts

class NoDeviceGet(Exception):
    pass

def main():
    while(True):
        try:
            Loop()
        except:
            print("An exception occourred while running the program, trying again in a few seconds...")
            pass
        else:
            break
        time.sleep(5)
if __name__ == '__main__':
    main()