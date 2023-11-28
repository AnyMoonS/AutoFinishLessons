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


def zLogin(driver: webdriver.Remote, name: str, passwd: str):
    luserid = name
    lpassword = passwd
    phonenumber = driver.find_element(By.ID, "lUsername")
    pw = driver.find_element(By.ID, "lPassword")
    loginbutton = driver.find_element(By.CLASS_NAME, "wall-sub-btn")
    phonenumber.send_keys(luserid)
    pw.send_keys(lpassword)
    loginbutton.click()

def xLogin(driver: webdriver.Remote, name: str, passwd: str):
    luserid = name
    lpassword = passwd
    phonenumber = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/form/div[1]/input")
    pw = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/form/div[2]/input")
    loginbutton = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/form/div[3]/button")
    phonenumber.send_keys(luserid)
    pw.send_keys(lpassword)
    loginbutton.click()

def log(msg:object):
    print("[{}]{}".format(datetime.datetime.now(),msg))

def logErr(msg:object):
    log("Err:{}".format(msg))

def zPlay(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        if driver.current_url.__contains__("studyvideoh5"):  # 检测打开视频播放页
            time.sleep(10)  # 等待手动关闭弹窗
            try:
                videos = driver.find_elements(By.CLASS_NAME, "videoArea")  # 定位视频窗口
                if not videos:
                    logErr("Failed to locate video window")
                    time.sleep(10)
                    continue
                video = videos[0]
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
                logErr(ex)
                break

def xPlay(driver: webdriver.Remote, token: CancelToken):
    while not token.IsStop():
        if driver.current_url.__contains__("studentstudy"):  # 检测打开视频播放页
            try:
                video = driver.find_element(By.ID, "iframe")  # 定位视频窗口
                log("Play video")
                video.click()  # 播放视频
                break
            except Exception as ex:
                logErr(ex.args)
                break
        else:
            time.sleep(2)
            log("Not Found Video")


def xSwitch(driver: webdriver.Remote, token: CancelToken):
    while not token.IsStop():
        main_window_handle = driver.current_window_handle
        new_window_handle = None
        while not new_window_handle:
            for handle in driver.window_handles:
                if handle != main_window_handle:
                    new_window_handle = handle
                    break
        driver.switch_to.window(new_window_handle)
        break

def zAutoAnswer(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        log("Check for answer window")
        try:
            questions = driver.find_elements(
                By.CLASS_NAME, "topic-item")  # 找到第一个选项
            if not questions:
                time.sleep(10)
                continue
            question = questions[0]
            question.click()
            time.sleep(1)
            close = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/span/div")  # 关闭答题界面
            close.click()
            video = driver.find_element(By.CLASS_NAME, "videoArea")  # 定位窗口
            video.click()
        except Exception as ex:
            logErr(ex)
        time.sleep(10)


def zCheckProgress(driver: webdriver.Remote,token:CancelToken):
    while not token.IsStop():
        log("Check for video progress")
        try:
            videos = driver.find_elements(By.CLASS_NAME, "videoArea")  # 定位窗口
            if not videos:
                logErr("Failed to locate video window")
                time.sleep(10)
                continue
            video = videos[0]
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
                zPlay(driver,token)
        except Exception as ex:
            logErr(ex)
        time.sleep(10)

def xCheckProgress(driver: webdriver.Remote, token: CancelToken):
    while not token.IsStop():
       try:
            time.sleep(10)
            video = driver.find_element(By.ID, "iframe")
            driver.switch_to.frame(video)
            videoframe = driver.find_element(By.XPATH, '/html/body/div[2]/div/p/div/iframe')
            driver.switch_to.frame(videoframe)
            current_time = driver.find_element(By.CLASS_NAME, "vjs-current-time-display")
            duration_time = driver.find_element(By.CLASS_NAME, "vjs-duration-display")
            time1 = current_time.get_attribute('innerText')
            time2 = duration_time.get_attribute('innerText')
            log("current_time:" + time1)
            log("duration_time:" +time2)
            driver.switch_to.parent_frame()
            driver.switch_to.default_content()
            if time1 == time2:
                log("Switch to next video")
                nextbutton = driver.find_element(By.ID, "right2")
                nextbutton.click()
                time.sleep(1)
                nextbutton2 = driver.find_element(By.ID, "right2")
                nextbutton2.click()
                nextbutton3 = driver.find_element(By.CSS_SELECTOR, '[class="bluebtn02 prebutton nextChapter"]')
                nextbutton3.click()
                time.sleep(5)
                xPlay(driver, token)
       except Exception as ex:
           logErr(ex)

def quit(token:CancelToken,sig:int,frame):
    token.Stop()
    log("Stop")

def ZHS(argv: Sequence[str]):
    name: str = ""
    passwd: str = ""
    browser: str = "chrome"
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
    driver.implicitly_wait(10)
    actions = ActionChains(driver)
    driver.get("https://onlineweb.zhihuishu.com/")  # 打开智慧树官网
    driver.maximize_window()
    token: CancelToken = CancelToken()
    time.sleep(2)
    zLogin(driver, name, passwd)
    zPlay(driver, token)
    t1 = threading.Thread(target=zAutoAnswer, args=(driver, token,))
    t2 = threading.Thread(target=zCheckProgress, args=(driver, token,))
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


def XXT(argv: Sequence[str]):
    name: str = ""
    passwd: str = ""
    browser: str = "chrome"
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
    driver.implicitly_wait(10)
    actions = ActionChains(driver)
    driver.get("https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https://i.chaoxing.com")  # 打开学习通官网
    driver.maximize_window()
    token: CancelToken = CancelToken()
    time.sleep(2)
    xLogin(driver, name, passwd)
    xSwitch(driver, token)
    time.sleep(10)
    xPlay(driver, token)
    t1 = threading.Thread(target=xCheckProgress, args=(driver, token,))
    t1.start()
    print("Use Enter any key to exit")
    _ = input()
    log("Stopping")
    token.Stop()
    t1.join()
    driver.close()
    log("Stoped")


if __name__ == "__main__":
    try:
        a = input("输入启动模式“z”代表智慧树，“x”代表学习通")
        if a == "z":
            ZHS(sys.argv[1:])
        elif a == "x":
            XXT(sys.argv[1:])
        else:
            log("输入错误")
    except Exception:
        pass
