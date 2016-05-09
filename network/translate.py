import re
import urllib,urllib2
import random

def translate(sentence):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533 (KHTML, like Gecko) Element Browser 5.0', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5748.400']
    index = random.randint(0, 8)
    index2 = random.randint(0,1)
    values = {'q':sentence}
    url = 'https://translate.google.com/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=130747.514627'
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    user_agent = user_agents[index]
    req.add_header('user-agent', user_agent)
    response = urllib2.urlopen(req,timeout=10)
    r = response.read()
    p = re.compile(",,+")
    m = p.findall(r)
    for i in m:
        r = r.replace(i,',')
    r=r.replace('[,','[')
    r= r.replace('true','1').replace('false','0')
    r = eval(r)
    trans_s = ''
    for l in r[0][:-1]:
        trans_s+=l[0]

    return trans_s

if __name__ == '__main__':
    f = open(r'../data/cn_train_label.txt')
    f2 = open(r'../data/en_train_label.txt','w+')
    for line in f:
        s = translate(line[:-1])
        f2.write(s)
        f2.write('\n')
    f2.close()
    f.close()