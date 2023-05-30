#pypi.douban.com/simple镜像下载selenium
#https://npmmirror.com/
#https://vikyd.github.io/download-chromium-history-version/#/ 找一个版本，下载chromium和对应的chromdriver，放到项目下
import os

from lxml import etree
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC #等到加载完

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait #对付js动态加载的情况
from selenium.webdriver.edge.service import Service #DeprecationWarning新路径写法
import time
import re
import concurrent.futures #多线程并行爬取

# 针对window文件夹命名规则，将不支持的符号替换为_
def replace_forbidden_symbols(input_string):
    # 定义正则表达式
    pattern = r'[\\/:*?"<>|]'
    # 将不支持的符号替换成下划线_
    output_string = re.sub(pattern, '_', input_string)
    return output_string


def download_mp4(url,num,name,savepath):
    url = url
    temp_name = str(num)+'_'+name+'.mp4'
    # 处理转义错误file or directory: 'A:\\yourpath\\save_path_test\\9871_K/DA.mp4'
    # if "/" in filename:
        # filename = filename.replace("/", "_")#.replace("*", "_") #可连写
        # filename = filename.replace('*', '_')#.replace('/', '_') #不太管用
        # filename = re.sub('[/]', '_', filename)
    # 测试
    filename = replace_forbidden_symbols(temp_name)
    print(filename)

    folder_path = savepath  # 指定文件夹路径

    response = requests.get(url)
    if response.status_code == 200:
        # with open(folder_path + '/' + filename, 'wb') as f:
        with open(os.path.join(folder_path, filename), 'wb') as f:
            f.write(response.content)
            print("视频已下载到指定文件夹。")
    else:
        print("下载失败。")


def main(path):
    #=========chrome配置======指定调用某个地方的chrome
    options = webdriver.ChromeOptions()
    #=============================================

    #=========增加隐蔽性============================
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')

    #add_argument对浏览器使用什么命令


    #-----------手机端防御弱一些
    # mobileEmulation = {'deviceName': 'iPhone 8'}
    # options.add_experimental_option("mobileEmulation",mobileEmulation)

    #----------代理http https sock4 sock5-------------------------------
    # options.add_argument('--proxy-server=%s'%'sock5://127.0.0.1:10808')

    #-----------更改浏览器语言--假装国外-----------
    options.add_argument("--lang=en-US")


    #=========资源优化=========静默模式:不跳出浏览器操作
    options.add_argument("headless")

    # options = webdriver.EdgeOptions()
    #chromium浏览器的主程序位置
    # location = r"A:\PythonEnvironment\Pycharm_location_projects\Myprojects\pachong\chrome-win\chrome.exe"
    # #在options增加读取位置
    # options.binary_location = location
    # driver = webdriver.Chrome("A:\PythonEnvironment\Pycharm_location_projects\Myprojects\pachong\chromedriver_win32\chromedriver.exe",options=options)
    #====================提示“executable_path”已被弃用，建议使用一个Service对象来传递驱动程序路径。参考如下：

    # # 创建一个Service对象
    service = Service('A:\PythonEnvironment\Pycharm_location_projects\Myprojects\pachong\chromedriver_win32\chromedriver.exe')
    # 创建一个EdgeOptions对象，并设置一些选项
    # options.add_argument('--start-maximized') #最大化
    options.service = service


    driver = webdriver.Chrome(options=options)

    # url = Aimurl
    # for i in range(1004, 200000):
    for i in range(360000, 380000): #平均一个2MB，一半出货率就是1GB
        # url = 'https://wp.cheetahfun.com/personal/wallpaper?dwid={+'+str(i)+'}'.format(i)
        url = 'https://wp.cheetahfun.com/personal/wallpaper?dwid='+str(i)
        print("正在爬取第" + str(i) + "页")
        # time.sleep(1)
        driver.get(url)

        # driver.get("https://wp.cheetahfun.com/personal/wallpaper?dwid=1004")
        #chromium与chrome区别，除了看视频和直播之外都一模一样，内核没有解码器

        # print(driver.get_cookie()) #获取当前cookie
        # driver.find_element_by_xpath("//button[@class='banner_btn']").click #找到按钮
        # driver.find_element_by_id("j-input").send_keys("蜡笔")  # 根据id方法找到名为j-input的搜索框，输入关键词蜡笔搜索
        # print(driver.current_url) #获取当前页面地址（尚未切换标签情况）
        # print(driver.page_source) #获取页面源码
        # time.sleep(2)
        # driver.refresh() #刷新页面，抢票

        # title = driver.find_element_by_xpath("//h1").text
        # video = driver.find_element_by_xpath("//div[@class='bd']/video/@src").text #旧版本selenium-4.4.2写法
        # title = driver.find_element(By.XPATH, "//h1").text #新版写法
        # video = driver.find_element(By.XPATH,"//div[@class='bd']/video/@src").text

        #=============等待元素出现并筛选目标元素================
        wait = WebDriverWait(driver, 3)
        # element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
        # 等待直到页面中显示想要的元素（解决js加载问题，比第一种好）
        title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1")))
        # video = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='bd']/video/@src"))) #报错，xpath语法本身不支持选择属性，只是浏览器插件中可以
        try:
            video = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='bd']/video")))
        except Exception: #通用的exception捕获所有异常
            print("元素超时："+str(url))
            continue
        else:
        # print(title.text)
        # print(video.get_attribute('src'))
            url = video.get_attribute('src')
        if url == '':
            print("该页面未发现视频下载链接,已自动跳过")
            continue
        else:
            print("现在开始爬取"+url)
            # title = url.split('/')[-1]
            title = title.text

            #--------------键盘按键包，有时候不是post和get，需要模拟键盘打字，也是反爬处理--------
            # driver.find_element(By.ID,"j-input").send_keys("这是模拟在input输入框中打字")
            # driver.find_element(By.ID,"j-input").send_keys(Keys)


            #===========下载目标===========================
            print("视频下载链接："+str(url))
            download_mp4(url,i,title,path)


    time.sleep(5)#程序暂停执行，浏览器窗口停留60s
    driver.quit() #不关闭会残留进程
    pass






if __name__ == '__main__':

    # GoalUrl = input("输入爬取目标url：")
    # save_path=input("输入保存路径：")
    # save_path='A:\yourpath\save_path'
    save_path='E:\save_path'
    main(save_path)

    print("全部爬取完毕")





