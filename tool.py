#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from optparse import OptionParser

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
    #TODO
    parser.add_option("-y", "--system-hive", dest="system_hive", default=None,
                    help="Specify the absolute path to the system hive")
    #TODO
    parser.add_option("-o", "--software-hive", dest="software_hive",
                    default=None,
                    help="Specify the absolute path to the software hive")
    #TODO
    parser.add_option("-a", "--sam-hive", dest="sam_hive", default=None,
                    help="Specify the absolute path to the sam hive")
    #TODO
    parser.add_option("-u", "--users-hives", dest="users_hives", default=None,
                    help="Specify a list of (username, user_hive) couples")
    (options, args) = parser.parse_args()

    if not options.input_disk:
        print("You need to specify the path to the disk you want to analyze")
        sys.exit(-1)
    else:
        options.input_disk = os.path.abspath(options.input_disk)
        if options.input_disk[-1] != "/":
            options.input_disk = options.input_disk + "/"

    # Create new user session
    user_session = session.Session(options.input_disk, options.session_name, options.session_directory, options.plugins_directory)

    # Load the different plugins and there commands
    user_session.launch_plugins()

    # Run the renderer
    user_session.run_renderer()
 

if __name__ == '__main__':
    main()

