#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import platform

def install():
    if (platform.system() == 'Linux'):
        if os.system("dpkg --get-selections | grep -v deinstall | grep plaso"):
            try:
                print "Installing log2timeline"
                os.system("sudo add-apt-repository universe > /dev/null")
                os.system("sudo apt-get update > /dev/null")
                os.system("sudo add-apt-repository ppa:gift/stable > /dev/null")
                os.system("sudo apt-get update > /dev/null")
                os.system("sudo apt-get install python-plaso > /dev/null")
            except:
                print "An error occured during log2timeline installation"
                return 0
        print "Log2timeline installed"
        return 1
    else:
        print "Unknwon OS, couldn\'t install log2timeline" 
        return 0
