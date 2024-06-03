from requests_html import HTMLSession


session = HTMLSession()
# 其中get请求中的参数和requests库中的get是一样的可以随意添加


# 这里是获取yudou66的首页最新的一个分享文章的链接
yudouSession = session.get('https://www.yudou66.com/')
yudouAElement = yudouSession.html.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a')
yudouUrl = yudouAElement[0].attrs['href']


# 获取youtube的的链接
youtubeSession = session.get(yudouUrl)
youtubeElement = youtubeSession.html.xpath('//*[@id="post-body"]/p[8]/a')
youtubeUrl = youtubeElement[0].attrs['href']


