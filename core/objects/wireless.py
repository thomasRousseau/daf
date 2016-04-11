from os import listdir, walk
from os.path import isfile, join
import xmltodict

DEFAULT_WIRELESS_IF_FOLDER = "ProgramData/Microsoft/Wlansvc/Profiles/Interfaces/"


class WirelessInterface():
	def __init__(self, xml_file):
		self.xml_file = xml_file
		self.xml_dict = self.get_xml_dict(self.xml_file)
		self.SSID = self.xml_dict['WLANProfile']['SSIDConfig']['SSID']['name']
		self.encryption = self.xml_dict['WLANProfile']['MSM']['security']['authEncryption']['encryption']
		self.authentication = self.xml_dict['WLANProfile']['MSM']['security']['authEncryption']['authentication']


	def get_xml_dict(self, xml_file):
		try:
			with open(xml_file) as fd:
				return xmltodict.parse(fd.read())
		except IOError as e:
			print('No such file ({e})'.format(e=e))
		except ExpatError as e:
			print('XML parsing error ({e})'.format(e=e))


def find_wireless_if(conf):
	interfaces = {}
	folder = conf.folder + DEFAULT_WIRELESS_IF_FOLDER
	for network_adaptater in next(walk(folder))[1]:
		interfaces[network_adaptater] = []
		wireless_ifs = [f for f in listdir(join(folder, network_adaptater)) if isfile(join(folder, network_adaptater, f))]
		for wireless_if in wireless_ifs:
			interfaces[network_adaptater].append(
				WirelessInterface(join(folder, network_adaptater, wireless_if)))
	return interfaces



