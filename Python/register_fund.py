import pyodbc
from download_nav import get_nav_data

server = "localhost"
database = "MFInvestmentDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)
# Load AMFI data
df = get_nav_data()

# Ask user for Scheme Code
scheme_code = input("Enter Scheme Code: ")

# Search the fund
fund = df[df["Scheme Code"] == scheme_code]

if fund.empty:
    print("\n❌ Scheme Code not found.")

else:

    # Get values from DataFrame
    scheme_name = fund.iloc[0]["Scheme Name"]
    isin_growth = fund.iloc[0]["ISIN Div Payout/ ISIN Growth"]
    isin_reinvestment = fund.iloc[0]["ISIN Div Reinvestment"]

    # Detect AMC automatically
    if scheme_name.startswith("HDFC"):
        amc = "HDFC"
    elif scheme_name.startswith("ICICI"):
        amc = "ICICI"
    elif scheme_name.startswith("Nippon"):
        amc = "Nippon"
    else:
        amc = "Unknown"

    # Display fund details
    print("\nFund Details")
    print("-" * 50)
    print(f"Scheme Name        : {scheme_name}")
    print(f"AMC                : {amc}")
    print(f"ISIN Growth        : {isin_growth}")
    print(f"ISIN Reinvestment  : {isin_reinvestment}")

    # Collect business details
    print("\nBusiness Configuration")
    print("-" * 50)

    category = input("Enter Fund Category        : ")
    #below code is for the verify the sip day is in between 1st and 31st day of month
    while True:

        sip_day = input("Enter Configured SIP Day   : ")

        if sip_day.isdigit():

            sip_day = int(sip_day)

            if 1 <= sip_day <= 31:
                break

        print("❌ SIP Day must be between 1 and 31.")

# Below code is written to verify the threshold given is in correct format or not
    while True:

        threshold = input("Enter Alert Threshold      : ")

        try:

            threshold = float(threshold)

            break

        except ValueError:

            print("❌ Please enter a valid number.")

    # Confirmation Screen
    print("\n" + "=" * 60)
    print("FUND REGISTRATION SUMMARY")
    print("=" * 60)

    print(f"Scheme Code        : {scheme_code}")
    print(f"Scheme Name        : {scheme_name}")
    print(f"AMC                : {amc}")
    print(f"Category           : {category}")
    print(f"ISIN Growth        : {isin_growth}")
    print(f"ISIN Reinvestment  : {isin_reinvestment}")
    print(f"Configured SIP Day : {sip_day}")
    print(f"Alert Threshold    : {threshold}")

    confirm = input("\nRegister this fund? (Y/N): ")

    if confirm.upper() == "Y":

        conn = pyodbc.connect(connection_string)

        cursor = conn.cursor()

        insert_query = """
                       INSERT INTO FundMaster
                       (SchemeCode, \
                        FundName, \
                        AMC, \
                        FundCategory, \
                        ISINGrowth, \
                        ISINReinvestment, \
                        ConfiguredSIPDay, \
                        AlertThreshold)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?) \
                       """

        cursor.execute(
            insert_query,
            scheme_code,
            scheme_name,
            amc,
            category,
            isin_growth,
            isin_reinvestment,
            sip_day,
            threshold
        )

        conn.commit()

        cursor.close()
        conn.close()

        print("\n✅ Fund registered successfully!")

    else:

        print("\n❌ Registration cancelled.")
