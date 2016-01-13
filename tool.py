#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from optparse import OptionParser
import ConfigParser

import session

# Tool version
VERSION = '0.1'

def main(argv=None):
    parser = OptionParser()
    parser.add_option("-i", "--input-disk", dest="input_disk",
                    default=None, 
                    help="Set the base path of the mounted disk to analyze",
                    metavar="DISK_PATH")
    parser.add_option("-n", "--session-name", dest="session_name",
                    default="default_session", 
                    help="Set the session name to SESSION_NAME",
                    metavar="SESSION_NAME")
    parser.add_option("-d", "--session-directory", dest="session_directory",
                    default="",
                    help="Put the files created during session into DIRECTORY",
                    metavar="DIRECTORY")
    parser.add_option("-p", "--plugins-directory", dest="plugins_directory",
                    default="plugins",
                    help="Specify the directory of the plugins")
    parser.add_option("-y", "--system-hive", dest="system_hive", default=None,
                    help="Specify the absolute path to the system hive")
    parser.add_option("-o", "--software-hive", dest="software_hive",
                    default=None,
                    help="Specify the absolute path to the software hive")
    parser.add_option("-a", "--sam-hive", dest="sam_hive", default=None,
                    help="Specify the absolute path to the sam hive")
    parser.add_option("-u", "--users-hives", dest="users_hives", default=None,
                    help="Specify a list of (username, user_hive) couples")
    parser.add_option("-c", "--continue", dest="cont",
                    help="Specify a list of (username, user_hive) couples")
    (options, args) = parser.parse_args()

    if not options.input_disk:
        print("You need to specify the path to the disk you want to analyze")
        sys.exit(-1)
    else:
        options.input_disk = os.path.abspath(options.input_disk)
        if options.input_disk[-1] != "/":
            options.input_disk = options.input_disk + "/"

    users_hives = None
    if options.users_hives:
        pattern = re.compile("^\[(\([a-zA-Z0-9.\s-]+,[a-zA-Z0-9./\s-]+\)(\s*,\s*)?)+\]$")
        if not pattern.match(options.users_hives):
            print("Wrong pattern for given users hives.")
            sys.exit(-1)
        users_hives = []
        for couples in options.users_hives.split("(")[1::]:
            couple = couples.split(")")[0].split(",")
            users_hives += [(couple[0], couple[1])]

    if options.cont:
        if not os.path.isdir(options.cont):
            print("You specified a session folder that doesn't exist: " + options.cont)
            sys.exit(-1)
        if not options.cont[-1] == "/":
            options.cont += "/"
        if not os.path.isfile(options.cont + "session_config.ini") or not os.path.isfile(options.cont + "session_results.ini"):
            print("The folder you specified to continue a session is missing one of the needed files (session_config.ini or session_results.ini)")
            sys.exit(-1)
        options.session_directory = options.cont
        parser = ConfigParser.SafeConfigParser()
        parser.read(options.cont + "session_config.ini")
        options.session_name = parser.get("session_information", "session_name")

    # Create new user session
    user_session = session.Session(options.input_disk, options.session_name,
        options.session_directory, options.plugins_directory,
        options.system_hive, options.software_hive, options.sam_hive,
        users_hives)

    # Load the different plugins and there commands
    user_session.launch_plugins()

    # Run the renderer
    user_session.run_renderer()
 

if __name__ == '__main__':
    main()

