# ==========================================================
# MUTUAL FUND TRANSACTION REGISTRATION
# ==========================================================

import pyodbc
import pandas as pd
from datetime import datetime

# ==========================================================
# SQL SERVER CONNECTION
# ==========================================================

server = "localhost"
database = "MFInvestmentDB"

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    # ------------------------------------------------------
    # LOAD ACTIVE FUNDS
    # ------------------------------------------------------

    query = """
    SELECT
        FundID,
        FundName
    FROM FundMaster
    WHERE IsActive = 1
    ORDER BY FundID;
    """

    funds = pd.read_sql(query, conn)

    print("\n" + "=" * 60)
    print("      MUTUAL FUND TRANSACTION REGISTRATION")
    print("=" * 60)

    print("\nAvailable Funds\n")

    for index, row in funds.iterrows():
        print(f"{row['FundID']}. {row['FundName']}")

    # ------------------------------------------------------
    # FUND SELECTION
    # ------------------------------------------------------

    try:
        fund_id = int(input("\nEnter Fund ID : "))
    except ValueError:
        print("\n❌ Invalid Fund ID.")
        continue

    if fund_id not in funds["FundID"].values:
        print("\n❌ Fund ID does not exist.")
        continue

    selected_fund = funds.loc[
        funds["FundID"] == fund_id,
        "FundName"
    ].values[0]

    print(f"\n✅ Selected Fund : {selected_fund}")

    # ------------------------------------------------------
    # TRANSACTION DATE
    # ------------------------------------------------------

    transaction_date = input(
        "\nEnter Transaction Date (dd-mm-yyyy): "
    )

    try:
        transaction_date = datetime.strptime(
            transaction_date,
            "%d-%m-%Y"
        ).date()

    except ValueError:
        print("\n❌ Invalid Date Format.")
        continue

    # ------------------------------------------------------
    # FETCH NAV
    # ------------------------------------------------------

    nav_query = """
    SELECT NAV
    FROM NAVHistory
    WHERE FundID = ?
    AND NAVDate = ?;
    """

    nav_df = pd.read_sql(
        nav_query,
        conn,
        params=[fund_id, transaction_date]
    )

    if nav_df.empty:
        print("\n❌ NAV not available for selected date. Possible reasons:Weekend, Matket holiday, Nav not loaded Yet")
        continue

    nav = float(nav_df.iloc[0]["NAV"])

    print(f"\n✅ NAV on {transaction_date.strftime('%d-%b-%Y')} : {nav:.4f}")

    # ------------------------------------------------------
    # TRANSACTION TYPE
    # ------------------------------------------------------

    print("\nTransaction Type")
    print("1. BUY")
    print("2. SELL")

    choice = input("\nEnter Choice (1/2): ")

    if choice == "1":
        transaction_type = "BUY"

    elif choice == "2":
        transaction_type = "SELL"

    else:
        print("\n❌ Invalid Choice.")
        continue

    # ------------------------------------------------------
    # TRANSACTION AMOUNT
    # ------------------------------------------------------

    try:
        amount = float(
            input("\nEnter Transaction Amount (₹): ")
        )

    except ValueError:
        print("\n❌ Invalid Amount.")
        continue

    if amount <= 0:
        print("\n❌ Amount must be greater than zero.")
        continue

    # ------------------------------------------------------
    # CALCULATE UNITS
    # ------------------------------------------------------

    units = round(amount / nav, 6)

    # ------------------------------------------------------
    # TRANSACTION SUMMARY
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print("               TRANSACTION SUMMARY")
    print("=" * 60)

    print(f"Fund Name        : {selected_fund}")
    print(f"Transaction Date : {transaction_date.strftime('%d-%b-%Y')}")
    print(f"Transaction Type : {transaction_type}")
    print(f"Amount           : ₹{amount:,.2f}")
    print(f"NAV              : {nav:.4f}")
    print(f"Units            : {units:.6f}")

    print("=" * 60)

    # ------------------------------------------------------
    # CONFIRM TRANSACTION
    # ------------------------------------------------------

    confirm = input(
        "\nConfirm Transaction? (Y/N): "
    ).upper()

    if confirm != "Y":
        print("\n❌ Transaction Cancelled.")

    else:

        insert_query = """
        INSERT INTO Transactions
        (
            FundID,
            TransactionDate,
            TransactionType,
            Amount,
            NAV,
            Units
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
        """

        try:

            cursor = conn.cursor()

            cursor.execute(
                insert_query,
                (
                    fund_id,
                    transaction_date,
                    transaction_type,
                    amount,
                    nav,
                    units
                )
            )

            conn.commit()

            print("\n✅ Transaction Registered Successfully!")

        except Exception as e:

            print(f"\n❌ Error : {e}")

        finally:

            cursor.close()

    # ------------------------------------------------------
    # ANOTHER TRANSACTION
    # ------------------------------------------------------

    again = input(
        "\nRegister Another Transaction? (Y/N): "
    ).upper()

    if again != "Y":
        break

# ==========================================================
# CLOSE CONNECTION
# ==========================================================

conn.close()

print("\n======================================")
print("Thank You!")
print("Transaction Utility Closed Successfully.")
print("======================================")
