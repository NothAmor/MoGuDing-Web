from flask import Flask

class flaskConfig:
    # DEBUG模式
    DEBUG = True

    # html模版路径
    template_folder = './templates'

    # 静态资源目录
    static_folder = './static'

    # 静态资源链接
    static_url_path = '/static'

    # 创建flask app
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path=static_url_path)

    # app secret key
    app.config['SECRET_KEY'] = 'whatthefucksafety'

    # 网站名称
    websiteName = "蘑菇丁自动云"

    userAgents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K30 Pro Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/14.7.10",
        "Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro; GMSCore 21.02.14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 HuaweiBrowser/11.1.1.301 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K30 Pro Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.6 Mobile Safari/537.36 COVC/045635",
        "Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/12.17 SP-engine/2.32.0 baiduboxapp/12.18.0.10 (Baidu; P1 11) NABar/1.0",
        "Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.09.4.5079"
    ]