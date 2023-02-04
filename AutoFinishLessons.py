from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
from tkinter import *
import tkinter as tk

root = Tk()  # 创建主窗口
root.title("AutoFinishLessons    By AnyMoonS")


def center_window(root, width, height):  # 窗口居中函数
    screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
    screenheight = root.winfo_screenheight()  # 获取显示屏高度
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
    root.geometry(size)  # 让窗口居中显示


center_window(root, 360, 240)
root.resizable(0, 0)

Label(root, text='智慧树账号（手机号）：').grid(row=0, column=0, padx=10, pady=30)
Label(root, text='智慧树密码：').grid(row=1, column=0, padx=0, pady=0)

userid = tk.StringVar()  # 创建账号与密码变量
password = tk.StringVar()

entryuserid = tk.Entry(root, textvariable=userid).grid(row=0, column=1, padx=0, pady=30)
entrypassword = tk.Entry(root, textvariable=password, show='*').grid(row=1, column=1, padx=0, pady=10)

Button(root, text='登录', width=10, command=root.destroy).grid(row=2, column=1, sticky=W, padx=0, pady=30)  # 登录

root.mainloop()  # 主窗口进入循环

driver = webdriver.Firefox()
actions = ActionChains(driver)
driver.get("https://onlineweb.zhihuishu.com/")  # 打开智慧树官网
driver.maximize_window()
time.sleep(2)


def login():
    luserid = userid.get()
    lpassword = password.get()
    phonenumber = driver.find_element(By.ID, "lUsername")
    pw = driver.find_element(By.ID, "lPassword")
    loginbutton = driver.find_element(By.CLASS_NAME, "wall-sub-btn")
    phonenumber.send_keys(luserid)
    pw.send_keys(lpassword)
    loginbutton.click()


def lesson():
    while 1:
        if driver.current_url.__contains__("studyvideoh5"):  # 检测打开视频播放页
            time.sleep(10)  # 等待手动关闭弹窗
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位视频窗口
            video.click()  # 播放视频
            try:
                ActionChains(driver).move_to_element(video).perform()
                speedbox = driver.find_element(By.CLASS_NAME, "speedBox")
                speedbox.click()
                time.sleep(1)
                speedtab15 = driver.find_element(By.CLASS_NAME, "speedTab15")  # 1.5倍播放
                speedtab15.click()
                break
            except:
                pass


def test():
    while 1:
        try:
            question = driver.find_element(By.CLASS_NAME, "topic-item")  # 找到第一个选项
            question.click()
            time.sleep(1)
            close = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[6]/div/div[3]/span/div")  # 关闭答题界面
            close.click()
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
            video.click()
        except:
            pass
        time.sleep(10)


def videoend():
    while 1:
        video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
        try:
            ActionChains(driver).move_to_element(video).perform()
            current_time = driver.find_element(By.CLASS_NAME, "currentTime")  # 当前视频播放时间
            total_time = driver.find_element(By.CLASS_NAME, "duration")  # 总时间
            time1 = current_time.get_attribute('innerText')
            time2 = total_time.get_attribute('innerText')
            if time1 == time2:
                video.click()
                nextvideo = driver.find_element(By.CLASS_NAME, "nextButton")  # 定位下一个视频按钮
                nextvideo.click()  # 切换到下一个视频
                lesson()
                print("运行成功")
        except:
            pass
        time.sleep(10)


login()
lesson()
t1 = threading.Thread(target=test)
t2 = threading.Thread(target=videoend)
t2.start()
t1.start()

# version：1.1
