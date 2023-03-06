import csv
from urllib import parse
import re
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth

async def main(keyword):
    type_name = parse.unquote(keyword)
    browser = await launch({'args': ['--no-sandbox'], })
    page = await browser.newPage()
    await stealth(page)
    await page.setJavaScriptEnabled(enabled=True)
    # 设置UserAgent
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    await page.goto('https://search.jd.com/search?keyword={}&qrst=1&stock=1&psort=3'.format(keyword))  # 跳转
    # 每个产品最多只显示一百页
    for i in range(1,100):
        # 下拉到最底部 加载当前页面所有产品
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        await asyncio.sleep(2) #等待2s加载剩下的产品信息
        # 匹配所有产品Xpath规则
        content = await page.xpath('//ul[@class="gl-warp clearfix"]/li/*[@class="gl-i-wrap"]')
        # 遍历所有产品
        for index,item in enumerate(content,start=1):
            try:
                a = await item.xpath('./*[@class="p-img"]/a')
                em = await item.xpath('./*[@class="p-name p-name-type-2"]/a/em')
                i = await item.xpath('./*[@class="p-price"]/strong/i')
                a1 = await item.xpath('./div[@class="p-commit"]/strong/a')
                item_href = await (await a[0].getProperty('href')).jsonValue()
                item_id = re.findall('https://item.jd.com/(.+?).html', item_href)[0]
                item_name = await (await em[0].getProperty('textContent')).jsonValue()
                item_price = await (await i[0].getProperty('textContent')).jsonValue()
                item_comment_count = await (await a1[0].getProperty('textContent')).jsonValue()
                item_comment_count = item_comment_count.replace('万','0000').replace('+','')
                dic = {
                    "item_id": str(item_id),  # 评价人昵称
                    "item_href": item_href,  # 产品ID
                    "item_name": item_name.strip(),  # 产品名称
                    "item_price": float(item_price),  # 产品价格
                    "type_name": type_name,
                    "item_comment_count": int(item_comment_count),  # 产品分类
                }
                # 写入csv
                writer.writerow(dic)
            except:
                pass
        # 如果当前页满六十个翻下一页
        if len(content) == 60:
            await asyncio.sleep(1)
            await page.click('.pn-next')
        else:
            break
    await browser.close()


# 产品信息列表
serach = ['超声波洁牙仪','电动牙刷','冲牙器']
with open('.//口腔护理产品信息.csv'.format(''.join(serach)), "a", encoding="utf-8", newline='') as f:
    # 设置表头
    writer = csv.DictWriter(f, fieldnames=['item_id','item_href','item_name','item_price','type_name','item_comment_count'])
    for s in serach:
        keyword = parse.quote(s)
        asyncio.get_event_loop().run_until_complete(main(keyword))
