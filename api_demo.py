#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

import logging
import pprint
import sys, os
import resource
#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger('openzwave')
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

#Specify the path to your ZWave stick or controller e.g. (/dev/zwave or /dev/ttyACM0)
device="/dev/zwave1"
log="Debug"

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#Define some manager options
options = ZWaveOption(device, \
  config_path="/srv/hass/src/python-openzwave/openzwave/config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
#Set to True for direct logging output into the console
options.set_console_output(False)
options.set_save_log_level(log)
#options.set_save_log_level('Info')
options.set_logging(False)
options.lock()

print("------------------------------------------------------------")
print("------------------------------------------------------------")
print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))

#Create a network object
network = ZWaveNetwork(options, log=None)

time_started = 0
print("------------------------------------------------------------")
print("Waiting for network awaked : ")
print("------------------------------------------------------------")
for i in range(0,300):
    if network.state>=network.STATE_AWAKED:

        print(" done")
        print("------------------------------------------------------------")
        print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time_started += 1
        time.sleep(1.0)
if network.state<network.STATE_AWAKED:
    print(".")
    print("Network is not awake but continue anyway")
print("------------------------------------------------------------")
print("Use openzwave library : {}".format(network.controller.ozw_library_version))
print("Use python library : {}".format(network.controller.python_library_version))
print("Use ZWave library : {}".format(network.controller.library_description))
print("Network home id : {}".format(network.home_id_str))
print("Controller node id : {}".format(network.controller.node.node_id))
print("Controller node version : {}".format(network.controller.node.version))
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Waiting for network ready : ")
print("------------------------------------------------------------")
for i in range(0,300):
    if network.state>=network.STATE_READY:
        print(" done in {} seconds".format(time_started))
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        #sys.stdout.write(network.state_str)
        #sys.stdout.write("(")
        #sys.stdout.write(str(network.nodes_count))
        #sys.stdout.write(")")
        #sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)


print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
if not network.is_ready:
    print(".")
    print("Network is not ready but continue anyway")


print("------------------------------------------------------------")
print("Controller capabilities : {}".format(network.controller.capabilities))
print("Controller node capabilities :")
pp.pprint(network.controller.node.capabilities)
print("Nodes in network : {}".format(network.nodes_count))
print("Driver statistics :")
pp.pprint(network.controller.stats)
print("------------------------------------------------------------")
for node in network.nodes:

    print("New node: Node {}".format(network.nodes[node].node_id))
    print("   ---------   ")
    print("Node {} - Name : {}".format(network.nodes[node].node_id,network.nodes[node].name))
    print("Node {} - Manufacturer name / id : {} / {}".format(network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
    print("Node {} - Product name / id / type : {} / {} / {}".format(network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type))
    print("Node {} - Version : {}".format(network.nodes[node].node_id, network.nodes[node].version))
    print("Node {} - Command classes :".format(network.nodes[node].node_id))
    pp.pprint(network.nodes[node].command_classes_as_string)
    print("Node {} - Capabilities : {}".format(network.nodes[node].node_id,network.nodes[node].capabilities))
    print("Node {} - Neigbors : {}".format(network.nodes[node].node_id,network.nodes[node].neighbors))
    print("Node {} - Can sleep : {}".format(network.nodes[node].node_id,network.nodes[node].can_wake_up()))
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print("Node {} - Groups : {}".format (network.nodes[node].node_id, groups))
    values = {}
    for val in network.nodes[node].values :
        values[network.nodes[node].values[val].object_id] = {
            'label':network.nodes[node].values[val].label,
            'help':network.nodes[node].values[val].help,
            'command_class':network.nodes[node].values[val].command_class,
            'max':network.nodes[node].values[val].max,
            'min':network.nodes[node].values[val].min,
            'units':network.nodes[node].values[val].units,
            'data':network.nodes[node].values[val].data_as_string,
            'ispolled':network.nodes[node].values[val].is_polled
            }
    #print("{} - Values : {}".format(network.nodes[node].node_id, values))
    #print("------------------------------------------------------------")
    for cmd in network.nodes[node].command_classes:
        print("   ---------   ")
        #print("cmd = {}".format(cmd))
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print("Node {} - Values for command class : {} :".format(network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd)))
        pp.pprint(values)
    print("------------------------------------------------------------")

print("Driver statistics :")
pp.pprint(network.controller.stats)
print("------------------------------------------------------------")
print("------------------------------------------------------------")
print("Try to autodetect nodes on the network")
print("------------------------------------------------------------")
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Retrieve switches on the network")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  state: {}".format(network.nodes[node].get_switch_state(val)))
if (len(network.nodes[node].get_switches())<1):
    print("Result: No switches found")
