from xrospf import Cisco_IOS_XR_ipv4_ospf_cfg
from ncclient import manager
import pyangbind.lib.pybindJSON as pybindJSON
import json
import sys
import os
import argparse

def read_file(fn):
    with open(fn) as f:
        result = f.read()
    return result

def get_args() :
    parser = argparse.ArgumentParser(description='Configure OSPF routing using NETCONF')
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
model = Cisco_IOS_XR_ipv4_ospf_cfg()

with open(filename, 'r') as f :
    for line in f :
        if "router" in line :
            r, o, p = line.split()
            processid = p
            newospf = model.ospf.processes.process.add(processid)
            newospf.start = "True"
        if "default-information" in line :
            newospf.default_vrf.default_information.always_advertise = "False"
        if "area" in line :
            a, n = line.split()
            areaid = n
            ospfarea = newospf.default_vrf.area_addresses.area_area_id.add(areaid)
            ospfarea.running = "True"
        if "interface" in line :
            i, g = line.split()
            interface = g
            networkadd = ospfarea.name_scopes
            network = networkadd.name_scope.add(interface)
            network.running = "True"

json_data = pybindJSON.dumps(model, mode='ietf')

with open('xrospf.json', 'w') as f:
    f.write(json_data)

## Json to XML
os.system('json2xml -t config -o xrospf.xml xrospf.jtox xrospf.json')

##  Send XML
exists = os.path.isfile('xrospf.xml')
if exists :  
    os.remove('xrospf.json')
    xml = read_file('xrospf.xml')
    os.remove('xrospf.xml')

    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
        reply = m.edit_config(target='candidate', config=xml)
        c = m.commit()

    print("Edit Config Success? {}".format(reply.ok))
    print("Commit Success? {}".format(c.ok))

else:
    print("XML File Does Not Exist")
