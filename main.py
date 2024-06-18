from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime
import pushplus
import os,re
import GetYoutubeUrl
import speechToText.baiduSpeech  as baiduSpeech

from requests_html import HTMLSession
from aesDecrypt import decrypt,decodeUrl


# 视频下载路径
video_path = "./video/"
video_filename = "code.mp4"
video_fullpath = video_path + video_filename

i = 0



# 获取要下载的 YouTube 视频链接
tmpResult= GetYoutubeUrl.getYoutubeUrl()
yudouTodayUrl = tmpResult['yudouTodayUrl']      # 今日yudou最新连接
youtubeUrl = tmpResult['youtubeUrl']            # youtobe最新连接解密视频的链接






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





# 要计算一个4位数字的字符串中出现连续两次的数字的个数，可以使用以下代码：
def count_grouped_consecutive_occurrences(input_str):
    count = 0
    i = 0
    while i < len(input_str) - 1:
        if input_str[i] == input_str[i + 1]:
            count += 1
            i += 2  # 跳过下一个字符
        else:
            i += 1
    return count









def validateMima(mimaStr):
    # 验证密码是否为4位数字
    try:
        mima = mimaStr[(mimaStr.index("密码") + 2):(mimaStr.index("密码") + 10)]
        mima = re.findall(r'\d+', mima)[0]
        if len(mima) == 5:
            mima1 = mima[:4]
            mima2 = mima[1:5]
            mimaInt = int(max(count_grouped_consecutive_occurrences(mima1), count_grouped_consecutive_occurrences(mima2)))
            return mimaInt
        elif len(mima) == 4:
            mimaInt = int(mima)
            return mimaInt
        elif len(mima) >= 6 or len(mima) <=3:
            return -1
    except Exception as e:
        print(e)
        return -1



# 获取密码
def getMima(videoUrl,videoFullpath):
    videPath, videoFilename = os.path.split(videoFullpath)
    videPath = videPath + r'/'

    # 创建 YouTube 对象
    yt = YouTube(videoUrl)

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
            print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' Google提取的文字为 : '+ subtitleGoogle)

            # 验证密码
            mima = validateMima(subtitleGoogle)
            if mima != -1:
                print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 密码：", str(mima))
                return mima
            else:
                subtitleBaidu = baiduSpeech.wavToText(tempAudioPath)
                print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' Baidu 提取的文字为 : ' + subtitleBaidu)
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
def getV2ray(yudouTodayUrl,mima):
    # 执行页面的js代码
    uncodeJs = "multiDecrypt('" + str(mima) + "');"


    with HTMLSession() as session:
        yudouSession = session.get(yudouTodayUrl)
        tmpStr = yudouSession.text
        encryption = re.findall(r'.+var encryption.+"(.+==)",.+', tmpStr, re.S)
        encryption = encryption[0].encode('utf-8')
        mima = str(mima).encode('utf-8')

        # 解密
        result = decrypt(encryption, mima)
        result = decodeUrl(result)

        # 匹配 v2ray 链接
        v2rayUrl =  re.findall(r'.+>(http.+\.txt)<.+', result, re.S)[0]
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新的V2Ray订阅链接地址：", v2rayUrl)



    if not os.path.exists("./docs/v2ray/"):
        os.makedirs(os.path.abspath("./docs/v2ray"))

    #  写入github page 主页文件
    with open("./docs/index.html", "w", encoding="utf-8") as f:
        f.write('{},{},{} '.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), " 最新的V2Ray订阅链接地址：\n", result))




    # 下载最新V2Ray订阅链接
    with HTMLSession() as session:
        v2raySession = session.get(v2rayUrl)
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

    # 从youtube获取密码
    mima = getMima(youtubeUrl,video_fullpath)

    # 从页面获取v2ray链接并下载
    v2rayUrl = getV2ray(yudouTodayUrl, mima)

    # pushplus` 推送到微信
    pushplus.pushplus_notify('最新的V2Ray订阅链接', v2rayUrl)

    # 清理临时文件
    removeTempFile()





######################################################################################################################################
