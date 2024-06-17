from requests_html import HTMLSession
from datetime import datetime


def getYoutubeUrl():
    session = HTMLSession()
    # 其中get请求中的参数和requests库中的get是一样的可以随意添加

    # 这里是获取yudou66的首页最新的一个分享文章的链接
    yudouSession = session.get('https://www.yudou66.com/')

    yudouAElement = yudouSession.html.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a')
    yudouUrl = yudouAElement[0].attrs['href']
    print('\n'+datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新文章链接：" + yudouUrl)

    # 获取youtube的的链接
    youtubeSession = session.get(yudouUrl)
    youtubeElement = youtubeSession.html.xpath('//*[@id="post-body"]/p[8]/a')
    youtubeUrl = youtubeElement[0].attrs['href']
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新解密youtube视频链接：" + youtubeUrl)



    youtubeSession.html.render(script="document.title = '新的页面标题';", retries=1, timeout=3, sleep=2)
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 页面标题：" + youtubeSession.html.find('title', first=True).text)


    # 返回youtube的链接和session对象
    return {'url' : youtubeUrl,'session' : session,'response' : youtubeSession}

if __name__ == '__main__':
    video_result =getYoutubeUrl()
    print(video_result)





