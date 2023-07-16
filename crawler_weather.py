import requests
import pandas as pd

header = {
    "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"""}


# 提取指定年份和月份的数据
def craw_table(year, month):
    url = """https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D\
            =54511&areaInfo%5BareaType%5D\
            =2&date%5Byear%5D=""" + """%d""" % year + \
          """&date%5Bmonth%5D=""" + """%d""" % month
    r = requests.get(url, headers=header)
    r.encoding = r.apparent_encoding
    r_data = r.json()['data']
    data = pd.read_html(r_data)[0]
    return data


data_list = []
for year in range(2012, 2023):
    for month in range(1, 12):
        data = craw_table(year, month)
        data_list.append(data)
        print("正在爬取的时间：" + "%d年" % year + "%d月" % month)
# 输出保存为excel格式
pd.concat(data_list).to_excel("北京近十年天气情况.xlsx", index=False)

