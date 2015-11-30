import sys
import os.path
import time
import struct
import core.functions.registry as registry

DEFAULT_SYSTEM_HIVE = "Windows/System32/config/SYSTEM"
DEFAULT_SOFTWARE_HIVE = "Windows/System32/config/SOFTWARE"
DEFAULT_SAM_HIVE = "Windows/System32/config/SAM"

class Configuration():
    def __init__(self, folder, system_hive=None, software_hive=None, sam_hive=None, users_hives=None):
        self.folder = folder
        self.system_hive = self.get_system_hive(system_hive)
        self.software_hive = self.get_software_hive(software_hive)
        self.sam_hive = self.get_sam_hive(sam_hive)
        self.users_hives = self.get_users_hives(users_hives)
        self.os = self.get_os()
        self.current_control_set = self.get_current_control_set()
        self.timezone = self.get_timezone()
        self.os_version = self.get_os_version()
        self.os_build = self.get_os_build()


    def get_system_hive(self, system_hive):
        if system_hive:
            if not os.path.isfile(system_hive):
                raise Exception("Given SYSTEM hive path invalid ! \
                    Make sure you gave the absolute path !")
            else:
                return system_hive
        else:
            if not os.path.isfile(self.folder + DEFAULT_SYSTEM_HIVE):
                raise Exception("SYSTEM hive couldn't be found ! \
                    Use the -y (or --system-hive) option to manually give \
                    its path.")
            else:
                return self.folder + DEFAULT_SYSTEM_HIVE


    def get_software_hive(self, software_hive):
        if software_hive:
            if not os.path.isfile(software_hive):
                raise Exception("Given SOFTWARE hive path invalid ! \
                    Make sure you gave the absolute path !")
            else:
                return software_hive
        else:
            if not os.path.isfile(self.folder + DEFAULT_SOFTWARE_HIVE):
                raise Exception("SOFTWARE hive couldn't be found ! \
                    Use the -o (or --software-hive) option to manually give \
                    its path.")
            else:
                return self.folder + DEFAULT_SOFTWARE_HIVE


    def get_sam_hive(self, sam_hive):
        if sam_hive:
            if not os.path.isfile(sam_hive):
                raise Exception("Given SAM hive path invalid ! \
                    Make sure you gave the absolute path !")
            else:
                return sam_hive
        else:
            if not os.path.isfile(self.folder + DEFAULT_SAM_HIVE):
                raise Exception("SAM hive couldn't be found ! \
                    Use the -a (or --sam-hive) option to manually give \
                    its path.")
            else:
                return self.folder + DEFAULT_SAM_HIVE


    def get_users_hives(self, users_hives):
        if users_hives:
            for (username, hive) in users_hives:
                if not os.path.isfile(hive):
                    raise Exception("Given user hive " + hive + " not found !")
            return users_hives
        else:
            users_hives=[]
            sam_info = registry.samparse(self.sam_hive)
            for user in sam_info['users']:
                username = user
                for key in (k for k in registry.find_key_start_with(
                    self.software_hive,
                    "Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
                    if "ProfileImagePath" in k['Name']):
                    if key['Value'].split("\\")[-1] == username:
                        user_folder = str(key['Value'][3:].replace("\\", "/"))
                        if os.path.isfile(self.folder + user_folder +
                            "/NTUSER.DAT"):
                            users_hives.append((username,
                                self.folder + user_folder + "/NTUSER.DAT"))
            return users_hives


    def get_os(self):
        product_name = registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "ProductName")[0]['Value']
        if "Windows Vista" in product_name:
            return "Windows Vista"
        elif "Windows 7" in product_name:
            return "Windows 7"
        elif "Windows 8" in product_name:
            return "Windows 8"
        elif "Windows 10" in product_name:
            return "Windows 10"
        else:
            raise Exception("Impossible to detect OS version !")


    def get_current_control_set(self):
        return "ControlSet00" + registry.get_registry_key_specific_value(
            self.system_hive, "Select", "Current")[0]['Value']


    def get_timezone(self):
        timezone_bias = int(registry.get_registry_key_specific_value(
            self.system_hive,
            self.current_control_set + "\\Control\\TimezoneInformation",
            "Bias")[0]['Value'])
        if timezone_bias > 0:
            return "UTC +" + str(timezone_bias/60)
        elif timezone_bias < 0:
            return "UTC " + str(timezone_bias/60)
        else:
            return "UTC"


    def get_os_version(self):
        product_name = registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "ProductName")[0]['Value'] 
        CSD_version = registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "CSDVersion")[0]['Value']
        return product_name + " " + CSD_version


    def get_os_build(self):
        return registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "CurrentBuild")[0]['Value']


    def get_os_registered_organization(self):
        return registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "RegisteredOrganization")[0]['Value']


    def get_os_registered_owner(self):
        return registry.get_registry_key_specific_value(
            self.software_hive, "Microsoft\\Windows NT\\CurrentVersion",
            "RegisteredOwner")[0]['Value']


    def get_last_reboot(self):
        shutdown_time = registry.get_registry_key_specific_value(
            self.system_hive, self.current_control_set + "\\Control\\Windows",
            "ShutdownTime")[0]['Value']
        return format(registry.filetime_to_date(shutdown_time),
            '%a, %d %B %Y %H:%M:%S %Z')


    def get_computer_name(self, folder):
        return registry.get_registry_key_specific_value(self.system_hive,
            self.current_control_set + "\\Control\\ComputerName\\ComputerName",
            "ComputerName")[0]['Value']

        
    def get_startup_list(self):
        startup_list = []
        key_list = []
        for key_name in ["Microsoft\\Windows\\CurrentVersion\\Run",
            "Microsoft\\Windows\\CurrentVersion\\RunOnce",
            "Microsoft\\Windows\\CurrentVersion\\RunOnceEx",
            "Microsoft\\Windows\\CurrentVersion\\RunServices",
            "Microsoft\\Windows\\CurrentVersion\\RunServicesOnce",
            "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Userinit",
            "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Notify",
            "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Shell"]:
            try:
                key = registry.get_registry_subkeys(self.software_hive,
                    key_name)
                key_list += key
            except:
                pass
        for subkey in key_list:
            startup_list.append(subkey)
        return startup_list


    def get_registered_applications(self):
        return registry.get_registry_subkeys(self.software_hive,
            "RegisteredApplications")

