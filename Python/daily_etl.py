from download_nav import get_nav_data
import pyodbc
import pandas as pd
import time
import os
from datetime import datetime

# ==========================
# Start Timer
# ==========================
start_time = time.time()

# ==========================git add .
# Log File Setup
# ==========================
log_folder = "logs"

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(
    log_folder,
    f"{datetime.now().strftime('%Y-%m-%d')}.log"
)

def write_log(message):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(message + "\n")

write_log("")
write_log("=" * 50)
write_log("MF DAILY NAV ETL")
write_log(f"Started : {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
write_log("=" * 50)

# ==========================
# SQL Server Connection
# ==========================
server = "localhost"
database = "MFInvestmentDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

# ==========================
# Read FundMaster
# ==========================
try:
    conn = pyodbc.connect(connection_string)

    query = """
    SELECT
        FundID,
        SchemeCode
    FROM FundMaster
    WHERE IsActive = 1;
    """

    fund_master = pd.read_sql(query, conn)
    conn.close()

except Exception as e:
    write_log("STATUS : FAILED")
    write_log("Unable to read FundMaster from SQL Server.")
    write_log(str(e))
    write_log("=" * 50)

    print("\n❌ Unable to read FundMaster from SQL Server.")
    print(e)
    raise SystemExit

# ==========================
# Download AMFI NAV
# ==========================
try:
    nav_data = get_nav_data()

except Exception as e:
    write_log("STATUS : FAILED")
    write_log("Unable to download AMFI NAV file.")
    write_log(str(e))
    write_log("=" * 50)

    print("\n❌ Unable to download AMFI NAV file.")
    print(e)
    raise SystemExit

print(f"\nAMFI Records    : {len(nav_data)}")
print(f"Tracked Funds   : {len(fund_master)}")

# ==========================
# Prepare Data
# ==========================
fund_master["SchemeCode"] = fund_master["SchemeCode"].astype(str)
nav_data["Scheme Code"] = nav_data["Scheme Code"].astype(str)

nav_data.rename(
    columns={"Scheme Code": "SchemeCode"},
    inplace=True
)

# ==========================
# Merge Data
# ==========================
try:
    merged_df = pd.merge(
        fund_master,
        nav_data,
        on="SchemeCode",
        how="inner"
    )

    merged_df["Date"] = pd.to_datetime(
        merged_df["Date"],
        format="%d-%b-%Y"
    ).dt.date

except Exception as e:
    write_log("STATUS : FAILED")
    write_log("Error while merging data.")
    write_log(str(e))
    write_log("=" * 50)

    print("\n❌ Error while merging data.")
    print(e)
    raise SystemExit

print(f"\nMerged Records : {len(merged_df)}")
print(f"Processed {len(merged_df)} fund(s).")

# ==========================
# Load NAVHistory
# ==========================
inserted = 0
skipped = 0
status = "SUCCESS"

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO NAVHistory
    (
        FundID,
        NAV,
        NAVDate
    )
    VALUES (?, ?, ?)
    """

    for _, row in merged_df.iterrows():
        try:
            cursor.execute(
                insert_query,
                row["FundID"],
                row["Net Asset Value"],
                row["Date"]
            )
            inserted += 1

        except pyodbc.IntegrityError:
            skipped += 1
            print(
                f"Skipped - NAV already exists for "
                f"FundID {row['FundID']} "
                f"on {row['Date']}"
            )

    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    status = "FAILED"

    write_log("STATUS : FAILED")
    write_log("Unable to insert NAV data into SQL Server.")
    write_log(str(e))
    write_log("=" * 50)

    print("\n❌ Unable to insert NAV data into SQL Server.")
    print(e)

# ==========================
# ETL Summary
# ==========================
end_time = time.time()
execution_time = end_time - start_time

print("\n=========================================")
print("        MF DAILY NAV ETL")
print("=========================================")
print(f"AMFI Records      : {len(nav_data)}")
print(f"Tracked Funds     : {len(fund_master)}")
print(f"Merged Records    : {len(merged_df)}")
print(f"Inserted          : {inserted}")
print(f"Skipped           : {skipped}")
print(f"\nExecution Time    : {execution_time:.2f} seconds")
print(f"\nSTATUS            : {status}")
print("=========================================")

write_log(f"AMFI Records      : {len(nav_data)}")
write_log(f"Tracked Funds     : {len(fund_master)}")
write_log(f"Merged Records    : {len(merged_df)}")
write_log(f"Inserted          : {inserted}")
write_log(f"Skipped           : {skipped}")
write_log(f"Execution Time    : {execution_time:.2f} seconds")
write_log(f"STATUS            : {status}")
write_log(f"Finished          : {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
write_log("=" * 50)
