import pandas as pd

# File locations
input_file = "Data/Raw/Demography.xlsx"
output_file = "Data/Clean/demography_clean.csv"

# Read the Excel file
df = pd.read_excel(input_file, header=6)

# Rename the first column
df = df.rename(columns={df.columns[0]: "label"})

# Remove extra spaces from labels
df["label"] = df["label"].astype(str).str.strip()

# The remaining columns are years
year_columns = df.columns[1:]

# Convert year values to numbers
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove National Total
df = df[df["label"] != "National Total"].copy()

print(df[df["label"].str.contains("Life expectancy", case=False, na=False)].head(20))

# Identify city rows
# Each city header is followed by "Resident population (Persons)"
city_rows = (
    df[year_columns].isna().all(axis=1)
    & df["label"].shift(-1).eq("Resident population (Persons)")
)

# Create the City column
df["City"] = df["label"].where(city_rows)
df["City"] = df["City"].ffill()

# Identify the TOTAL row directly underneath
# "Life expectancy at birth (years)"
life_expectancy_total = (
    (df["label"] == "Total")
    & (df["label"].shift(1) == "Life expectancy at birth (years)")
)

# Keep only the Total life expectancy rows
df = df[life_expectancy_total].copy()

# Keep only rows that belong to a city
df = df[df["City"].notna()].copy()

# Calculate average using available years only
df["Average"] = df[year_columns].mean(axis=1, skipna=True)

# Count how many years are available
df["Years Available"] = df[year_columns].notna().sum(axis=1)

# Add the variable name
df["Variable"] = "Life expectancy at birth (years)"

# Keep useful columns
cleaned = df[[
    "City",
    "Variable",
    "Average",
    "Years Available"
]]

# Save the cleaned dataset
cleaned.to_csv(output_file, index=False)

print("Demography data cleaned successfully!")
print(f"Saved to: {output_file}")
print(f"Number of cities: {len(cleaned)}")
print("\nFirst 5 cities:")
print(cleaned.head())