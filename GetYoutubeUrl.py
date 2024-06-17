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

    # 返回youtube的链接和session对象
    return {'url' : youtubeUrl,'session' : session,'response' : youtubeSession}

if __name__ == '__main__':
    video_result =getYoutubeUrl()
    print(video_result)

    video_url = video_result['url']
    uncodeSession = video_result['response']
    session = video_result['session']

    #   首次执行 页面的js代码 以自动安装 chrome 浏览器 #################################################################
    async def firstExecuteJs(uncodeSession):
        # 首次执行 页面的js代码
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 首次执行 js代码：', "multiDecrypt('哈哈哈哈哈哈')")
        uncodeSession.html.render(timeout=3000)
        await uncodeSession.html.render(script="multiDecrypt('哈哈哈哈哈哈')", retries=3, timeout=60, sleep=10,
                                        keep_page='true')
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 首次执行 js代码完成：', "multiDecrypt('哈哈哈哈哈哈')")
        # 交互语句
        await uncodeSession.html.page.keyboard.press('Enter')
        return uncodeSession.html.xpath('//*[@id="result"]/p[2]/text()[2]')[0]

    try:
        session.loop.run_until_complete(firstExecuteJs(uncodeSession))
    finally:
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '首次执行 js代码 页面交互完成')
    #   首次执行 页面的js代码 以自动安装 chrome 浏览器 #################################################################






