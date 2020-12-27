############################################################################################
# Imports and gather data
############################################################################################
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
sns.set(font_scale=1.5) 

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from bs4 import BeautifulSoup
import requests

from helper_functions import dailyChanges
from helper_functions import smoother
from helper_functions import sumByDate

# URL to NY Times COVID-19 data
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# Read the values, set the indices, parse the dates, and alphabetize
df = pd.read_csv(url, 
                 header=0, 
                 index_col=['state','county','date'], 
                 parse_dates=True).sort_index()

############################################################################################
# Fetch table of state and postal code names so we don't have to type out the full names
############################################################################################
# Lists of the regions of the US
northeast = ['CT', 'DE', 'ME', 'MD', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']
midwest = ['IL', 'IN', 'IA', 'KS', 'MI', 'MO', 'MN', 'NE', 'ND', 'OH', 'SD', 'WI']
south = ['AL', 'AR', 'FL', 'GA', 'KY', 'LA', 'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV']
west = ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WY']
mainland = set(northeast + midwest + west + south) - set(['AK', 'HI'])

url = "https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696"
html_content = requests.get(url).text      # Make a GET request to fetch the raw HTML content
soup = BeautifulSoup(html_content, "lxml") # Parse the html content

fips, countyName, stateName = [], [], []
for tr in soup.find_all('tr')[29:-6]: #Found bounds manually
    tds = tr.find_all('td')
    fips.append(tds[0].text.replace('\r\n\t\t\t\t',''))
    countyName.append(tds[1].text.replace('\r\n\t\t\t\t',''))
    stateName.append(tds[2].text.replace('\r\n\t\t\t\t',''))

statefips = pd.DataFrame()
statefips['name'] = fips
statefips['postal code'] = countyName
statefips['fips'] = stateName

# Reset the index to default
data = df.reset_index()

# Drop the old fips column and merge with the statefips DataFrame on most similar column
data = data.drop('fips', axis=1).merge(statefips, left_on='state', right_on='name', how='inner')

# Drop the redundant name and state columns and index by date
data = data.drop(['name','state'], axis=1).set_index('date').sort_values('date')

############################################################################################
# Filter data by regions and gather relevant statistics for the figure
############################################################################################
NE = data[data['postal code'].isin(northeast)]
S = data.loc[data['postal code'].isin(south)]
MW  = data.loc[data['postal code'].isin(midwest)]
W = data.loc[data['postal code'].isin(west)]

# Aggregate the multiple cases on any one date
sum_NE = sumByDate(NE, ['cases','deaths'])
sum_S = sumByDate(S, ['cases','deaths'])
sum_MW = sumByDate(MW, ['cases','deaths'])
sum_W = sumByDate(W, ['cases','deaths'])

# Find the newly reported daily cases 
dailyNE = dailyChanges(sum_NE, ['cases','deaths'])
dailyS = dailyChanges(sum_S, ['cases','deaths'])
dailyMW = dailyChanges(sum_MW, ['cases','deaths'])
dailyW = dailyChanges(sum_W, ['cases','deaths'])

# Populations as of the 2019 Census
popNE, popS, popMW, popW = 55982803, 68329004, 78347268, 125580448

# Number of total cases per region 
casesW, casesMW, casesNE, casesS = dailyW.sum()[0], dailyMW.sum()[0], dailyNE.sum()[0], dailyS.sum()[0]

# Number of total deaths per region 
deathsW, deathsMW, deathsNE, deathsS = dailyW.sum()[1], dailyMW.sum()[1], dailyNE.sum()[1], dailyS.sum()[1]

# Percent of regional population infected
percentW = (casesW / popW) * 100
percentMW = (casesMW / popMW) * 100
percentNE = (casesNE / popNE) * 100
percentS = (casesS / popS) * 100

############################################################################################
# Plot Regions
############################################################################################
fig, ax = plt.subplots(2,2, sharey=True, sharex=True, figsize=(18,8))

plt.style.use('ggplot')

# Format the dates displayed on the xaxis
date_form = DateFormatter("%b")

# Set overall title
fig.suptitle('Daily Reported Cases and Deaths by US Region', fontsize=24)

# Pad the space on the top to allow for an annotation below suptitle
fig.subplots_adjust(top=0.87)
plt.annotate('*Percentages approximate: risk of reinfection still unclear\n' + ' '*12 + 'Updated on ' + date_str, 
             (-200,450), 
             fontsize=12, 
             xycoords='axes pixels')

# Tuples of Cases, deaths, and percentages of population for later annotations
numbers = [(percentW, int(casesW), int(deathsW)),
           (percentMW, int(casesMW), int(deathsMW)),
           (percentNE, int(casesNE), int(deathsNE)),
           (percentS, int(casesS), int(deathsS))]

plot_data = [dailyW, dailyMW, dailyNE, dailyS]

titles = ['Western US', 'Midwestern US', 'Northeastern US', 'Southern US']

# Will effectively become [axW, axMW, axNE, axS]
new_axes = []
axes = [ax[0,0], ax[0,1], ax[1,1], ax[1,0]]

# Set the cases plot parameters in a relatively efficient manner
for i, axis in enumerate(axes):
    axis.set_title(titles[i], fontsize=18)
    axis.xaxis.set_major_formatter(date_form)
    axis.annotate('Percent Infected:  {:.2f}%\nTotal Cases:  {:,}\nTotal Deaths: {:,}'.format(*numbers[i]), 
                  (10,143) if axis not in [ax[0,1], ax[1,1]] else (295,143), 
                  fontsize=14, 
                  xycoords='axes pixels')
    axis.bar(plot_data[i].index, 
             plot_data[i].new_cases, 
             width=1,
             color='deepskyblue',
             alpha=0.6)
    
    axis.set_ylim([0,125000])
    
    # Make dual axes
    new_axes.append(axis.twinx())

# Set the deaths plot parameters in a relatively efficient manner
for i, axis in enumerate(new_axes):
    axis.tick_params(axis='y', labelcolor='purple')
    axis.xaxis.set_major_formatter(date_form)
    axis.set_ylim([0,2250])
    axis.grid(False)                                 # Turn off second grid
    new_axes[i].step(plot_data[i].index, 
                     plot_data[i].new_deaths,  
                     color='purple',
                     alpha=0.6)
    
plt.savefig('../figures/Daily_US_Regions')