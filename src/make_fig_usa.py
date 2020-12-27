############################################################################################
# Imports
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

############################################################################################
# Gather data and relevant stats for use in the figure
############################################################################################

# URL to NY Times COVID-19 data
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

# Read the values, set the indices, parse the dates, and alphabetize
usa = pd.read_csv(url, 
                  header=0, 
                  index_col=['date'], 
                  parse_dates=True).sort_index()


usa_daily = dailyChanges(usa, ['cases','deaths'])

usa_pop = 328231337 # from 2019 Census
usa_cases = usa.cases.values[-1]
usa_deaths = usa.deaths.values[-1]
percent_infected = (usa_cases / usa_pop) * 100

############################################################################################
# Daily Changes USA
############################################################################################
fig, ax = plt.subplots(figsize=(13,7))

plt.style.use('ggplot')

# Let the deaths be described by another pair of axis for enlargement
ax2 = ax.twinx()

# Plot the new US cases
ax.bar(usa_daily.index,
       usa_daily.new_cases,
       color='deepskyblue',
       label='New Cases',
       width=1,
       alpha=0.6)

# Plot the new US deaths
ax2.step(usa_daily.index,
         usa_daily.new_deaths,
         color='purple',
         label='New Deaths',
         alpha=0.8)

# Pad the space on the top to allow for an annotation below suptitle
fig.suptitle('Daily Reported Cases and Deaths in the US*', fontsize=22)
fig.subplots_adjust(top=0.87) 
plt.annotate('*Percentage approximate: risk of reinfection still unclear\n' + ' '*12 + 'Updated on ' + date_str, (200,390), 
              fontsize=12, 
              xycoords='axes pixels')

# Annotate with the total number of cases and deaths. 
ax.annotate('Percent Infected:  {:.2f}%\nTotal Cases:  {:,}\nTotal Deaths: {:,}'.format(percent_infected, usa_cases, usa_deaths), 
            (10,260), 
            fontsize=14, 
            xycoords='axes pixels')

# Formate the x-axis dates
date_form = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_form)

# Make ax2 tick labels the color of the graph
ax2.tick_params(axis='y', labelcolor='purple')
ax2.set_ylim([0,4000])

# Format the legend and grid
ax.legend(loc='upper left')
ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.92))
ax2.grid(False)

# Save the figure
plt.savefig('../figures/Daily_US')