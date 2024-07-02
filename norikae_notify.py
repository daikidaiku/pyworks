from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException # type: ignore

'''
現在時刻から直近の乗換案内を検索して、到着時間を表示する
Yahoo乗換から到着時間をスクレイピングで抽出している
'''
import urllib.request
from bs4 import BeautifulSoup # type: ignore
import urllib.parse # URLエンコード、デコード
import json
import datetime
import re
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

# import pyperclip # type: ignore #クリップボードにコピーする用

startsta = '西早稲田' # 出発駅
endsta = '鶴川' # 到着駅

# 改行を追加する関数
def add_newline_to_times(times):
  updated_times = []
  for time in times:
    if '着' in time and '発' in time:
      # '着'の後と'発'の前に改行を追加
      time = time.replace('着', ' 着\n').replace('発', ' 発')
    updated_times.append(time)
  return updated_times

# 発着間にスペースを追加する関数
def delete_line_from_times(times):
  updated_times = []
  for time in times:
    if '着' in time and '発' in time:
      # '着'の後と'発'の前に改行を追加
      time = time.replace('着', '').replace('発', '')
    updated_times.append(time)
  return updated_times

# 出発時間と到着時間、所要時間のフォーマット関数
def transform_time_string(time_string):
  # Use regex to match the parts of the string, allowing for 1 or 2 digits for the ride time
  pattern = r'(\d{2}:\d{2})発→(\d{2}:\d{2})着(\d+分)（乗車(\d+分)）'
  match = re.match(pattern, time_string)
  
  if match:
    # Extract matched groups
    departure, arrival, total_time, ride_time = match.groups()
    # Format the string with spaces
    formatted_string = f"{departure}発 → {arrival}着  {total_time}（乗車 {ride_time}）"
    return formatted_string
  else:
    return "Invalid input format"

