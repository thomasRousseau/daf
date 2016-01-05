import core.functions.registry as registry
import core.functions.sqlite_parser as sqlite_parser
import json

class Browser():
    def __init__(self, name, version):
        self.name = name
        self.version = version


class Chrome():
    def __init__(self, folder, name, version, user, chrome_folder=None):
        self.folder = folder
        self.name = name
        self.version = version
        self.user = user
        self.chrome_folder = chrome_folder if chrome_folder else "Users/" + \
            user + "/AppData/Local/Google/Chrome/User Data/Default/"

    def get_cache(self, filepath=""):
        #TODO
        pass

    def get_current_session(self, filepath=""):
        #TODO
        pass

    def get_current_tabs(self, filepath=""):
        #TODO
        pass

    def get_cookies(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Cookies"
            # TODO: Decrypt cookies values
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_extensions(self, filepath=""):
        #TODO
        pass

    def get_extension_cookies(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "Extension Cookies"
            # TODO: Decrypt cookies values
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_favicons(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Favicons"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_history(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "History"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_history_provider_cache(self, filepath=""):
        #TODO
        pass

    def get_login_data(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Login Data"
            # TODO: Decrypt passwords
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_network_action_predictor(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "Network Action Predictor"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_network_persistent_state(self, filepath=""): 
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "Network Persistent State"
            f = open(filepath, "r")
            raw_data = f.read()
            f.close()
            return json.loads(raw_data)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_origin_bound_certs(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "Origin Bound Certs"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_preferences(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Preferences"
            f = open(filepath, "r")
            raw_data = f.read()
            f.close()
            return json.loads(raw_data)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_quotamanager(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "QuotaManager"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_secure_preferences(self, filepath=""): 
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "Secure Preferences"
            f = open(filepath, "r")
            raw_data = f.read()
            f.close()
            return json.loads(raw_data)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_shortcuts(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Shortcuts"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_tops_sites(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Top Sites"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_transportsecurity(self, filepath=""): 
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + \
                    "TransportSecurity"
            f = open(filepath, "r")
            raw_data = f.read()
            f.close()
            return json.loads(raw_data)
        except:
            print "The \"" + filepath + "\" file couldn't be found."

    def get_visited_links(self, filepath=""):
        #TODO
        pass

    def get_web_data(self, filepath=""):
        try:
            if not filepath:
                filepath = self.folder + self.chrome_folder + "Web Data"
            return sqlite_parser.sqlite_parser(filepath)
        except:
            print "The \"" + filepath + "\" file couldn't be found."


class IE():
    def __init__(self):
        pass


class Firefox():
    def __init__(self):
        pass


def find_installed_browser(config):
    """
    Find the installed browser in the analysed disk.
    For now, the tool only supports IE, Firefox and Chrome, which
    should nonetheless represents the majority of users on Windows.

    Return: List of (name, version) for all installed browser
    """
    #TODO: Replace registry hive path with Configuration object
    #TODO: Check what happens if multiple version of same browser are installed
    browsers_list = []
    try:
        new_ie = registry.get_registry_key_specific_value(config.software_hive,
            "Microsoft\\Internet Explorer", "svcVersion")
        if new_ie:
            browsers_list.append({'Browser Name': "Internet Explorer",
                                  'Browser Version': new_ie[0]['Value']})
    except:
        try:
            ie = registry.get_registry_key_specific_value(config.software_hive,
                "Microsoft\\Internet Explorer", "Version")
            if ie:
                browsers_list.append({'Browser Name': "Internet Explorer",
                                      'Browser Version': ie[0]['Value']})
        except:
            pass
    try:
        firefox = registry.get_registry_key_specific_value(config.software_hive,
            "Mozilla\\Mozilla Firefox", "CurrentVersion")
        if firefox:
            browsers_list.append({'Browser Name': "Mozilla Firefox",
                                  'Browser Version': firefox[0]['Value']})
    except:
        pass
    for (user, hive) in config.users_hives:
        try:
            chrome = registry.get_registry_key_specific_value(hive,
                "Software\\Google\\Chrome\\BLBeacon", "version")
            if chrome:
                browsers_list.append({'Browser Name': "Google Chrome",
                                      'Browser Version': chrome[0]['Value'],
                                      'User': user})
        except:
            pass
        try:
            chromium = registry.get_registry_key_specific_value(hive,
                "Software\\Chromium\\BLBeacon", "version")
            if chromium:
                browsers_list.append({'Browser Name': "Chromium",
                                      'Browser Version': chromium[0]['Value'],
                                      'User': user})
        except:
            pass
    return browsers_list


def get_settings(folder, browser):
    pass


def get_plugins_list(folder, browser):
    pass


def get_profiles(folder, browser):
    pass


def get_bookmarks_list(folder, browser):
    pass


def get_typed_url(config, folder, browser):
    # TODO: Change NTUSER path using Configuration object
    return registry.get_registry_subkey(folder + "Users/IEUser/NTUSER.DAT", "Software\\Microsoft\\Internet Explorer\\TypedURLs")


def get_history(folder, browser):
    pass


def get_cookies_list(folder, browser):
    pass

DISK = '/mnt/441EDCA81EDC93F0/Data/Linux/Documents/Eurecom/Project/Samples/disk_mounted/disk4/'
import core.objects.config as config
import core.functions.registry as registry
#print registry.get_registry_subkey(DISK + "Users/IEUser/NTUSER.DAT", "Software\\Microsoft\\Internet Explorer\\TypedURLs")
#print registry.browse_registry_from_key(DISK + registry.SOFTWARE_PATH, "Microsoft\\Windows\\CurrentVersion\\Uninstall", 2)
import core.objects.config as config
a = config.Configuration(DISK)
for browser in find_installed_browser(a):
    print browser
#    if browser['Browser Name'] == "Google Chrome":
#        chrome = Chrome(DISK, browser['Browser Name'], browser['Browser Version'], "IEUser")
#        print chrome.get_cookies()


