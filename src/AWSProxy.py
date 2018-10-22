
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
            return "1.2.3.4:8888"

    def stop_proxies(self):
        pass

    def start_proxy(self):
        return None
