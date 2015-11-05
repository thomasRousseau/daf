import os, io, sys, imp
import ConfigParser
from Registry import Registry

class RegparsePluginManager(object):
	
	def __init__(self, plugin_directory=None, plugin=None):
		self.plugin_directory = plugin_directory
		self.plugin = plugin

	def gatherallPlugins(self, plugin_directory):
		allPlugins = []
		for plugin in os.listdir(plugin_directory):
			if plugin.endswith(".py") and plugin[:-3] != "__init__":
				plugin_name = plugin[:-3]
				allPlugins.append(plugin_name)	
		return(allPlugins)				

	def listPlugin(self, plugin_directory):
		for plugin in self.gatherallPlugins(plugin_directory):
			print plugin
			
	def detailedPlugin(self, plugin_directory):
		dict = {}		
		
		for plugin_doc in os.listdir(plugin_directory):
			if plugin_doc.endswith(".plugin"):
				plugin_doc_path = os.path.join(plugin_directory, plugin_doc)
				config = ConfigParser.RawConfigParser(allow_no_value=True)
				config.readfp(open(plugin_doc_path))
				try:
					plugin = config.get("Documentation", "Plugin")
					author = config.get("Documentation", "Author")
					version = config.get("Documentation", "Version")
					reference = config.get("Documentation", "Reference")
					printfields = config.get("Documentation", "PrintFields")
					description = config.get("Documentation", "Description")
					print plugin.upper()
					print '\tPlugin: \t%s' % (plugin.upper())
					print '\tAuthor: \t%s' % (author)
					print '\tVersion: \t%s' % (version)
					print '\tReference: \t%s' % (reference)
					print '\tPrint Fields: \t%s' % (printfields)
					print '\tDescription: \t%s' % (description)
				except ConfigParser.NoOptionError:
					print plugin_doc.upper()[:-7] + " does not have a proper .plugin config file."
				
	def findPlugin(self, plugin, plugin_directory):
		try:
			found_plugins = imp.find_module(plugin, [plugin_directory])
			
		except ImportError as error:
			print 'Plugin Not Found:', error		
		
		return found_plugins
	
	def loadPlugin(self, plugin, found_plugin):
		try:
			module = imp.load_module(plugin, found_plugin[0], found_plugin[1], found_plugin[2])
		except TypeError as error:
			print error

		return module
	
class HelperFunctions(object):

	def __init__(self, hive=None):	
		self.hive = hive

	def CurrentControlSet(self):
		select = Registry.Registry(self.hive).open("Select")
		current = select.value("Current").value()
		controlsetnum = "ControlSet00%d" % (current)
		return(controlsetnum)