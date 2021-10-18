import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CATALOG_LIST = ["zhivopis", "graphika", "portret", "object",
                "photographii", "collazh", "video",
                "printi", "abstraktsiya", "peyzazh"]

CATALOG_NAME = "raw_all"
CATALOG_URL = f"https://artzip.ru/catalog/{CATALOG_NAME}/"

RAW_CSV_HEAD = ['author_name', 'years_of_life', 'place_of_residence', 'author_description',
                'image_name', 'execution_technique', 'size', 'year', 'price', 'genre']

AUTHOR_HEAD = ['author_id', 'author_name',
               'year_of_birth', 'year_of_death',
               'place_of_residence', 'author_description']

PRODUCT_HEAD = ['product_id', 'author_id',
                'product_name',
                'execution_technique',
                'length', 'width', 'height', 'size_currency',
                'year', 'year_1',
                'price_1', 'price_1_currency',
                'price_2', 'price_2_currency',
                'price_3', 'price_3_currency', 'genre']

SOURCE = BASE_DIR + "/parser/"