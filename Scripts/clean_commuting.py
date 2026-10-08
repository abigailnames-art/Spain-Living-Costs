import pandas as pd

# File locations
input_file = "Data/Raw/Commuting to Work.xlsx"
output_file = "Data/Clean/commuting_clean.csv"

# Read the Excel file
df = pd.read_excel(input_file, header=6)

# Rename the first column
df = df.rename(columns={df.columns[0]: "label"})

# Remove extra spaces
df["label"] = df["label"].astype(str).str.strip()

# Year columns
year_columns = df.columns[1:]

# Convert years to numbers
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove National Total
df = df[df["label"] != "National Total"].copy()

# Variables we want to keep
variables_to_keep = [
    "Average time of journey to work (minutes)",
    "Percentage of commutes to work by public transport (%)",
    "Proportion of journeys to work by foot (percentage)"
]

# Identify city rows
city_rows = (
    df[year_columns].isna().all(axis=1)
    & df["label"].shift(-1).eq(
        "Proportion of journeys to work by car (percentage)"
    )
)

# Create City column
df["City"] = df["label"].where(city_rows)
df["City"] = df["City"].ffill()

# Track which variable each Total row belongs to
current_variable = None
variable_groups = []

for label in df["label"]:
    if label in variables_to_keep:
        current_variable = label
    variable_groups.append(current_variable)

df["Variable"] = variable_groups

# Keep only Total rows for our selected variables
df = df[
    (df["label"] == "Total")
    & (df["Variable"].isin(variables_to_keep))
].copy()

# Calculate average using available years
df["Average"] = df[year_columns].mean(axis=1, skipna=True)

# Count available years
df["Years Available"] = df[year_columns].notna().sum(axis=1)

# Keep useful columns
cleaned = df[[
    "City",
    "Variable",
    "Average",
    "Years Available"
]]

# Turn variables into columns
cleaned = cleaned.pivot_table(
    index="City",
    columns="Variable",
    values=["Average", "Years Available"],
    aggfunc="mean"
)

# Make column names easier to read
cleaned.columns = [
    f"{variable}_{measure}"
    for measure, variable in cleaned.columns
]

# Turn City back into a regular column
cleaned = cleaned.reset_index()

# Save
cleaned.to_csv(output_file, index=False)

print("Commuting data cleaned successfully!")
print(f"Saved to: {output_file}")
print(f"Number of cities: {len(cleaned)}")
print("\nFirst 5 cities:")
print(cleaned.head())