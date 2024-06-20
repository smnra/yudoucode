
from datetime import datetime
import os,re
from requests_html import HTMLSession
from aesDecrypt import decrypt,decodeUrl
import GetYoutubeUrl
import pushplus









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





# 从网页上获取加密后的密文
def getEncryption(yudouTodayUrl):
    with HTMLSession() as session:
        yudouSession = session.get(yudouTodayUrl)
        tmpStr = yudouSession.text
        encryption = re.findall(r'.+var encryption.+"(.+==)",.+', tmpStr, re.S)
        encryption = encryption[0].encode('utf-8')
    return encryption






def verifyCiphertext(encryption):
    # 解密
    for password in range(1000, 10000):
        try:
            # 编码
            password = str(password).encode('utf-8')

            # 解密
            result = decrypt(encryption, password)
            result = decodeUrl(result)
            if '免费节点订阅链接' in result:
                print('密码:{}正确, 解密结果为:{}'.format(password, result))
                return result
            else:
                # print('密码:{} 解密错误, 重试下一个...'.format(password))
                continue
        except Exception as e:
            print('密码:{}  解密失败, 重试下一个...'.format(password))
            continue








# 提取v2ray连接, 写入文件
def v2rayToFile(v2rayResult):
    if not os.path.exists("./docs/v2ray/"):
        os.makedirs(os.path.abspath("./docs/v2ray"))

    #  写入github page 主页文件
    with open("./docs/index.html", "w", encoding="utf-8") as f:
        f.write('{},{},{} '.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), " 最新的V2Ray订阅链接地址：\n", v2rayResult))

    try:
        # 匹配 v2ray 链接  并下载最新订阅链接
        v2rayUrl =  re.findall(r'.+等订阅链接，不需要开代理，即可更新订阅链接\<br \/\>(http.+\.txt)\<.+', v2rayResult, re.S)
        v2rayUrl = v2rayUrl[0]
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 最新的V2Ray订阅链接地址：", v2rayResult)
    except Exception as e:
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " 解析V2Ray订阅链接异常：", e)
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " re  匹配异常",  re.findall(r'.+等订阅链接，不需要开代理，即可更新订阅链接\<br \/\>(http.+\.txt)\<.+', v2rayResult, re.S))

    # 下载最新V2Ray订阅链接
    with HTMLSession() as session:
        v2raySession = session.get(v2rayUrl)
        v2rayText = v2raySession.text
        # print('\n', datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ' 最新V2Ray订阅链接内容：\n', v2rayText)

    #  写入github page文件
    with open("./docs/v2ray/index.html", "w", encoding="utf-8") as f:
        f.write(v2rayText)

    return v2rayUrl












if __name__ == '__main__':
    # 获取要下载的 YouTube 视频链接
    tmpResult = GetYoutubeUrl.getYoutubeUrl()
    yudouTodayUrl = tmpResult['yudouTodayUrl']  # 今日yudou最新连接

    # 从今日yudou最新连接 获取加密后的密文
    encryption = getEncryption(yudouTodayUrl)

    # 穷举法解密
    v2rayResult = verifyCiphertext(encryption)

    # v2ray结果 写入文件
    v2rayUrl = v2rayToFile(v2rayResult)


    # pushplus` 推送到微信
    pushplus.pushplus_notify('最新的V2Ray订阅链接:\n', v2rayResult)

    # 清理临时文件
    removeTempFile()
