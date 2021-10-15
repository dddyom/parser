import os
import pathlib
import shutil


def check_csv_exist(csv_name: str):
    if os.path.exists(f"{csv_name}.csv"):
        return True


# def copy_to_dir(src: str, dst: str, pattern: str = '*'):
#     if not os.path.isdir(dst):
#         pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
#     for f in os.listdir(src):
#         if pattern in f:
#             shutil.copy(os.path.join(src, f), os.path.join(dst, f))


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
    from config import SOURCE, CATALOG_NAME

    sort_by_folders(SOURCE, catalog_name=CATALOG_NAME)
