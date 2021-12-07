from app.views.views import viewFunctions
from config import flaskConfig
from app.db.db import db

if __name__ == '__main__':
    flaskConfig.app.run(debug = flaskConfig.DEBUG)