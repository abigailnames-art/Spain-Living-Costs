import pandas as pd

# File locations
input_file = "Data/Raw/Economic Aspects.xlsx"
output_file = "Data/Clean/economic_clean.csv"

# Read the Excel file
df = pd.read_excel(input_file, header=6)

# Rename the first column
df = df.rename(columns={df.columns[0]: "label"})

# Remove extra spaces from the labels
df["label"] = df["label"].astype(str).str.strip()

# The remaining columns are years
year_columns = df.columns[1:]

# Convert year values to numbers
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove National Total
df = df[df["label"] != "National Total"].copy()

# Identify city rows
city_rows = df[year_columns].isna().all(axis=1)

# Create the City column
df["City"] = df["label"].where(city_rows)
df["City"] = df["City"].ffill()

# Variables we want to keep
variables_to_keep = [
    "Unemployment rate (percentage)",
    "Ratio of employed between 20-64 to economically active population (percentage)",
    "Economic activity rate (Percentage)",
    "Average annual net household income (Euros)",
    "Average disposable annual income per person (Euros)"
]

# Keep only our selected variables
df = df[df["label"].isin(variables_to_keep)].copy()

# Remove rows that don't belong to a city
df = df[df["City"].notna()].copy()

# Calculate average using available years only
df["Average"] = df[year_columns].mean(axis=1, skipna=True)

# Count how many years are available
df["Years Available"] = df[year_columns].notna().sum(axis=1)

# Keep the useful columns
cleaned = df[["City", "label", "Average", "Years Available"]]

# Turn variables into columns
cleaned = cleaned.pivot(
    index="City",
    columns="label",
    values=["Average", "Years Available"]
)

# Make column names easier to read
cleaned.columns = [
    f"{variable}_{measure}"
    for measure, variable in cleaned.columns
]

# Turn City back into a regular column
cleaned = cleaned.reset_index()

# Save the cleaned dataset
cleaned.to_csv(output_file, index=False)

print("Economic data cleaned successfully!")
print(f"Saved to: {output_file}")
print(f"Number of cities: {len(cleaned)}")
print("\nFirst 5 cities:")
print(cleaned.head())
