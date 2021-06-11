from tkinter import *
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from InfScanner import InformationCollector
import json
import time
import pathlib
from selenium.webdriver.common.action_chains import ActionChains
def konturGetLink(driver, mail):
    
    resp = driver.request("POST", "https://focus.kontur.ru/api/sendauthemail", data = {
        "email": mail
    })
    driver.close()
    if resp.status_code == 200:
        return True
    return False

def konturAuth(driver, link):
    driver.get(link)
    driver.close()

def sbisAuth(driver):
    try:
        driver.get("https://online.saby.ru/auth/?tab=demo")
        time.sleep(3)
        elem = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div[1]")
        ActionChains(driver).move_to_element(elem).click(elem).perform()
        time.sleep(5)
        driver.close()
        return True
    except:
        return False
def main():
    main_window = Tk()
    main_window.geometry("700x800")
    main_window.title("Вебсервис")

    scanner = InformationCollector.InformationScanner()
    driver = scanner.driver
    #sbisAuth(driver)
    setting_up_sbis_button = Button(main_window, text = "Преднастройка СБИС",  command=lambda: driver.get("https://online.saby.ru/page/company"), width = 75, height = 3 )
    setting_up_kontur_button = Button(main_window, text = "Преднастройка Контур",  command=lambda: driver.get("https://focus.kontur.ru/"), width = 75, height = 3 )
    setting_up_sbis_button.grid(row = 1, column = 1)
    setting_up_kontur_button.grid(row = 2, column = 1)
    main_window.mainloop()

if __name__ == "__main__":
    main()