def route_to(startsta, endsta):
  startstaen = urllib.parse.quote(startsta) # encode
  endstaen = urllib.parse.quote(endsta) # encode

  url0 = 'https://transit.yahoo.co.jp/search/result?from='
  url1 = '&flatlon=&to='
  url2 = '&viacode=&viacode=&viacode=&shin=&ex=&hb=&al=&lb=&sr=&type=1&ws=3&s=&ei=&fl=1&tl=3&expkind=1&ticket=ic&mtf=1&userpass=0&detour_id=&fromgid=&togid=&kw='

  url = url0 + startstaen + url1 + endstaen + url2 + endstaen
  # print(url)

  req = urllib.request.urlopen(url)
  
  html = req.read().decode('utf-8')
  # print(html)
  soup = BeautifulSoup(html, 'html.parser')

  detail = soup.find(class_="routeDetail")
  # times = detail.find_all(class_="time")
  times = []
  tms = detail.select("ul.time")
  for i in tms:
    times.append(i.text)

  # 改行を追加した時間データ
  train_times = add_newline_to_times(times)

  # print(times)

  # 各駅の所要時間データ
  spend_times = []
  spnd_tm = delete_line_from_times(times)
  # print(spnd_tm)
  for i in range(len(spnd_tm)-1):
    bound_time = spnd_tm[i][:5] if i == 0 else spnd_tm[i][5:]
    arrive_time = spnd_tm[i+1][:5]
    if len(arrive_time) > 5:
      arrive_time = arrive_time[5:]
    bound_time = datetime.datetime.strptime(bound_time, '%H:%M')
    arrive_time = datetime.datetime.strptime(arrive_time, '%H:%M')
    # print(bound_time, arrive_time)
    spend_time = arrive_time - bound_time
    total_seconds = int(spend_time.total_seconds())
    spend_time = (total_seconds % 3600) // 60
    spend_time = str(spend_time)
    spend_time += "分"
    spend_times.append(spend_time)

  # print(spend_times)

  # 発着駅データ
  stations = []
  stat = detail.find_all("dt")
  for i in stat:
    if i.find("a"):
      stations.append(i.find("a").text)

  # 路線データ
  lines = []
  lns = detail.find_all(class_="transport")
  for i in lns:
    i = i.find("div")
    i.find("span", {"class":"icon icnTrain"}).extract()
    i.find("span").extract()
    i = i.get_text()
    lines.append(i)

  #総所要時間データ
  total_time = soup.find_all('li', attrs={'class': 'time'})
  # total_time.find("span").extract()
  # total_time = total_time.select(class_="time")
  total_time = total_time[-1].text
  total_time = transform_time_string(total_time)
  # print(total_time)

  # 発着番線データ
  platform_nums = []
  home_num = detail.find_all('span', attrs={'class': 'num'})
  for n in home_num:
    platform_nums.append(n.text+" 番線")
  # print(platform_nums)

  # for i in lns:
  # 	lines.append(i.text)
  # print(lines)

  # print(stations)
  # print(json.dumps(times, indent=4,ensure_ascii=False))

  # for time in times:
  # 	print(time.text)
  # for station in stat:
  # 	print(station)





  json_template = {
    "type": "bubble",
    "size": "mega",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "FROM",
              "color": "#ffffff66",
              "size": "sm"
            },
            {
              "type": "text",
              "text": stations[0],
              "color": "#ffffff",
              "size": "xl",
              "flex": 1,
              "weight": "bold"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "TO",
              "color": "#ffffff66",
              "size": "sm"
            },
            {
              "type": "text",
              "text": stations[-1],
              "color": "#ffffff",
              "size": "xl",
              "flex": 1,
              "weight": "bold"
            }
          ]
        }
      ],
      "paddingAll": "20px",
      "backgroundColor": "#0367D3",
      "spacing": "md",
      "height": "154px",
      "paddingTop": "22px"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": total_time,
          "color": "#000000",
          "size": "sm"
        }
      ]
    }
  }

  # 駅と時間の情報をBODYセクションに追加
  body_contents = json_template["body"]["contents"]
  for i in range(len(stations)):
    # 駅情報
    station_box = {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": train_times[i],
          "size": "sm",
          "gravity": "center",
          "wrap": True,
          "align": "center",
          "flex": 2
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "filler"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [],
              "cornerRadius": "30px",
              "height": "12px",
              "width": "12px",
              "borderColor": "#EF454D" if i == 0 else "#6486E3",
              "borderWidth": "2px"
            },
            {
              "type": "filler"
            }
          ],
          "flex": 0
        },
        {
          "type": "text",
          "text": stations[i],
          "gravity": "center",
          "flex": 4,
          "weight": "bold",
          "size": "sm"
        }
      ],
      "spacing": "lg",
      "cornerRadius": "30px",
      "margin": "xl" if i == 0 else "none"
    }
    body_contents.append(station_box)
    
    # 最後の駅以外は間に線とコメントを追加
    if i < len(stations) - 1:
      connection_box = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": spend_times[i],
            "align": "end",
            "gravity": "center",
            "flex": 2,
            "size": "xs",
            "color": "#8c8c8c"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "2px",
                    "backgroundColor": "#B7B7B7" if i < len(stations) - 1 else "#6486E3"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              }
            ],
            "width": "12px",
            "flex": 0
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": platform_nums[2*i],
                "gravity": "center",
                "size": "xs",
                "color": "#5c5c5c"
              },
              {
                "type": "text",
                "text": lines[i],
                "gravity": "center",
                "size": "xs",
                "color": "#8c8c8c"
              },
              {
                "type": "text",
                "text": platform_nums[2*i + 1],
                "gravity": "center",
                "size": "xs",
                "color": "#5c5c5c"
              }
            ],
            "flex": 4,
            "justifyContent": "center"
          }
        ],
        "spacing": "lg",
        "height": "64px"
      }
      separator = {
        "type": "separator"
      }
      body_contents.append(separator)
      body_contents.append(connection_box)
      body_contents.append(separator)
  json_data = json.dumps(json_template, ensure_ascii=False, indent=2)
  return json_template

configuration = Configuration(
  access_token = os.getenv('LINE_ACCESS_TOKEN')
)

print(os.getenv('LINE_ACCESS_TOKEN'))
message_dict = {
  'to': os.getenv('LINE_MY_ADRESS'),
  'messages': [
    {
      'type': 'flex',
      'altText': 'test',
      'contents': route_to('西早稲田','鶴川')
    },
  ]
}

# print(route_to('西早稲田','鶴川'))
# pyperclip.copy(json.dumps(route_to('西早稲田','鶴川'), ensure_ascii=False, indent=2))

with ApiClient(configuration) as api_client:
    # Create an instance of the API class
  api_instance = MessagingApi(api_client)
  push_message_request = PushMessageRequest.from_dict(message_dict)

  try:
    push_message_result = api_instance.push_message_with_http_info(push_message_request, _return_http_data_only=False)
    print(f'The response of MessagingApi->push_message status code => {push_message_result.status_code}')
  except ApiException as e:
    print('Exception when calling MessagingApi->push_message: %s\n' % e)


