import boto3
import os
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
        proxy_list = self.get_proxy_list(user)
        self.logger.debug("get_proxy_list(%s) return: %s" % (user, proxy_list))
        if len(proxy_list) > 0:
            proxy = proxy_list[0].public_ip_address
            while not self.check_proxy(proxy):
                sleep(1)
            return '%s:%s' % (proxy, PORT)

        proxy = self.create_new_proxy(user)
        return '%s:%s' % (proxy.public_ip_address, PORT)

    def restart(self, user):
        proxy_list = self.get_proxy_list(user)
        self.logger.debug("get_user(%s) return: %s" % (user, proxy_list))
        if len(proxy_list) <= 0:
            return self.get(user=user)

        for proxy in proxy_list:
            return self.restart_proxy(proxy)

    def create_new_proxy(self, user):
        instance = self.ec2.create_instances(
            ImageId=IMAGE_ID, InstanceType='t2.micro',
            KeyName='proxy', SecurityGroups=['proxy'],
            MaxCount=1, MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': user
                        },
                    ]
                },
            ],
        )[0]

        while not instance.public_ip_address:
            sleep(1)
            instance = self.ec2.Instance(instance.id)

        while not self.check_proxy(instance.public_ip_address):
            sleep(1)

        return instance

    def check_proxy(self, proxy):
        return True

    def stop_proxies(self):
        for proxy in self.get_proxies():
            self.logger.warning(self.stop_proxy(proxy))

    def get_proxy_list(self, user):
        d = {'Key': 'Name', 'Value': user}
        return list(
            filter(lambda i: (i.state['Name'] == 'pending' or i.state['Name'] == 'running') and d in i.tags,
                   self.get_proxies()))

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
        proxy_list = self.get_proxy_list(user)
        self.logger.debug("get_user(%s) return: %s" % (user, proxy_list))
        for instance in proxy_list:
            self.stop_proxy(instance)

    def stop_proxy(self, proxy):
        return proxy.terminate()

    def restart_proxy(self, proxy):
        return proxy.reboot()
