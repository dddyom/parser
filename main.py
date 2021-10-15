import csv
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException


import tools
from config import *

DRIVER = webdriver.Chrome(f"{BASE_DIR}/parser/chromedriver")


class SitePage:
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


class AuthorPage(SitePage):
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:
        try:
            super().__init__(driver=driver, url=url)
            self.driver.get(self._url)

            self.author_name = None
            self.years_of_life = None
            self.place_of_residence = None
            self.author_description = None

            self.set_author_name("h1")
            self.set_personal_info("small")
            self.set_author_description("text-slide")
        except InvalidArgumentException:
            self.author_name = None
            self.years_of_life = None
            self.place_of_residence = None
            self.author_description = None

    def set_author_name(self, author_name_identifier_name: str, identifier_type: str = "tag") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=author_name_identifier_name)
        raw_author_name = ''.join((cur_string.text for cur_string in temp_list))
        self.author_name = ' '.join(raw_author_name.split(' ')[3:])

    def set_personal_info(self, personal_info_identifier_name: str, identifier_type: str = "tag") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=personal_info_identifier_name)
        raw_personal_info = ''.join((cur_string.text for cur_string in temp_list))
        raw_personal_info_list = raw_personal_info.replace(',', '').split(' ')
        self.years_of_life = raw_personal_info_list[0]
        self.place_of_residence = ', '.join(raw_personal_info_list[1:])

    def set_author_description(self, description_identifier_name: str, identifier_type: str = "class") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=identifier_type,
                                                    identifier_name=description_identifier_name)
        raw_description = ''.join((cur_string.text for cur_string in temp_list))
        self.author_description = raw_description.replace('\n', ' ')


class ImagePage(SitePage):
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:
        super().__init__(driver=driver, url=url)
        self.driver.get(self._url)

        self.image_name = None
        self.execution_technique = None
        self.size = None
        self.year = None
        self.price = None

        self.set_image_name(image_name_identifier_name="product-name")
        self.set_image_parameters(parameters_identifier_name="b")
        self.set_price(most_price_identifier_name="strong",
                       other_price_identifier_name="other-price")

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
        try:
            self.execution_technique = raw_list[1]
            self.size = raw_list[2]
            self.year = raw_list[3]
        except IndexError:
            print(raw_image_parameters, self.image_name)
    def set_price(self, most_price_identifier_name: str, other_price_identifier_name: str,
                  most_price_identifier_type: str = "tag",
                  other_price_identifier_type: str = "class") -> None:
        temp_list = self.get_elements_by_identifier(identifier_type=most_price_identifier_type,
                                                    identifier_name=most_price_identifier_name)
        raw_most_price = ''.join((cur_string.text for cur_string in temp_list))

        temp_list = self.get_elements_by_identifier(identifier_type=other_price_identifier_type,
                                                    identifier_name=other_price_identifier_name)
        raw_other_price = ' '.join((cur_string.text for cur_string in temp_list))
        self.price = raw_most_price + ' ' + raw_other_price


def main():
    cur_catalog = CatalogPage(driver=DRIVER, url=CATALOG_URL)
    if not tools.check_csv_exist(f"{CATALOG_NAME}"):
        with open(f"{CATALOG_NAME}.csv", 'w') as parsed_csv:
            writer = csv.writer(parsed_csv)
            writer.writerow(RAW_CSV_HEAD)
    page_counter = 0
    image_counter = 0
    while True:
        print(f"page count: {page_counter}, image count: {image_counter}")
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
                           image_dict["size"], image_dict["year"], image_dict["price"]]
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
    # pass
