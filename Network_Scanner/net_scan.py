#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='ip', help ='IP or IP range to be scanned')
    options = parser.parse_args()

    if not options.ip:
        parser.error('[-] Please specify a target, use --help for more info')
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #only getting element 0 (answered list because this function returns 2 things)

    clients_list = []
    for element in answered_list:
        client_dict = {'IP': element[1].psrc, 'MAC': element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print('IP\t\t\tMACADRESS\n-----------------------------------------')
    for i in results_list:
        print(i['IP']+'\t\t'+i['MAC'])


options = get_args()
scan_result = scan(options.ip)
print_result(scan_result)

