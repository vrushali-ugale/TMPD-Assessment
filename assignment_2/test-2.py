"""Script to read json files using pandas."""
import pandas as pd
import glob
import os

try:
    path = os.path.abspath(os.getcwd())
    all_files = glob.glob(path + "/sales_records/sale*.csv")
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    sorted_df = df.sort_values(by=['ID'])
    # print(sorted_df)
    sorted_df.to_csv("sales_records/all_sales.csv", index=False)
    print("Data added to csv file : sales_records/all_sales.csv")

    # csv_list = []
    # file_counter = 0
    # skiprow = 1
    # for filename in all_files:
    #     if file_counter > 0:
    #         skiprow = 0
    #     df = pd.read_csv(filename, skiprows=skiprow)
    #     csv_list.append(df)

    # df = pd.concat(csv_list, axis=0, ignore_index=True)
    # df.to_csv("sales_records/all_sales.csv", index=False)
    # print("Data added to csv file : sales_records/all_sales.csv")

except Exception as e:
    print("Error occurred in execution : {}".format(str(e)))
