from datetime import datetime
import ConfigParser
from core.objects.config import Configuration
import core.functions.common as common


class ConfigurationHandler():
    def __init__(self, session):
        self.session = session
        self.configuration = Configuration(session.input_disk)

    def display_config(self, arg):
        """\tDisplay the configuration parameters of the disk to analyze."""
        output = "Configuration of the input disk:\n"
        output += "--------------------------------\n"
        output += "Folder location: \t\t" + self.configuration.folder + "\n"
        output += "OS: \t\t\t\t" + self.configuration.os + "\n"
        output += "OS version: \t\t\t" + self.configuration.os_version + "\n"
        output += "OS build: \t\t\t" + self.configuration.os_build + "\n"
        output += "Computer name: \t\t\t" + self.configuration.get_computer_name() + "\n"
        output += "Timezone: \t\t\t" + self.configuration.timezone + "\n"
        output += "Last reboot: \t\t\t" + self.configuration.get_last_reboot() + "\n"
        output += "System hive: \t\t\t" + self.configuration.system_hive + "\n"
        output += "Software hive: \t\t\t" + self.configuration.software_hive + "\n" 
        output += "Sam hive: \t\t\t" + self.configuration.sam_hive + "\n"
        output += "Users hive:\n"
        for h in self.configuration.users_hives:
            if h!= self.configuration.users_hives[0]:
                output += "\t---------------------------------------\n" 
            output += "\tUsername: \t\t"+h[0]+"\n\tHive: \t\t\t"+h[1]+"\n" 
        output += "Current control set: \t\t" + self.configuration.current_control_set + "\n"
        output += "OS registered organization: \t" + self.configuration.get_os_registered_organization() + "\n"
        output += "OS registered owner: \t\t" + self.configuration.get_os_registered_owner() + "\n"
        output += "Startup applications: \t\t\n"
        for b in self.configuration.get_startup_list():
            for a in b['Values']:
                output += "\tName: "+a['Name']+"\t\t\tValue: "+a['Value']+"\n"
        output += "Registered applications: \t\t\n"
        for b in self.configuration.get_registered_applications():
            for a in b['Values']:
                output += "\tName: "+a['Name']+"\t\t\tValue: "+a['Value']+"\n"
        return output

