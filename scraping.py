import requests
import bs4
import pandas as pd
import os 
from selenium import webdriver
import selenium
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep

"""
    На вход подается ссылка на сайт и список запросов (Название компании, адрес, телефон, сайт, домен, ФИО руководителя, совладельца, доверительного управляющего, ИНН, ОГРН, ОКПО, БИК)
            "https://www.spark-interfax.ru/search?Query=9715308343"   

    - parsing(path_url, query):
            - получает два аргумента (1 - ссылка на сайт, 2 - список запросов) и конкатенирует их
            - вызывает функцию парсинга сайта (parsing_site) 
            - результат полученный от parsing_site (до)записывает в csv файл
    
    - parsing_site(page_url)
            - lib selenium - используется для сборки всех записей со страницы
            - lib bs4 - используется для парсинга страницы по тегам


--   --  запись в csv 

"""


def parsing(path_url, query=["9715308343"]):  # вызывает функцию парсинга сайта  и записывает dataframe в csv файл
    if os.path.exists("result.csv"):
        os.remove("result.csv")

    if len(query) > 1: # если в списке query записей больше одного, то передаем в функцию parsing_site поэлементно каждую 
        for i in range(0, len(query)):
            page_url = path_url + query[i]
            result_dataframe = parsing_site(page_url)
            result_dataframe.to_csv("result.csv", mode='a', index=False, header=False)
    else:
        page_url = path_url + query[0]
        dict_rows = parsing_site(page_url)
        print(type(dict_rows), "\n", dict_rows)


def parsing_site(page_url):  # парсит страницу по тегам и возвращает dataframe

    #page = requests.get(page_url)
    driver = webdriver.Chrome(r'C:/Users/riskenderov/Python_Advanced/scraping/chromedriver.exe')
    driver.get(page_url)
    
    search_result_counter = int( driver.find_element_by_class_name("search-result__counter").text.replace("Найдено результатов: ","") )
    
     
    try:  # если есть кнопка "показать еще" нажимаем на на нее необходимое количество раз
        link =  driver.find_element_by_id('form0')
        if search_result_counter > 10:
            for i in range(0, int(search_result_counter / 10)):
                link.click()
                sleep(5)
    except NoSuchElementException:
        print("")
 
    
    #soup = bs4.BeautifulSoup(page.content, 'html.parser')
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')  # передаем в руки bs4 все записи со страницы которые нам собрал selenium
    driver.close()
    driver.quit()

    soup = soup.find_all("div", class_="summary")

    row_list = []
    for i in soup:
        dict_row = {}
        if i.find("a") is not None:  # в некоторых записях нет тега "a href", в которой находится название компании 
            company = i.find("a").text.strip()
            dict_row.update({"Компания": company})
            div_code = i.find("div", class_="code")
            for j in range(0, len(div_code.select("span"))-1):
                if div_code.select("span")[j].text.strip() in ["ИНН", "ОГРН", "ОКПО", "БИК"]:  # забираем именно те атрибуты которые нам нужны (убираются теги в которых записан мусор)
                    dict_row.update({div_code.select("span")[j].text.strip() : div_code.select("span")[j+1].text.strip()})

            row_list.append(dict_row)
            print(dict_row)
        else:
            company = i.find("h3").text.strip()  # название компаниии для записей у которых нет тега "a href", оно находится в теге "h3"
            dict_row.update({"Компания": company})
            div_code = i.find("div", class_="code")
            for j in range(0, len(div_code.select("span"))-1):
                if div_code.select("span")[j].text.strip() in ["ИНН", "ОГРН", "ОКПО", "БИК"]:
                    dict_row.update({div_code.select("span")[j].text.strip() : div_code.select("span")[j+1].text.strip()})

            row_list.append(dict_row)
            print(dict_row)

    return pd.DataFrame(row_list)

    



if __name__ =="__main__":
        
    path_url = "https://www.spark-interfax.ru/search?Query="
    query = ["9715308343","ТИНЬКОФФ", "7710140679", "7702070139"]

    parsing(path_url, query)
