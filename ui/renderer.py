#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Handle the graphical outputs of the tool using iPython
"""

from datetime import datetime
import cmd
import types
import inspect
import os

class ShellRenderer(cmd.Cmd):
    def __init__(self, session_name, session_directory):
        cmd.Cmd.__init__(self)
        self.session_directory = session_directory
        self.prompt = "\033[1;32m" + datetime.now().strftime(" %H:%M:%S> ") + "\033[1;34m" + session_name + ": \033[1;m"
        cmd.Cmd.intro = "------------------------------\n   Disk Analysis Framework\n------------------------------\n"

    def precmd(self, command): # TODO: Make this less ugly
        results_file = open(self.session_directory + "/session_results.ini", "r")
        response = True
        found_line = False
        found_command = False
        for i, line in enumerate(results_file):
            if line == ">>> " + command + " <<<\n":
                response = raw_input("This command has already been played. Do you want to replay it (y) or see the last response (n)? [Y/n]:")
                if response in ["n", "N", "no", "NO", "No"]:
                    response = False
                    start_command_line_number = i
                    found_line = True
                    found_command = True
            if found_line and line == ">>> ---------------------- <<<\n":
                end_command_line_number = i + 1
                found_line = False
        results_file.close()
        if not found_command:
            return cmd.Cmd.precmd(self, command)
        else:
            results_file = open(self.session_directory + "/session_results.ini", "r")
            lines = results_file.readlines()
            results_file.close()
            results_file = open(self.session_directory + "/session_results.ini", "w")
            for i, line in enumerate(lines):
                if i < start_command_line_number or i > end_command_line_number:
                    results_file.write(line)
            if response:
                results_file.close()
                return cmd.Cmd.precmd(self, command)
            else:
                for i, line in enumerate(lines):
                    if i >= start_command_line_number and i <= end_command_line_number:
                        results_file.write(line)
                        if i > start_command_line_number and i < end_command_line_number - 1:
                            print line[:-1]
                results_file.close()
                return cmd.Cmd.precmd(self, "nothing")
                

    def postcmd(self, stop, line):
        if stop == True:
            print "Exiting"
            return cmd.Cmd.postcmd(self, True, line)
        elif line == "":
            return cmd.Cmd.postcmd(self, None, line)
        elif stop is not None:
            print stop
            results_file = open(self.session_directory + "/session_results.ini", "a")
            results_file.write(">>> " + line + " <<<\n")
            results_file.write(stop)
            results_file.write("\n>>> ---------------------- <<<\n\n")
            results_file.close()
        self.prompt = "\033[1;32m" + datetime.now().strftime(" %H:%M:%S>") + self.prompt.split(">")[1]
        return cmd.Cmd.postcmd(self, None, line)

    def do_EOF(self, line):
        """\tCtrl+D command quit the program."""
        return True

    def do_quit(self, line):
        """\tExit the program."""
        return True

    def do_exit(self, line):
        """\tExit the program."""
        return True

    def do_nothing(self, line):
        pass

    def do_help(self, line):
        """\tDisplay this help."""
        for function in [a for a in inspect.getmembers(self, predicate=inspect.ismethod) if a[0][0:3] == "do_" and a[0] not in ["do_EOF", "do_nothing", "do_exit", "do_quit"]]:
            print function[0][3::]
            if function[1].__doc__ != None:
                print function[1].__doc__
            print "----------------------------\n"

