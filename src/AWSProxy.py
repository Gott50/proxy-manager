import os
from time import sleep

import boto3
import requests

IMAGE_ID = 'ami-02ae436ce7c43df2b'
PORT = 8888


class AWSProxy:
    def __init__(self):
        self.user_proxy_dic = {}
        self.ec2 = boto3.resource('ec2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.client = boto3.client('ec2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                   aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.stop_proxies()

    def get(self, user):
        if user in self.user_proxy_dic:
            while not self.check_proxy(self.user_proxy_dic[user].public_ip_address):
                sleep(1)
            return '%s:%s' % (self.user_proxy_dic[user].public_ip_address, PORT)

        proxy = self.create_new_proxy(user)
        return '%s:%s' % (proxy.public_ip_address, PORT)

    def create_new_proxy(self, user):
        instance = self.ec2.create_instances(
            ImageId=IMAGE_ID, InstanceType='t2.micro',
            KeyName='proxy', SecurityGroups=['proxy'],
            MaxCount=1, MinCount=1
        )[0]

        while not instance.public_ip_address:
            sleep(1)
            instance = self.ec2.Instance(instance.id)
        self.user_proxy_dic[user] = instance

        while not self.check_proxy(instance.public_ip_address):
            sleep(1)

        return instance

    def check_proxy(self, proxy):
        try:
            requests.get('http://example.com', proxies={'http': '%s:%s' % (proxy, PORT)})
        except IOError:
            return False
        else:
            return True

    def stop_proxies(self):
        for proxy in self.get_proxies():
            print(self.stop_proxy(proxy))

    def get_proxies(self):
        response = self.client.describe_instances(Filters=[
            {
                'Name': 'image-id',
                'Values': [
                    IMAGE_ID,
                ]
            },
        ], )
        ids = list(map(lambda i: i['Instances'][0]['InstanceId'], response['Reservations']))
        return list(map(lambda i: self.ec2.Instance(i), ids))

    def stop(self, user):
        return self.stop_proxy(self.user_proxy_dic.pop(user))

    def stop_proxy(self, proxy):
        return proxy.terminate()
