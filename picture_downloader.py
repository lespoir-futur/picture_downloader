import requests
import sys
import re
import os
from urllib.parse import urlparse
from urllib.parse import urljoin

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_content(url):
    response = requests.get(url,headers=headers)
    rawData = response.content
    return rawData


url = sys.argv[1]
data = get_content(url).decode('utf-8')
img_tags = re.findall('<img.*?>',data)
img_urls=[]

for img in img_tags:
    src = re.findall('src="(.*?)"',img)
    if src:
        if urlparse(src[0]).scheme == '':
            src[0] = urljoin(url,src[0])
        img_urls.append(src[0])
    
dir = url.split('/')[-1]
os.mkdir(dir)

for img_url in img_urls:
    pic = requests.get(img_url,headers=headers)

    filename = img_url.split('/')[-1]
    filepath = os.path.join(dir,filename)

    with open(filepath,'wb') as f:
        f.write(pic.content)
    
print('saved success!')
