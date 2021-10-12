import os
import csv
# import pandas as pd
from selenium import webdriver

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DRIVER = webdriver.Chrome(f"{BASE_DIR}/parser/chromedriver")
CATALOG_URL = "https://artzip.ru/catalog/zhivopis/"
RESULT_SCV_NAME = "zhivopis"


class SitePage(object):
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:
        self._driver = driver
        self._url = url
        self._driver.get(self._url)

    @property
    def driver(self) -> webdriver.Chrome:
        return self._driver

    @driver.setter
    def driver(self, driver: webdriver.Chrome) -> None:
        self._driver = driver

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        self._url = url

    def get_elements_by_identifier(self, identifier_type: str, identifier_name: str) -> list:
        result_list = []
        if identifier_type.lower() not in ("class", "tag"):
            raise ValueError(f"Unexpected identifier type -> {identifier_type}")

        if identifier_type.lower() == "class":
            result_list = self._driver.find_elements_by_class_name(identifier_name)
        elif identifier_type.lower() == "tag":
            result_list = self._driver.find_elements_by_tag_name(identifier_name)

        if result_list is None:
            print("Result is empty. Maybe identifier name is wrong")
        return result_list


class CatalogPage(SitePage):

    def __init__(self, driver, url) -> None:
        super().__init__(driver=driver, url=url)

    def set_url_to_next_page(self, next_page_btn_class_name: str) -> None:
        next_page_btn = self.get_elements_by_identifier(identifier_type="class",
                                                        identifier_name=next_page_btn_class_name)[0]
        self._url = next_page_btn.get_attribute("href")

    def get_images_links(self, image_links_class_name: str, identifier_type: str = "class") -> list:
        return self.get_elements_by_identifier(identifier_type=identifier_type,
                                               identifier_name=image_links_class_name)


class ImagePage(SitePage):
    def __init__(self, driver, url) -> None:
        super().__init__(driver=driver, url=url)
        self.driver.get(self._url)
        self.author_info = None
        self.image_name = None
        self.execution_technique = None
        self.size = None
        self.year = None
        self.most_price = None
        self.other_price = None
        self.description = None

    # def set_author_info(self, author_info_identifier_name: str, identifier_type: str = "class") -> None:
    #     temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
    #                                                 identifier_name=author_info_identifier_name)
    #     raw_author_info = ''.join((cur_string.text for cur_string in temp_list))
    #     self.author_info = raw_author_info

    def set_image_name(self, image_name_identifier_name: str, identifier_type: str = "class") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=image_name_identifier_name)
        raw_image_name = ''.join((cur_string.text for cur_string in temp_list))
        self.image_name = raw_image_name[10:]

    def set_image_parameters(self, parameters_identifier_name: str, identifier_type: str = "tag") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=parameters_identifier_name)
        raw_image_parameters = '\n'.join((cur_string.text for cur_string in temp_list))
        raw_list = raw_image_parameters.split('\n')
        self.author_info = raw_list[0]
        self.execution_technique = raw_list[1]
        self.size = raw_list[2]
        self.year = raw_list[3]

    def set_price(self, most_price_identifier_name: str, other_price_identifier_name: str,
                  most_price_identifier_type: str = "tag",
                  other_price_identifier_type: str = "class") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=most_price_identifier_type,
                                                    identifier_name=most_price_identifier_name)
        raw_most_price = ''.join((cur_string.text for cur_string in temp_list))
        self.most_price = raw_most_price

        temp_list = self.get_elements_by_identifier(identifier_type=other_price_identifier_type,
                                                    identifier_name=other_price_identifier_name)
        raw_other_price = '\n'.join((cur_string.text for cur_string in temp_list))
        self.other_price = raw_other_price

    def set_description(self, description_identifier_name: str, identifier_type: str = "class") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=description_identifier_name)
        raw_description = ''.join((cur_string.text for cur_string in temp_list))
        self.description = raw_description


def main():
    cur_driver = DRIVER
    cur_url = CATALOG_URL
    cur_catalog = CatalogPage(driver=cur_driver, url=cur_url)
    csv_head = ['author_info', 'image_name', 'execution_technique',
                'size', 'year', 'most_price', 'other_price', 'description']
    with open(f"{RESULT_SCV_NAME}.csv", 'w') as parsed_csv:
        writer = csv.writer(parsed_csv)
        writer.writerow(csv_head)

    while True:
        images_links_obj = cur_catalog.get_images_links(image_links_class_name="products-item-img")
        images_links = [image_link.get_attribute("href") for image_link in images_links_obj]

        for image_link in images_links:
            print(image_link)
            image_page = ImagePage(driver=cur_catalog.driver, url=image_link)
            # image_page.set_author_info(author_info_identifier_name="author-name_link")
            image_page.set_image_name(image_name_identifier_name="product-name")
            image_page.set_image_parameters(parameters_identifier_name="b")
            image_page.set_price(most_price_identifier_name="strong",
                                 other_price_identifier_name="other-price")
            image_page.set_description(description_identifier_name="product-text")

            parsed_dict = image_page.__dict__
            print(parsed_dict)

            parsed_list = [parsed_dict['author_info'], parsed_dict['image_name'],
                           parsed_dict['execution_technique'], parsed_dict['size'],
                           parsed_dict['year'], parsed_dict['most_price'],
                           parsed_dict['other_price'], parsed_dict['description']]
            with open(f"{RESULT_SCV_NAME}.csv", 'a') as parsed_csv:
                writer = csv.writer(parsed_csv)
                writer.writerow(parsed_list)

            image_page.driver.get(cur_catalog.url)
        break
        # try:
        #     cur_catalog.set_url_to_next_page("modern-page-next")
        #     cur_catalog.driver.get(cur_catalog.url)
        # except IndexError:
        #     break
    DRIVER.quit()

    # images = driver.find_elements_by_tag_name('img')
    # # for i in images:
    # #     src = i.get_attribute("src")
    # #     urllib.request.urlretrieve(src, f"{src.split('/')[-1]}")


if __name__ == "__main__":
    main()
    # print(pd.read_csv(f"{RESULT_SCV_NAME}.csv"))
