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
chosen_indicator = ['Terrestrial and marine protected areas (% of total territorial area)', 
                    'Total greenhouse gas emissions (kt of CO2 equivalent)', 
                    'Disaster risk reduction progress score (1-5 scale; 5=best)', 
                    'Electric power consumption (kWh per capita)', 
                    'Arable land (% of land area)',
                    'Energy use (kg of oil equivalent per capita)', 
                    'Ease of doing business rank (1=most business-friendly regulations)' ]

UK_stat = stat_summary('United Kingdom', chosen_indicator)
Mexico_stat = stat_summary('Mexico', chosen_indicator)
US_stat = stat_summary('United States', chosen_indicator)
print(UK_stat, Mexico_stat, US_stat, sep='\n')


def comp_countries_stat(countries, indicator):
 
    stat_country = []
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

#Lets investigate how the different indicators for climate change influence each other
def plot_barchart(df, countries, indicator, start_year, end_year, increment):
 
    
    #filter dataframe to contain selected countries and indicator
    newdf = df[df['Country Name'].isin(countries)]
    newdf = newdf[newdf['Indicator Name'] == indicator]
    
    # To select year range between 1990 and 2015 for comparism among the countries.
    year_range = [str(year) for year in range(start_year, end_year+1, increment)]
    
    newdf = newdf[['Country Name'] + year_range]
    newdf.set_index('Country Name').plot.bar(figsize = (14,9)) 
    plt.xlabel('Country',fontweight ='bold', fontsize = 14)
    plt.ylabel(indicator,fontweight ='bold', fontsize = 14)
    plt.title(indicator, fontsize = 14)
    plt.savefig("bar chart.png")
    

# Plot trend of CO2 emission used from 1990 to 2015 at 5 years increment
plot_barchart(orig_df, countries, 'CO2 emissions (kg per PPP $ of GDP)', 1990, 2015, 5)

#line plot
def plot_line(df, countries, indicator, start_year, end_year, increment):

    newdf = df[df['Country Name'].isin(countries)]
    newdf = newdf[newdf['Indicator Name'] == indicator]
    
    #filter a specific year if that argument were enter
    if start_year or end_year:
        newdf = newdf[['Country Name'] + [str(year) for year in range(start_year, end_year+1, increment)]]
    
    newdf = newdf.set_index('Country Name').iloc[:, 3:].T
    print(newdf)
    newdf.columns.name = None
    
    newdf.plot( figsize=(12, 9))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Year',fontweight ='bold', fontsize = 16)
    plt.ylabel(indicator,fontweight ='bold', fontsize = 16)
    plt.title(indicator + ' trend', fontsize = 16)
    plt.savefig("lINE PLOT.png")
    plt.show()


# check whether the trend for energy used is similar at the continent level (North America) and compare with another region
location = countries + ['North America', 'Sub-Saharan Africa']
plot_line(orig_df, location, 'Energy use (kg of oil equivalent per capita)', 1990, 2015, 5)

 
