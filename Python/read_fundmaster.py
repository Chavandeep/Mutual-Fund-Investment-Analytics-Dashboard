import pyodbc
import pandas as pd

server = "localhost"
database = "MFInvestmentDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

conn = pyodbc.connect(connection_string)

query = """
SELECT *
FROM FundMaster
WHERE IsActive = 1;
"""

funds = pd.read_sql(query, conn)

print(funds)

conn.close()
