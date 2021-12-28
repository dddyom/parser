import os
import pathlib
import shutil
import pandas as pd
import numpy as np

def check_csv_exist(csv_name: str):
    if os.path.exists(f"{csv_name}.csv"):
        return True


# def copy_to_dir(src: str, dst: str, pattern: str = '*'):
#     if not os.path.isdir(dst):
#         pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
#     for f in os.listdir(src):
#         if pattern in f:
#             shutil.copy(os.path.join(src, f), os.path.join(dst, f))

def merge_csv(csv_list):
    df = pd.concat(map(pd.read_csv, [f"csv/raw/{single_csv}.csv" for single_csv in csv_list]), ignore_index=True)
    df.to_csv("raw_all.csv", index=False)


def move_dir(src: str, dst: str, pattern: str = '*'):
    if not os.path.isdir(dst):
        pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(src):
        if pattern in f:
            shutil.move(os.path.join(src, f), os.path.join(dst, f))


def sort_by_folders(source: str, catalog_name: str) -> None:
    product_dst = os.path.normpath(source + '/csv/' + catalog_name)
    author_dst = os.path.normpath(source + '/csv/' + catalog_name)
    raw_dst = os.path.normpath(source + '/csv/raw/')
    move_dir(source, product_dst, pattern='_product.csv')
    move_dir(source, author_dst, pattern='_author.csv')
    move_dir(source, raw_dst, pattern=f"{catalog_name}.csv")


if __name__ == "__main__":
    from config import SOURCE, CATALOG_NAME, CATALOG_LIST
    merge_csv(CATALOG_LIST)
    sort_by_folders(SOURCE, catalog_name=CATALOG_NAME)
    # df = pd.read_csv("csv/all/all_product.csv")
    # for i in range(len(df)):
    #     # print(df.iloc[i])
    #     try:
    #         a = int(df.iloc[i]["length"])
    #     except ValueError:
    #         df.iloc[i]["length"] = None

    # for i in df["length"]:
    #     print(i)

    # df.to_csv("product.csv", index=False)