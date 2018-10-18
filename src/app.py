from flask import Flask
from flask import request
import AWSProxy

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_root():
    try:
        user = request.args.get("user")
        proxy = AWSProxy.get(user)
        return proxy, 200
    except Exception as exc:
        # 500 Internal Server Error
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
