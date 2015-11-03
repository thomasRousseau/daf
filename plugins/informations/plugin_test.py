from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)
from IPython.core.magic import (Magics, magics_class, line_magic)


@magics_class
class Test(Magics):
    def __init__(self, shell, session):
        super(Test, self).__init__(shell)
        self.session_directory = session._directory


    @magic_arguments()
    @argument('-o', '--option', help='An optional argument.')
    @argument('i', type=int, help='An integer positional argument.')
    @line_magic
    def test(self, arg):
        """ A really cool magic command.
    
        """
        args = parse_argstring(self.test, arg)
        if args.i==1:
            print("toto")
        else:
            print("tata")
        print(self.session_directory)



