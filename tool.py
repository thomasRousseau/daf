#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

import session

# Tool version
VERSION = '0.1'

def main(argv=None):
    parser = OptionParser()
    parser.add_option("-n", "--session-name", dest="session_name", default="default_session",
                  help="Set the session name to SESSION_NAME", metavar="SESSION_NAME")
    parser.add_option("-d", "--session-directory", dest="session_directory", default="",
                  help="Put the files created during session into DIRECTORY", metavar="DIRECTORY")
    parser.add_option("-p", "--plugins-directory", dest="plugins_directory", default="plugins",
                  help="Specify the directory of the plugins")
    (options, args) = parser.parse_args()

    # Create new user session
    user_session = session.Session(options.session_name, options.session_directory, options.plugins_directory)

    # Load the different plugins and there commands
    user_session.launch_plugins()

    # Run the renderer
    user_session.run_renderer()
 

if __name__ == '__main__':
    main()

