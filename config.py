from flask import Flask

class flaskConfig:
    DEBUG = True
    template_folder = './templates'
    static_folder = './static'
    static_url_path = '/static'
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path=static_url_path)
    app.config['SECRET_KEY'] = 'whatthefucksafety'