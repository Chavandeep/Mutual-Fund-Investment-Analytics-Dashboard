import pyodbc

server = 'localhost'
database = 'MFInvestmentDB'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(connection_string)
    print("✅ Connected Successfully!")
    conn.close()
except Exception as e:
    print("❌ Error:", e)
