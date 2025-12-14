import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================
# CONFIGURATION
# ==========================================
SERVER = 'localhost'
DATABASE = 'PortfolioProject'
USERNAME = 'sa'
PASSWORD = 'RealStrongPass123!'
FILE_NAME = 'NashvilleHousingDataforDataCleaning.xlsx'
TABLE_NAME = 'NashvilleHousing'

# ==========================================
# STEP 1: EXTRACT (Read Data from Excel)
# ==========================================
print(f"Reading {FILE_NAME}...")
try:
    # Read the Excel file
    df = pd.read_excel(FILE_NAME)
    print(f"Successfully read {len(df)} rows.")
except FileNotFoundError:
    print(f"ERROR: Could not find '{FILE_NAME}'. Make sure it is in the same folder as this script!")
    exit()

# ==========================================
# STEP 2: TRANSFORM (Basic Cleanup)
# ==========================================
# The "Nashville Housing" dataset is famously messy.
# We will convert all columns to String (Text) format first.
# This prevents the upload from failing if a "Date" column has a weird typo.
# You will fix the data types inside SQL later (that's the point of the project!)
df = df.astype(str)

# Replace "nan" (Python's null) with None (SQL's NULL)
df = df.replace('nan', None)

# ==========================================
# STEP 3: LOAD (Upload to SQL Server)
# ==========================================
print("Connecting to Database...")

# Connection String for Mac (using pymssql)
connection_string = f"mssql+pymssql://{USERNAME}:{PASSWORD}@{SERVER}:1433/{DATABASE}"

try:
    engine = create_engine(connection_string)
    
    print(f"Uploading to table '{TABLE_NAME}'... (This might take 30-60 seconds)")
    
    # 'replace': Drops table if it exists and creates a new one
    # 'chunksize': Uploads 500 rows at a time to keep it stable
    df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False, chunksize=500)
    
    print("✅ SUCCESS! Data Pipeline Finished.")
    print(f"Table '{TABLE_NAME}' is ready for cleaning.")

except Exception as e:
    print(f"❌ ERROR: {e}")