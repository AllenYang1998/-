import wordcloud
import numpy as np
import pandas as pd
from PIL import Image  # Image模块是在Python PIL图像处理常用的模块
import jieba
from wordcloud import WordCloud,STOPWORDS
# 设置停用词
stopwords_file = open('cn_stopwords.txt', 'r', encoding='utf-8')
stopwords = [words.strip() for words in stopwords_file.readlines()]

# 设置停用词
csv_file = '产品信息.csv'
try:
    dataframe = pd.read_csv(csv_file,encoding='gbk')
except:
    dataframe = pd.read_csv(csv_file, encoding='utf-8')
print(dataframe)
type_list = dataframe['产品分类'].value_counts()
pic = Image.open("tooth.jpg")  # 打开图片路径，形成轮廓
shape = np.array(pic)  # 图像轮廓转换为数组
for type in dict(type_list):
    df = dataframe[dataframe['产品分类'] == type]
    text = '\n'.join(list(df['产品名称']))
    print(text)
    wc = wordcloud.WordCloud(
        mask=shape,
        font_path="simkai.ttf", background_color="white",
        max_font_size=100,
        stopwords=stopwords, width=1920, height=1080, scale=4)  # mask为图片背景，font_path为字体，若不设置可能乱码
    cut_text = jieba.cut(text)
    result = " ".join(cut_text)
    wc.generate(result)
    wc.to_file("./各产品词云1/{}.jpg".format(type.replace('/','')))