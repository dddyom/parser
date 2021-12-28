from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import time
from config import *

driver = webdriver.Chrome(f"{BASE_DIR}/parser/chromedriver")


driver.get(f"https://artzip.ru/search/?q=Динара+Хёртнагль")

result_list = driver.find_elements_by_class_name("products-item-img")

print(result_list[0].get_attribute("href"))