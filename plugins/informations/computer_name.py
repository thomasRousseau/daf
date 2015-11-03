#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pythonregistry.Registry.Registry as Registry

def rec(key, depth=0):
    print("\t" * depth + key.path())

    for subkey in key.subkeys():
        rec(subkey, depth + 1)

def launch(input_disk, config):
    if not isinstance(config, bool):
        print('Error: Expected a boolean for the informations/computer_name configuration')
        sys.exit(-1)
    if not config:
        return 0

    reg = Registry.Registry(input_disk)
    #rec(reg.root())

    try:
        key = reg.open('ControlSet002\\Control\\ComputerName\\ComputerName')
        key = reg.open('ControlSet001\\Services\\Tcpip\\Parameters')
    except Registry.RegistryKeyNotFoundException:
        print('Couldn\'t find Run key. Exiting...')
        sys.exit(-1)

    for value in [v for v in key.values() \
        if v.value_type() == Registry.RegSZ or \
             v.value_type() == Registry.RegExpandSZ]:
            if value.name() == 'Hostname':
                print('%s: %s' % (value.name(), value.value()))

    #regripper_loader.info()

