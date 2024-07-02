import cv2
import sys
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

camera_id = 0
delay = 1
window_name = 'frame'

cap = cv2.VideoCapture(camera_id)

if not cap.isOpened():
    sys.exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
# print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
ret, frame = cap.read()
cv2.imwrite(os.getenv('LAB_IMAGE_PATH'), frame)

cap.release()