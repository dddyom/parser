import csv
import pandas as pd
from selenium import webdriver
# from selenium.common.exceptions import InvalidArgumentException

import tools
from config import *
from Page import *

DRIVER = webdriver.Chrome(f"{BASE_DIR}/parser/chromedriver")


def main():
    cur_catalog = CatalogPage(driver=DRIVER, url=CATALOG_URL)
    if not tools.check_csv_exist(f"{CATALOG_NAME}"):
        with open(f"{CATALOG_NAME}.csv", 'w') as parsed_csv:
            writer = csv.writer(parsed_csv)
            writer.writerow(RAW_CSV_HEAD)
    page_counter = 0
    image_counter = 0
    while True:
        images_links_obj = cur_catalog.get_images_links(image_links_class_name="products-item-img")
        images_links = [image_link.get_attribute("href") for image_link in images_links_obj]
        for image_link in images_links:
            print(image_link)
            if image_link.split('/')[-2] in CATALOG_LIST:
                continue
            image_counter += 1
            raw_csv = pd.read_csv(f"{CATALOG_NAME}.csv")
            image_page = ImagePage(driver=cur_catalog.driver, url=image_link)
            author_name_obj = image_page.get_elements_by_identifier(identifier_type="class",
                                                                    identifier_name="author-name_link")[0]

            if author_name_obj.text not in set(list(raw_csv["author_name"])):
                author_link = author_name_obj.get_attribute("href")
                author_page = AuthorPage(cur_catalog.driver, url=author_link)
                author_dict = author_page.__dict__
                image_page.driver.get(image_page.url)
            else:
                years_of_life = raw_csv.loc[raw_csv['author_name'] == author_name_obj.text, "years_of_life"].values[0]
                try:
                    years_of_life = int(years_of_life)
                except ValueError:
                    years_of_life = str(years_of_life)
                place_of_residence = \
                    raw_csv.loc[raw_csv['author_name'] == author_name_obj.text, "place_of_residence"].values[0]
                author_description = \
                    raw_csv.loc[raw_csv['author_name'] == author_name_obj.text, "author_description"].values[0]
                author_dict = {"author_name": author_name_obj.text, "years_of_life": years_of_life,
                               "place_of_residence": place_of_residence,
                               "author_description": author_description}

            image_dict = image_page.__dict__

            parsed_list = [author_dict["author_name"], author_dict["years_of_life"],
                           author_dict["place_of_residence"], author_dict["author_description"],
                           image_dict["image_name"], image_dict["execution_technique"],
                           image_dict["size"], image_dict["year"], image_dict["price"], CATALOG_NAME, image_dict['_url']]
            # print(parsed_list)
            with open(f"{CATALOG_NAME}.csv", 'a') as parsed_csv:
                writer = csv.writer(parsed_csv)
                writer.writerow(parsed_list)

            image_page.driver.get(cur_catalog.url)

        try:
            cur_catalog.set_url_to_next_page("modern-page-next")
            print(cur_catalog.url)
            cur_catalog.driver.get(cur_catalog.url)
            page_counter += 1

            print(f"page count: {page_counter}, image count: {image_counter}")
        except IndexError:
            print("IndexError")
            print(f"page count: {page_counter}, image count: {image_counter}")
            break
    DRIVER.quit()

    # images = driver.find_elements_by_tag_name('img')
    # # for i in images:
    # #     src = i.get_attribute("src")
    # #     urllib.request.urlretrieve(src, f"{src.split('/')[-1]}")


if __name__ == "__main__":
    main()

    df = pd.read_csv(f"{CATALOG_NAME}.csv")
    df.drop_duplicates(inplace=True)
    df.to_csv(f"{CATALOG_NAME}.csv", index=False)
