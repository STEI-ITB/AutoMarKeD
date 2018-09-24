from binding_python import ietf_routing
import pyangbind.lib.pybindJSON as pybindJSON
import json

model = ietf_routing()
new_routing = model.routing
new_routing.router_id = "RouterName"

## Add New Control Plane
controlplane = new_routing.control_plane_protocol.add("TypeName")
controlplane.type = "identityref"
controlplane.name = "StringName"
controlplane.description = "StringDescription"

## Add New Static Route
routestatic = controlplane.ipv4.route.add("ipv4-prefix")
routestatic.description = "stringDescription"
# Next Hop Config
routestatic.next_hop.outgoing_interface = "interfaceRef"
routestatic.next_hop.next_hop_address = "3.3.3.3"
# Special Next Hop
routestatic.next_hop.special_next_hop = "hopEnumeration"
# Next Hop List
statichoplist = routestatic.next_hop.next_hop_list.next_hop.add('indexString')
statichoplist.outgoing_interface = "interfaceRef"
statichoplist.next_hop_address = "1.1.1.1"

## Add New RIB Routing
new_rib = new_routing.ribs.rib("RIB Name")
new_rib.address-family "identityref"
new_rib.description = "StringDescription"
# Check active route
new_rib.active-route.input.destination_address = "2.2.2.2"

json_data = pybindJSON.dumps(model, mode='ietf')

with open('routing.json', 'w') as f:
     f.write(json_data)
