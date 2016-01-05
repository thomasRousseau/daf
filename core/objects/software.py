class Software():
    def __init__(self, folder):
        self.name = ""
        self.last_use = ""


class Browser(Software):
    def __init__(self, folder):
        Software.__init__(self, folder)
        self.history = ""
        self.cache = ""
        self.downloads = []


class Office(Software):
    def __init__(self, folder):
        Software.__init__(self, folder)
        self.recent_documents = []

