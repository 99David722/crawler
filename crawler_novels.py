from bs4 import BeautifulSoup
import requests
import os


# 抓取所有章节目录
def get_novel_chapter():
    root_usl = 'https://www.xxbiqudu.com/5_5354/'
    r = requests.get(root_usl)
    if r.status_code != 200:
        raise Exception("error")
    root_html = r.text
    soup = BeautifulSoup(root_html, 'html.parser')
    data = []
    for dd in soup.find_all("dd"):
        charpters = dd.find_all("a")[0]
        if not charpters:
            continue
        data.append([charpters['href'], charpters.get_text()])
    return data


# 抓取每个章节内容
def get_novel_content(usl):
    html = requests.get(usl).text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find("div", class_="content_read")
    content = links.find("div", id="content").get_text()
    return content


# 创建目录
def createDir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print("该文件已存在")
    except:
        print("创建失败！")


datas = get_novel_chapter()
createDir("novels/龙王传说")
contents = ""
# 数据切片，从小说第一章开始
datas = datas[9:]
# 进度所需参数初始化
total = len(datas)
progress = 1
for data in datas:
    per = progress / total
    progress += 1
    usl, title = data
    # 将小说分段
    content = get_novel_content(usl).replace("　　", '\n       ')
    # 将小说不同章节拼接到一个文本文件中
    contents = contents + "\n%s\n" % title + content
    with open("novels/龙王传说/龙王.txt", "w", encoding='utf-8') as fout:
        fout.write(contents)
    # 进度展示
    if progress % 10 == 0:
        print("以及加载到第%d章，" % (progress - 1) + "加载进度为%.4f%%" % (per * 100.))
    if progress == total:
        print("加载完成！")
