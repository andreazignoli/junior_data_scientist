import pandas as pd

'''
The task involves calculating the crude death rate and age-standardized death rate for chronic obstructive pulmonary disease (COPD) in the United States and Uganda for 2019. To accomplish this, we require the following data:

1. Age-specific death rates from COPD in both the United States and Uganda.
2. Population data for both countries for 2019.
3. Standard population data

With the provided data, we can proceed as follows:

Compute the crude death rate for each country by aggregating the age-specific death rates.
Calculate the age-standardized death rate for each country utilizing age-standardization methodologies.
'''

# Practical considerations
# Read data provided in the application website
# Download data about total world population from https://population.un.org/wpp/Download/Standard/MostUsed/ and then use it to grab population data for US and Uganda
# Extract the value for 2019

# Read how age standardisation works at 
# https://cdn.who.int/media/docs/default-source/gho-documents/global-health-estimates/gpe_discussion_paper_series_paper31_2001_age_standardization_rates.pdf

try:
    # Executing from repo dir
    df_death_rates = pd.read_csv('../data/death_rates_COPD.csv')
    df_population = pd.read_csv('../data/USA_UG_population.csv')
    df_standard = pd.read_csv('../data/standard_population.csv')

except:
    # Executing from src dir
    df_death_rates = pd.read_csv('data/death_rates_COPD.csv')
    df_population = pd.read_csv('data/USA_UG_population.csv')
    df_standard = pd.read_csv('data/standard_population.csv')

# Grab 2019 population (in 100,000s)
us_population = df_population['tot_population'][(df_population['country']=='United States of America') & (df_population['year']==2019)].values[0]/100000
ug_population = df_population['tot_population'][(df_population['country']=='Uganda') & (df_population['year']==2019)].values[0]/100000

# Calculate the crude death rate for each country
us_crude_death_rate = df_death_rates['Death rate, United States, 2019'].sum()
uganda_crude_death_rate = df_death_rates['Death rate, Uganda, 2019'].sum()

# Bind the dfs
merged_df = pd.merge(df_death_rates, df_standard, on='age_group', how='inner')

# You calculate the weighted sum of age-specific rates using the standard population
us_weighted_sum = (merged_df['WHO'] * merged_df['Death rate, United States, 2019']).sum()
uganda_weighted_sum = (merged_df['WHO'] * merged_df['Death rate, Uganda, 2019']).sum()

# Normalize by the total population of each country
us_age_standardized_death_rate = (us_weighted_sum / us_population)
uganda_age_standardized_death_rate = (uganda_weighted_sum / ug_population)

# Print the results
print("Crude Death Rate (COPD) - United States: {:.1f} per 100,000 people".format(us_crude_death_rate))
print("Crude Death Rate (COPD) - Uganda: {:.1f} per 100,000 people".format(uganda_crude_death_rate))
print("Age-Standardized Death Rate (COPD) - United States: {:.1f} per 100,000 people".format(us_age_standardized_death_rate))
print("Age-Standardized Death Rate (COPD) - Uganda: {:.1f} per 100,000 people".format(uganda_age_standardized_death_rate))
