import sys
import time
import struct
import datetime
import core.functions.registry as registry

class Configuration():
    def __init__(self, folder):
        self.os = self.get_os(folder)
        if not self.os:
            sys.exit(-1)
        self.current_control_set = self.get_current_control_set(folder)
        self.timezone = self.get_timezone(folder)
        self.os_version = self.get_os_version(folder)
        self.os_build = self.get_os_build(folder)
        self.os_registered_organization = self.get_os_registered_organization(folder)
        self.os_registered_owner = self.get_os_registered_owner(folder)
        self.last_reboot = self.get_last_reboot(folder)
        self.computer_name = self.get_computer_name(folder)
        self.network_interfaces = []
        self.firewall_config = ""
        self.security_events_list = []
        self.startup_list = self.get_startup_list(folder)
        self.registered_applications = self.get_registered_applications(folder)


    def get_current_control_set(self, folder):
        return "ControlSet00" + str(registry.find_registry_key_by_name(folder, "Select\\Current")[1])

    def get_timezone(self, folder):
        timezone_bias = registry.find_registry_key_by_name(folder, self.current_control_set + "\\Control\\TimezoneInformation\\Bias")[1]
        if timezone_bias > 0:
            return "UTC +" + str(timezone_bias/60)
        elif timezone_bias < 0:
            return "UTC " + str(timezone_bias/60)
        else:
            return "UTC"

    def get_os(self, folder):
        product_name = registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\ProductName")[1]
        if "Windows 7" in product_name:
            return "Windows 7"
        elif "Windows Vista" in product_name:
            return "Windows Vista"
        elif "Windows XP" in product_name:
            return "Windows XP"
        else:
            print "Impossible to detect OS version"

    def get_os_version(self, folder):
        product_name = registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\ProductName")[1] 
        CSD_version = registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\CSDVersion")[1]
        return product_name + " " + CSD_version

    def get_os_build(self, folder):
        return registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\CurrentBuild")[1]

    def get_os_registered_organization(self, folder):
        return registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\RegisteredOrganization")[1]

    def get_os_registered_owner(self, folder):
        return registry.find_registry_key_by_name(folder, "Microsoft\\Windows NT\\CurrentVersion\\RegisteredOwner")[1]

    def get_last_reboot(self, folder):
        shutdown_time = registry.find_registry_key_by_name(folder, self.current_control_set + "\\Control\\Windows\\ShutdownTime")
        return format(self.__filetime_to_date(shutdown_time[1]), '%a, %d %B %Y %H:%M:%S %Z')

    # Windows store the last shutdown time in 64-bit filetime format (in hex string little endian).
    def __filetime_to_date(self, little_endian):
        big_endian = ""
        for c in little_endian[::-1]:
            big_endian += format(ord(c), "x")
        microseconds = int(big_endian, 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds)

    def get_computer_name(self, folder):
        return registry.find_registry_key_by_name(folder, self.current_control_set + "\\Control\\ComputerName\\ComputerName\\ComputerName")[1]
        
    def get_startup_list(self, folder):
        startup_list = []
        key_list = []
        for key_name in ["Microsoft\\Windows\\CurrentVersion\\Run", "Microsoft\\Windows\\CurrentVersion\\RunOnce", "Microsoft\\Windows\\CurrentVersion\\RunOnceEx", "Microsoft\\Windows\\CurrentVersion\\RunServices", "Microsoft\\Windows\\CurrentVersion\\RunServicesOnce", "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Userinit", "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Notify", "Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Shell"]:
            try:
                key = registry.get_registry_key(folder + registry.SOFTWARE_PATH, key_name, 0)[1]
                key_list += key
            except:
                pass
        for subkey in key_list:
            startup_list.append(subkey)
        return startup_list

    def get_registered_applications(self, folder):
        return registry.get_registry_key(folder + registry.SOFTWARE_PATH, "RegisteredApplications", 0)[1] #TODO : go deeper and return formatted output ?
        
