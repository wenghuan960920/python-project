from queue import Queue
from thread import CrawlThread


def scope_search(url, depth, max_thread):
    threadpool = []
    if depth == 0:
        return False
    else:
        print('进入爬虫')
        now_depth = 1
        print(url)
        th = CrawlThread(url)
        th.setDaemon(True)
        th.start()
        th.join()
        url_queue = Queue()
        print(f'创建队列成功：{url_queue}')
        url_links = th.get_datas()
        print(f'获取到未下载资源的数据：{url_links}')
        for url in url_links:
            url_queue.put(url)

        while now_depth < int(depth) and url_queue:
            print('进入到爬虫循环')
            now_depth = now_depth + 1
            print('爬虫深度：=====================', now_depth)
            tmp_links = []
            while url_queue.empty() is not True: #每爬取一个深度后停止爬取，
                i = 0
                j = 0
                #直到此层爬取完毕。
                print(f'队列中的url是：=================={url_queue.qsize()}')
                while len(threadpool) < int(max_thread):
                    i = i + 1
                    if url_queue.empty() is not True:
                        t = CrawlThread(url_queue.get())
                        print(f'爬取到的第{now_depth}层第{i}===========个url')
                        t.setDaemon(True)
                        threadpool.append(t)
                        t.start()
                        print(f'第{now_depth}层{i}次线程开始了')
                    else:
                        break

                for thread in threadpool:     #等待线程结束
                    j = j + 1
                    thread.join()
                    tmp = thread.get_datas()#取出线程数据
                    url_queue.task_done()
                    if tmp:
                        tmp_links.extend(tmp)

            threadpool = []  #在进行完一次深度数据采集后所做的操作
            url_queue.join()  #一次数据采集完成，queue不再阻塞
            print(f'第{now_depth}层某个URL终结了')
            if tmp_links is not True:
                url_queue = []
            else:
                url_list = list(set(tmp_links))
                for url in url_list:
                    url_queue.put(url)
        return True