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

info = requests.get("https://atcoder.jp/home?lang=ja")
bs = BeautifulSoup(info.content, "html.parser")

today = bs.find("div", id="contest-table-upcoming")
l = today.find("a").text
tag_a_list = today.select("a")
# val = today.select_one('a')
url = tag_a_list[1].get("href")
tim = tag_a_list[0].text

url = "https://atcoder.jp" + str(url)

message = str(tim[:-8]) + "から\n\n" + tag_a_list[1].text + "\n\n" + url + "\n\n" + "が開催されます。"












configuration = Configuration(
    access_token = os.getenv('LINE_ACCESS_TOKEN')
)

message_dict = {
    'to': os.getenv('LINE_MY_ADRESS'),
    'messages': [
        {
            'type': 'text',
            'text': message
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

