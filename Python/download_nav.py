import requests
import pandas as pd
from io import StringIO


def get_nav_data():

    url = "https://www.amfiindia.com/spages/NAVAll.txt"

    response = requests.get(url)

    data = StringIO(response.text)

    df = pd.read_csv(
        data,
        sep=";",
        on_bad_lines="skip"
    )

    df = df.dropna(subset=["Net Asset Value"])

    return df

if __name__ == "__main__":

    df = get_nav_data()
    print("AMFI NAV download successful.")
    print(f"Rows: {len(df)}")
