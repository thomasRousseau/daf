from datetime import datetime
import core.functions.registry as registry


class UsbPartition():
    def __init__(self, serial_number, name, usb_type, vendor, product, version,
        drive, guid, user, first_connection, first_connection_since_reboot,
        last_connection):
        self.serial_number = serial_number
        self.firendly_name = name
        self.usb_type = usb_type
        self.vendor = vendor
        self.product = product
        self.version = version
        self.drive = drive
        self.guid = guid
        self.user = user
        self.first_connection = first_connection
        self.first_connection_since_reboot = first_connection_since_reboot
        self.last_connection = last_connection


class Usb():
    def __init__(self, pid_vid, partitions_list):
        self.pid_vid = pid_vid
        self.partitions_list = partitions_list



def find_usbstor_info(config):
    """ 
    Find all usb informations present in the 
        SYSTEM\CurrentControlSet\Enum\USBSTOR registry key.

    Arguments: The Configuration object for the analyzed disk.

    Return: A list of all the present informations by tuple.
            For Windows XP, a tuple contains the usb type, vendor, product,
                version, serial number and parent prefix id.
            For other Windows versions, a tuple contains the same informations
                with the exception of the parent prefix id which doesn't exist
                anymore.
    """
    usbstor_info_list = []
    serial_number_list = []
    try:
        for usb_info in registry.find_key_start_with(config.system_hive,
            config.current_control_set + "\\Enum\\USBSTOR"):
            if "FriendlyName" in usb_info['Name']:
                last_write = usb_info['Last Write Time']
                serial_number = str(usb_info['Name'].split("\\")[4])
                usb_type, usb_vendor, usb_product_id, usb_revision = \
                    usb_info['Name'].split("\\")[3].split("&")
                friendly_name = str(usb_info['Value'])
                if serial_number not in serial_number_list:
                    usbstor_info_list.append([last_write, serial_number,
                    usb_type, usb_vendor, usb_product_id, usb_revision,
                    friendly_name])
                    serial_number_list.append(serial_number)
    finally:
        return usbstor_info_list


def find_usb_info(config):
    """
    Find all usb informations present in the SYSTEM\CurrentControlSet\Enum\USB 
        registry key.

    Arguments: The Configuration object for the analyzed disk.

    Return: A list of all the present informations by tuple.
            A tuple contains the serial number of the device and the 
            identifiant of the device composed by a vendor id (VID), a product
            id (PID) and eventually a MI number.
    """
    usb_info_list = []
    serial_number_list = []
    for usb_info in registry.find_key_start_with(config.system_hive,
        config.current_control_set + "\\Enum\\USB"):
        last_write = usb_info['Last Write Time']
        pid_vid = usb_info['Name'].split("\\")[3]
        serial_number = str(usb_info['Name'].split("\\")[4])
        if serial_number not in serial_number_list:
            usb_info_list.append([last_write, serial_number, pid_vid])
            serial_number_list.append(serial_number)
    return usb_info_list


def find_mounteddevices_info(config, serial_number):
    """
    Parse the SYSTEM\MountedDevices registry key looking for informations
    corresponding to the USB device with the given serial number.

    Arguments: The Configuration object for the analyzed disk.
               The serial number of the device to look for.

    Return: A list with the drive where the USB device was mount and his guid.
            A None object if the informations couldn't be retrieved.
    """
    drive = None
    device_guid = None
    for subkey in registry.get_registry_subkeys(config.system_hive, 
        "MountedDevices")[0]['Values']:
        subkey_value = "".join(chr(ord(c)) for c in subkey['Value'] if c != '\x00')
        if serial_number in subkey_value and "DosDevices" in subkey['Name']:
            drive = subkey['Name'].split("\\")[-1]
        else:
            device_guid = subkey['Name'].split("Volume")[-1]
    if drive and device_guid:
        return [drive, device_guid]
    return ["Drive couldn't be found :(", "GUID couldn't be found :("]


def find_usb_user(config, guid):
    """
    Find the user (if any) that used the specific usb device.
    This information is contained in the NTUSER.DAT\SOFTWARE\Microsoft\Windows\
        CurrentVersion\Explorer\MountPoints2 registry key.

    Arguments:  The Configuration object for the analyzed disk.
                The guid of the device.
    
    Return: The username of the user who used the device.
            A None object if the information can't be retrieved.
    """
    try:
        for user, user_hive in config.users_hives:
            for key in registry.find_key_start_with(config.users_hives, 
                "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\" + 
                "MountPoints2"):
                if guid in key['Name']:
                    return user
    except:
         return "User couldn't be found :("


def find_first_connection(config, serial_number):
    """
    Find the time of the first connection of the device with the given serial
        number.
    This information is stored in the C:\Windows\setupapi.log file for Windows
        XP and in the C:\Windows\inf\setupapi.dev.log for the other versions.

    Arguments: The Configuration object of the analyzed disk.
               The serial number of the device.

    Return: The time of the first connection for the device.
            A None object if the information couldn't be retrieved.
    """
    if config.os == "Windows 10":
        setupapi_dev_file = "Windows/INF/setupapi.dev.log" 
    else:
        setupapi_dev_file = "Windows/inf/setupapi.dev.log"
    with open(config.folder + setupapi_dev_file, "r") as setupapi_file:
        for line in setupapi_file:
            if serial_number in line:
                first_connection = setupapi_file.next().strip()[19:]
                return datetime.strptime(first_connection, '%Y/%m/%d %H:%M:%S.%f')
    

def get_usb_objects_list(config):
    """
    Create all the usb objects according to the analysed disk.

    Arguments: The Configuration object for the analysed disk.

    Return: A list of all the Usb objects populates this their informations.
    """
    usb_objects_list = []
    usbstor = find_usbstor_info(config)
    usb = find_usb_info(config)
    for usb_info in usb:
        partitions_list = []
        for usbstor_info in usbstor:
            if usb_info[1] in usbstor_info[1]:
                drive = find_mounteddevices_info(config, usbstor_info[1])
                user = find_usb_user(config, drive[1])
                first_connection = find_first_connection(config,
                    usbstor_info[1])
                partitions_list.append(UsbPartition(usb_info[1], 
                    usbstor_info[6], usbstor_info[2], usbstor_info[3],
                    usbstor_info[4], usbstor_info[5], drive[0], drive[1],
                    user, first_connection, usbstor_info[0], usb_info[0]))
        usb_objects_list.append(Usb(usb_info[2], partitions_list))
    return usb_objects_list


def find_usb_by_serial_number(usb_list, serial_number):
    """
    Find a specific usb object in a usb_list thanks to the serial number

    Arguments:  A Usb objects list.
                The serial_number to look for.

    Return: The Usb object among the list that have the given serial number if
                it exist.
            A None object otherwise.
    """
    for usb in usb_list:
        for partition in usb.partitions_list:
            if partition.serial_number == serial_number:
                return usb
    return None


def find_usb_by_pid_vid(usb_list, pid_vid):
    """
    Find a specific usb object in a usb_list thanks to the serial number

    Arguments:  A Usb objects list.
                The serial_number to look for.

    Return: The Usb object among the list that have the given serial number if
                it exist.
            A None object otherwise.
    """
    for usb in usb_list:
        if usb.pid_vid == pid_vid:
            return usb
    return None