print("------------------------------------------------------------")
print("Retrieve dimmers on the network")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_dimmers() :
        print("node/name/index/instance : {}/{}/{}/{}".format (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format (network.nodes[node].values[val].id_on_network))
        print("  level: {}".format (network.nodes[node].get_dimmer_level(val)))
if (len(network.nodes[node].get_dimmers())<1):
    print("Result: No dimmers found")
print("------------------------------------------------------------")
print("Retrieve RGB bulbs on the network")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_rgbbulbs() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  level: {}".format(network.nodes[node].get_dimmer_level(val)))
if (len(network.nodes[node].get_rgbbulbs())<1):
    print("Result: No RGB bulbs found")
print("------------------------------------------------------------")
print("Retrieve sensors on the network")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_sensors() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value: {} {}".format(network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
if (len(network.nodes[node].get_sensors())<1):
    print("Result: No sensors found")
print("------------------------------------------------------------")
print("Retrieve thermostats on the network")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_thermostats() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value: {} {}".format(network.nodes[node].get_thermostat_value(val), network.nodes[node].values[val].units))
if (len(network.nodes[node].get_thermostats())<1):
    print("Result: No thermostats found")
print("------------------------------------------------------------")
print("Retrieve switches all compatibles devices on the network    ")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches_all() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value / items:  / {}".format(network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
        print("  state: {}".format(network.nodes[node].get_switch_all_state(val)))
if (len(network.nodes[node].get_switches_all())<1):
    print("Result: No switches all compatible devices found")
print("------------------------------------------------------------")
print("Retrieve protection compatibles devices on the network    ")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_protections() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : ".format(network.nodes[node].values[val].id_on_network))
        print("  value / items: {} / {}".format(network.nodes[node].get_protection_item(val), network.nodes[node].get_protection_items(val)))
if (len(network.nodes[node].get_protections())<1):
    print("Result: No protection compatible devices found")
print("------------------------------------------------------------")
print("Retrieve battery compatibles devices on the network         ")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_battery_levels() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value : {}".format(network.nodes[node].get_battery_level(val)))
if (len(network.nodes[node].get_battery_levels())<1):
    print("Result: No battery compatible devices found")
print("------------------------------------------------------------")
print("Retrieve power level compatibles devices on the network         ")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_power_levels() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value : {}".format(network.nodes[node].get_power_level(val)))
if (len(network.nodes[node].get_power_levels())<1):
    print("Result: No power level compatible devices found")
#print
#print("------------------------------------------------------------")
#print "Activate the switches on the network"
#print "Nodes in network : {}".format network.nodes_count
#print("------------------------------------------------------------")
#for node in network.nodes:
#    for val in network.nodes[node].get_switches() :
#        print("Activate switch {} on node {}".format \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,True)
#        print("Sleep 10 seconds")
#        time.sleep(10.0)
#        print("Dectivate switch {} on node {}".format \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,False)
#print("Done"))
#print("------------------------------------------------------------")
print("------------------------------------------------------------")
print("Driver statistics :")
pp.pprint(network.controller.stats)
print("------------------------------------------------------------")
print("Driver label : {}".format(network.controller.get_stats_label('retries')))
print("------------------------------------------------------------")
print("Stop network")
print("------------------------------------------------------------")
network.stop()
print("------------------------------------------------------------")
print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
print("------------------------------------------------------------")
print("------------------------------------------------------------")
