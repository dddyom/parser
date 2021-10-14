import os


def check_csv_exist(csv_name):
    if os.path.exists(f"{csv_name}.csv"):
        return True

