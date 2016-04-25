#!usr/bin/env python
#coding=utf-8

import numpy as np
from pyaudio import PyAudio,paInt16
from datetime import datetime
import base64
import urllib2
import urllib
import json
import wave
import pyaudio
import os
from pydub import AudioSegment

#define of params
NUM_SAMPLES = 2000
framerate = 8000
channels = 1
sampwidth = 2
#record time
TIME = 10

def get_answer(info):
  URL = 'http://www.tuling123.com/openapi/api'
  _params = urllib.urlencode({'key': '15576eb36ece7704933635c64a246c70',
                              'info': info})
  _res = urllib2.Request(URL, _params)
  _response = urllib2.urlopen(_res)
  _data = _response.read()
  _data = json.loads(_data)
  return _data['text']

def play_sound(file):
  sound = AudioSegment.from_mp3(file)
  exp_wav_file = "Play-"+datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
  sound.export(exp_wav_file, format="wav")
  chunk = 1024
  wf = wave.open(exp_wav_file, 'rb')
  p = pyaudio.PyAudio()
  stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True)
  data = wf.readframes(chunk)

  while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

  stream.close()
  p.terminate()

def text2audio(text):
  URL = 'http://tsn.baidu.com/text2audio'
  _params = urllib.urlencode({'tex': text.encode('utf-8'),
                              'lan': 'zh',
                              'ctp': '1',
                              'cuid': 'B8-AC-6F-2D-7A-94',
                              'tok': get_token()})

  _res = urllib2.Request(URL, _params)
  _response = urllib2.urlopen(_res)

  fname = "Play-"+datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".mp3"
  file = open(fname, 'wb')
  file.write(_response.read())
  file.close()
  play_sound(fname)
  os.popen('rm ./*.mp3')
  os.popen('rm ./*.wav')
  record_wave()
  # os.popen('mplayer '+fname)
  
  # record_wave()

def get_token():
  URL = 'http://openapi.baidu.com/oauth/2.0/token'
  _params = urllib.urlencode({'grant_type': 'client_credentials',
                              'client_id': '3t7BMc8GdMt5dYvDFBQ6E2Tc',
                              'client_secret': 'kIVOkbNs31jTOoMtgr6vkmRtdpwqwYD3'})
  _res = urllib2.Request(URL, _params)
  _response = urllib2.urlopen(_res)
  _data = _response.read()
  _data = json.loads(_data)
  return _data['access_token']

def save_wave_file(filename, data):
  '''save the date to the wav file'''
  wf = wave.open(filename, 'wb')
  wf.setnchannels(channels)
  wf.setsampwidth(sampwidth)
  wf.setframerate(framerate)
  wf.writeframes("".join(data))
  wf.close()

def wav_to_text(wav_file):
  try:
      wav_file = open(wav_file, 'rb')
  except IOError:
      print u'文件错误啊，亲'
      return
  wav_file = wave.open(wav_file)
  n_frames = wav_file.getnframes()
  frame_rate = wav_file.getframerate()
  if n_frames == 1 or frame_rate not in (8000, 16000):
      print u'不符合格式'
      return
  audio = wav_file.readframes(n_frames)
  seconds = n_frames/frame_rate+1
  minute = seconds/60 + 1
  for i in range(0, minute):
      sub_audio = audio[i*60*frame_rate:(i+1)*60*frame_rate]
      base_data = base64.b64encode(sub_audio)
      data = {"format": "wav",
              "token": get_token(),
              "len": len(sub_audio),
              "rate": frame_rate,
              "speech": base_data,
              "cuid": "B8-AC-6F-2D-7A-94",
              "channel": 1}
      data = json.dumps(data)
      res = urllib2.Request('http://vop.baidu.com/server_api',
                            data,
                            {'content-type': 'application/json'})
      response = urllib2.urlopen(res)
      res_data = json.loads(response.read())
      decode_text = res_data['result'][0].encode('utf-8')
      text = get_answer(decode_text)
      # text = u"欢迎来到 Segment Fault"
      print decode_text
      print text.encode('utf-8')
      text2audio(text)

def record_wave():
  pa = PyAudio()
  stream = pa.open(format = paInt16, channels = 1,
          rate = framerate, input = True,
          frames_per_buffer = NUM_SAMPLES)
  save_buffer = []
  count = 0
  while count < TIME:
    string_audio_data = stream.read(NUM_SAMPLES)
    save_buffer.append(string_audio_data)
    count += 1

  filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
  save_wave_file(filename, save_buffer)
  save_buffer = []
  wav_to_text(filename)

def main():
  record_wave()
  # play_sound('Play-2015-08-26_16_21_21.mp3')


if __name__ == "__main__":
  main()