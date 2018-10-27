import logging
from AWSProxy import AWSProxy

from sqlalchemy.exc import OperationalError

import models
from time import sleep


def s(time=0):
    print("sleep: " + str(time))
    sleep(time)


def init_db():
    try:
        for m in models.list():
            print(str(m))
            print(str(m.query.filter_by(id=1).first()))
    except OperationalError as oe:
        print(oe)
        s(10)
        init_db()
    except Exception as e:
        print("DB ERROR: ", e)
        print("initDB now!")
        import create_db

        create_db
        print("initDB DONE")


init_db()

aws_proxy = AWSProxy(logger=logging)
aws_proxy.stop_proxies()
