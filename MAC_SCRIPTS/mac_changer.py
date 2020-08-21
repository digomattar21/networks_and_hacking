#!/usr/bin/env python
import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC')
    parser.add_option('-m', '--mac', dest='mac', help='MAC Address to be replaced')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #code to handle error
        parser.error('[-] Please specify a interface use --help for info.')
    elif not options.mac:
        #code to handle error
        parser.error('[-] Please specify a mac address use --help for info.')
    return options


def change_mac(interface, mac):
    print('[+] Changing MAC Address for ' + interface + ' to ' + mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    # Getting the results of interface and mac to check if it has been changed
    ifconfig_result = subprocess.check_output(['ifconfig', interface])

    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] Sorry, could not get mac address')


options = get_args()

current_mac = get_current_mac(options.interface)
print('[+] Current MAC: ' +str(current_mac))

change_mac(options.interface, options.mac)

#after the above function is realize, gets the updated mac address
current_mac = get_current_mac(options.interface)
#checks if the mac is the same

if current_mac == options.mac:
    print('[+] MAC address successfully changed to ' + current_mac)
else:
    print('[-] MAC address did not change')
