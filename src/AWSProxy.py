import boto3
import os
import requests
from time import sleep

IMAGE_ID = 'ami-02ae436ce7c43df2b'
PORT = 8888


class AWSProxy:
    def __init__(self, logger):
        import db
        self.db = db
        self.logger = logger
        self.ec2 = boto3.resource('ec2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.client = boto3.client('ec2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                   aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    def get(self, user):
        self.logger.info(self.db.get_user(user))
        if self.db.get_user(user):
            while not self.check_proxy(self.db.get_proxy(user)):
                sleep(1)
            return '%s:%s' % (self.db.get_proxy(user), PORT)

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
        self.db.add_user(name=user, proxy=instance.public_ip_address, instance=instance.id)

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
            self.logger.warning(self.stop_proxy(proxy))

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
        instance = self.ec2.Instance(self.db.get_user(user).instance)
        self.db.delete(user)

        return instance

    def stop_proxy(self, proxy):
        return proxy.terminate()
