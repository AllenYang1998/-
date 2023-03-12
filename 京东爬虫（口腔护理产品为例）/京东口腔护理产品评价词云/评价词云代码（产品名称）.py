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
        font_path="simkai.ttf", background_color="white", max_words=50, prefer_horizontal=1.0,
        max_font_size=100, width=1920, height=1080, scale=4)  # mask为图片背景，font_path为字体，若不设置可能乱码
    cut_text = jieba.lcut(text)
    word_count = {}
    # 统计词频
    for word in [word.strip() for word in cut_text]:
        # 去停用词
        if word not in stopwords:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    # generate_from_frequencies根据词频生成词云图
    wc.generate_from_frequencies(word_count)
    # 保村词云图
    wc.to_file("./各产品词云(名称)/{}.jpg".format(type.replace('/', '')))
    # 词频排序
    word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    print(word_count)
    # 保存排序后词频txt文件
    with open("./各产品词云(名称)/{}.txt".format(type.replace('/', '')), 'w',encoding='utf-8') as f:
        for i in word_count:
            f.writelines(i[0] + ":" + str(i[1]) + '\n')