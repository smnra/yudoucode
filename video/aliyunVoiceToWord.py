# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html

import dashscope
from urllib import request
import json





def voiceToWord(voiceFile,api_key):
    dashscope.api_key = api_key
    task_response=dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[voiceFile]
        )
    transcription_response=dashscope.audio.asr.Transcription.wait(task_response.output.task_id)

    transcription_url=transcription_response.output['results'][0]['transcription_url']
    transcription_results=json.loads(request.urlopen(transcription_url).read().decode('utf8'))
    print(transcription_results['transcripts'][0]['text'])

if __name__ == '__main__':
    api_key = 'sk-c2c975dee5e44f29af16ac2f6df1c80c'
    voiceFile = 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav'
    voiceToWord(voiceFile,api_key)





# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html

import dashscope
from urllib import request
import json

dashscope.api_key='your-dashscope-api-key'

task_response=dashscope.audio.asr.Transcription.async_call(
    model='paraformer-v1',
    file_urls=['https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/2022_apsara_conference_keynote.mp4']
    )

transcription_response=dashscope.audio.asr.Transcription.wait(task_response.output.task_id)

transcription_url=transcription_response.output['results'][0]['transcription_url']
transcription_results=json.loads(request.urlopen(transcription_url).read().decode('utf8'))

for sentence in transcription_results['transcripts'][0]['sentences']:
        print(sentence['text'])
