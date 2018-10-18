from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_root():
    try:
        args = request.args

        return str(args), 200
    except Exception as exc:
        # 500 Internal Server Error
        return str(exc), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
