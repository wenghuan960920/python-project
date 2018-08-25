from urllib import parse, request
import threading
from bs4 import BeautifulSoup
import requests


dead_url = []
crawled_url = []
mutex = threading.Lock()


class CrawlThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.linklist = []
        self.img_url = []

    def url_status(self, url):
        try:
            status = request.urlopen(url)
            if status.code == 200:
                return True
            else:
                dead_url.append(url)
                return False
        except:
            return False

    def judge_domain(self, testlink):
        if parse.urlparse(testlink).netloc == '':
            return False
        else:
            return True

    def get_html(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except:
            print('请求页面时出错')
            return None

    def get_url_a(self, soup):
        url_a = soup.find_all('a')
        return url_a

    def get_url_img(self, soup):
        url_img = soup.find_all('img')
        return url_img

    def get_herf(self, url_a):
        herf_list = []  # 存放正常的链接
        bad_links = {None, '', '#', ' '}  # 无用链接列表
        bad_protocol = {'javascript', 'mailto', 'tel', 'telnet'}  # 无用的头部协议，如javas
        for link in url_a:
            if link.get('href') in bad_links or link.get('href').split(':')[0] in bad_protocol:#去除无用链接
                continue
            else:
                herf_list.append(link.get('href'))
        herf_list = [str for str in herf_list if str not in ['', ' ', None]]
        return herf_list

    def get_src(self, url_img):
        img_list = []  # 存放正常的链接
        for link in url_img:
            if link.get('src'):
                img_list.append(link.get('src'))
            elif link.get('data-src'):
                img_list.append(link.get('data-src'))
        img_list = [str for str in img_list if str not in ['', ' ', None]]
        return img_list

    def get_long_url(self, url):
        linklist_tmp = []
        right_protocol = {'http', 'https'}#存放正确的协议头部
        for link in url:
            if self.judge_domain(link):
                link_temp = parse.urljoin(self.url, link)
                linklist_tmp.append(link_temp)
            elif link.split(':')[0] in right_protocol:
                linklist_tmp.append(link)
        return linklist_tmp

    def life_judge(self, url_list):
        tmplinks = []
        if url_list:
            for link in url_list:
                if self.url_status(link) and link not in crawled_url: #url存活性判断，去除死链
                    tmplinks.append(link)
                    mutex.acquire()
                    crawled_url.append(link)
                    mutex.release()
            return tmplinks
        else:
            return None

    def url_judge_kind(self, url_a_0):
        for url in url_a_0:
            sign = url.split('.')[-1]
            if sign in ['gif', 'jpg', 'png', 'jpeg']:
                self.img_url.append(url)
            else:
                self.linklist.append(url)

    def url_set(self, url_list):
        url_list = list(set(url_list) - set(crawled_url))
        return url_list

    def get_url(self):
        soup = self.get_html(self.url)
        url_a = self.get_url_a(soup)
        link_herf = self.get_herf(url_a)
        long_url = self.get_long_url(link_herf)
        set_url = self.url_set(long_url)
        life_url = self.life_judge(set_url)
        try:
            self.url_judge_kind(life_url)
        except:
            pass

    def run(self):
        self.get_url()
        self.get_img()
        self.down_img()

    def get_datas(self):
        return self.linklist

    def url_img_add(self, urls):
        for url in urls:
            if url is not None:
                self.img_url.append(url)

    def get_img(self):
        soup = self.get_html(self.url)
        url_img = self.get_url_img(soup)
        src_list = self.get_src(url_img)
        long_url_list = self.get_long_url(src_list)
        link_set = self.url_set(long_url_list)
        link_life = self.life_judge(link_set)
        try:
            self.url_img_add(link_life)
        except:
            pass
        return self.linklist


    def down_img(self):
        i = 0
        print(f'下载第i次：{self.img_url}')
        for url in self.img_url:
            url_sign = url.split('.')[-1]
            try:
                    with open(rf'./img/{url_sign}/'+str(i) + f".{url_sign}", "wb") as fd:
                        response = requests.get(url)
                        fd.write(response.content)
                    i += 1
            except:
                pass
        print('第i次下载完成')