import subprocess
import optparse
import re

print('''
                              _                                 
  _ __ ___   __ _  ___    ___| |__   __ _ _ __   __ _  ___ _ __ 
 | '_ ` _ \ / _` |/ __|  / __| '_ \ / _` | '_ \ / _` |/ _ \ '__|
 | | | | | | (_| | (__  | (__| | | | (_| | | | | (_| |  __/ |   
 |_| |_| |_|\__,_|\___|  \___|_| |_|\__,_|_| |_|\__, |\___|_|   
                                                |___/           
''')

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change the mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac")
    (options, arguments) =  parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify the new mac, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing the mac address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current Mac address > " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address has successfully changed to " + current_mac)
else:
    print("[-] Mac address did not get changed.")




