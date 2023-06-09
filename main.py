import requests as rq
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass
from tqdm import tqdm
from pprint import pprint


@dataclass
class Property:
    name: str                # 道具名字
    pic: str                 # 图片链接
    propType: str            # 道具类型
    propQuality: str         # 道具品质
    propSource: str          # 道具来源


url = 'https://wiki.biligame.com/reverse1999/%E9%81%93%E5%85%B7%E5%9B%BE%E9%89%B4'

t = rq.get(url).text

soup = BeautifulSoup(t, "html.parser")

divs = list(soup.find("div", class_="resp-tab-content", style="display: block"))


props = []
for div in tqdm(divs):
    a = div.findNext("a")

    href = "https://wiki.biligame.com" + a.get("href")
    name = a.get("title")
    img = a.find("img")
    # 跳过部分没有图片的图鉴
    if not img:
        continue
    pic = img.get("src")

    p = rq.get(href)
    s = BeautifulSoup(p.text, "html.parser")

    trs = s.find_all("tr")

    propType = trs[3].findNext("td", style="width:30%").text.replace("\n", '')
    # print(propType)
    if propType != "养成材料":
        continue
    # print(trs[4])
    propQuality = trs[4].findNext("td", colspan="3").text.replace("\n", '')
    # print(propQuality)
    propSource = trs[7].findNext("td", colspan="3").text.replace("\n", '')

    prop = Property(name=name, pic=pic,
                    propQuality=propQuality,
                    propSource=propSource,
                    propType=propType)
    props.append(prop)
    # print(prop)
    # break

# pprint(props)

