#!/usr/bin/env python

import subprocess
import optparse
import re

print('''
   *                                                         
 (  `    (       (              )                            
 )\))(   )\      )\          ( /(    )       (  (    (  (    
((_)()((((_)(  (((_)      (  )\())( /(  (    )\))(  ))\ )(   
(_()((_)\ _ )\ )\___      )\((_)\ )(_)) )\ )((_))\ /((_(()\  
|  \/  (_)_\(_((/ __|    ((_| |(_((_)_ _(_/( (()(_(_))  ((_) 
| |\/| |/ _ \  | (__    / _|| ' \/ _` | ' \)/ _` |/ -_)| '_| 
|_|  |_/_/ \_\  \_______\__||_||_\__,_|_||_|\__, |\___||_|   
                   |_____|  By:Abdul_Samad  |___/                                  
''')


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Name of Interface e.g eth0/wlan0")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter New Mac Address e.g ##:##:##:##:##:##")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the name of Interface e.g eth0/wlan0")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address e.g ##:##:##:##:##:##")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Unable to read Mac Address")

options = get_args()
current_mac = get_current_mac(options.interface)
print("Current Mac Address = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address has been successfully changed to " + current_mac)
else:
    print("[-] MAC Address didn't get changed")
