class MailClient():
    def __init__(self, folder):
        self.name = ""
        self.version = ""
        self.last_used = ""
        self.mails_list = []


class Mail():
    def __init__(self, folder):
        self.date = ""
        self.transmitter = ""
        self.receivers = []
        self.attached_files = []
        self.content = ""

