from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)
from IPython.core.magic import (Magics, magics_class, line_magic)
import shutil
import os

@magics_class
class SessionDirectoryHandler(Magics):
    def __init__(self, shell, session):
        super(SessionDirectoryHandler, self).__init__(shell)
        self.session = session

    @line_magic
    def get_session_directory(self, arg):
        """ 
        Return the session directory.    
        """
        print(self.session._directory) 


    @magic_arguments()
    @argument('directory', type=str, help='The new directory where to put the results for this session')
    @line_magic
    def set_session_directory(self, arg):
        """ 
        Change the session directory.    
        """
        args = parse_argstring(self.set_session_directory, arg)
        shutil.move(self.session._directory, args.directory)
        self.session._directory = os.path.abspath(args.directory)

