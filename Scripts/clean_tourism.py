import pandas as pd

# File locations
input_file = "Data/Raw/Tourism.xlsx"
output_file = "Data/Clean/tourism_clean.csv"

# Read the Excel file
df = pd.read_excel(input_file, header=6)

# Rename the first column
df = df.rename(columns={df.columns[0]: "label"})

# Remove extra spaces
df["label"] = df["label"].astype(str).str.strip()

# The remaining columns are years
year_columns = df.columns[1:]

# Convert values to numbers
# The "." entries are treated as missing values
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove National Total
df = df[df["label"] != "National Total"].copy()

# Variable we want to keep
variable_to_keep = "Number of annual tourist overnight stays (number)"

# Identify city rows
# Each city header is followed by the overnight-stays variable.
city_rows = (
    df[year_columns].isna().all(axis=1)
    & df["label"].shift(-1).eq(variable_to_keep)
)

# Create the City column
df["City"] = df["label"].where(city_rows)
df["City"] = df["City"].ffill()

# Keep only our selected variable
df = df[df["label"] == variable_to_keep].copy()

# Keep only rows that belong to a city
df = df[df["City"].notna()].copy()

# Calculate average using available years only
df["Average"] = df[year_columns].mean(axis=1, skipna=True)

# Count how many years are available
df["Years Available"] = df[year_columns].notna().sum(axis=1)

# Keep useful columns
cleaned = df[[
    "City",
    "label",
    "Average",
    "Years Available"
]]

# Rename the variable column
cleaned = cleaned.rename(columns={
    "label": "Variable"
})

# Save the cleaned dataset
cleaned.to_csv(output_file, index=False)

print("Tourism data cleaned successfully!")
print(f"Saved to: {output_file}")
print(f"Number of cities: {len(cleaned)}")
print("\nFirst 5 cities:")
print(cleaned.head())