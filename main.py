from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime
import pushplus

import GetYoutubeUrl


# 获取要下载的 YouTube 视频链接
# video_url = "https://youtu.be/2EJ9pBRUo6k"

video_result = GetYoutubeUrl.getYoutubeUrl()

video_url=video_result['url']


video_path = "./video/"
video_filename = "code.mp4"
video_fullpath = video_path + video_filename

# 创建 YouTube 对象
yt = YouTube(video_url)

# 选择要下载的视频流
# video_stream = yt.streams.filter(file_extension='mp4').first()
video_stream = yt.streams.filter(type="audio").first()
# 下载视频
video_stream.download(output_path=video_path,filename=video_filename)



# 从视频中提取音频

audio = AudioSegment.from_file(video_fullpath, format="mp4")

# 将音频保存为临时文件
temp_audio_path = "temp_audio.wav"
audio.export(temp_audio_path, format="wav")


recognizer = sr.Recognizer()
with sr.AudioFile(temp_audio_path) as source:
    audio_data = recognizer.record(source)
    subtitleGoogle = recognizer.recognize_google(audio_data, language="zh-CN")

print(subtitleGoogle)
mima = subtitleGoogle[(subtitleGoogle.index("密码")+2):(subtitleGoogle.index("密码")+6)]


print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 密码：",mima)

# 执行页面的js代码
uncodeJs = "multiDecrypt('" + mima + "');"
uncodeSession = video_result['response']
uncodeSession.html.render(script=uncodeJs)


# 获取 'v2ray/小火箭/winxray等订阅链接，不需要开代理，即可更新订阅链接'
# '//*[@id="result"]/p[2]/text()[2]'
v2rayElement = uncodeSession.html.xpath('//*[@id="result"]/p[2]/text()[2]')
v2rayUrl = v2rayElement[0]
print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新的V2Ray订阅链接地址：",v2rayUrl)

v2raySession = video_result['session'].get(v2rayUrl)
v2rayText = v2raySession.text
print(v2rayText)

pushplus.pushplus_notify('最新的V2Ray订阅链接', v2rayUrl)

#  写入文件
with open("v.txt", "w", encoding="utf-8") as f:
    f.write(v2rayText)
