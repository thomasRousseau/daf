from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)
from IPython.core.magic import (Magics, magics_class, line_magic)
from datetime import datetime
import ConfigParser
from core.objects.config import Configuration
import core.functions.common as common


@magics_class
class ConfigurationHandler(Magics):
    def __init__(self, shell, session):
        super(ConfigurationHandler, self).__init__(shell)
        self.session = session
        self.configuration = Configuration(session.input_disk)

    @line_magic
    def display_config(self, arg):
        """ 
        Return the session name.    
        """
        print("Configuration of the input disk:")
        print("--------------------------------\n")
        print("Folder location: \t\t" + self.configuration.folder)
        print("OS: \t\t\t\t" + self.configuration.os)
        print("OS version: \t\t\t" + self.configuration.os_version)
        print("OS build: \t\t\t" + self.configuration.os_build)
        print("Computer name: \t\t\t" + self.configuration.get_computer_name())
        print("Timezone: \t\t\t" + self.configuration.timezone)
        print("Last reboot: \t\t\t" + self.configuration.get_last_reboot())
        print("System hive: \t\t\t" + self.configuration.system_hive)
        print("Software hive: \t\t\t" + self.configuration.software_hive) 
        print("Sam hive: \t\t\t" + self.configuration.sam_hive)
        print("Users hive:")
        for h in self.configuration.users_hives:
            if h!= self.configuration.users_hives[0]:
                print("\t---------------------------------------") 
            print("\tUsername: \t\t"+h[0]+"\n\tHive: \t\t\t"+h[1]) 
        print("Current control set: \t\t" + self.configuration.current_control_set)
        print("OS registered organization: \t" + self.configuration.get_os_registered_organization())
        print("OS registered owner: \t\t" + self.configuration.get_os_registered_owner())
        print("Startup applications: \t\t")
        for b in self.configuration.get_startup_list():
            for a in b['Values']:
                print("\tName: "+a['Name']+"\t\t\tValue: "+a['Value'])
        print("Registered applications: \t\t")
        for b in self.configuration.get_registered_applications():
            for a in b['Values']:
                print("\tName: "+a['Name']+"\t\t\tValue: "+a['Value'])

