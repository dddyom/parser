# import csv
import pandas as pd

# csv_head = ['author_name', 'image_name', 'execution_technique',
            # 'size', 'year', 'most_price', 'other_price', 'author_description']



data = pd.read_csv("zhivopis.csv")

# print(data)
# print(data.iloc[0]["author_name"] == data.iloc[1]["author_name"])


def main():
    author_csv_head = ['author_id', 'author_name', 'author_description', 'products']

    images_csv_head = ['product_id', 'product_name', 'execution_technique', 'size', 'year', 
                        'dollar_price', 'euro_price', 'ruble_price', 'author_id']
    
    for i in range(len(data)):
        # create new row product
        # product_id = (save to variable)
        if data[i]["author_name"] in csv_author["author_name"]:
            # change prod id in author row (product_id)
            # add author id to prod row
            continue
        # create new row author (add product_id)
        

    # with open(f"{RESULT_SCV_NAME}.csv", 'w') as parsed_csv:
    #     writer = csv.writer(parsed_csv)
    #     writer.writerow(csv_head)

if __name__ == "__main__":
    main()