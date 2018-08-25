from breadth_crawler import scope_search
from configs import strip
from pic import win
from download_pc import spiderPic
from pattern_img import pic_model


def main():
    win()
    spiderPic()
    search_sign = scope_search(**(strip['com_url']))
    pic_model()
    if search_sign:
        print('成功展示')
    else:
        print('下载失败')


if __name__ == '__main__':
    main()



