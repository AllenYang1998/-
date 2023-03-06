# import pyppeteer
# print(pyppeteer.__chromium_revision__)  # 查看版本号
# print(pyppeteer.executablePath())  # 查看 Chromium 存放路径
import re
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import pandas as pd
import csv

async def main(productID,url,productName,productPrice,productType):
    browser = await launch({'args': ['--no-sandbox'], })
    page = await browser.newPage()
    await stealth(page)
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.setJavaScriptEnabled(enabled=True)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    await page.goto(url)  # 跳转
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
    await asyncio.sleep(1)
    # 点开评论
    await (await page.xpath('//*[@id="detail"]/div[1]/ul/li[5]'))[0].click()
    await (await page.xpath('//*[@id="comm-curr-sku"]'))[0].click()
    await asyncio.sleep(10)

    while(1):
        await asyncio.sleep(1)
        comment_item = await page.xpath('//*[@class="comment-item"]')
        for index, item in enumerate(comment_item[:10], start=1):

            nickname = await item.xpath('./div[@class="user-column"]/div[@class="user-info"]/img')
            nickname = await (await nickname[0].getProperty('alt')).jsonValue()

            conmment = await item.xpath('./div[@class="comment-column J-comment-column"]/p[@class="comment-con"]')
            conmment = await (await conmment[0].getProperty('textContent')).jsonValue()

            star5 = await item.xpath('./div[@class="comment-column J-comment-column"]/div[@class="comment-star star5"]')
            star4 = await item.xpath('./div[@class="comment-column J-comment-column"]/div[@class="comment-star star4"]')
            star3 = await item.xpath('./div[@class="comment-column J-comment-column"]/div[@class="comment-star star3"]')
            star2 = await item.xpath('./div[@class="comment-column J-comment-column"]/div[@class="comment-star star2"]')
            star1 = await item.xpath('./div[@class="comment-column J-comment-column"]/div[@class="comment-star star1"]')
            if len(star5) != 0:
                conmment_type = '好评'
            if len(star4) != 0 or len(star3) != 0 or len(star2) != 0:
                conmment_type = '中评'
            if len(star1) != 0:
                conmment_type = '差评'
            if '此用户未填写评价内容' not in conmment:
                print(nickname,conmment,conmment_type)
            dic = {
                "nickname": nickname,  # 评价人昵称
                "productID": productID,  # 产品ID
                "productName": productName,  # 产品名称
                "productPrice": productPrice,  # 产品价格
                "productType": productType,  # 产品分类
                "conmment": conmment,  # 评价内容
                "conmment_type": conmment_type,
            }
            writer.writerow(dic)
        await asyncio.sleep(5)
        # 判断是否有下一页按钮
        next = await page.xpath('//a[@class="ui-pager-next"]')
        if len(next) != 0:
            await page.click('.ui-pager-next')
        else:
            break
    await browser.close()

dataframe = pd.read_csv('口腔护理产品信息.csv',header=None)
with open(".//口腔护理产品评价.csv", "a", encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f,
                            fieldnames=['nickname','productID',
                                        'productName','productPrice',
                                        'productType','conmment','conmment_type'])
    for index, row in dataframe.iterrows():
        print(row[0],row[1],row[2],row[3],row[4])
        asyncio.get_event_loop().run_until_complete(main(row[0],row[1],row[2],row[3],row[4]))
