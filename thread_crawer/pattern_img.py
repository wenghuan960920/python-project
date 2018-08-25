# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def fix_pic(file_list, file_name):
    print(f'进入到fix——pic')
    i = 0
    mw = 133  # 图片大小+图片间隔
    ms = 5
    msize = mw * ms  # 大小
    toImage = Image.new('RGB', (msize, msize))
    for y in range(1, 6):  ## 先试一下 拼一个5*5 的图片
        for x in range(1, 6):
            i = i+1
            fromImage = file_list[i]
            # fromImage =fromImage.resize((mw, mw), Image.ANTIALIAS)   # 先拼的图片不多，不用缩小
            toImage.paste(fromImage, ((x - 1) * mw, (y - 1) * mw))
    file_name = file_name.split('/')[-1]
    toImage.save(rf'./img/new/fix_pic/fix_pic.{file_name}')
    toImage.show()


#图片模糊
def blur(file_list, file_name):
    blur_list = []
    files = os.listdir(file_name)
    for i, img in enumerate(file_list):
        print('对图片虚化')
        img = img.filter(ImageFilter.BLUR)
        fm = files[0].split('.')[-1]
        print(f'fm:{fm}')
        img.save(f'./img/new/blur/blur.{fm}')
        blur_list.append(img)
        return blur_list


#图片重叠
def cover(img1, img2, img_name):
    r, g, alpha = img2.split()
    alpha = alpha.point(lambda i: i > 0 and 100)#此处参数可调节背景图片的深度
    img = Image.composite(img2, img1, alpha)
    img.show()
    img1_name = img_name.split('.')
    img.save(f"./img/new/cover/{img1_name[0]}.{img1_name[1]}")
    print(img_name)
    return


def black(file_list):
    for file in file_list:
        file = file.convert('1')
        file.show()
        file.save('./img/new/black/black.png')


#加文字====》对new图片
def set_water_text(directory,imagefile, text): #文件名和文字
    img = Image.open(f'{directory}/{imagefile}')
    img = img.convert('RGB')
    img = img.resize((400, 400))
    (img_x, img_y) = img.size
    # 文字字体像素高度为图片高度的 1/20
    ttfont = ImageFont.truetype('C:/Windows/Fonts/simsun.ttc', int(img_y / 20))
    draw = ImageDraw.Draw(img)
    draw.text((int(img_x / 20), img_y - int((img_y * 1.3) / 20)), text, (0, 0, 0), font=ttfont)
    # if not os.path.exists(newdir):
    #     os.mkdir(newdir)
    img.save(rf'./img/new/pwd/{imagefile}')
    img.show()


def pwd(directory):
    print(f'进入到pwd:{directory}')
    files = os.listdir(directory)
    print(f'{files}')
    for filename in files:
        if 'jpg' == filename.split('.')[-1] or 'png' == filename.split('.')[-1]:
            set_water_text(directory, filename, filename.split('_')[0])


def file_list(directory):
    files = os.listdir(directory)
    file_list = []
    for filename in files:
        try:
            img = Image.open(rf'{directory}/{filename}')
        except:
            continue
        img = img.convert('RGB')
        img = img.resize((400, 400))
        img.save(rf'{directory}/{filename}')
        file_list.append(img)
    return file_list


def pic_model():
    file_name_list = ['./img/jpg', './img/png', './img/jpeg', './img/pa/jpg']
    for file_name in file_name_list:
        file_list1 = file_list(file_name)
        print(f'file_name:{file_name}')
        fix_pic(file_list1, file_name)
    file_list1 = file_list('./img/new/fix_pic')
    blur_list = blur(file_list1, './img/new/fix_pic')
    file_list2 = file_list('./img/pa/jpg')
    file_list2_name = os.listdir('./img/pa/jpg')
    print(file_list2_name)
    file_list3 = file_list('./img/jpeg')
    for i, file_name in enumerate(blur_list):
        print(f'i:{i}')
        print(file_list2_name[i])
        cover(file_list2[i], file_name, file_list2_name[i])
    pwd('./img/new/cover')
    black(file_list3)


