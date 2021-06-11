from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import time
import os
try:
    from InfScanner.XlsxUtils import XlsxUtils
    from InfScanner.OkvedXlsxUtils import OkvedXlsxUtils
except:
    from OkvedXlsxUtils import OkvedXlsxUtils
    from XlsxUtils import XlsxUtils
import pathlib
import random
from selenium.webdriver.common.action_chains import ActionChains
from seleniumrequests import Chrome
import math
import json
import glob
from dbf_light import Dbf
class InformationScanner():

    def init_downloads(self, download_path):
        
        options = webdriver.ChromeOptions()
        profile_driver_path = pathlib.Path().absolute()
        profile_path = profile_driver_path.joinpath("Profile")
        print("PAAAAATH",profile_path)
        webdriver_path = profile_driver_path.joinpath("chromedriver.exe")
        print(webdriver_path)
        options.add_argument("user-data-dir={}".format(profile_path))     
        prefs = {}
        prefs["download.default_directory"]=str(download_path)
        options.add_experimental_option("prefs", prefs) 
        self.driver = Chrome(executable_path=webdriver_path, chrome_options=options)

    def __init__(self):

        download_path = pathlib.Path("information_dowloads").absolute()
        self.init_downloads(download_path)
        self.data = json.loads(open("zipbase.json", "r").read())
        
        #self.__createLists(10)
   
    def import_companies(self, inns, list_id):
        from selenium.webdriver.common.action_chains import ActionChains
        driver = self.driver
        link = "https://focus.kontur.ru/lists/import?id={list_id}".format(list_id = list_id)
        driver.get(link)
        inn_lst = "\n".join(inns)
        print(inn_lst)
        elem = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/main/div/div[2]/div/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[6]/div[1]/div/div/div/div[5]/div/pre")
        ActionChains(driver).move_to_element(elem[0]).click(elem[0]).send_keys(inn_lst).perform()
        
        elem = driver.find_elements_by_xpath('//*[@id="appRoot"]/div[1]/main/div/div[2]/div/main/div/div[1]/div/div[2]/div/div[2]/div/span/button')
        ActionChains(driver).move_to_element(elem[0]).click(elem[0]).perform()
        time.sleep(2)
        elem = driver.find_elements_by_xpath('//*[@id="appRoot"]/div[1]/main/div/div[2]/div/main/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[2]/label/span')
        ActionChains(driver).move_to_element(elem[0]).click(elem[0]).perform()
        elem = driver.find_elements_by_xpath('//*[@id="appRoot"]/div[1]/main/div/div[2]/div/main/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[3]/label/span')
        ActionChains(driver).move_to_element(elem[0]).click(elem[0]).perform()
        elem = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/main/div/div[2]/div/main/div/div[2]/div/div[1]/div/div[2]/span/button')
        ActionChains(driver).move_to_element(elem[0]).click(elem[0]).perform()
    def __createList(self):
        
        resp = self.driver.request("POST", "https://focus.kontur.ru/api/lists/create", data = {
            'name': "test"+str(random.randint(1000000,1000000000000000)),
            'descr': '',
            'color': 'green'
        })
        
        #elem = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/div[2]/a")
        #ActionChains(self.driver).move_to_element(elem).click(elem).send_keys(str(random.randint(1000000,1000000000000000))).perform()
        
        return resp.text
    def __addCompanies(self, list_id, inns):
        flag = False
        
        resp = self.driver.request("POST", "https://focus.kontur.ru/api/lists/parse", data = {
            "text": "\n".join(inns)
        })
        found_companies = json.loads(resp.text)
        if len(found_companies["result"]) == 2:
            found_companies = found_companies["result"][0]["fids"] + found_companies["result"][1]["fids"]

        elif len(found_companies["result"]) == 1:
            found_companies = found_companies["result"][0]["fids"] 
        else:
            return False
        print(found_companies)
        while not flag:
            resp = self.driver.request("POST", "https://focus.kontur.ru/api/lists/toggleItems", data = {
                "id": list_id,
                "fids": ",".join(found_companies),
                "active": "true"
            })
            if resp.status_code == 200:
                flag = True
                return True
            else:
                resp = self.driver.request("POST", "https://focus.kontur.ru/api/lists/update", data = {
                "id": list_id,
                "isMon": "False"
                
            })
            print(resp.text)
        return False
    def __getDataFromList(self, list_id):

        filename = "table" + str(random.randint(1,10000)) + ".xlsx"
        file_path = pathlib.Path("information_dowloads\\"+filename).absolute()
        self.driver.get("https://focus.kontur.ru/lists/export/{filename}?format=Xlsx&id={list_id}".format(filename = filename, list_id = list_id))
        time.sleep(3)
        
        data = XlsxUtils.XlsxToJson(str(file_path))
        return data
    def scan(self, path, out_path, inn_input_column, output_file_fields = {
        "authCapital": "AF",
        "phones": "R",
        "address": "P",
        "workers": "AG",
        "shortName": "AH",
        "fullName": "AI",
        "inn": "H",
        "ogrn": "N",
        "status": "AJ",
        "regDate": "AK",
        "directors": "AL",
        "holders": "AM",
        "reportYear": "AN",
        "earnings": "AO",
        "govContracts": "AP",
        "govBuyings": "AQ",
        "city": "AR",
        "region": "AS"}):
        inns = XlsxUtils.ColumnToList(path, inn_input_column)
        inns_splitted = [inns[i:i+10000] for i in range(0,len(inns),10000)]
        inn_lists = [(self.__createList(),i) for i in inns_splitted]
        print(inn_lists)
        
        for inn_list in inn_lists:
            try:
                list_id = inn_list[0]
                
                if self.__addCompanies(list_id, inn_list[1]):
                    time.sleep(3)
                    print("companies added")
                    data = self.__getDataFromList(list_id)
                    print("data getted")
                    for company in data.keys():
                        print("key started")
                        addr = data[company]["address"]
                        zipCode = self.__getZipCodeByAddress(addr)
                        pair = self.__getRegionAndCityByZipCode(zipCode)
                        data[company]["region"] = pair[0]
                        data[company]["city"] = pair[1]
                        print(pair[0], pair[1])
                        
                    print(data)
                    print("ДАТАААА")
                    print(output_file_fields)
                    XlsxUtils.JsonToXlsx(data, path, fields = output_file_fields, outpath = out_path)
                    
                else:
                    print("хана рулю")
            except:
                continue
        
        self.driver.close()
    def __downloadByOgrns(self, ogrns_list):
        pass
    def __getRegionAndCityByZipCode(self, code):
        
        try:
            return self.data[str(code)]
        except:

            return ("","")
    def __getZipCodeByAddress(self, address):
        zipCode = address.split(",")[0]
        try:
            return int(zipCode)
        except:
            return False
    def scanOkveds(self, path, out_path, ogrn_input_column, ogrn_output_column, output_file_fields =  {
        "main" : "AR",
        "additional": "AS",
        "all_start": "AT"
    }):
        
        ogrns = XlsxUtils.ColumnToList(path, ogrn_input_column)
        dirname = "okved_scan" + str(random.randint(10000000, 1000000000))
        try:
            self.driver.close()
        except:
            pass
        os.mkdir(dirname)
        dirpath = pathlib.Path(dirname).absolute()
        self.init_downloads(dirpath)
        
        dir_path = pathlib.Path(dirname).absolute()
        for ogrn in ogrns:
            filename = str(ogrn)+".xlsx"
            file_path = pathlib.Path("information_dowloads\\"+filename).absolute()
            link = "https://focus.kontur.ru/xlsx/{ogrn}/{filename}?type=Default&summary=1".format(filename = filename, ogrn = str(ogrn))
            
            self.driver.get(link)
            if ( "ошибка" in str(self.driver.page_source)):
                print("Не удалось скачать файл")
                self.driver.get("https://focus.kontur.ru/")
                time.sleep(1)
                continue
            
            '''
            try:

                file_path.replace(dir_path.joinpath(filename))
            except:
                continue
            '''      
           
        self.driver.close()
        files = glob.glob(str(dir_path.joinpath("*.xlsx")))
        data = OkvedXlsxUtils.getOkvedsByOgrn(files) 
        OkvedXlsxUtils.toXlsx(data, path, ogrn_output_column, fields = output_file_fields, outpath=out_path)




        
            

        
      



#download_by_ogrns()

if __name__ == "__main__":
      
    pass
    #scanner.scan("Domains_small_test.xlsx", "Domains_small_test.xlsx", "H")
    #scanner.scanOkveds("Domains_small_test.xlsx", "Domains_small_test.xlsx", "N", "N")
    

                



    #driver.get("https://focus.kontur.ru/lists/analytics?id=89b1b483-e4fc-4c70-9f08-dfd58b3c7aa3&type=ru&viewMode=analytics&page={page}".format(page=page))
 
