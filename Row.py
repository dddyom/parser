from typing import Dict
import math

class ProductRow:
    def __init__(self, product_link, product_id: int, product_name: str, execution_technique: str,
                 size: str, year: str, price: str, genre: str) -> None:
        self.product_link = product_link
        self.product_id: int = product_id
        self.author_id: int = None

        self.product_name: str = product_name
        self.execution_technique: str = execution_technique
        self.size: Dict = self.unraw_size(size)
        self.year: Dict = self.unraw_year(str(year))
        self.price: Dict = self.unraw_price(price)
        self.genre: str = genre

    # def set_product_id(self, csv_result: pd.DataFrame) -> int:
    #     if csv_result.empty:
    #         self.product_id = 0
    #
    #     else:
    #         self.product_id = int(csv_result.iloc[-1]["product_id"]) + 1
    #     return self.product_id

    def set_author_id(self, new_author_id):
        self.author_id = new_author_id

    @staticmethod
    def unraw_size(size: str) -> Dict:
        size_list = size.split()
        size_currency = size_list[-1]
        if len(size_list[:-1]) > 5:
            raise ValueError("unexpected size_list length")
        length = size_list[0].replace(',', '.') if len(size_list[:-1]) > 1 else None
        width = size_list[2].replace(',', '.') if len(size_list[:-1]) == 3 else None
        height = size_list[4].replace(',', '.') if len(size_list[:-1]) == 5 else None

        return {"length": length,
                "width": width,
                "height": height,
                "size_currency": size_currency}

    @staticmethod
    def unraw_year(year: str) -> Dict:
        try:
            if math.isnan(float(year)):
                year, year_1 = None, None
            elif len(year.split()) == 1:
                year, year_1 = year.split()[0], None
        except ValueError:
            try:
                year, year_1 = int(year.split('-')[0]), int(year.split('-')[-1])
            except ValueError:
                year, year_1 = year, None
        return {"year": year,
                "year_1": year_1}

    @staticmethod
    def unraw_price(price: str) -> Dict:
        price_list = price.split()
        if len(price_list) == 6:
            euro_price, dollar_price, ruble_price = price_list[0], price_list[2], price_list[4]
        elif len(price_list) == 7:
            euro_price = ''.join(price_list[:2])
            dollar_price, ruble_price = price_list[3], price_list[5]
        else:
            raise ValueError("unexpected price list length")

        return {"price_1": euro_price, "price_1_currency": "euro",
                "price_2": dollar_price, "price_2_currency": "dollar",
                "price_3": ruble_price, "price_3_currency": "ruble"}


class AuthorRow:
    def __init__(self, name: str, author_year: str, place_of_residence: str, author_description: str) -> None:
        self.author_id: int = None
        self.author_name: str = name
        self.author_year: Dict = self.unraw_author_year(author_year)
        self.place_of_residence: str = place_of_residence
        self.author_description: str = author_description

    def set_author_id(self, csv_result: pd.DataFrame) -> int:
        if csv_result.empty:
            self.author_id = 0
        else:
            self.author_id = int(csv_result.iloc[-1]["author_id"]) + 1
        return self.author_id

    @staticmethod
    def unraw_author_year(author_year: str) -> Dict:
        try:
            if math.isnan(float(author_year)):
                year_of_birth, year_of_death = None, None
            else:
                year_of_birth, year_of_death = int(author_year), None
        except ValueError:
            year_of_birth, year_of_death = author_year.split('-')[0], author_year.split('-')[-1]
        return {"year_of_birth": year_of_birth,
                "year_of_death": year_of_death}