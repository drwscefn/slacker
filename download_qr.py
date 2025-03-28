import requests
import os
import re

with open('files.txt', 'r') as file:
    content = file.read()
    urls = re.findall(r'https://[^"\s]+', content)

os.makedirs('from_slack', exist_ok=True)

for num, url in enumerate(urls, 0):
    response = requests.get(url)
    filename = f'from_slack/image_{num:03}.png'
    with open(filename, 'wb') as file:
        file.write(response.content)
