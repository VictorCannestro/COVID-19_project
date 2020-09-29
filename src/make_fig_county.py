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
# Cumulative King County
############################################################################################
daily_king = dailyChanges(df.loc[('Washington','King')], ['cases','deaths']).abs()

fig, ax = plt.subplots(figsize=(13,7))

plt.style.use('ggplot')

ax.bar(king.index,
       king.cases,
       color='thistle',
       label='Cumulative Cases',
       width=1)

ax.bar(king.index,
       king.deaths,
       color='purple',
       label='Cumulative Deaths',
       width=1,
       alpha=0.8)

ax.set_title('Cumulative Reported Cases and Deaths (King County WA)', fontsize=18)

# Annotate with the total number of cases and deaths.
ax.annotate('Total Cases:  {:,}'.format(king.cases.values[-1]), (10,302), fontsize=17, xycoords='axes pixels')
ax.annotate('Total Deaths:      {:,}'.format(king.deaths.values[-1]), (10,282), fontsize=17, xycoords='axes pixels')

date_form = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_form)

plt.legend()
plt.savefig('../figures/Cumulative_King_County')
plt.show()

############################################################################################
# Daily Changes King County
############################################################################################
daily_king = dailyChanges(df.loc[('Washington','King')], ['cases','deaths']).abs()
smoothed = smoother(daily_king, daily_king.columns, 7)

fig, ax = plt.subplots(2, 1, figsize=(13,13))

plt.style.use('ggplot')

# Plot the new reported cases
ax[0].bar(daily_king.index, 
           daily_king.new_cases,  
           color='deepskyblue',
           label='Daily Reported Cases',
           alpha=0.8)

ax[0].step(smoothed.index, 
           smoothed.average_new_cases, 
           color='black',
           alpha=0.8,
           label='7-day Average Cases')

# Plot the new reported deaths
ax[1].bar(daily_king.index, 
           daily_king.new_deaths, 
           color='purple',
           label='Daily Reported Deaths',
           alpha=0.6)

ax[1].step(smoothed.index, 
           smoothed.average_new_deaths, 
           color='black',
           alpha=0.8,
           label='7-day Average Deaths')

# Set axis labels and titles
ax[0].set_title('Reported New Cases King County WA', fontsize=18)
ax[0].set_ylabel('Daily Cases', fontsize=18)
ax[1].set_title('Reported New Deaths King County WA', fontsize=18)
ax[1].set_ylabel('Daily Deaths', fontsize=18)

# Format the dates displayed on the xaxis
date_form = DateFormatter("%b")
ax[0].xaxis.set_major_formatter(date_form)
ax[1].xaxis.set_major_formatter(date_form)

# Show the legend and plots
ax[0].legend()
ax[1].legend(loc='upper center')

plt.savefig('../figures/Daily_King_County')
plt.show()