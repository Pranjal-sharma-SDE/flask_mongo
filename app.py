from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'test'

# dynamic route

# @app.route('/test2', defaults={'username': None})
# @app.route('/test2/', defaults={'username': None})     got error for guest if doing without this . tell the reason.
@app.route('/test2/<username>')
def test2(username:str = None)->str:    # type hinting
    if username is None:
        return 'Hello, Guest!'
    return 'Hello, ' + username

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


