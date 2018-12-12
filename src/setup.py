import logging
from AWSProxy import AWSProxy

aws_proxy = AWSProxy(logger=logging)
aws_proxy.stop_proxies()
