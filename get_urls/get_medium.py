from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

products = pd.read_csv("artist_works_artzip.csv")


driver = webdriver.Chrome(f"chromedriver")
counter = 0
medium_list = []
for page_link in products["work_link"]:
    counter += 1
    driver.get(f"{page_link}")
    try:
        medium = driver.find_element_by_id("bx_breadcrumb_2")
        medium_text = medium.text
    except NoSuchElementException:
        medium_text = None
    medium_list.append([page_link, medium_text])
    #print(medium_text, counter)
medium = pd.DataFrame(medium_list, columns=["page_link", "medium"])
medium.to_csv("medium.csv", index=False)
driver.quit()

#     try:
#         img_obj= driver.find_element_by_class_name("pslider-photo-link.fancybox")
#         img_link = img_obj.get_attribute("href")
#     except NoSuchElementException:
#         product_links = pd.DataFrame(links_list, columns=["page_link","image_link"])

#         product_links.to_csv(f"product_links{counter}.csv", index=False)
#         # product_links.to_csv(f"product_links{counter}.csv", index=False)
#         img_link = None
#     print(counter)
#     links_list.append([page_link, img_link])        
#     print(img_link)


# product_links.to_csv("product_links.csv", index=False)
