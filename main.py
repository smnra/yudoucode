from datetime import datetime
import pushplus
import os,re

from requests_html import HTMLSession
from aesDecrypt import decrypt,decodeUrl


# 视频下载路径
video_path = "./video/"
video_filename = "code.mp4"
video_fullpath = video_path + video_filename

# 清理临时文件
def removeTempFile():
    video_fullpath = "./video/code.mp4"
    temp_audio_path = "./video/temp_audio.wav"
    if os.path.exists(video_fullpath):
        os.remove(video_fullpath)
        print(f"文件 {video_fullpath} 已被删除。")
    else:
        print(f"文件 {video_fullpath} 不存在。跳过删除")
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
        print(f"文件 {temp_audio_path} 已被删除。")
    else:
        print(f"文件 {temp_audio_path} 不存在。跳过删除")










# 使用密码在页面上获取v2ray的免费连接地址 并下载
def getV2ray(url='https://www.mibei77.com'):
    session = HTMLSession()
    # 其中get请求中的参数和requests库中的get是一样的可以随意添加

    # 这里是获取yudou66的首页最新的一个分享文章的链接
    yudouSession = session.get(url)

    yudouAElement = yudouSession.html.xpath('//*[@id="Blog1"]//h2[@class="entry-title"]/a')
    yudouTodayUrl = yudouAElement[0].attrs['href']
    print('\n' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新文章链接：" + yudouTodayUrl)

    # 获取youtube的的链接
    youtubeSession = session.get(yudouTodayUrl)
    v2rayTag = youtubeSession.html.xpath('//*[@id="post-body"]/p[9]')
    v2rayUrl = v2rayTag[0].full_text
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新v2rayUrl链接：" + v2rayUrl)

    v2raySession = session.get(v2rayUrl)
    if v2raySession.status_code == 200:
        v2rayText = v2raySession.text
        print(f"v2rayText: {v2rayText}")
        # 返回youtube的链接和session对象
        return {'v2rayUrl': v2rayUrl, 'v2rayText': v2rayText}

        if not os.path.exists("./docs/v2ray/"):
            os.makedirs(os.path.abspath("./docs/v2ray"))

        #  写入github page 主页文件
        with open("./docs/index.html", "w", encoding="utf-8") as f:
            f.write('{},{},{} '.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), " 最新的V2Ray订阅链接地址：\n", v2rayUrl))

        #  写入github page文件
        with open("./docs/v2ray/index.html", "w", encoding="utf-8") as f:
            f.write(v2rayText)

    return {'v2rayUrl' : v2rayUrl,'v2rayText': v2rayText}









if __name__ == '__main__':
    # 获取要下载的 YouTube 视频链接
    v2rayDict = getV2ray()
    v2rayText = v2rayDict['v2rayText']
    v2rayUrl = v2rayDict['v2rayUrl']
    # pushplus` 推送到微信
    pushplus.pushplus_notify('最新的V2Ray订阅链接', v2rayUrl + '\n' + v2rayText)
    # 清理临时文件
    removeTempFile()


