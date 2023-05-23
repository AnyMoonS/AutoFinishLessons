from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import getopt
import sys
import signal
from typing import Sequence


def checkBrowser(browser: str) -> bool:
    return browser == "edge" or browser == "firefox" or browser == "chrome"

def produceDriver(browser:str)->webdriver.Remote:
    if browser == "edge":
        return webdriver.Edge()
    elif browser == "firefox":
        return webdriver.Firefox()
    elif browser == "chrome":
        return webdriver.Chrome()
    else:
        return webdriver.Edge()

def usage():
    print("usage:")
    print("\t-h - show help")
    print("\t-n <name>")
    print("\t-p <password>")
    print("\t-b [edge|firefox|chrome]")

def login(driver: webdriver.Remote, name: str, passwd: str):
    luserid = name
    lpassword = passwd
    phonenumber = driver.find_element(By.ID, "lUsername")
    pw = driver.find_element(By.ID, "lPassword")
    loginbutton = driver.find_element(By.CLASS_NAME, "wall-sub-btn")
    phonenumber.send_keys(luserid)
    pw.send_keys(lpassword)
    loginbutton.click()


def play(driver: webdriver.Remote):
    while 1:
        if driver.current_url.__contains__("studyvideoh5"):  # 检测打开视频播放页
            time.sleep(10)  # 等待手动关闭弹窗
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位视频窗口
            try:
                video.click()  # 播放视频
                ActionChains(driver).move_to_element(video).perform()
                speedbox = driver.find_element(By.CLASS_NAME, "speedBox")
                speedbox.click()
                time.sleep(1)
                speedtab15 = driver.find_element(
                    By.CLASS_NAME, "speedTab15")  # 1.5倍播放
                speedtab15.click()
                break
            except:
                break


def autoAnswer(driver: webdriver.Remote):
    while 1:
        try:
            question = driver.find_element(
                By.CLASS_NAME, "topic-item")  # 找到第一个选项
            question.click()
            time.sleep(1)
            close = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[6]/div/div[3]/span/div")  # 关闭答题界面
            close.click()
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
            video.click()
        except:
            pass
        time.sleep(10)


def checkProgress(driver: webdriver.Remote):
    while 1:
        video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
        try:
            ActionChains(driver).move_to_element(video).perform()
            current_time = driver.find_element(
                By.CLASS_NAME, "currentTime")  # 当前视频播放时间
            total_time = driver.find_element(By.CLASS_NAME, "duration")  # 总时间
            time1 = current_time.get_attribute('innerText')
            time2 = total_time.get_attribute('innerText')
            if time1 == time2:
                video.click()
                nextvideo = driver.find_element(
                    By.CLASS_NAME, "nextButton")  # 定位下一个视频按钮
                nextvideo.click()  # 切换到下一个视频
                print("Move to next video")
                play(driver)
                print("Success")
        except:
            pass
        time.sleep(10)

def main(argv: Sequence[str]):

    name: str = ""
    passwd: str = ""
    browser: str = "edge"
    try:
        opts, args = getopt.getopt(argv, "n:p:t:b:")
        for opt, arg in opts:
            if opt == "-n":
                name = arg
            elif opt == "-p":
                passwd = arg
            elif opt == "-t":
                browser = arg
        if not checkBrowser(browser):
            usage()
            return
    except getopt.GetoptError:
        usage()
        return
    while name == "":
        name = input("Please input name:")
    while passwd == "":
        passwd = input("Please input password")
    driver = produceDriver(browser)
    actions = ActionChains(driver)
    driver.get("https://onlineweb.zhihuishu.com/")  # 打开智慧树官网
    driver.maximize_window()
    time.sleep(2)
    login(driver,name,passwd)
    play(driver)
    t1 = threading.Thread(target=autoAnswer,args=(driver,))
    t2 = threading.Thread(target=checkProgress,args=(driver,))
    t2.start()
    t1.start()
    print("Use CTRL+C to exit")
    t2.join()
    t1.join()

def quit():
    sys.exit(0)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        main(sys.argv[1:])
    except Exception:
        pass
