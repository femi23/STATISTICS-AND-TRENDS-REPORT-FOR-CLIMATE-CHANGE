# Library for data processing
import pandas as pd
import numpy as np
# Libraries for data visualisation 
import matplotlib.pyplot as plt
#import seaborn as sns


def read_file(filename):
 
    #read csv file
    orig_df = pd.read_csv(filename + '.csv')
    
    # transposes the dataframe and modifies it
    trans_df = orig_df.set_index('Country Name').T
    trans_df.columns = [ trans_df.columns,  trans_df.iloc[1].tolist() ]
    trans_df.drop(['Country Code','Indicator Name', 'Indicator Code'], axis=0, inplace=True)
    #trans_df = trans_df.apply(pd.to_numeric, errors='coerce')
    
    return orig_df, trans_df

#calling function to read csv file.
orig_df, trans_df = read_file('API_19_DS2_en_csv_v2_4700503')
row, col = orig_df.shape 
print(row, col)
print(f'there are {row} rows and {col} columns in the dataset')

## Lets take a look at the dataframes
print(orig_df.head())
print(trans_df.head())


# Let's look at all the indicators
inidicator_count = orig_df['Indicator Name'].nunique()
print(f'We have {inidicator_count} Indicators in this data set')
print(orig_df['Indicator Name'].unique())


# get statistical summary of several indicactors for different countries
def stat_summary(country, indicators):

    df = trans_df[country].describe()[indicators]
    return df


# indicators to investigate
chosen_indicator = ['Terrestrial and marine protected areas (% of total territorial area)', 'Total greenhouse gas emissions (kt of CO2 equivalent)', 'Disaster risk reduction progress score (1-5 scale; 5=best)', 'Electric power consumption (kWh per capita)', 'Arable land (% of land area)','Energy use (kg of oil equivalent per capita)', 'Ease of doing business rank (1=most business-friendly regulations)' ]

UK_stat = stat_summary('United Kingdom', chosen_indicator)
Germany_stat = stat_summary('Germany', chosen_indicator)
Canada_stat = stat_summary('Canada', chosen_indicator)
Saudi_stat = stat_summary('Saudi Arabia', chosen_indicator)
Kenya_stat = stat_summary('Kenya', chosen_indicator)
Brazil_stat = stat_summary('Brazil', chosen_indicator)
US_stat = stat_summary('United States', chosen_indicator)
print(UK_stat, Germany_stat, Canada_stat,Saudi_stat,Kenya_stat,Brazil_stat, US_stat, sep='\n\n')



def comp_countries_stat(countries, indicator):
 
    stat_country = list()
    for country in countries:
        stat = trans_df[country].describe()[indicator]
        stat.name = country
        stat_country.append(stat)
    summary_stat = pd.concat(stat_country, axis=1)
    
    return summary_stat


# cross-compare the gdp and electric power consumption between these countries
countries = ['Brazil', 'Germany', 'Kenya', 'United Kingdom', 'Canada', 'Saudi Arabia', 'United States' ]
gdp_stat = comp_countries_stat(countries, 'GDP (current US$)') 
power_consumption_stat = comp_countries_stat(countries, 'Electric power consumption (kWh per capita)')


print(gdp_stat, power_consumption_stat, sep='\n' )




 




