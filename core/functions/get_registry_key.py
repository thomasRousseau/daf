from Registry import Registry

def get_registry_key(hive, key_path, depth):
    try:
        key_list = []
        subkey_list = []
        key = Registry.Registry(hive).open(key_path)
        last_write = key.timestamp()
        for value in key.values():
            key_name = value.name()
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
        print e


