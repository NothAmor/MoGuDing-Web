from app.cron.cron import cronMethod
from config import flaskConfig
 
if __name__ == '__main__':
    flaskConfig.scheduler.add_job(func=cronMethod.refreshJobs, trigger='cron', second='*/5', id='refresh')
    flaskConfig.scheduler.start()

    # 启动网站
    flaskConfig.app.run(debug = flaskConfig.DEBUG)