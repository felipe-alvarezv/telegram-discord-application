class Channel:
    def __init__(self, id, title, webhooks):
        self.id = id
        self.title = title
        self.webhooks = webhooks

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_channel_webhooks(self):
        webhook_list = []
        webhook_list.append(self.webhooks)
        return webhook_list

    def set_channel_webhooks(self, webhooks):
        self.webhooks = webhooks
