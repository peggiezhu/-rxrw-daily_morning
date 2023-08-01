from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import requests

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = ["olv_Y5tnOPHhSXGtioKsNo008CZk", "olv_Y5rg2_wv_Sxs5TMdHc3aijOM"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://eolink.o.apispace.com/456456/weather/v001/now"
  payload = {"areacode" : "101190403","lonlat" : "116.407526,39.904030"}
  headers = {
    "X-APISpace-Token":"9e1o3xkw5m6fiq2hzlqh8lbe799k36yf",
    "Authorization-Type":"apikey"
  }
  res = requests.request("GET", url, params=payload, headers=headers).json()
  weather = res['result']['realtime']
  return weather['text'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

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
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
