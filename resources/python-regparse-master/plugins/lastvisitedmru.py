import sys
from Registry import Registry
from jinja2 import Template, Environment, PackageLoader

class PluginClass(object):

    def __init__(self, hives=None, search=None, format=None, format_file=None):
        self.hives = hives
        self.search = search
        self.format = format
        self.format_file = format_file

    def ProcessPlugin(self):

        env = Environment(keep_trailing_newline=True, loader=PackageLoader('regparse', 'templates'))

        lastvisited = ["Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedMRU",
                       "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU",
                       "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRULegacy"
                       ]

        for hive in self.hives:
            try:
                for k in lastvisited:
                    last_write = Registry.Registry(hive).open(k).timestamp()
                    key = Registry.Registry(hive).open(k).name()
                    mruorder = Registry.Registry(hive).open(k).value("MRUList").value()
                    for entry in list(mruorder):
                        for vals in Registry.Registry(hive).open(k).values():
                            if vals.name() == entry:
                                value = vals.name()
                                data = vals.value()
                                if self.format_file is not None:                
                                    with open(self.format_file[0], "rb") as f:
                                        template = env.from_string(f.read())
                                        sys.stdout.write(template.render(last_write=last_write, \
                                                                         key=key, \
                                                                         mruorder=mruorder, \
                                                                         value=value, \
                                                                         data=data) + "\n")
                                elif self.format is not None:           
                                    template = Environment().from_string(self.format[0])
                                    sys.stdout.write(template.render(last_write=last_write, \
                                                                     key=key, \
                                                                     mruorder=mruorder, \
                                                                     value=value, \
                                                                     data=data) + "\n")                                
            except (Registry.RegistryKeyNotFoundException, Registry.RegistryValueNotFoundException):
                continue



