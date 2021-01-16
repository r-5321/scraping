

from selenium import webdriver
import selenium
from selenium.webdriver import ActionChains
from time import sleep
import csv 

path_url = "https://www.spark-interfax.ru/search?Query="
query = ["9715308343", "ТИНЬКОФФ", "7710140679", "7702070139"]


def scraping(path_url, query=["ТИНЬКОФФ"]):
    """
    docstring

    """
    page_url = path_url + query[0]
    driver = webdriver.Chrome(r'C:/Users/riskenderov/Python_Advanced/chromedriver.exe')
    driver.get(page_url)
    
    search_result_counter = int( driver.find_element_by_class_name("search-result__counter").text.replace("Найдено результатов: ","") )
    
    link =  driver.find_element_by_id('form0')
    
    # закоментировано специально --- "не могла парсить некоторые записи" ПОПРОБОВАТЬ ПОТОМ
    if search_result_counter > 10:
        for i in range(0, int(search_result_counter / 10)):
            link.click()
            sleep(1)
 
    

    all_elems = driver.find_element_by_id("search-result-items")
         
    
    print(all_elems.find_elements_by_class_name("search-result-list__item")[0].text)
    all_rows = all_elems.find_elements_by_class_name("search-result-list__item")
    with open("test_selenium.csv", "w") as csvfile:
        wr = csv.writer(csvfile)
        print("all_rows",all_rows)
        for row in all_rows:
            wr.writerow(row.text)
            print("row.text = ",row.text)
    
    
    """ - этот участок кода не работает из-за того, что в некоторых записях нет тега a href, и будет падать с ошибкой
    for i in all_elems.find_elements_by_class_name("search-result-list__item"):
        dict_row = {}
        #print(i.find_element_by_class_name("highlight").text, i.find_elements_by_class_name("code")[0].text)
        print(i.find_element_by_tag_name("a").text, i.find_elements_by_class_name("code")[0].text)
        for j in i.find_elements_by_class_name("code"):
            for x in j.find_elements_by_tag_name("span"):
                
                print("===> ",x.text)
        #dict_row.update({"Компания": i.find_element_by_tag_name("a").text})

    """
  




 
   
    driver.close()
    driver.quit()
 

scraping(path_url)
