from flask import Flask, request
app = Flask(__name__)

ids = []

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/", methods=['GET', 'POST'])
def id_handler():
    if request.method == 'POST':
        id = request.args.get('id', '')
        ids.append(id)
        return ""
    else:
        return ids.pop()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(debug=False)
