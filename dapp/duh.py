from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hi from dumdum'


@app.route('/health')
def health():
    ret_status = {
        "status": "up",
        "context": {'message': '42'}
    }
    return json.dumps(ret_status)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
