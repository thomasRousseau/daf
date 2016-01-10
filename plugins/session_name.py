import ConfigParser


class SessionNameHandler():
    def __init__(self, session):
        self.session = session

    def get_session_name(self, arg):
        """\tReturn the session name."""
        return self.session._name 


    def set_session_name(self, name):
        """\tArgument: new session name 
        Change the session name."""
        #Change the name in the session object
        self.session._name = name
        # Change the name in the shell
        self.session.renderer.prompt = self.session.renderer.prompt.split(">")[0] + "> \033[1;34m" + name + ": \033[1;m"
        #Change the name in the config file
        config_location = "".join([self.session._directory, "/session_config.ini"])
        config_file = open(config_location, "r+")
        parser = ConfigParser.SafeConfigParser()
        parser.readfp(config_file)
        parser.remove_option("session_information", "session_name")
        parser.set("session_information", "session_name", name)
        parser.write(config_file)
        config_file.close()

