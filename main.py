from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
last_back=os.environ["LAST_BACK"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  weather1 = weather['weather']
  temp1 = math.floor(weather['temp'])
  if "雨" in weather1:
    weather1 += "  注意带伞，别淋湿了"
  elif "晴" in weather1:
    weather1 += "  注意防晒，别晒黑了，小黑球"
  if temp1 >=24:
    temp2 = "%.2f  适合穿短袖/短裤，但是不能穿的太凉快"
  elif temp1 >=15:
    temp2 = "%.2f  适合穿薄外套，注意不要感冒哦"
  else:
    temp2 = "%.2f  天气冷，要注意保暖哦"
  return weather1, temp2

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_back():
  next = datetime.strptime(str(date.today().year) + "-" + last_back, "%Y-%m-%d")
  if (next-today).days>=0:
    return "距离下次回来还有%d天" % (next-today).days
  else :
    return "距离上次回来已经过去%d天" % (today-next).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"last_back":{"value":get_back()},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
