from Registry import Registry

SYSTEM_PATH = "Windows/System32/config/SYSTEM"
SOFTWARE_PATH = "Windows/System32/config/SOFTWARE"
SAM_PATH = "Windows/System32/config/SAM"

def get_registry_key(hive, key_path, depth=0):
    try:
        key_list = []
        subkey_list = []
        key = Registry.Registry(hive).open(key_path)
        last_write = key.timestamp()
        for value in key.values():
            key_name = key_path + "\\" +  value.name()
            key_value = value.value()

            key_list.append((key_name, key_value))

        if depth:
            for subkey in key.subkeys():
                subkey_name = subkey.name()
                subkey_info = get_registry_key(hive, key_path + "\\" + subkey_name, depth -1)
                if subkey_info:
                    subkey_list.append(subkey_info)

        return [last_write, key_list, subkey_list]

    except Registry.RegistryKeyNotFoundException as e:
        pass


def find_registry_key_by_name(folder, name, hive_list=[SYSTEM_PATH, SOFTWARE_PATH, SAM_PATH]):
    split_name = name.split("\\")
    for hive in hive_list:
        for i in range(len(split_name), 0, -1):
            try:
                key_name = restore_key_name(split_name[0:i])
                key = get_registry_key(folder + hive, key_name, 0)
                for subkey in key[1]:
                    if subkey[0] == name:
                        return subkey
            except: 
                pass
    print "Registry key \"" + name + "\" not found :("
    return ""


def restore_key_name(subname_list):
    key_name = ""
    for subname in subname_list:
        key_name += subname
        key_name += "\\"
    return key_name[:-1]


def find_key_start_with(hive, key_start, depth=-1):
    try: 
        key_list = []
        key = Registry.Registry(hive).open(key_start)
        last_write = key.timestamp()
        for value in key.values():
            key_name = key_start + "\\" +  value.name()
            key_value = value.value()

            key_list.append((key_name, key_value))

        if depth:
            for subkey in key.subkeys():
                subkey_name = subkey.name()
                subkey_info = find_key_start_with(hive, key_start + "\\" + subkey_name, depth -1)
                if subkey_info:
                    key_list += subkey_info

        return key_list

    except Registry.RegistryKeyNotFoundException as e:
        pass

