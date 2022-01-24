from ..db.db import mogudingAddress, mogudingAccount, mogudingLogs, mogudingTaskSend, mogudingTasks, db
from ..views.views import API
from config import flaskConfig

import datetime
import requests
import json
import time

class cronCheckMethod:
    def CHECK(taskId):
        begin_time = time.time()
        url = "https://api.moguding.net:9000/attendence/clock/v2/save"
        salt = "3478cbbc33f84bd00d75d7dfa69e0daa"
        taskInformation = mogudingTasks.query.filter_by(id=taskId).first()
        accountInformation = mogudingAccount.query.filter_by(phoneNumber=taskInformation.runAccount).first()
        addressInformation = mogudingAddress.query.filter_by(phoneNumber=taskInformation.runAccount).first()

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

        headers = {
            'Accept-Language':"zh-CN,zh;q=0.8",
            'roleKey': 'student',
            'Host':'api.moguding.net:9000',
            "Content-Type": "application/json; charset=UTF-8",
            "Cache-Control": "no-cache",
            'User-Agent': userAgent
        }

        url = "https://api.moguding.net:9000/session/user/v1/login"

        print("开始登录...")
        data = {
            "password": password,
            "loginType": "android",
            "uuid": "",
            "phone": phoneNumber
        }

        print("开始获取代理")
        proxies = {}
        import time
        while True:
            proxyRequest = requests.get(flaskConfig.proxyApiUrl)
            proxyContent = json.loads(proxyRequest.content)
            ip = proxyContent["obj"][0]["ip"] + ":" + proxyContent["obj"][0]["port"]
            print(proxyContent, ip)

            proxies = {"https": "https://" + proxyContent["obj"][0]["ip"] + ":" + proxyContent["obj"][0]["port"]}
            print(proxies)

            req = requests.post(url=url, headers=flaskConfig.request_header, data=json.dumps(data), verify=False, proxies=proxies)
            text = req.json()
            if text["code"] == 200:
                break
            else:
                print("代理IP: {}，无效，继续尝试!".format(proxyContent["obj"][0]["ip"] + ":" + proxyContent["obj"][0]["port"]))
                time.sleep(1)
                continue

        print(text)
        token = json.loads(req.text)['data']['token']
        userId = json.loads(req.text)['data']['userId']
        headers["authorization"] = token


        body = {
            "country": "中国",
            "address": address,
            "province": province,
            "city": city,
            "latitude": latitude,
            "description": taskInformation.description,
            "type": taskType,
            "device": "Android",
            "longitude": longitude
        }
        body["planId"] = planId
        headers["sign"] = API.GenerateSign("Android" + taskType + planId + userId + address + salt)

        saveUrl = "https://api.moguding.net:9000/attendence/clock/v2/save"
        response = requests.post(saveUrl, data=json.dumps(body), headers=headers, verify=False, timeout=20, proxies=proxies)
        response = json.loads(response.text)
        print(response)
        end_time = time.time()
        run_time = end_time - begin_time

        messageSend = mogudingTaskSend.query.filter_by(owner=owner, account=taskInformation.runAccount).all()
        messageSendFirst = mogudingTaskSend.query.filter_by(owner=owner, account=taskInformation.runAccount).first()

        if response["code"] == 200:
            taskResult = True
            print("{}账户的{}点打卡任务已完成!".format(owner, taskInformation.runTime.split(':')[0]))
            addTaskRecord = mogudingLogs(owner=taskInformation.owner, taskType=taskInformation.taskType, account=taskInformation.runAccount, 
                                         goal=taskInformation.runGoalName, runTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                         taskTime=run_time, taskResult=taskResult)
            db.session.add_all([addTaskRecord])
            db.session.commit()
            if len(messageSend) != 0:
                API.weChatSendMsg(messageSendFirst.sendKey, "蘑菇丁打卡成功", "打卡状态: " + response["msg"] + "\n\n打卡时间: " + response["data"]["createTime"])
        else:
            taskResult = False
            addTaskRecord = mogudingLogs(owner=taskInformation.owner, taskType=taskInformation.taskType, account=taskInformation.runAccount, 
                                         goal=taskInformation.runGoalName, runTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                         taskTime=run_time, taskResult=taskResult, failReason=response["msg"])
            db.session.add_all([addTaskRecord])
            db.session.commit()
            if len(messageSend) != 0:
                API.weChatSendMsg(messageSendFirst.sendKey, "蘑菇丁打卡失败", "打卡失败" + "\n\n失败原因: " + response["msg"])
            print(response)
            print("蘑菇丁打卡失败","打卡失败"+"\n\n失败原因: "+response["msg"])
    
    
    """
        每天零点重新下发打卡任务，随机设定打卡时间为设定时间5分钟左右
    """
    def setJobs():
        import random
        for job in flaskConfig.scheduler.get_jobs():
            if job.id == "refresh":
                continue
            flaskConfig.scheduler.remove_job(job.id)
        tasks = mogudingTasks.query.filter_by(status=True).all()
        for task in tasks:
            # 运行时间，为时：分，[0]是时，[1]是分
            runTime = task.runTime.split(':')

            # 给分钟随机加5以内随机数
            minute = random.randint(0, 5)
            h = int(runTime[0])
            m = int(runTime[1])
            if m >= 55 and minute + m > 59:
                h += 1
                m = minute + m - 60
            elif m >= 55 and minute + m < 60:
                m = m + minute
            else:
                m += minute
            if m == 60:
                m -= 1
            runTime[0] = h
            runTime[1] = m

            second = random.randint(5, 59)
            if task.runRule == "everyDay":
                flaskConfig.scheduler.add_job(func=cronCheckMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                day_of_week='mon-sun', second=second)

            elif task.runRule == "everyWeek":
                flaskConfig.scheduler.add_job(func=cronCheckMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                    day_of_week='fri', second=second)

            elif task.runRule == "everyMonth":
                flaskConfig.scheduler.add_job(func=cronCheckMethod.CHECK, args=(str(task.id),), trigger='cron', hour=runTime[0], minute=runTime[1], 
                                    month='*', second=second)
        for job in flaskConfig.scheduler.get_jobs():
            print(job)