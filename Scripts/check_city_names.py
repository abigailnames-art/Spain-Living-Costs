import pandas as pd

files = {
    "Economic": "Data/Clean/economic_clean.csv",
    "Social": "Data/Clean/social_clean.csv",
    "Commuting": "Data/Clean/commuting_clean.csv",
    "Education": "Data/Clean/education_clean.csv",
    "Land": "Data/Clean/land_clean.csv",
    "Tourism": "Data/Clean/tourism_clean.csv",
    "Demography": "Data/Clean/demography_clean.csv"
}

city_sets = {}

for name, file in files.items():
    df = pd.read_csv(file)
    city_sets[name] = set(df["City"].dropna())

all_cities = set().union(*city_sets.values())

print("\nNumber of cities in each dataset:")
for name, cities in city_sets.items():
    print(f"{name}: {len(cities)}")

print("\nCities missing from each dataset:")

for name, cities in city_sets.items():
    missing = sorted(all_cities - cities)

    print(f"\n{name} is missing {len(missing)} cities:")

    for city in missing:
        print(f"  - {city}")