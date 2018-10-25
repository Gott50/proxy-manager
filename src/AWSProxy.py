import requests

import boto3
from time import sleep


class AWSProxy:
    def __init__(self):
        self.user_proxy_dic = {}
        self.stop_proxies()
        self.ec2 = boto3.resource('ec2')

    def get(self, user):
        if user in self.user_proxy_dic:
            return self.user_proxy_dic[user]

        proxy = self.create_new_proxy()
        self.user_proxy_dic[user] = proxy
        return '%s:%s' % (proxy.public_ip_address, 8888)

    def create_new_proxy(self):
        instance = self.ec2.create_instances(
            ImageId='ami-02ae436ce7c43df2b', InstanceType='t2.micro',
            KeyName='proxy', SecurityGroups=['proxy'],
            MaxCount=1, MinCount=1
        )[0]

        while not instance.public_ip_address:
            sleep(1)
            instance = self.ec2.Instance(instance.id)

        while not self.check_proxy(instance.public_ip_address):
            sleep(1)

        return instance

    def check_proxy(self, proxy):
        try:
            requests.get('http://example.com', proxies={'http': proxy})
        except IOError:
            return False
        else:
            return True

    def stop_proxies(self):
        for proxy in self.get_proxies():
            self.stop(proxy)

    def get_proxies(self):  # TODO implement
        return []

    def stop(self, user):
        self.stop_proxy(self.user_proxy_dic.pop(user))

    def stop_proxy(self, proxy):  # TODO implement
        pass
