# 🏠 Nashville Housing Data Cleaning Project

## 📌 Project Overview
This project demonstrates a data engineering and cleaning workflow using a raw real estate dataset. The goal was to transform "dirty" raw data into a standardized format usable for analysis.

Because this project was implemented on a **macOS** environment, standard Windows-based SQL tools (like the Import Wizard) were not natively available. To solve this, I containerized MS SQL Server using **Docker** and used a custom **Python script** to handle the data ingestion.

## 🛠 Tools & Technologies
* **Database:** Microsoft SQL Server 2022 (running via Docker Container)
* **Language:** T-SQL (for data cleaning)
* **ETL:** Python, Pandas, SQLAlchemy (for data ingestion)
* **Editor:** VS Code

## 🏗 Workflow

### Step 1: Data Ingestion (Python)
Since the database was running in a Linux Docker container on a Mac, I wrote a Python script (`etl_pipeline.py`) to handle the "Extract and Load" phase.
* **Problem:** Raw Excel data contained mixed data types that often fail standard import wizards.
* **Solution:** The script forces a conversion to string format (`astype(str)`) before loading. This ensured all raw data made it into the staging table without rejection, allowing me to handle type casting strictly within SQL.

### Step 2: Data Cleaning (SQL)
Once the data was loaded into SQL Server, I performed the following transformations using `project.sql`:

#### 1. Standardizing Date Formats
Converted the `SaleDate` column from a timestamp format to a standard Date format.
```sql
ALTER TABLE NashvilleHousing
ADD SaleDateConverted Date;

UPDATE NashvilleHousing
SET SaleDateConverted = CONVERT(Date, SaleDate);
```

#### 2. Populating Missing Address Data
Identified `NULL` values in the `PropertyAddress` column. I performed a **Self-Join** on the table to locate records where the same `ParcelID` existed but had a populated address, then used `ISNULL` to fill the missing data.
```sql
UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM NashvilleHousing a
JOIN NashvilleHousing b
    ON a.ParcelID = b.ParcelID
    AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress IS NULL;
```

#### 3. Parsing Long Addresses
The raw address data combined street, city, and state into single strings.
* Used `SUBSTRING` and `CHARINDEX` to separate Property Address into Address and City.
* Used `PARSENAME` and `REPLACE` to split Owner Address into Address, City, and State.

#### 4. Normalizing Fields
The `SoldAsVacant` column contained inconsistencies ('Y','N','Yes','No'). I used a `CASE` statement to standardize all values to 'Yes' and 'No'.

#### 5. Removing Duplicates
I used a CTE (Common Table Expression) combined with the `ROW_NUMBER()` window function to identify duplicate records based on unique identifiers (ParcelID, SalePrice, SaleDate, LegalReference).
```sql
WITH RowNumCTE AS(
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY ParcelID, PropertyAddress, SalePrice, SaleDate, LegalReference
            ORDER BY UniqueID
        ) row_num 
    FROM PortfolioProject.dbo.NashvilleHousing
)
DELETE FROM RowNumCTE
WHERE row_num > 1;
```

#### 6. Drop Unused Columns
Removed the raw, unformatted columns (`OwnerAddress`, `TaxDistrict`, `PropertyAddress`, `SaleDate`) to finalize teh clean schema.

## 📁 Files in this Repository
* `etl_pipeline.py`: The Python script used to connect to the Docker container and upload the raw Excel data.
* `Project.sql`: The T-SQL script containing the full cleaning logic.
* `README.md`: Project documentation.
