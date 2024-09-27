from requests_html import HTMLSession
from datetime import datetime


def getYoutubeUrl():
    session = HTMLSession()
    # 其中get请求中的参数和requests库中的get是一样的可以随意添加

    # 这里是获取yudou66的首页最新的一个分享文章的链接
    yudouSession = session.get('https://www.yudou66.com/')

    yudouAElement = yudouSession.html.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a')
    yudouTodayUrl = yudouAElement[0].attrs['href']
    print('\n'+datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新文章链接：" + yudouTodayUrl)

    # 获取youtube的的链接
    youtubeSession = session.get(yudouTodayUrl)
    youtubeElement = youtubeSession.html.xpath("//*[contains(@href, 'https://youtu.be')]")
    youtubeUrl = youtubeElement[0].attrs['href']
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新解密youtube视频链接：" + youtubeUrl)

    # try:
    #     youtubeSession.html.render(script="console.log('hhhhhhhhh');", retries=1, timeout=30,sleep=2)
    # except Exception as e:  # 这里是为了测试render方法是否正常工作
    #     print(e)

    # 返回youtube的链接和session对象
    return {'youtubeUrl' : youtubeUrl,'yudouTodayUrl': yudouTodayUrl}

if __name__ == '__main__':
    video_result =getYoutubeUrl()
    print(video_result)





