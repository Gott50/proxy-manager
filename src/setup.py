import logging
import sqlite3

from AWSProxy import AWSProxy

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS user''')
# Create table
c.execute('''CREATE TABLE User
             (name text, proxy text, instance text)''')
# Save (commit) the changes
conn.commit()
conn.close()

aws_proxy = AWSProxy(logger=logging)
aws_proxy.stop_proxies()
