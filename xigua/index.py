# encoding:utf-8
from PIL import Image
from bs4 import BeautifulSoup
import pytesseract
import os
import sys
import requests
import re

reload(sys)
sys.setdefaultencoding('utf-8')

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

header = {
  "User-Agent":
  "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",
  "Host":
  "www.baidu.com",
  "Cache-Control":
  "no-cache"
}

while True:
  if os.path.isfile('autojump.png'):
    im = Image.open('autojump.png')
    x = 40
    y = 210
    w = 1000
    h = 1100
    region = im.crop((x, y, x + w, y + h))
    width, height = region.size
    for w in xrange(0, width):
      for h in xrange(0, height):
        r, g, b, a = region.getpixel((w, h))
        if r < 215 and g < 215 and b < 215:
          region.putpixel([w,h], (0, 0, 0))
        else :
          region.putpixel([w,h],(255, 255,255))
    # region.save('tt.png')
    # break
    result_str = pytesseract.image_to_string(region, lang='chi_sim')
    result_str = result_str.replace("\n", "", 1).replace("唧", "哪", 1)
    result = filter(None, result_str.split("\n"))
    question = result[0].split(".")[1].strip()

    session = requests.session()
    # session.proxies = {'http': 'socks5://127.0.0.1:1086',
                   # 'https': 'socks5://127.0.0.1:1086'}
    content = ""
    for i in xrange(0, 5):
      page = i * 10
      # url = "https://www.google.com.sg/search?q=" + question + "&start=" + str(page)
      url = "https://www.baidu.com/s?wd=" + question
      google_result = session.get(url=url, headers=header)
      # google_result = session.get("https://www.google.com.sg/search?q=" + question)
      soup = BeautifulSoup(google_result.text, 'html.parser')
      [script.extract() for script in soup.findAll('script')]
      [style.extract() for style in soup.findAll('style')]
      # tmp_content = reg1.sub('',soup.prettify())
      # tmp_content = tmp_content.replace("\n", "")
      # tmp_content = tmp_content.replace(" ", "")
      content += soup.prettify()
      pass

    reg1 = re.compile("<[^>]*>")
    content = reg1.sub("", content)
    content = content.replace("\n", "")
    content = content.replace(" ", "")
    
    print question
    for i in xrange(1, len(result)):
      if result[i]:
        print result[i].replace(" ", "")
        print content.count(result[i].replace(" ", ""))
    os.remove('autojump.png')