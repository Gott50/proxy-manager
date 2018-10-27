import logging
from AWSProxy import AWSProxy
import create_db

create_db

aws_proxy = AWSProxy(logger=logging)
aws_proxy.stop_proxies()
