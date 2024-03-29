############################################################################################
# Imports
############################################################################################
import pandas as pd
import time

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns
sns.set(font_scale=1.5) 

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from helper_functions import dailyChanges

############################################################################################
# Gather data and relevant stats for use in the figure
############################################################################################

date = time.localtime()
date_str = f'{date.tm_year}-{date.tm_mon}-{date.tm_mday} (YYYY-MM-DD)'

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
fig.subplots_adjust(top=0.9) 
plt.annotate(f"*Percentage approximate. Updated on {date_str}",
             (175,400), 
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

# Make axes tick labels the color of the graph
highest_cases, highest_deaths = max(usa_daily.new_cases), max(usa_daily.new_deaths)
ax2.tick_params(axis='y', labelcolor='purple')
ax.set_ylim([0, highest_cases + highest_cases//10])
ax2.set_ylim([0, highest_deaths + highest_deaths//10])

# Format the legend and grid
ax.legend(loc='upper left')
ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.92))
ax2.grid(False)


if __name__ == '__main__':
    # Save the figure
    plt.savefig('../figures/Daily_US')
    plt.show()