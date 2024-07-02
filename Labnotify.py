from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

configuration = Configuration(
  access_token = os.getenv('LINE_ACCESS_TOKEN')
)
image_file = os.getenv('LAB_IMAGE')

message_dict = {
    'to': os.getenv('LINE_MY_ADRESS'),
    'messages': [
        {
            'type': 'image',
            'originalContentUrl': image_file,
            'previewImageUrl': image_file
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


