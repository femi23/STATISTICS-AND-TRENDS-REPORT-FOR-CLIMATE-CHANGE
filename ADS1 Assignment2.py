# Library for data processing
import pandas as pd
import numpy as np
import scipy as sp

# Libraries for data visualisation 
import matplotlib.pyplot as plt
import seaborn as sns


#Define a function that reads, transposes the dataframe and modifies it.
def read_file(filename):
    '''
        Takes a string which represents the file name of the dataset in csv format and returns a pandas dataframe in 
        the original and a transposed format
        
        Args:
            filename => str, representing the name of csv file
        Returns:
            original_df => pandas.Dataframe, original format
            transposed_df => pandas.Dataframe, tranposed format     
    '''
    #read csv file
    orig_df = pd.read_csv(filename + '.csv')
    
    # transposes the dataframe and modifies it
    trans_df = orig_df.set_index('Country Name').T
    trans_df.columns = [ trans_df.columns,  trans_df.iloc[1].tolist() ]
    trans_df.drop(['Country Code','Indicator Name', 'Indicator Code'], axis=0, inplace=True)
    trans_df = trans_df.apply(pd.to_numeric, errors='coerce')
    
    return orig_df, trans_df

#calling function to read csv file.
orig_df, trans_df = read_file('API_19_DS2_en_csv_v2_4700503')
row, col = orig_df.shape 

print(f'there are {row} rows and {col} columns in the dataset')

## Lets take a look at the dataframes
print(orig_df.head())
print(trans_df.head())


# Let's look at all the indicators
inidicator_count = orig_df['Indicator Name'].nunique()
print(f'We have {inidicator_count} Indicators in this data set')
print(orig_df['Indicator Name'].unique())


# get statistical summary of several indicators for different chosen countries
def stat_summary(country, indicators):
    '''
        Explore the statistical properties of a few indicators for a country
        
        Args:
            country => str, chosen country
            indicators => list, preferred indicators
        Returns:
            summary_stat => pandas.Dataframe, a statistical summary of the selected indicators for a country 
    '''
    df = trans_df[country].describe()[indicators]
    return df


# indicators to investigate for different chosen countries
chosen_indicator = ['Terrestrial and marine protected areas (% of total territorial area)', 'Total greenhouse gas emissions (kt of CO2 equivalent)', 'Disaster risk reduction progress score (1-5 scale; 5=best)', 'Electric power consumption (kWh per capita)', 'Arable land (% of land area)','Energy use (kg of oil equivalent per capita)', 'Ease of doing business rank (1=most business-friendly regulations)' ]

UK_stat = stat_summary('United Kingdom', chosen_indicator)
Germany_stat = stat_summary('Germany', chosen_indicator)
Canada_stat = stat_summary('Canada', chosen_indicator)
Saudi_stat = stat_summary('Saudi Arabia', chosen_indicator)
Kenya_stat = stat_summary('Kenya', chosen_indicator)
Brazil_stat = stat_summary('Brazil', chosen_indicator)
US_stat = stat_summary('United States', chosen_indicator)
print(UK_stat, Germany_stat, Canada_stat,Saudi_stat,Kenya_stat,Brazil_stat, US_stat, sep='\n\n')

# function to cross-compare the gdp and electric power consumption between these countries
def comp_countries_stat(countries, indicator):
    '''
        compares the statistical properties of an indicators accross different countries
        
        Args:
            countries => list, representing the list of countries to compare indicator activities
            indicator => str, representing indicators for comparison
        Returns:
            summary_stat => pandas.Dataframe, a statistical summary of the selected countries 
    '''
    stat_country = list()
    for country in countries:
        stat = trans_df[country].describe()[indicator]
        stat.name = country
        stat_country.append(stat)
    summary_stat = pd.concat(stat_country, axis=1)
    
    return summary_stat


# cross-compare the gdp and electric power consumption between these countries
countries = [ 'Brazil', 'Germany', 'Kenya', 'United Kingdom', 'Canada', 'Saudi Arabia', 'United States' ]
gdp_stat = comp_countries_stat(countries, 'GDP (current US$)') 
power_consumption_stat = comp_countries_stat(countries, 'Electric power consumption (kWh per capita)')
print('GDP Statistics', gdp_stat, 'Power_consumption_stat', power_consumption_stat, sep='\n\n' )


