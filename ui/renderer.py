#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Handle the graphical outputs of the tool using iPython
"""

from datetime import datetime

from traitlets.config.loader import Config
from IPython.terminal.embed import InteractiveShellEmbed

    
class IPythonRenderer(object):
    def __init__(self, session_name):
        """Creates a new ipython renderer.
        
        Returns:
            a IPythonRenderer object.
        """
        self.cfg = Config()
        prompt_config = self.cfg.PromptManager
        prompt_config.in_template = "".join(["{color.LightCyan}", session_name, "{color.Green}",  datetime.now().strftime(" %H:%M:%S> "), "{color.normal}"])
        prompt_config.in2_template = "   .\\D.: "
        prompt_config.out_template = "Out<\\#>: "
        self.ipshell = InteractiveShellEmbed(config=self.cfg,
                       banner1 = "",
                       exit_msg = "")


    def run(self):
        """
        Run the ipython embeded shell.
        """
        self.ipshell("----------------------------------------------------------\n"
            "           Disk Forensic Analysis Framework v0.1\n"
            "----------------------------------------------------------")


    def change_session_name(self, name):
        """
        Change the session name in the prompt.
        """
        self.ipshell.magic("".join(["config PromptManager.in_template = \"{color.LightCyan}", name, "{color.Green}",  datetime.now().strftime(" %H:%M:%S> "), "{color.normal}\""]))

