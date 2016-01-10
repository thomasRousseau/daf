import shutil
import os

class SessionDirectoryHandler():
    def __init__(self, session):
        self.session = session

    def get_session_directory(self, arg):
        """\tReturn the session directory."""
        return self.session._directory 


    def set_session_directory(self, directory):
        """\tArgument: new folder name in relative name
        Change the session directory."""
        shutil.move(self.session._directory, directory)
        self.session._directory = os.path.abspath(directory)
        self.session.renderer.session_directory =  os.path.abspath(directory)

