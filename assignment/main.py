from io import StringIO
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

url="https://www.hko.gov.hk/tide/eCLKtext2024.html"
response = requests.get(url)

if response.ok:
    print("Data is ready")

    soup = bs(response.text, 'html.parser')
    table = soup.find('table')

type(table)

table_str = str(table)

table_io = StringIO(table_str)

df = pd.read_html(table_io, header=1)[0]

df=df.values
print(df)
year = int(2024)

data = []

for row in df:
    # 只保留前三列
    month, day, value = row[:3] #数据切片
    month=int(month)
    day=int(day)
    datetime = f"{year}-{month:02d}-{day:02d}"
    data.append((datetime, value))



df = pd.DataFrame(data, columns=['Date', 'Value'])


df['Date'] = pd.to_datetime(df['Date'])
df['Value'] = df['Value'].astype(float)

print(df)

fig, ax = plt.subplots(figsize=(10, 5))

fig.patch.set_facecolor('black')
ax.set_facecolor('black')


ax.plot(df['Date'], df['Value'], marker='o', linestyle=':', color='#FFC0CB', linewidth=3)

ax.set_title('ASSIGNMENT01', fontsize=20, color='white')
ax.set_xlabel('Date', fontsize=10, color='white')
ax.set_ylabel('Value', fontsize=10, color='white')

ax.grid(True, which='both', linestyle='--', linewidth=1, color='white')

ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=2))

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

plt.show()


