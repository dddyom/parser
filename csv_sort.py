import csv
import pandas
import pandas as pd
import tools
from config import *
from Row import *

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
                     attr_dict['price']['price_3'], attr_dict['price']['price_3_currency'], attr_dict['genre'], attr_dict['product_link']]
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
        # csv_product = pd.read_csv(f"{CATALOG_NAME}_product.csv")

        if str(raw_data.iloc[i]["author_name"]) == "nan":
            continue
        else:
            unparsed_author_name = raw_data.iloc[i]["author_name"]
        cur_product = ProductRow(product_link=raw_data.iloc[i]["product_link"],product_id=i, product_name=raw_data.iloc[i]["image_name"],
                                 execution_technique=raw_data.iloc[i]["execution_technique"],
                                 size=raw_data.iloc[i]["size"],
                                 year=raw_data.iloc[i]["year"],
                                 price=raw_data.iloc[i]["price"],
                                 genre=raw_data.iloc[i]["genre"])
        # cur_product.set_product_id(csv_product)
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
    tools.sort_by_folders(SOURCE, CATALOG_NAME)
