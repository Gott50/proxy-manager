from flask import Flask
from flask import request
from AWSProxy import AWSProxy
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

aws_proxy = AWSProxy(logger=app.logger)


@app.route('/', methods=['GET'])
def get_root():
    try:
        user = request.args.get("user")
        app.logger.info('create Proxy for: %s' % user)
        proxy = aws_proxy.get(user)
        return proxy, 200
    except Exception as exc:
        # 500 Internal Server Error
        return str(exc), 500


@app.route('/stop', methods=['GET'])
def get_stop():
    try:
        user = request.args.get("user")
        response = aws_proxy.stop(user)
        return response, 200
    except Exception as exc:
        # 500 Internal Server Error
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
