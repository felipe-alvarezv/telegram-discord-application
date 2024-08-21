class Channel:
    def __init__(self, desc, id, webhook):
        self.desc = desc
        self.id = id
        self.webhook = webhook

    def get_desc(self):
        return self.desc

    def set_desc(self, desc):
        self.desc = desc

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_webhook(self):
        return self.webhook

    def set_webhook(self, webhook):
        self.webhook = webhook

    def __str__(self):
        output = str(self.get_id()) + ' {' + self.get_desc() + '}'
        return output