# encoding:utf-8
import requests
from PIL import Image

for i in range(5261, 100000):
  url = 'https://pin.aliyun.com/get_img?identity=sm-shopsystem&sessionid=7b80c6e54506426c14409e0a2b5adfac&type=number&t=1514271600732'
  file_name = 'predict_set/' + str(i) + '.jpeg'
  req = requests.get(url, stream=True)
  output = open(file_name,'wb')
  output.write(req.content)
  output.close()
  print(file_name)
