# MoGuDing-Web

蘑菇丁自动打卡平台，基于flask进行制作

## 已完成的功能点

1. 控制台登陆注册
2. 添加蘑菇丁账户
3. 获取蘑菇丁账户token
4. 打卡地址功能
5. 使用APScheduler进行指定时间的打卡
6. 在每次对任务变更后，程序重新设置一次cron任务

## 未完成功能点

1. 每次执行任务后进行日志记录
2. 添加对表单的修改功能
3. 添加定时任务的立即执行

## 部署该项目

```shell
git clone http://kod.nothamor.cn:3000/NothAmor/MoGuDing-Web.git
cd MoGuDing-Web
pip3 install -r requirements.txt
python3 run.py
```