#Lets investigate how the different indicators for climate change influence each other
def plot_barchart(df, countries, indicator, start_year, end_year, increment):
    '''
        Plots a barchart showing the indicator performance of chosen countries over a range of years
        
        Args:
            df => pandas.Dataframe, original format
            countries => list, of countries of interest
            indicator => str, selected indicator
            start_year => int, year to start plot from
            end_year => int, year to end plot
            increment => years increment for plot
        Returns:
            plot => barchart 
    '''
    
    #filter dataframe to contain selected countries and indicator
    newdf = df[df['Country Name'].isin(countries)]
    newdf = newdf[newdf['Indicator Name'] == indicator]
    
    # To select year range between 1990 and 2015 for comparism among the countries.
    year_range = [str(year) for year in range(start_year, end_year+1, increment)]
    
    newdf = newdf[['Country Name'] + year_range]
    newdf.set_index('Country Name').plot.bar(figsize = (12,9)) 
    plt.xlabel('Country',fontweight ='bold', fontsize = 16)
    plt.ylabel(indicator,fontweight ='bold', fontsize = 16)
    plt.title(indicator,fontweight ='bold', fontsize = 16)
    plt.savefig("bar chart.png")
    

# Plot trend of CO2 emission, Total greenhouse gas emission and Energy used from 1990 to 2015 at 5 years increment
plot_barchart(orig_df, countries, 'CO2 emissions (kg per PPP $ of GDP)', 1990, 2015, 5)
plot_barchart(orig_df, countries, 'Total greenhouse gas emissions (kt of CO2 equivalent)', 1990, 2015, 5)
plot_barchart(orig_df, countries, 'Energy use (kg of oil equivalent per capita)', 1990, 2015, 5)

# All the countries reduced their Co2 emission over the years, with developed countries like USA, Germany and Canada reducing significantly more than the other countries
# For total green house emmission, US had by far the most emission with an upward trend in the first few years then a downward trend in the last few years. A similar trend is also noticed with Canada
# We can see that the energy consumed also displayed a similar trend for US which means it probably influenced the change in total greenhouse gases emitted in the US, let investigate further

# define Function to pass a line plot showing check whether the trend for energy used is similar at the continent level (North America) and compare with another region.
def plot_line(df, countries, indicator, start_year = None, end_year = None):
    '''
        Plots a line chart showing the indicator performance of certain countries over the years
        
        Args:
            df => pandas.Dataframe, original format
            countries => list, of countries of interest
            indicator => str, selected indicator
            start_year => int, the year range start for the plot
            end_year => int, the year range  end for the plot
        Returns:
            plot => line chart 
    '''
    
    newdf = df[df['Country Name'].isin(countries)]
    newdf = newdf[newdf['Indicator Name'] == indicator]
    
    #filter a specific year if that argument were enter
    if start_year or end_year:
        newdf = newdf[['Country Name'] + [str(year) for year in range(start_year, end_year)]]
    
    newdf = newdf.set_index('Country Name').iloc[:, 3:].T
    newdf.columns.name = None
    
    plt.style.use('bmh')

    newdf.plot( figsize=(10, 9))

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
    plt.xlabel('Year',fontweight ='bold', fontsize = 16)
    plt.ylabel(indicator,fontweight ='bold', fontsize = 16)
    plt.title(indicator + ' trend', fontweight ='bold', fontsize = 16)
    plt.savefig("lINE PLOT.png")
    plt.show()


# check whether the trend for energy used is similar at the continent level (North America) and compare with another region
location = countries + ['North America', 'Sub-Saharan Africa']
plot_line(orig_df, location, 'Energy use (kg of oil equivalent per capita)')


