from pytube import YouTube
from playwright.sync_api import sync_playwright
from pydub import AudioSegment
import speech_recognition as sr


import GetYoutubeUrl


# 获取要下载的 YouTube 视频链接
# video_url = "https://youtu.be/2EJ9pBRUo6k"
with GetYoutubeUrl.sync_playwright() as p:
    video_url = GetYoutubeUrl.getYoutubeUrl(p)



video_path = "./video/"
video_filename = "code.mp4"
video_fullpath = video_path + video_filename

# 创建 YouTube 对象
yt = YouTube(video_url)

# 选择要下载的视频流
video_stream = yt.streams.filter(file_extension='mp4').first()

# 下载视频
video_stream.download(output_path=video_path,filename=video_filename)



# 从视频中提取音频

audio = AudioSegment.from_file(video_fullpath, format="mp4")

# 将音频保存为临时文件
temp_audio_path = "temp_audio.wav"
audio.export(temp_audio_path, format="wav")

# 使用音频识别库进行语音识别
recognizer = sr.Recognizer()
with sr.AudioFile(temp_audio_path) as source:
    audio_data = recognizer.record(source)
    subtitleGoogle = recognizer.recognize_google(audio_data, language="zh-CN")

print(subtitleGoogle)
mima = subtitleGoogle[(subtitleGoogle.index("密码")+2):(subtitleGoogle.index("密码")+6)]


print(mima)




