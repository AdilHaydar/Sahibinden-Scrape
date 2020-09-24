from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
#from time import sleep
import sys

model = []
ilan_basligi = []
yil = []
km = []
renk = []
fiyat = []


if len(sys.argv) == 2:
    if sys.argv[1].lower() == '-h' or sys.argv[1] == '--help':
        print("Example : "+"sahibinden_scrape.py https://www.sahibinden.com/chevrolet-cruze")
        sys.exit()

    else:
        options = Options()
        options.add_argument('-headless')
        browser = webdriver.Firefox(executable_path=r"add executable path here.",options=options)
        wait = WebDriverWait(browser, 10)
        #next_page = "https://www.sahibinden.com/chevrolet-cruze"
        next_page = sys.argv[1]
        page_count = 0

        while page_count < 5:
            browser.get(next_page)
            #sleep(3)

            # ilan_basligi_scrape =  browser.find_elements_by_css_selector(".searchResultsTitleValue")
            # model_scrape = browser.find_elements_by_css_selector(".searchResultsTagAttributeValue")
            # yil_km_renk_scrape = browser.find_elements_by_css_selector(".searchResultsAttributeValue")
            # fiyat_scrape =  browser.find_elements_by_css_selector(".searchResultsPriceValue")

            ilan_basligi_scrape = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsTitleValue")))
            model_scrape = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsTagAttributeValue")))
            yil_km_renk_scrape = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsAttributeValue")))
            fiyat_scrape = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsPriceValue")))

            for data in yil_km_renk_scrape:
                if data.text.isdigit() and len(data.text) is 4 and not '.' in data.text:
                    yil.append(data.text)
                elif not (data.text.isdigit()) and not '.' in data.text:
                    renk.append(data.text)
                else:
                    km.append(data.text)

            for data in ilan_basligi_scrape:
                ilan_basligi.append(data.text)

            for data in model_scrape:
                model.append(data.text)

            for data in fiyat_scrape:
                fiyat.append(data.text)
            
            if page_count >= 1:
                try:
                    next_page = browser.find_elements_by_css_selector(".prevNextBut")
                    next_page = next_page[1].get_attribute('href')
                except IndexError:
                    break
                
            else:
                try:
                    next_page = browser.find_element_by_css_selector(".prevNextBut")
                    next_page = next_page.get_attribute('href')
                except NoSuchElementException:
                    break

            page_count += 1
            print("Stage {} Completed.".format(page_count))

        pure_fiyat = []
        for i in fiyat:
            pf = i.replace('.','')
            pf = pf.replace('TL','')
            pf = pf.strip()
            pf = int(pf)
            pure_fiyat.append(pf)
        ortalama = sum(pure_fiyat)/len(fiyat)
        print("Ortlama Fiyat : ",ortalama,"TL")


        df = pd.DataFrame({'Model':model,'İlan Başlığı':ilan_basligi,'Yıl':yil,'KM':km,'Renk':renk,'Fiyat':fiyat})
        df.to_csv('ilan_scrape.csv',index=False,encoding='utf-8')

        data = pd.read_csv('ilan_scrape.csv')

        print(data)

else:
    print("Example : "+"sahibinden_scrape.py https://www.sahibinden.com/chevrolet-cruze")
    sys.exit()