# We can see that trend is specific to North America, Now lets explore USA
def country_heatmap(df, country, indicators, start_year=None, end_year=None):
    '''
        plot the heatmap of country for different indicators
        
        Args:
            df => pandas.Dataframe, original format
            countries => str, selected countries 
            indicator => list, of indicators to check correlation on
            start_year => int, dataset would only data from start from
            end_year => int, dataset would data up to this year
        Returns:
            plot => line chart 
    '''
    country_df = df[df['Country Name'] == country]
    country_df = country_df[country_df['Indicator Name'].isin(indicators)]
    
    #filter a specific year if that argument were enter
    if start_year or end_year:
        country_df = country_df[['Indicator Name'] + [str(year) for year in range(start_year, end_year)]]
    
    corr_df = country_df.set_index('Indicator Name').iloc[:, 3:].T
    corr_df.columns.name = None
    corr_df.index.name = None
    
    
    #set plot size and plot heatmap for correlation
    plt.figure(figsize=(8,5))
    corr = corr_df.corr()
    sns.heatmap(corr, annot=True, linewidths=.2, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(country,fontweight ='bold', fontsize = 16)
    plt.savefig("heatmap.png")
    
# plot showing the correlation of energy use (kg of oil equivalent per capita) and other chosen indicators in USA and it's continent(North America)    
Ind_explore = ['Urban population (% of total population)', 'Energy use (kg of oil equivalent per capita)', 'Total greenhouse gas emissions (kt of CO2 equivalent)', 'Renewable energy consumption (% of total final energy consumption)', 'Forest area (% of land area)', 'CO2 emissions (metric tons per capita)', 'Agricultural land (% of land area)'] 
country_heatmap(orig_df, 'United States', Ind_explore)
country_heatmap(orig_df, 'North America', Ind_explore)

# function to pass selected countries and countries with highest renewable energy use.
def get_table(df, countries, indicator):
    '''
        returns a table showing the changes in a specific indicator over the years
        
        Args:
            df => pandas.Dataframe, original format
            countries => list, of countries 
            indicator => str, of interest 
        Returns:
            plot => pandas.Dataframe, original format sorted from highest difference
    '''
    
    newdf = df[df['Country Name'].isin(countries)]
    newdf = newdf[newdf['Indicator Name'] == indicator]
    newdf = newdf[['Country Name', '1990', '2005', '2019']]
    newdf['change'] =  newdf['2019'] - newdf['1990']
    newdf = newdf.sort_values('change',  ascending=False)
    return newdf.set_index('Country Name')  


# Lets explore how renewable energy use has changed for the countries of interest and also check at global level 
country_energy_used = get_table(orig_df, countries, 'Renewable energy consumption (% of total final energy consumption)')
top_ten_country_energy_used = get_table(orig_df, orig_df['Country Name'].unique(), 'Renewable energy consumption (% of total final energy consumption)').head(10)
print('renewable energy used for the selected countries',country_energy_used, 'Global Renewable Energy Adopters', top_ten_country_energy_used, sep='\n\n')


#Germany had the highest growth in renewable energy consumption from our selected countries
#Globally, Kiribati and Denmark were the biggest adopters of renewable energy, lets add this 2 countries
ren_countries = countries + ['Kiribati', 'Denmark']

#plot showing forest area usage in relation to renewable energy consumption for selected countries
plot_line(orig_df, ren_countries, 'Forest area (% of land area)') 

#plot showing Agricutural land usage in relation to renewable energy consumption for selected countries
plot_line(orig_df, ren_countries, 'Agricultural land (% of land area)')

# No noticable influence of increase in renewable energy on forest area. Brazil had significantly higher Forest area which dropped steeply over the years
# Similar trend is notice for the agriculture land however Saudi Arabia had sharp rise between 1980 to 2000, let's investigate 

#plot showing correlation among indicators chosen for Saudi Arabia
saudi_indicators = ['Urban population (% of total population)', 'Agricultural land (% of land area)', 'Arable land (% of land area)', 'GDP (current US$)', 'Other greenhouse gas emissions (% change from 1990)', 'Electricity production from natural gas sources (% of total)', 'CO2 intensity (kg per kg of oil equivalent energy use)']
country_heatmap(orig_df, 'Saudi Arabia', saudi_indicators, 1982, 1999)


# Agricultural land had a high negative correlation with other greenhouse gas emission and electricity production from natural gas sources

# lets check the trend of the indicators for saudi arabia over that period
plot_line(orig_df, countries, 'Other greenhouse gas emissions (% change from 1990)')
plot_line(orig_df, countries, 'Electricity production from natural gas sources (% of total)')


# there was no notable change in other greenhouse gas emissions during that period
# Electricity production from natural gas sources dropped over that period which lead to sharp rise in Agricultural land for saudi arabia


