import re  # 导入正则表达式模块
import requests  # python HTTP客户端 编写爬虫和测试服务器经常用到的模块
from configs import par_url


def spiderPic():
    result = requests.get(par_url['pa_url']+par_url['word'])
    print(par_url['pa_url']+par_url['word'])
    html = result.text
    keyword = par_url['word']
    i = 0
    print('正在查找 ' + keyword + ' 对应的图片,下载中，请稍后......')
    for addr in re.findall('"objURL":"(.*?)"', html, re.S):  # 查找URL
        print('正在爬取URL地址：' + str(addr)[0:30] + '...')  # 爬取的地址长度超过30时，用'...'代替后面的内容
        try:
            pics = requests.get(addr, timeout=10)  # 请求URL时间（最大10秒）
        # except requests.exceptions.ConnectionError:
        except:
            print('您当前请求的URL地址出现错误')
            continue

        i = i + 1
        fq = open(rf'./img/pa/jpg/{keyword}_{i}.jpg', 'wb')  # 下载图片，并保存和命名
        fq.write(pics.content)
        fq.close()

