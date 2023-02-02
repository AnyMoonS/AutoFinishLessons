from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading

import config

driver = webdriver.Firefox()
actions = ActionChains(driver)
driver.get("https://onlineweb.zhihuishu.com/")  # 打开智慧树官网
driver.maximize_window()
time.sleep(5)


def login():
    phonenumber = driver.find_element(By.ID, "lUsername")
    pw = driver.find_element(By.ID, "lPassword")
    loginbutton = driver.find_element(By.CLASS_NAME, "wall-sub-btn")
    phonenumber.send_keys(config.userid)
    pw.send_keys(config.password)
    loginbutton.click()


def lesson():
    while 1:
        if driver.current_url.__contains__("studyvideoh5"):  # 检测打开视频播放页
            time.sleep(10)  # 等待手动关闭弹窗
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位视频窗口
            video.click()#播放视频
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
                nextvideo = driver.find_element(By.CLASS_NAME, "nextButton") #定位下一个视频按钮
                nextvideo.click()#切换到下一个视频
                lesson()
        except:
            pass
        time.sleep(10)


login()
lesson()
t1 = threading.Thread(target=test)
t2 = threading.Thread(target=videoend)
t2.start()
t1.start()


# version：1.0
