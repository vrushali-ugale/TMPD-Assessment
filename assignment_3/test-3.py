"""Script to read json files using pandas."""
import pandas as pd
import glob
import os
from sqlalchemy import create_engine

class ForexTransaction:
    """Forex transactions."""
    def __init__(self):
        """Read forex rates from json file."""
        self.engine = create_engine('sqlite:///forexdb.db')
        self.forex_rate = None
        self.USD = {
            "AUD": 1.50,
            "EUR": 0.97,
            "GBP": 0.84,
        }

        self.AUD = {
            "EUR": 0.65,
            "GBP": 0.56,
            "USD": 0.67,
        }

        self.EUR = {
            "AUD": 1.55,
            "GBP": 0.87,
            "USD": 1.03,
        }

        self.GBP = {
            "AUD": 1.78,
            "EUR": 1.15,
            "USD": 1.19,
        }

    def save_to_db(self, currency_data):
        currency_data.to_sql('forex_data', self.engine, if_exists='append')
        print("Data saved in DB : forexdb.db --> forex_data")

    def show_forex_data(self):
        """Display forex data stored in DB."""
        output_str = "SRC | DEST | AMOUNT | C AMT |\n"
        outs = self.engine.execute('SELECT "source_currency", "destination_currency", "source_amount", "destination_amount"  FROM "forex_data"')
        for row in outs:
            output_str += row["source_currency"] + " | " + \
                row["destination_currency"] + " | " + \
                str(row["source_amount"]) + " | " + \
                str(row["destination_amount"]) + "\n"
        print("")
        print("*** Foreign exchange transaction requests ***")
        print(output_str)

    def get_input(self):
        """Read customer requests as input csv files."""
        try:
            self.df_master = pd.DataFrame()
            path = os.path.abspath(os.getcwd())
            all_files = glob.glob(path + "/customer_requests/format*/input*.csv")
            data = []
            if all_files:
                for f in all_files:
                    df = pd.read_csv(f, sep='[,|]', engine='python')
                    data.append(df)

                    # Rename processed files to not process again
                    file_name = os.path.basename(f)
                    file_name_new = "process_" + file_name
                    new_path = f.replace(file_name, file_name_new)
                    os.rename(f, new_path)

                # Concate csv file data in df
                df_master = pd.concat(
                    [dfi.rename({old: new for new, old in enumerate(dfi.columns)}, axis=1) \
                        for dfi in data], ignore_index=True
                )
                df_master[1] = df_master[1].str.strip()
                df_master[2] = df_master[2].str.strip()
                self.df_master = df_master
        except Exception as e:
            print("Error occurred in execution : {}".format(str(e)))

    def convert_currency(self):
        """Convert currecy as per the inputs and add destination currency to dataframe."""
        df = self.df_master
        for index, row in df.iterrows():

            source_currency = row[1]
            destination_currency = row[2]
            source_amount = row[3]
            destination_amount = 0

            if source_currency.strip() == "USD":
                destination_amount = self.USD[destination_currency] * source_amount

            if source_currency.strip() == "AUD":
                destination_amount = self.AUD[destination_currency] * source_amount

            if source_currency.strip() == "EUR":
                destination_amount = self.EUR[destination_currency] * source_amount

            if source_currency.strip() == "GBP":
                destination_amount = self.GBP[destination_currency] * source_amount

            df.loc[index, 4] = round(destination_amount, 2)

        # Rename columns and remove first column
        df = df.rename(columns={
            0: 'id',
            1: 'source_currency',
            2: 'destination_currency',
            3: 'source_amount',
            4: 'destination_amount'}
        )
        df = df.iloc[: , 1:]
        return df

if __name__ == "__main__":
    obj = ForexTransaction()
    obj.get_input()
    currency_data = obj.convert_currency()

    obj.save_to_db(currency_data)
    obj.show_forex_data()
