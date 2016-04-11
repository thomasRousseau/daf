import core.objects.wireless as w


class WirelessHandler():
	def __init__(self, session):
		self.session = session

	def display_wireless_if(self, arg):
		"""\tDisplay the registered Wireless Interfaces"""
		output = "List of registered Wireless Interfaces:\n\n"
		for wireless_adapt, wireless_ifs in w.find_wireless_if(self.session.configuration).items():
			output += "On {adapt}\n".format(adapt=wireless_adapt)
			for wireless_if in wireless_ifs:
				output += "\tSSID : {ssid}\n\t\tAuthentication : {auth}\n\t\tEncryption : {enc}\n".format(
					ssid=wireless_if.SSID, auth=wireless_if.authentication, enc=wireless_if.encryption)
		if output.count("\n") == 2:
			output += "No registered wireless interfaces were found"
		return output
