import core.objects.browser as b


class BrowsersHandler():
    def __init__(self, session):
        self.session = session

    def display_installed_browsers(self, arg):
        """\tDisplay the installed browsers. (Only support Chrome, Chromium, Firefox and IE for now)"""
        output = "List of installed browsers:\n\n"
        for browser in b.find_installed_browser(self.session.configuration):
            output += "Name: " + browser['Browser Name'] + "\n"
            output += "Version: " + browser['Browser Version'] + "\n"
            if "Chrom" in browser['Browser Name']: 
                output += "User: " + browser['User'] + "\n"
            output += "\n"
        output = output[:-1]
        return output

