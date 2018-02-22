import json

from flask import abort, Flask, request

from auth import __check_creds


app = Flask(__name__)


# note this can all be done with the python keystonemiddleware automatically
# but this is here to show how to validate a token and allow access to service functionality

@app.route('/')
def index():
    # get auth headers
    token = request.headers.get('X-Auth-Token')
    if __check_creds(token):
        print('Passed auth.')
        return 'Hi from dumdum'
    else:
        abort(401)


@app.route('/health')
def health():
    # get auth headers
    token = request.headers.get('X-Auth-Token')
    if __check_creds(token):
        print('Passed auth.')
        ret_status = {
            "status": "up",
            "context": {'message': '42'}
        }
        return json.dumps(ret_status)
    else:
        abort(401)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=56567)
