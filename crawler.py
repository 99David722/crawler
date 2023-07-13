import requests
import selenium
from bs4 import BeautifulSoup
import pandas as pd
import pprint


# 下载网页html
def download_all():
    # 下载网页的HTML
    htmls = []
    for page in page_index:
        url = f"https://movie.douban.com/top250?start={page}&filter="
        print("爬取的网页：", url)
        r = requests.get(url, headers=header)
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    return htmls


# 解析单个html，得到数据
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 每部电影按照item的区域划分
    links = soup.find("div", class_="article") \
        .find("ol", class_="grid_view") \
        .find_all("div", class_="item")
    datas = []
    for link in links:
        title = link.find("span", class_="title").get_text()
        rank = link.find("em", class_='').get_text()
        star = link.find("div", class_="star").find_all("span")  # 等级列表
        rank_star = star[0]["class"][0]  # 星级
        rank_num = star[1].get_text()  # 分数
        comments = star[3].get_text()  # 评论人数
        datas.append(({"title": title,
                       "rank": rank,
                       "星级": rank_star.replace("rating", "")\
                       .replace("-t", "").replace("45", "4.5"),
                       "评分": rank_num,
                       "评论人数": comments}))
    return datas


if __name__ == "__main__":
    # 初始化信息
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"}

    # 构造分页数字列表
    page_index = range(0, 250, 25)
    htmls = download_all()
    all_datas = []
    # 对每一个网页进行分析
    for html in htmls:
        parse_html(html)
        all_datas.extend(parse_html(html))
    # 输出为excel
    df = pd.DataFrame(all_datas)
    df.to_excel("豆瓣电影TOP250.xlsx")
    print("解析完成")
