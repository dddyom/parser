from selenium.common.exceptions import InvalidArgumentException
from selenium import webdriver


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
        raw_personal_info_list = [string for string in raw_personal_info_list if string.strip()]
        try:
            self.years_of_life = raw_personal_info_list[0]
            self.place_of_residence = ', '.join(raw_personal_info_list[1:])
        except IndexError:
            self.years_of_life = None
            self.place_of_residence = None

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
        raw_list = [string for string in raw_list if string.strip()]
        if len(raw_list) == 4:
            self.execution_technique, self.size, self.year = raw_list[1], raw_list[2], raw_list[3]
        elif len(raw_list) == 3:
            self.execution_technique, self.size, self.year = raw_list[1], raw_list[2], None
        elif len(raw_list) == 2:
            self.execution_technique, self.size, self.year = raw_list[1], None, None
        else:
            self.execution_technique, self.size, self.year = None, None, None


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
