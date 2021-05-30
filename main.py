from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess

audio_file = "ding.mp3"

orte = ["1", "2", "3", "4", "5"]
phone_number = "ENTER YOUR PHONE NUMBER"

driver = webdriver.Chrome("drivers/chromedriver")


def try_click(xpath, interval):
    while True:
        try:
            driver.find_element_by_xpath(xpath).click()
            break
        except Exception:
            time.sleep(interval)


def check_if_dates_exist():
    try:
        element = driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[1]')
        attr = element.get_attribute("class")
        if str(attr).startswith("SelectList"):
            return True
    except Exception:
        print("Error while finding element")
    return False


def get_date_element():
    try:
        element = driver.find_element_by_xpath('//*[@id="logged-in-area"]/div/div[2]/div[1]/div[2]')
        attr = element.get_attribute("class")
        if str(attr).startswith("TimeSelectorButton__SplitWrapper"):
            return element
    except Exception:
        print("Error while finding element")
    return False


driver.get("https://www.impfen-saarland.de/")
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[2]/button[2]").click()
inputField = driver.find_element_by_xpath("/html/body/main/div[1]/form/div/div[2]/div/input")
inputField.send_keys(phone_number)
inputField.send_keys(Keys.ENTER)
x = input("press enter to proceed")
time.sleep(3)
driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[1]/button[2]").click()
time.sleep(1)
driver.switch_to.default_content()

while True:
    for ort in orte:
        driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[1]/button[" + ort + "]").click()
        time.sleep(0.1)
        driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[2]/button[2]").click()
        time.sleep(0.5)
        if check_if_dates_exist():
            # subprocess.call(["afplay", audio_file]) Uncomment to activate an notification sound
            for i in range(2, 6, 1):
                try:
                    driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[1]/div[" + str(i) + "]").click()
                    driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[2]/button[2]").click()
                except Exception:
                    print("no more dates: " + str(i))
                time.sleep(0.1)
            time.sleep(10)
            driver.switch_to.default_content()
            try_click("/html/body/main/div[1]/div/div[2]/div[2]/button[1]", 1)
        else:
            try_click("/html/body/main/div[1]/div/div[2]/div/button", 1)
