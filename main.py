from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime
import pushplus
import os
import GetYoutubeUrl
import speechToText.baiduSpeech  as baiduSpeech




# 获取要下载的 YouTube 视频链接
# video_url = "https://youtu.be/2EJ9pBRUo6k"

video_result = GetYoutubeUrl.getYoutubeUrl()

video_url=video_result['url']
uncodeSession = video_result['response']

video_path = "./video/"
video_filename = "code.mp4"
video_fullpath = video_path + video_filename



# 转换音频格式
def mp4ToWav(sourpath, targetpath='temp_audio.wav'):
    # 从视频中提取音频
    audio = AudioSegment.from_file(sourpath, format="mp4")
    # 将音频保存为临时文件
    audio.export(targetpath, format="wav")
    return targetpath


# 语音识别为文字
def wavToText(sourpath='temp_audio.wav'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(sourpath) as source:
        audio_data = recognizer.record(source)
        subtitleGoogle = recognizer.recognize_google(audio_data, language="zh-CN")
    return subtitleGoogle



def validateMima(mimaStr):
    # 验证密码是否为4位数字
    try:
        mima = mimaStr[(mimaStr.index("密码") + 2):(mimaStr.index("密码") + 6)]
        mimaInt = int(mima)
        if mimaInt >=1000 and mimaInt <= 9999:
            return mimaInt
        else:
            return -1
    except Exception as e:
        print(e)
        return -1



# 获取密码
def getMima(yt):
    videPath = "./video/"
    videoFilename = "code.mp4"
    videoFullpath = videPath + videoFilename

    # 获取视频可下载的视频列表
    videoList = yt.streams.order_by("type").fmt_streams
    # minSizeVideo = yt.streams.filter(type="audio").first()   #获取最低音频流

    for i,videoStream in enumerate(videoList):

        try:
            # 下载视频
            videoStream.download(output_path=videPath, filename=videoFilename)
            print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 第" + str(i+1) + "次下载视频链接：", videoList[i])
            # mp4 转换音频wav格式
            tempAudioPath = mp4ToWav(videoFullpath, targetpath=videPath + "temp_audio.wav")

            # 语音识别为文字
            subtitleGoogle = wavToText(sourpath=tempAudioPath)
            print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 提取的文字为 : '+ subtitleGoogle)

            # 验证密码
            mima = validateMima(subtitleGoogle)
            if mima != -1:
                print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 密码：", str(mima))
                return mima
            else:
                subtitleBaidu = baiduSpeech.wavToText(tempAudioPath)
                # 验证密码
                mima = validateMima(subtitleBaidu)
                if mima != -1:
                    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 密码：", str(mima))
                    return mima
                else:
                    continue
                print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 解析密码异常:" + str(mima) + "，将删除文件并继续循环")
                removeTempFile()
                continue
        except Exception as e:
            subtitleBaidu = baiduSpeech.wavToText(tempAudioPath)
            # 验证密码
            mima = validateMima(subtitleBaidu)
            if mima != -1:
                print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 密码：", str(mima))
                return mima
            else:
                continue
            print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 过程异常：", e)
            removeTempFile()
            continue

# 使用密码在页面上获取v2ray的免费连接地址 并下载
def getV2ray(uncodeSession,mima):
    # 执行页面的js代码
    uncodeJs = "multiDecrypt('" + str(mima) + "');"

    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 执行js代码：', uncodeJs)
    # uncodeSession.html.render(timeout=30000)
    uncodeSession.html.render(script="multiDecrypt('" + str(mima) + "')",retries = 3,timeout = 60,sleep = 10)

    async def run():
        # 交互语句
        await uncodeSession.html.page.keyboard.press('Enter')
    try:
        video_result['session'].loop.run_until_complete(run())
    finally:
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 页面交互完成:' + uncodeSession.html.xpath('//*[@id="result"]/p[2]/text()[2]')[0])



    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 执行js代码wancheng：', uncodeJs)
    # 获取 'v2ray/小火箭/winxray等订阅链接，不需要开代理，即可更新订阅链接'
    # '//*[@id="result"]/p[2]/text()[2]'
    v2rayElement = uncodeSession.html.xpath('//*[@id="result"]/p[2]/text()[2]')
    v2rayUrl = v2rayElement[0]
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新的V2Ray订阅链接地址：", v2rayUrl)

    #  写入github page 主页文件
    with open("./docs/index.html", "w", encoding="utf-8") as f:
        f.write('{},{},{} '.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), " 最新的V2Ray订阅链接地址：", v2rayUrl))

    # 下载最新V2Ray订阅链接
    v2raySession = video_result['session'].get(v2rayUrl)
    v2rayText = v2raySession.text
    print('\n', datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 最新V2Ray订阅链接内容：\n', v2rayText)

    #  写入github page文件
    with open("./docs/v2ray/index.html", "w", encoding="utf-8") as f:
        f.write(v2rayText)

    return v2rayUrl

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


if __name__ == '__main__':
    # 创建 YouTube 对象
    yt = YouTube(video_url)

    # 从youtube获取密码
    mima = getMima(yt)

    # 从页面获取v2ray链接并下载
    v2rayUrl = getV2ray(uncodeSession, mima)

    # pushplus` 推送到微信
    pushplus.pushplus_notify('最新的V2Ray订阅链接', v2rayUrl)

    # 清理临时文件
    removeTempFile()





######################################################################################################################################
