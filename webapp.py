from flask import Flask

webapp = Flask(__name__)

@webapp.route('/')
def index():
    return 'Hello world'


if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')