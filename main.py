import sys
import pandas as pd
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.explore import load_data, basic_info, clean_locations
from src.visualize import (plot_top_cases, plot_global_trend, plot_death_rate,
                            plot_vaccination_rollout, plot_gdp_vs_vaccination,
                            plot_cases_by_continent, plot_reproduction_rate,
                            plot_icu_patients, plot_age_vs_deaths, plot_africa_vs_europe)
from src.database import create_database, query

DATA_PATH = 'data/owid-covid-data.csv'
DB_PATH = 'data/covid.db'

df = load_data(DATA_PATH)
basic_info(df)
df = clean_locations(df)
print(f"\nAfter cleaning: {df.shape}")
print(f"Countries remaining: {df['location'].nunique()}")

plot_top_cases(df)
plot_global_trend(df)
plot_death_rate(df)
plot_vaccination_rollout(df)
plot_gdp_vs_vaccination(df)
plot_cases_by_continent(df)
plot_reproduction_rate(df)
plot_icu_patients(df)
plot_age_vs_deaths(df)
plot_africa_vs_europe(df)

print("\nBuilding database...")
create_database(DATA_PATH, DB_PATH)

print("\n--- SQL Query Results ---")

top_cases = query(DB_PATH, """
    SELECT location, MAX(total_cases) as total_cases
    FROM covid
    WHERE continent IS NOT NULL
    GROUP BY location
    ORDER BY total_cases DESC
    LIMIT 10
""")
print("\nTop 10 countries by total cases:")
print(top_cases.to_string(index=False))

death_rate = query(DB_PATH, """
    SELECT location, MAX(total_deaths_per_million) as deaths_per_million
    FROM covid
    WHERE continent IS NOT NULL
    GROUP BY location
    ORDER BY deaths_per_million DESC
    LIMIT 10
""")
print("\nTop 10 countries by deaths per million:")
print(death_rate.to_string(index=False))

continent_vax = query(DB_PATH, """
    SELECT continent, ROUND(AVG(people_fully_vaccinated_per_hundred), 2) as avg_vax_rate
    FROM covid
    WHERE people_fully_vaccinated_per_hundred IS NOT NULL
    GROUP BY continent
    ORDER BY avg_vax_rate DESC
""")
print("\nAverage full vaccination rate by continent:")
print(continent_vax.to_string(index=False))

from src.visualize import (plot_top_cases, plot_global_trend, plot_death_rate,
                            plot_vaccination_rollout, plot_gdp_vs_vaccination,
                            plot_cases_by_continent, plot_reproduction_rate,
                            plot_icu_patients, plot_age_vs_deaths, plot_africa_vs_europe,
                            plot_interactive_vaccinations)

vax_data = query(DB_PATH, """
    SELECT iso_code, location, date, people_fully_vaccinated_per_hundred
    FROM covid
    WHERE people_fully_vaccinated_per_hundred IS NOT NULL
""")

vax_data['date'] = pd.to_datetime(vax_data['date'])
plot_interactive_vaccinations(vax_data)