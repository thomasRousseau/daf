from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)
from IPython.core.magic import (Magics, magics_class, line_magic)
from datetime import datetime
import ConfigParser


@magics_class
class SessionNameHandler(Magics):
    def __init__(self, shell, session):
        super(SessionNameHandler, self).__init__(shell)
        self.session = session

    @line_magic
    def get_session_name(self, arg):
        """ 
        Return the session name.    
        """
        print(self.session._name) 


    @magic_arguments()
    @argument('name', type=str, help='The new name you want to give to the session')
    @line_magic
    def set_session_name(self, arg):
        """ 
        Change the session name.    
        """
        args = parse_argstring(self.set_session_name, arg)
        #Change the name in the session object
        self.session._name = args.name
        # Change the name in the shell
        self.session.renderer.change_session_name(args.name)
        #Change the name in the config file
        config_location = "".join([self.session._directory, "/session_config.ini"])
        config_file = open(config_location, "r+")
        parser = ConfigParser.SafeConfigParser()
        parser.readfp(config_file)
        parser.remove_option("session_information", "session_name")
        parser.set("session_information", "session_name", args.name)
        parser.write(config_file)

