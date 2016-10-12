import os

partner = "2088711552060890"
key = "dvuz6l7y5cqmntfwqdu6pdqx0glbiyn8"
seller_mail = "89144681@qq.com"

if 'SERVER_SOFTWARE' in os.environ:
    notify_url = "http://peggysbeauty.com/peggy/paid_notify_wap"
    return_url = "http://peggysbeauty.com/peggy/paid_wap"
    show_url = "http://peggysbeauty.com"
else:
    notify_url = "http://127.0.0.1:8000/peggy/paid_notify_wap"
    return_url = "http://127.0.0.1:8000/peggy/paid_wap"
    show_url = "http://127.0.0.1:8000/peggy"