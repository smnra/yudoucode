# pip install baidu-aip chardet
from pydub import AudioSegment
import os
from aip import AipSpeech



# 你的APPID AK SK
APP_ID = '82419253'
API_KEY = 'I6KU8my5YbJODFqaTYivk8yd'
SECRET_KEY = 'mslltsRDNwVCEsmiQjcQih2K9wYHU7au'

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")






client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 定义函数，将音频文件分割为1分钟片段并保存
def wavSplit(file_path, split_time=60):
    # 加载音频文件
    # audio = AudioSegment.from_mp3("original_audio.mp3")  # 假设是mp3格式，根据实际情况调整
    audio = AudioSegment.from_wav(file_path)  # 假设是wav格式，根据实际情况调整
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)

    path, filename = os.path.split(file_path)  # 获取文件路径和文件名
    baseName = os.path.splitext(filename)[0]  # 获取文件名（不含扩展名）
    extName = os.path.splitext(filename)[1]  # 获取文件扩展名
    # 计算音频总时长（秒）

    total_milliseconds = len(audio)
    result = []

    # 分割音频为1分钟片段，包括最后一个不足一分钟的部分
    start = 0
    i=1
    while start < total_milliseconds:
        end = start + split_time * 1000  # 每个片段60秒
        if end > total_milliseconds:  # 如果结束位置超过总长度，则设置为总长度
            end = total_milliseconds
        segment = audio[start:end]

        # 保存每个片段，指定输出格式和采样率
        segment.export(f"{path}/{baseName}_part_{i}.wav", format="wav", bitrate="48k" )
        result.append( f"{path}/{baseName}_part_{i}.wav")

        start = end  # 更新起始位置到当前片段的结束位置，准备下一次切割
        i += 1
    return list(result)











def recognize_audio(file_path):
    """调用百度语音识别API"""
    with open(file_path, 'rb') as fp:
        audio_data = fp.read()
    # 调用识别接口
    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,  # 识别模型，1536表示普通话（默认）
    })
    if 'result' in result:
        return result['result'][0]  # 返回识别结果
    else:
        return "识别失败：" + str(result)


def wavToText(file_path):
    """将音频文件转为文字"""
    resultAllTxt = ''
    resultWavList = wavSplit(file_path,30)  # 将音频文件分割为1分钟片段并保存
    for i,resultWav in enumerate(resultWavList):
        resultTxt = recognize_audio(resultWav)
        # print(f"第{i+1}段结果：{resultTxt}")
        resultAllTxt = resultAllTxt + resultTxt
        os.remove(resultWav)  # 删除分割后的音频文件
    return resultAllTxt


if __name__ == '__main__':
    result = wavToText('../video/test.wav')
    print(result)