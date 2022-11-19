"""Script to read json files using pandas."""
import pandas as pd

try:
    # Read two json files
    df1 = pd.read_json("dummy_data_1.json")
    df2 = pd.read_json("dummy_data_2.json")

    # compare the columns for both json, if match concate and write to csv
    if list(df1.columns.values) == list(df2.columns.values):
        frames = [df1, df2]
        df_concat = pd.concat(frames)
        df_concat.to_csv("data.csv", index=False)
        print("Data added to csv file : data.csv")
except Exception as e:
    print("Error occurred in execution : {}".format(str(e)))
