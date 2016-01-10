#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
This file aims to define the user session class.

This class permits to keep track of executed actions
in order to permit correlation between steps of the analysis
and resumption of a previous analysis
"""

from datetime import datetime
from ui import renderer
import importlib
import os
from fnmatch import fnmatch
import pyclbr
import sys
import shutil
import ConfigParser
import types
import inspect


class Session(object):
    def __init__(self, input_disk, session_name, directory, plugins_directory):
        """Creates a new user session.
        
        Returns:
            a Session object.
        """
        # Start time of the session
        start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Path to the disk to analyze
        self.input_disk = input_disk

        # Session name
        self._name = session_name

        # Sesion directory in order to permit resumption of analysis
        self._directory = os.path.abspath(directory) if directory else os.path.abspath("".join(["sessions/", self._name, "-", start_time]))

        # Plugins directory
        self._plugins_directory = plugins_directory

        # Set a renderer to handle graphical stuff
        self.renderer = renderer.ShellRenderer(self._name, self._directory)

        # Create folder and files for the session
        self.create_session_files()


    def create_session_files(self):
        """
        Create the session  folder in the specified directory (or the one by default).
        Later on, results of the plugins will be put in this folder.

        Also create a session_config.ini file in this directory.
        This file contains informations specific to the session.
        """
        try:
            os.makedirs(self._directory)
        except:
            pass
        shutil.copy("session_config.ini", self._directory)
        config_location = "".join([self._directory, "/session_config.ini"])
        config_file = open(config_location, "r+")
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_location)
        parser.set("session_information", "session_name", self._name)
        parser.write(config_file)
        config_file.close()
        results_location = "".join([self._directory, "/session_results.ini"])
        results_file = open(results_location, "a")


    def launch_plugins(self):
        """
        Import all the plugins contained in the specified plugins folder (or the one by default).
        
        As for now, only ipython can be used for rendering, so the plugins actions are registered
        as ipython magic commands.
        """
        for path, subdirs, files in os.walk(self._plugins_directory):
            try:
                importlib.import_module(path.replace("/", "."))
                for f in files:
                    if fnmatch(f, "*.py") and f != "__init__.py":
                        try:
                            plugin_file = os.path.join(path, f).split(".")[0].replace("/", ".")
                            plugin = importlib.import_module(plugin_file)
                            for plugin_class in pyclbr.readmodule(plugin_file):
                                pclass = getattr(plugin, plugin_class)(self)
                                for function in [a for a in inspect.getmembers(pclass, predicate=inspect.ismethod) if a[0]!="__init__"]:
                                    setattr(self.renderer, "do_" + function[0], function[1])
                                    #def doc(self):
                                    #    print function[1].__doc__
                                    #setattr(self.renderer, "do_help_" + function[0], doc)
                        except:
                            print("Error when trying to load plugins from file " + path + "/" + f)
                            pass
            except: 
                print("Error during plugins load")
                pass


    def run_renderer(self):
        """
        Launch the renderer.

        For now only ipython can be used as renderer
        """
        self.renderer.cmdloop()

