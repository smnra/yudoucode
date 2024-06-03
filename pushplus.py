import requests
import datetime
import json


def pushplus_notify(title, content):
    today = datetime.date.today()
    date_text = today.strftime("%Y-%m-%d")
    token = 'ac1394d74de4420db6fb79ddcc0da2ed'  # 在pushpush网站中可以找到
    title = title + date_text
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)

if __name__ == '__main__':
    title = '测试标题'
    content = '测试内容'
    pushplus_notify(title, content)