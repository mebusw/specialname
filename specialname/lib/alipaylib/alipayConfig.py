import os

partner = "2088711552060890"
key = "dvuz6l7y5cqmntfwqdu6pdqx0glbiyn8"
seller_mail = "89144681@qq.com"

if 'SERVER_SOFTWARE' in os.environ:
    notify_url = "http://www.namechinesename.com/paid_notify_wap"
    return_url = "http://www.namechinesename.com/paid_wap"
    show_url = "http://www.namechinesename.com/"
else:
    notify_url = "http://127.0.0.1:8000/paid_notify_wap"
    return_url = "http://127.0.0.1:8000/paid_wap"
    show_url = "http://127.0.0.1:8000/"