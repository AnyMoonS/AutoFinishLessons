import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import getopt
import sys
import signal
import datetime
from typing import Sequence

class CancelToken:
    token:bool

    def __init__(self) -> None:
        self.token = False

    def Stop(self) -> None:
        self.token = True

    def IsStop(self) -> bool:
        return self.token

def checkBrowser(browser: str) -> bool:
    return browser == "edge" or browser == "firefox" or browser == "chrome"


def produceDriver(browser: str) -> webdriver.Remote:
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

def log(msg:object):
    print("[{}]{}".format(datetime.datetime.now(),msg))

def logErr(msg:object):
    log("Err:{}".format(msg))

def play(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        if driver.current_url.__contains__("studyvideoh5"):  # 检测打开视频播放页
            time.sleep(10)  # 等待手动关闭弹窗
            try:
                video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位视频窗口
                log("Play video")
                video.click()  # 播放视频
                driver.execute_script('if(document.getElementsByClassName("video-topic").length !=0){document.getElementsByClassName("video-topic")[0].remove()}')
                ActionChains(driver).move_to_element(video).perform()
                speedbox = driver.find_element(By.CLASS_NAME, "speedBox")
                speedbox.click()
                time.sleep(1)
                speedtab15 = driver.find_element(
                    By.CLASS_NAME, "speedTab15")  # 1.5倍播放
                speedtab15.click()
                break
            except Exception as ex:
                logErr(ex.args)
                break


def autoAnswer(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        log("Check for answer window")
        try:
            question = driver.find_element(
                By.CLASS_NAME, "topic-item")  # 找到第一个选项
            question.click()
            time.sleep(1)
            close = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/span/div")  # 关闭答题界面
            close.click()
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
            video.click()
        except Exception as ex:
            logErr(ex.args)
        time.sleep(10)


def checkProgress(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        log("Check for video progress")
        try:
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
            ActionChains(driver).move_to_element(video).perform()
            current_time = driver.find_element(
                By.CLASS_NAME, "currentTime")  # 当前视频播放时间
            total_time = driver.find_element(By.CLASS_NAME, "duration")  # 总时间
            time1 = current_time.get_attribute('innerText')
            time2 = total_time.get_attribute('innerText')
            if time1 >= time2:
                log("Switch to next video")
                driver.execute_script('if(document.getElementsByClassName("video-topic").length !=0){document.getElementsByClassName("video-topic")[0].remove()}')
                nextvideo = driver.find_element(
                    By.CLASS_NAME, "nextButton")  # 定位下一个视频按钮
                nextvideo.click()  # 切换到下一个视频
                log("Switched")
                play(driver,token)
        except Exception as ex:
            logErr(ex.args)
        time.sleep(10)

def quit(token:CancelToken,sig:int,frame):
    token.Stop()
    log("Stop")

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
            elif opt == "-b":
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
        passwd = input("Please input password:")
    driver = produceDriver(browser)
    actions = ActionChains(driver)
    driver.get("https://onlineweb.zhihuishu.com/")  # 打开智慧树官网
    driver.maximize_window()
    token:CancelToken = CancelToken()
    time.sleep(2)
    login(driver, name, passwd)
    play(driver,token)
    t1 = threading.Thread(target=autoAnswer, args=(driver,token,))
    t2 = threading.Thread(target=checkProgress, args=(driver,token,))
    t2.start()
    t1.start()
    print("Use Enter any key to exit")
    _ = input()
    log("Stopping")
    token.Stop()
    t2.join()
    t1.join()
    driver.close()
    log("Stoped")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception:
        pass
