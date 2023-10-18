# coding:utf-8
import re
import os
import sys
import random
import requests
from bs4 import BeautifulSoup


def DuiTang(keyword):
    url = 'https://b-ssl.duitang.com/uploads/'
    headers = {'User-Agent': 'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'}

    name = 1  # 记录正在下载的是第几个文件

    # 在当前目录下创建文件夹
    try:
        os.mkdir(r'堆糖下载')
    except Exception:
        pass
    finally:
        os.chdir(r'堆糖下载')

    try:
        page = requests.get(url='https://www.duitang.com/search/?kw=' + keyword + '&type=feed', headers=headers)
        temp = 'https://www.duitang.com/search/?kw=' + keyword + '&type=feed'
        print(temp)
        print(page)

        print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, 'lxml')
        info = soup.find_all('img')[0:]
        print(info)
    except Exception:
        print('可能遇到了一些问题，脚本即将退出运行！')
        sys.exit()

    for tag in info:
        height = tag['height']
        if int(
                height) > 150:  # 因为tag[alt]的时候，在info中有大部分是没有alt=keyword的，是无效的，无法进行筛选。所以选择大家都有的height属性，其中，我们需要的资源都是height比较大的，根据观察一般而言都大于150，据此进行筛选。然后获取里面的tag[src]，
            num = re.search('item.*thumb', tag['src']).group()[:-1]
            pattern = re.search('224_0.*', tag['src']).group()[:-1]  # pattern是为了区分png，jpeg
            # print(pattern)
            if pattern == '224_0.jpe':
                downloadUrl = url + num + 'b.700_0.jpeg'
            else:
                downloadUrl = url + num + 'b.700_0.png'
            print(downloadUrl)
            try:
                document = requests.get(url=downloadUrl, headers=headers)
                filename = str(name) + '.jpeg'
                name = name + 1
                with open(filename, 'wb') as f:
                    f.write(document.content)
                    print('文件 ' + filename + '已下载完成！')
            except Exception:
                print('文件 ' + filename + ' 下载失败并忽略！')
                pass
    print('目前已经爬取到了第' + str(name) + '张！')


if __name__ == '__main__':
    word = input("Input key word: ")
DuiTang(word)
