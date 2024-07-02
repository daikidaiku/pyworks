from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse # URLエンコード、デコード
import json
import datetime
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

# 1月1日〜1月4日を除く最初の木曜日を算出
def first_thursday(year):
    # 1月4日から始める
    first_possible_day = datetime.date(year, 1, 5)
    # 最初の木曜日を探す
    days_to_thursday = (3 - first_possible_day.weekday()) % 7
    first_thursday = first_possible_day + datetime.timedelta(days=days_to_thursday)
    return first_thursday

def garbage_collection_day(today):
    # today = datetime.date.today()

    weekday = today.weekday()  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    # day_of_month = numberOfWeek(today)
    day_of_month = (today.day - 1)//7
    month = today.month

    is_garbage = True


    # Determine garbage collection based on the rules
    if weekday == 0:  # Monday
      if day_of_month == 1:
        return is_garbage, "ビン・カン・スプレー缶","有害ごみ（電池）"
      elif day_of_month == 3:
        return is_garbage,"ビン・カン・スプレー缶","有害ごみ\n（蛍光管・水銀体温計・ライター）"
      else:
        return is_garbage,"ビン・カン・スプレー缶"
      
    elif weekday == 1:  # Tuesday
      return is_garbage,"可燃ごみ"
    
    elif weekday == 2:  # Wednesday
      if day_of_month % 7 == 6:
        return is_garbage,"古紙・古着・段ボールごみ"
      
    elif weekday == 3:  # Thursday
      days_of_thursday = (today - first_thursday(today.year)).days
      # print(days_of_thursday%14)
      if days_of_thursday % 14 == 0:
        return is_garbage,"不燃ごみ"
      else:
        return is_garbage,"ペットボトル"
      
    elif weekday == 4:  # Friday
      return is_garbage, "可燃ごみ"
    
    elif weekday == 5:  # Saturday
      return is_garbage,"古紙・古着・段ボールごみ"

    # Default case for other days
    is_garbage = False
    return is_garbage,""

# Define the input array
input_array = garbage_collection_day(datetime.date.today())

garbage_pic = {"ビン・カン・スプレー缶":os.getenv('CANS'),
               "有害ごみ（電池）":os.getenv('BATTERY'),
               "有害ごみ\n（蛍光管・水銀体温計・ライター）":os.getenv('LIGHTER'),
               "可燃ごみ":os.getenv('FLAMMABLE'),
               "古紙・古着・段ボールごみ":os.getenv('PAPER'),
               "ペットボトル":os.getenv('PETBOTTLE'),
               "不燃ごみ":os.getenv('NONFLAMMABLE')
               }

# Function to update JSON structure dynamically
def update_json_structure(input_array):
  json_structure = {
    "type": "bubble",
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
              "text": "今日は",
              "weight": "bold"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": []
        }
      ]
      }
    }

  # Extract values from input_array
  status = input_array[0]
  text_message = ""
  if status:
    for item in input_array[1:]:
      # Create new box for the new items
      new_box = {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "image",
            "url": garbage_pic[item]
          },
          {
            "type": "text",
            "text": item,
            "weight": "bold",
            "align": "center",
            "gravity": "center",
            "wrap": True
          }
        ]
      }
      # Add the new box to the horizontal contents
      json_structure['body']['contents'][1]['contents'].append(new_box)
      
    text_message = ",".join(input_array[1:])
  return json_structure, text_message

# Update the JSON structure with the input array
updated_json,text_message = update_json_structure(input_array)

configuration = Configuration(
  access_token = os.getenv('LINE_ACCESS_TOKEN')
)
if input_array[0]:
  message_dict = {
    'to': os.getenv('LINE_MY_ADRESS'),
    'messages': [
      {
        'type': 'flex',
        'altText': text_message,
        'contents': updated_json
      },
    ]
  }
else:
  message_dict = {
    'to': os.getenv('LINE_MY_ADRESS'),
    'messages': [
        {
          'type': 'text',
          'text': '今日はゴミ捨ての日ではありません'
        },
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