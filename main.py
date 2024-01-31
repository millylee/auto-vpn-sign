import requests, json, re, os

session = requests.session()
siteUrl = os.environ.get('SITE_URL')
email = os.environ.get('EMAIL')
passwd = os.environ.get('PASSWORD')
pushPlusToken = os.environ.get('PUSHPLUS_TOKEN')

loginUrl = '{}/auth/login'.format(siteUrl)
checkInUrl = '{}/user/checkin'.format(siteUrl)
pushPlusUrl = 'http://www.pushplus.plus/send'

pushPlusData = {
  'token': pushPlusToken,
  'title': '签到领流量',
  'template': 'txt',
  'channel': 'wechat'
}

header = {
  'origin': siteUrl,
  'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

data = {
  'email': email,
  'passwd': passwd
}

try:
  print('[CheckIn] {}'.format('准备登录'))

  response = json.loads(session.post(url=loginUrl,headers=header,data=data).text)
  print('[CheckIn] {} {}'.format('请求数据', response['msg']))

  result = json.loads(session.post(url=checkInUrl,headers=header).text)
  content = result['msg']
  print('[CheckIn] {} {}'.format('签到结果', content))

  if pushPlusToken != '':
    pushPlusData['content'] = content
    requests.post(url=pushPlusUrl, data=json.dumps(pushPlusData))
    print('[CheckIn] {}'.format('推送成功'))
except Exception as e:
  print('[CheckIn] {} {}'.format('捕获异常', e))
  if pushPlusToken != '':
    pushPlusData['content'] = e
    requests.post(url=pushPlusUrl, data=json.dumps(pushPlusData))