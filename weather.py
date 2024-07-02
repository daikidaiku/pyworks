from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException

import requests
from bs4 import BeautifulSoup
import datetime
import schedule
import time
import re
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

info = requests.get("https://tenki.jp/forecast/3/16/4410/13209/")
bs = BeautifulSoup(info.content, "html.parser")

today = bs.find(class_="today-weather")
l = bs.find("h2").text
d=l.find("の天気")
location=l[0:d+3]

weather_icon = today.find("img").get("src")
date = today.find("h3").text
weather = today.find(class_="weather-telop").string
high_temp = today.find_all(class_="value")[0].string
low_temp = today.find_all(class_="value")[1].string
message = "今日の"  + location + "は" + weather + "、最高気温は{}℃".format(high_temp) + "、最低気温は{}℃です。".format(low_temp)

configuration = Configuration(
  access_token = os.getenv('LINE_ACCESS_TOKEN')
)

message_dict = {
    'to': os.getenv('LINE_MY_ADRESS'),
    'messages':[
        {
            'type': 'flex',
            'altText': message,
            'contents': {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": location,
            "color": "#000000",
            "size": "xl",
            "weight": "bold"
          },
          {
            "type": "text",
            "text": date,
            "color": "#000000",
            "size": "lg",
            "weight": "bold"
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": weather_icon,
                "size": "md"
              },
              {
                "type": "text",
                "text": weather,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "contents": [
                  {
                    "type": "span",
                    "text": "最高  ",
                    "size": "lg",
                    "color": "#ff0000"
                  },
                  {
                    "type": "span",
                    "text": high_temp,
                    "size": "xxl",
                    "weight": "bold",
                    "color": "#ff0000"
                  },
                  {
                    "type": "span",
                    "text": "℃",
                    "size": "lg",
                    "color": "#ff0000"
                  }
                ]
              },
              {
                "type": "text",
                "contents": [
                  {
                    "type": "span",
                    "text": "最高  ",
                    "size": "lg",
                    "color": "#0000ff"
                  },
                  {
                    "type": "span",
                    "text": low_temp,
                    "size": "xxl",
                    "weight": "bold",
                    "color": "#0000ff"
                  },
                  {
                    "type": "span",
                    "text": "℃",
                    "size": "lg",
                    "color": "#0000ff"
                  }
                ]
              }
            ],
            "alignItems": "center",
            "justifyContent": "center"
          }
        ]
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#ffffff",
    "spacing": "md",
    "paddingTop": "22px"
  }
}
        }
    ]
}

with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = MessagingApi(api_client)
    push_message_request = PushMessageRequest.from_dict(message_dict)

    try:
        push_message_result = api_instance.push_message_with_http_info(push_message_request, _return_http_data_only=False)
        print(f'The response of MessagingApi->push_message status code => {push_message_result.status_code}')
    except ApiException as e:
        print('Exception when calling MessagingApi->push_message: %s\n' % e)

