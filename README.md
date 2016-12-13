python_openzwave
===================


This repository contains useful scripts for testing and debugging python_openzwave.

----------
It is important to change:
1. The specify the path to your Zwave device on line 48: device="/dev/zwave1"
2. The path to your python_openzwave configuration file on line 63:    config_path="/srv/hass/src/python-openzwave/openzwave/config", \

Tip: make sure that there is no other process making use of the Zwave device

To run just type in the command line: python3 api_help.py
