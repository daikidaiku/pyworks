import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

path = os.getenv('DATA_PATH')
print(path)
# df = pd.read_csv(path,encoding="shift-jis")
# print(df)
# force = l(1,2)
# data = df.iloc[1:,0:3]
# stroke = data.iloc[0:,2]
# force = data.iloc[0:,1]
# plt.clf()
# plt.plot(stroke,force)


x = np.linspace(0, 10, 100)
y = x + np.random.randn(100) 
plt.clf()
plt.plot(x, y, label="test")
