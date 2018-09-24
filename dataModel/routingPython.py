from binding_python import ietf_routing
import pyangbind.lib.pybindJSON as pybindJSON
import json

model = ietf_routing()
new_routing = model.routing
new_routing.router_id = "Router01"
controlplane = new_routing.control_plane_protocol("TypeName")
controlplane.type = "identityref"
controlplane.name = "StringName"
controlplane.description = "StringDescription"
#controlplane.static_routes =

new_rib = new_routing.ribs.rib("RIB Name")
new_rib.address-family "identityref"
new_rib.description = "StringDescription"

json_data = pybindJSON.dumps(model, mode='ietf')

with open('routing.json', 'w') as f:
     f.write(json_data)
