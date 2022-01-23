from app.cron.cron import cronCheckMethod
from config import flaskConfig
from app.db.db import db
 
if __name__ == '__main__':
    db.create_all()
    flaskConfig.scheduler.add_job(func=cronCheckMethod.setJobs, day_of_week='mon-sun', trigger='cron', id='refresh')
    cronCheckMethod.setJobs()
    flaskConfig.scheduler.start()

    # 启动网站
    flaskConfig.app.run(debug = flaskConfig.DEBUG, use_reloader=False)
