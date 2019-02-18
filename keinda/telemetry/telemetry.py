from xrtelemetry import Cisco_IOS_XR_telemetry_model_driven_cfg
from ncclient import manager
import pyangbind.lib.pybindJSON as pybindJSON
import json
import sys
import os
import xml.dom.minidom

host = '10.10.1.23'
port = '830'
username = 'admin'
password = 'admin'

model = Cisco_IOS_XR_telemetry_model_driven_cfg()

sensgrp = 'ipv4ospf'
senspath = 'Cisco-IOS-XR-ipv4-ospf-oper:ospf/processes/process/default-vrf/route-information/connected-routes'
subid = 'IPV4' 
#sourceint = 'GigabitEthernet0/0/0/0'

# Add Sensor
newsensor = model.telemetry_model_driven.sensor_groups.sensor_group.add(sensgrp)
sensorpath = newsensor.sensor_paths.sensor_path.add(senspath)

# Add Subscription
newsubscript = model.telemetry_model_driven.subscriptions.subscription.add(subid)
profile = newsubscript.sensor_profiles.sensor_profile.add(sensgrp)
profile.sample_interval = 10000
#newsubscript.source_interface = sourceint

# Other Settings
#model.telemetry_model_driven.strict_timer = 'True'
model.telemetry_model_driven.enable = 'True'

json_data = pybindJSON.dumps(model, mode='ietf')

with open('xrtelemetry.json', 'w') as f:
    f.write(json_data)

## Json to XML
os.system('json2xml -t config -o xrtelemetry.xml xrtelemetry.jtox xrtelemetry.json')
dom = xml.dom.minidom.parse('xrtelemetry.xml')
prettyxml = dom.toprettyxml()
with open("xrtelemetry.xml", 'w') as f:
    f.write(prettyxml)

##  Send XML
exists = os.path.isfile('xrtelemetry.xml')
if exists :
    def read_file(fn):
        with open(fn) as f:
            result = f.read()
        return result
    
    os.remove('xrtelemetry.json')
    xml = read_file('xrtelemetry.xml')
    os.remove('xrtelemetry.xml')

    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
        reply = m.edit_config(target='candidate', config=xml)
        c = m.commit()

    print("Edit Config Success? {}".format(reply.ok))
    print("Commit Success? {}".format(c.ok))

else:
    print("XML File Does Not Exist")