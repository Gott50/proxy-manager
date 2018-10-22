class AWSProxy:
    def __init__(self):
        self.user_proxy_dic = {}
        self.stop_proxies()

    def get(self, user):
        if user in self.user_proxy_dic:
            return self.user_proxy_dic[user]

        proxy = self.create_proxy()
        self.user_proxy_dic[user] = proxy
        return proxy

    def create_proxy(self):
        existing_proxy = self.start_proxy()
        if existing_proxy:
            return existing_proxy
        else:
            return self.create_new_proxy()

    def create_new_proxy(self):  # TODO implement
        return "1.2.3.4:8888"

    def stop_proxies(self):  # TODO implement
        pass

    def start_proxy(self):  # TODO implement
        return None
