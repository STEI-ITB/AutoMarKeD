from xrinterface import Cisco_IOS_XR_ifmgr_cfg
from ncclient import manager
import pyangbind.lib.pybindJSON as pybindJSON
import json
import sys
import os
import xmltodict
import xml.dom.minidom
import argparse
import time

start_time = time.time()
def read_file(fn):
    with open(fn) as f:
        result = f.read()
    return result

def find_shutdown(data, act, iface_name):
    exist = False
    data_dict = xmltodict.parse(data, dict_constructor=dict)
    ifaces = data_dict['data']['interface-configurations']['interface-configuration']

    for iface in ifaces:
        if iface['active'] == act and iface['interface-name'] == iface_name:
            try:
                iface['shutdown']
                exist = True
            except:
                continue
    return exist

def get_args() :
    parser = argparse.ArgumentParser(description='Configure IOS-XR interface using NETCONF')
    parser.add_argument('-a', type=str, help='Host IP Address', required=True)
    parser.add_argument('-p', type=str, help='Host NETCONF Port', required=True)
    parser.add_argument('-u', type=str, help='Host Username', required=True)
    parser.add_argument('-w', type=str, help='Host Password', required=True)
    parser.add_argument('-f', type=str, help='Configuration File Name', required=True)
    args = parser.parse_args()
    host = args.a
    port = args.p
    username = args.u
    password = args.w
    filename = args.f
    return host, port, username, password, filename

host, port, username, password, filename = get_args()
model = Cisco_IOS_XR_ifmgr_cfg()


with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
    interface_filter = '''
                          <filter>
                             <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                             </interface-configurations>
                          </filter>
                          '''                             
    reply = m.get_config(source='running', filter=interface_filter).data_xml
    with open("running_interface.xml", 'w') as f:
        f.write(reply)
runconf = read_file('running_interface.xml')
os.remove('running_interface.xml')

shut = []
with open(filename, 'r') as f :
    for line in f :
        if "interface" in line :
            k,v = line.split()
        if "ipv4" in line :
            a = line.split()
            interface = 'act '+v
            ipv4addr = a[2]
            ipv4mask = a[3]
            ## Add New Interface GigabitEthernet
            new_interface = model.interface_configurations.interface_configuration.add(interface)
            ## IPv4 Configuration
            ipv4add = new_interface.ipv4_network.addresses.primary
            ipv4add.address = ipv4addr
            ipv4add.netmask = ipv4mask
            shutdown = find_shutdown(data=runconf, act='act', iface_name=v)
            shut.append(shutdown)

json_data = pybindJSON.dumps(model, mode='ietf')

with open('xrinterface.json', 'w') as f:
    f.write(json_data)

## Json to XML
os.system('json2xml -t config -o xrinterface.xml xrinterface.jtox xrinterface.json')

## No Shutdown
count = 0
for i in shut :
    if shut[i]==True :
        dom = xml.dom.minidom.parse('xrinterface.xml')
        noshutdown = dom.createElement('ifmgr-cfg:shutdown')
        noshutdown.setAttribute('nc:operation',"delete")
        intconfig = dom.getElementsByTagName('ifmgr-cfg:interface-configuration')[count]
        intconfig.appendChild(noshutdown)
        prettyxml = dom.toprettyxml()
        with open("xrinterface.xml", 'w') as f:
            f.write(prettyxml)
    count = count + 1

## Send XML
exists = os.path.isfile('xrinterface.xml')
if exists :
    os.remove('xrinterface.json')
    xml = read_file('xrinterface.xml')
    os.remove('xrinterface.xml')

    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
        reply = m.edit_config(target='candidate', config=xml)
        c = m.commit()

    print("Edit Config Success? {}".format(reply.ok))
    print("Commit Success? {}".format(c.ok))
    print("Execution time : %s seconds" % (time.time() - start_time))

else:
    print("XML File Does Not Exist")