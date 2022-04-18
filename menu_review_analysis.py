# Naver Open Api

import os
import sys
import urllib.request
import pandas as pd
import json
import re

client_id = "GisFsSEvBKY8PJtxjcUq"
client_secret = "AdwdEYrjE0"

query = urllib.parse.quote(input("product_name: "))
idx = 0
display = 100
start = 1
end = 1000

web_df = pd.DataFrame(columns=("bloggername", "description"))

for start_index in range(start, end, display):

  url = "https://openapi.naver.com/v1/search/blog?query=" + query \
        + "&display=" + str(display) \
        + "&start=" + str(start_index)

  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  response = urllib.request.urlopen(request)
  rescode = response.getcode()

  if(rescode==200):
      response_body = response.read()
      response_dict = json.loads(response_body.decode('utf-8'))
      items = response_dict['items']
      for item_index in range(0, len(items)):
        remove_tag = re.compile('<.*?>')
        bloggername = re.sub(remove_tag, '', items[item_index]['bloggername'])
        description = re.sub(remove_tag, '', items[item_index]['description'])
        web_df.loc[idx] = [bloggername, description]
        idx += 1
  else:
      print("Error Code:" + rescode)

web_df

reviews = web_df['description'].values.tolist()

# 한국어 토크나이저 설치 코드

import os
import tensorflow as tf

path_mecab_zip = tf.keras.utils.get_file(
    'mecab-0.996-ko-0.9.2.tar.gz', origin='https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz',
    extract=True)

path_mecab_dic_zip = tf.keras.utils.get_file(
    'mecab-ko-dic-2.1.1-20180720.tar.gz', origin='https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz',
    extract=True)

os.chdir(os.path.join(os.path.dirname(path_mecab_zip),'mecab-0.996-ko-0.9.2/'))
!./configure
!make
!make check
!sudo make install

os.chdir(os.path.join(os.path.dirname(path_mecab_zip), 'mecab-ko-dic-2.1.1-20180720/'))
!sudo ldconfig
!ldconfig -p | grep /usr/local
!./configure
!make
!sudo make install

!pip install mecab-python3
!apt-get update
!apt-get install g++ openjdk-8-jdk python-dev python3
!pip3 install JPype1-py3
!pip3 install konlpy
!JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
%cd /content/

from konlpy.tag import Mecab, Kkma, Komoran, Hannanum, Okt

tokenizer = Mecab()

for review in reviews:
   tokenized = tokenizer.morphs(review)
   print(f"origin review: {review}")
   print(f"tokenized review: {tokenized}")
   print("")

from konlpy.tag import Mecab, Kkma, Komoran, Hannanum, Okt

tokenizer = Mecab()

bag_of_words = {}
for review in reviews:
  if not isinstance(review, str):
    continue
  tokens = tokenizer.morphs(review)

  for token in tokens:
    if token not in bag_of_words:
      bag_of_words[token] = 0
    bag_of_words[token] += 1
bag_of_words

!pip install wordcloud
!apt-get update -qq
!apt-get install fonts-nanum* -qq

import os

# 한글 폰트의 경로 확인
path_font = '/usr/share/fonts/truetype/nanum/'
os.listdir(path_font)

import matplotlib.pyplot as plt
from wordcloud import WordCloud

nanum_gothic = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
wordcloud = WordCloud(font_path=nanum_gothic)
image = wordcloud.generate_from_frequencies(bag_of_words)
plt.imshow(image, interpolation='bilinear')
plt.axis("off")

bag_of_words = {}
for review in reviews:
    if not isinstance(review, str):
        continue
    tokens = tokenizer.pos(review)
    for token, pos in tokens:
        # 단어의 형태소가 체언이 아닌 경우 제외
        # 길이가 2보다 작을 경우 제외
        if (not pos.startswith("N")) or (len(token) < 2):
            continue
        if token not in bag_of_words:
            bag_of_words[token] = 0
        bag_of_words[token]+=1
bag_of_words

import matplotlib.pyplot as plt
from wordcloud import WordCloud

nanum_gothic = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

stopwords = ["펀치", "그래피티", "블렌디드", "후기", "렌디", "스타", "벅스", "스타벅스"]
for stopword in stopwords:
    if stopword in bag_of_words:
        del bag_of_words[stopword]

wordcloud = WordCloud(font_path=nanum_gothic).generate_from_frequencies(bag_of_words)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")