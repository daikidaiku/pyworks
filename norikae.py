'''
現在時刻から直近の乗換案内を検索して、到着時間を表示する
Yahoo乗換から到着時間をスクレイピングで抽出している
'''
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse # URLエンコード、デコード
import json
import requests

startsta = '西早稲田' # 出発駅
endsta = '鶴川' # 到着駅

startstaen = urllib.parse.quote(startsta) # encode
endstaen = urllib.parse.quote(endsta) # encode

url0 = 'https://transit.yahoo.co.jp/search/result?from='
url1 = '&flatlon=&to='
url2 = '&viacode=&viacode=&viacode=&shin=&ex=&hb=&al=&lb=&sr=&type=1&ws=3&s=&ei=&fl=1&tl=3&expkind=1&ticket=ic&mtf=1&userpass=0&detour_id=&fromgid=&togid=&kw='

url = url0 + startstaen + url1 + endstaen + url2 + endstaen
# print(url)
req = requests.get(url)

soup = BeautifulSoup(req.content, 'html.parser')
# print(soup)

detail = soup.find(class_="routeDetail")
# times = detail.find_all(class_="time")
times = []
tms = detail.select("ul.time")
for i in tms:
  times.append(i.text)
print(times)

stat = detail.find_all("dt")
stations = []
for i in stat:
  if i.find("a"):
    stations.append(i.find("a").text)
print(stations)

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
            "flex": 4,
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
            "flex": 4,
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
        "text": "Total: 1 hour",
        "color": "#b7b7b7",
        "size": "xs"
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
            "text": times[i],
            "size": "sm",
            "gravity": "center"
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
          "type": "box",
          "layout": "baseline",
          "contents": [
              {
                  "type": "filler"
              }
          ],
          "flex": 1
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
          "width": "12px"
        },
        {
          "type": "text",
          "text": "Metro 1hr",
          "gravity": "center",
          "flex": 4,
          "size": "xs",
          "color": "#8c8c8c"
        }
      ],
      "spacing": "lg",
      "height": "64px"
    }
    body_contents.append(connection_box)

# JSONデータをフォーマット
json_data = json.dumps(json_template, ensure_ascii=False, indent=2)

# 結果を表示
print(json_data)
