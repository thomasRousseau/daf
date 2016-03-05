import core.objects.usb as u

class UsbHandler():
    def __init__(self, session):
        self.session = session

    def display_usb(self, arg):
        """\tDisplay information about the usb devices that have been connected to the system."""
        output = "\n"
        usb_objects = u.get_usb_objects_list(self.session.configuration)
        for usb in usb_objects:
            output += "PID VID:\t\t" + usb.pid_vid + "\n"
            output += "Partitions:\n"
            for partition in usb.partitions_list:
                output += "\tSerial number:\t\t\t" + partition.serial_number + "\n"
                output += "\tName:\t\t\t\t" + partition.friendly_name + "\n"
                output += "\tType:\t\t\t\t" + partition.usb_type + "\n"
                output += "\tVendor:\t\t\t\t" + partition.vendor + "\n"
                output += "\tProduct:\t\t\t" + partition.product + "\n"
                output += "\tVersion:\t\t\t" + partition.version + "\n"
                output += "\tDrive:\t\t\t\t" + partition.drive + "\n"
                output += "\tGUID:\t\t\t\t" + partition.guid + "\n"
                output += "\tUser:\t\t\t\t" + partition.user + "\n"
                output += "\tFirst connection:\t\t" + '%s/%s/%s' % (partition.first_connection.month, partition.first_connection.day, partition.first_connection.year) + "\n"
                output += "\tFirst connection since reboot:\t" + '%s/%s/%s' % (partition.first_connection_since_reboot.month, partition.first_connection_since_reboot.day, partition.first_connection_since_reboot.year) + "\n"
                output += "\tLast connection:\t\t" +  '%s/%s/%s' % (partition.last_connection.month, partition.last_connection.day, partition.last_connection.year) + "\n"
                output += "\n"
            output = output[:-1]
            if not usb.partitions_list:
                output += "\t\tNone\n"
            output += "---------------------------------\n\n"
        return output
 
