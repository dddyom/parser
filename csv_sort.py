import csv
import pandas
import pandas as pd
from typing import Dict
import tools
from config import *


class ProductRow:
    def __init__(self, product_name: str, execution_technique: str, size: str, year: str, price: str) -> None:
        self.product_id: int = None
        self.author_id: int = None

        self.product_name: str = product_name
        self.execution_technique: str = execution_technique
        self.size: Dict = self.unraw_size(size)
        self.year: Dict = self.unraw_year(year)
        self.price: Dict = self.unraw_price(price)

    def set_product_id(self, csv_result: pd.DataFrame) -> int:
        if csv_result.empty:
            self.product_id = 0

        else:
            self.product_id = int(csv_result.iloc[-1]["product_id"]) + 1
        return self.product_id

    def set_author_id(self, new_author_id):
        self.author_id = new_author_id

    @staticmethod
    def unraw_size(size: str) -> Dict:
        size_list = size.split()
        size_currency = size_list[-1]
        if len(size_list[:-1]) > 5:
            raise ValueError("unexpected size_list length")
        length = size_list[0] if len(size_list[:-1]) > 1 else None
        width = size_list[2] if len(size_list[:-1]) == 3 else None
        height = size_list[4] if len(size_list[:-1]) == 5 else None

        return {"length": length,
                "width": width,
                "height": height,
                "size_currency": size_currency}

    @staticmethod
    def unraw_year(year: str) -> Dict:
        if isinstance(year, float):
            year, year_1 = None, None
        elif len(year.split()) == 1:
            year, year_1 = year.split()[0], None
        else:
            year, year_1 = year.split('-')[0], year.split('-')[-1]
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
        if isinstance(author_year, float):
            year_of_birth, year_of_death = None, None
        elif len(author_year) == 4:
            year_of_birth, year_of_death = author_year, None
        else:
            year_of_birth, year_of_death = author_year.split('-')[0], author_year.split('-')[-1]
        return {"year_of_birth": year_of_birth,
                "year_of_death": year_of_death}


def init_sorted_csv(name: str, head: list) -> pandas.DataFrame:
    with open(f"{name}.csv", 'w') as parsed_csv:
        writer = csv.writer(parsed_csv)
        writer.writerow(head)
    return pd.read_csv(f"{name}.csv")


def write_by_dict(catalog_name, attr_dict, csv_type):
    if csv_type == "product":

        attr_list = [attr_dict['product_id'], attr_dict['author_id'], attr_dict["product_name"],
                     attr_dict['execution_technique'],
                     attr_dict['size']['length'], attr_dict['size']['width'], attr_dict['size']['height'],
                     attr_dict['size']['size_currency'],
                     attr_dict['year']['year'], attr_dict['year']['year_1'],
                     attr_dict['price']['price_1'], attr_dict['price']['price_1_currency'],
                     attr_dict['price']['price_2'], attr_dict['price']['price_2_currency'],
                     attr_dict['price']['price_3'], attr_dict['price']['price_3_currency']]
    else:  # "author"
        attr_list = [attr_dict['author_id'], attr_dict['author_name'],
                     attr_dict['author_year']['year_of_birth'], attr_dict['author_year']['year_of_death'],
                     attr_dict['place_of_residence'], attr_dict['author_description'], ]

    with open(f"{catalog_name}_{csv_type}.csv", 'a') as result_csv:
        writer = csv.writer(result_csv)
        writer.writerow(attr_list)


def main():
    if not tools.check_csv_exist(csv_name=CATALOG_NAME):
        raise FileNotFoundError(f"{CATALOG_NAME}.csv does not exist")
    raw_data = pd.read_csv(f"{CATALOG_NAME}.csv")

    if not tools.check_csv_exist(csv_name=f"{CATALOG_NAME}_author"):
        init_sorted_csv(f"{CATALOG_NAME}_author", AUTHOR_HEAD)
    if not tools.check_csv_exist(csv_name=f"{CATALOG_NAME}_product"):
        init_sorted_csv(f"{CATALOG_NAME}_product", PRODUCT_HEAD)

    for i in range(len(raw_data)):
        csv_author = pd.read_csv(f"{CATALOG_NAME}_author.csv")
        csv_product = pd.read_csv(f"{CATALOG_NAME}_product.csv")

        unparsed_author_name = raw_data.iloc[i]["author_name"]
        cur_product = ProductRow(product_name=raw_data.iloc[i]["image_name"],
                                 execution_technique=raw_data.iloc[i]["execution_technique"],
                                 size=raw_data.iloc[i]["size"],
                                 year=raw_data.iloc[i]["year"],
                                 price=raw_data.iloc[i]["price"])
        # cur_product.set_product_id(csv_product)
        cur_product.product_id = i

        if unparsed_author_name in list(csv_author["author_name"]):
            author_id = list(csv_author.loc[csv_author["author_name"] == unparsed_author_name, 'author_id'])[-1]
            cur_product.set_author_id(author_id)

            write_by_dict(catalog_name=CATALOG_NAME,
                          attr_dict=cur_product.__dict__, csv_type="product")
            continue
        cur_author = AuthorRow(name=raw_data.iloc[i]["author_name"],
                               author_year=raw_data.iloc[i]["years_of_life"],
                               place_of_residence=raw_data.iloc[i]["place_of_residence"],
                               author_description=raw_data.iloc[i]["author_description"])
        author_id = cur_author.set_author_id(csv_author)
        cur_product.set_author_id(author_id)

        write_by_dict(catalog_name=CATALOG_NAME,
                      attr_dict=cur_product.__dict__, csv_type="product")

        write_by_dict(catalog_name=CATALOG_NAME,
                      attr_dict=cur_author.__dict__, csv_type="author")


if __name__ == "__main__":
    main()
