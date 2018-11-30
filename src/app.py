from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from AWSProxy import AWSProxy
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

aws_proxy = AWSProxy(logger=app.logger)


@app.route('/<user>', methods=['GET'])
def get_root(user):
    try:
        app.logger.warning('create Proxy for: %s' % user)
        proxy = aws_proxy.get(user)
        app.logger.info('return %s, 200' % proxy)
        return proxy, 200
    except Exception as exc:
        # 500 Internal Server Error
        app.logger.error('GET /%s Error: %s' % (user, exc))
        return str(exc), 500


@app.route('/stop/', methods=['GET'])
def get_stop():
    try:
        user = request.args.get("user")
        app.logger.warning('stop Proxy for: %s' % user)
        response = aws_proxy.stop(user)
        app.logger.warning('return %s, 200' % response)
        return response, 200
    except Exception as exc:
        # 500 Internal Server Error
        app.logger.error('GET /stop/%s Error: %s' % (user, exc))
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60000)
