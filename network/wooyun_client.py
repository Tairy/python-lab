import requests

headers = {
  "content-type": "application/text",
  "connection": "keep-alive",
  "accept-encoding": "gzip",
  "user-agent":""
}

proxies = {
  'http': 'http://127.0.0.1:8888',
}

r = requests.get('http://2935cc63796d47603.jie.sangebaimao.com/data.php', headers=headers, proxies=proxies)
print r.text