from ..db.db import mogudingAddress, mogudingAccount, mogudingTasks
from ..views.views import API
from config import flaskConfig

import requests
import json

class cronMethod:
    def CHECK(taskId):
        url = "https://api.moguding.net:9000/attendence/clock/v2/save"
        salt = "3478cbbc33f84bd00d75d7dfa69e0daa"
        taskInformation = mogudingTasks.query.filter_by(id=taskId).first()
        accountInformation = mogudingAccount.query.filter_by(phoneNumber=taskInformation.runAccount).first()
        addressInformation = mogudingAddress.query.filter_by(account=accountInformation.remark).first()

        owner = accountInformation.owner
        address = addressInformation.detailedAddress
        province = addressInformation.province + "省"
        city = addressInformation.city + "市"
        latitude = addressInformation.latitude
        longitude = addressInformation.longitude
        taskType = taskInformation.taskType

        planId = taskInformation.runGoalId
        userId = accountInformation.userId

        userAgent = accountInformation.userAgent
        phoneNumber = accountInformation.phoneNumber
        password = accountInformation.password

        sign = API.GenerateSign("Android" + taskType + planId + userId + address + salt)
        userId, token = API.returnToken(phoneNumber=phoneNumber, password=password, userAgent=userAgent)
        flaskConfig.request_header["authorization"] = token
        body = {
            "country": "中国",
            "address": address,
            "province": province,
            "city": city,
            "latitude": latitude,
            "description": "",
            "type": taskType,
            "device": "Android",
            "longitude": longitude,
            "planId": planId
        }
        flaskConfig.request_header.update(
            {"user-agent": userAgent, "roleKey": "student", }
        )
        flaskConfig.request_header["sign"] = sign

        response = requests.post(url, data=json.dumps(body), headers=flaskConfig.request_header, verify=False)
        response = json.loads(response.text)
        if response["code"] == 200:
            print("{}账户的{}点打卡任务已完成!".format(owner, taskInformation.runTime.split(':')[0]))
        else:
            print(response)
            print("蘑菇丁打卡失败","打卡失败"+"\n\n失败原因："+response["msg"])
    
    def refreshJobs():
        for job in flaskConfig.scheduler.get_jobs():
            if job.id == "refresh":
                continue
            flaskConfig.scheduler.remove_job(job.id)
        tasks = mogudingTasks.query.filter_by(status=True).all()
        for task in tasks:
            # 运行时间，为时：分，[0]是时，[1]是分
            runTime = task.runTime.split(':')
            if task.runRule == "everyDay":
                flaskConfig.scheduler.add_job(func=cronMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                day_of_week='mon-sun', second=00)

            elif task.runRule == "everyWeek":
                flaskConfig.scheduler.add_job(func=cronMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                    day_of_week='fri', second=00)

            elif task.runRule == "everyMonth":
                flaskConfig.scheduler.add_job(func=cronMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                    month='*', second=00)
        print(len(flaskConfig.scheduler.get_jobs()))
        for job in flaskConfig.scheduler.get_jobs():
            print(job)