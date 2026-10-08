import pandas as pd

# File locations
input_file = "Data/Raw/Training and Education.xlsx"
output_file = "Data/Clean/education_clean.csv"

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

# Variable we want to keep
variable_to_keep = (
    "Proportion of population aged 25-64 with ISCED level 5, 6, 7 or 8 "
    "as the highest level of education (percentage)"
)

# Identify city rows
# Each city header is followed by the day care/school variable.
city_rows = (
    df[year_columns].isna().all(axis=1)
    & df["label"].shift(-1).eq(
        "Proportion of children of 0-4 over the persons between 0-4 in day care or school"
    )
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

print("Education data cleaned successfully!")
print(f"Saved to: {output_file}")
print(f"Number of cities: {len(cleaned)}")
print("\nFirst 5 cities:")
print(cleaned.head())