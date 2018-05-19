# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import statistics
from scipy import stats
from sklearn import preprocessing
import math

get_ipython().magic('matplotlib inline')


# In[3]:


# Read all .csv files to data relevant frames
df_pubs = pd.read_csv("open_pubs.csv")
df_crimes = pd.read_csv("london_crime_by_lsoa.csv")
df_borough_demographics = pd.read_csv("london-borough-profiles-2016 Data set.csv")

df_pubs


# In[207]:


# Find the poorer boroughs
gap_list_original = df_borough_demographics['Gross Annual Pay, (2015)'].dropna().tolist()
print('gap_list_original', gap_list_original)

gap_list = []
for gap_amount in gap_list_original:
    if (gap_amount != '.'):
        int_gap_amount = int(gap_amount[1:].replace(',',''))
        gap_list.append(int_gap_amount)

print('gap_list', gap_list)

size_of_all_boroughs = len(gap_list)
print('size_of_all_boroughs: ' + str(size_of_all_boroughs))


median_gap = statistics.median(gap_list)
print('median_gap: ' + str(median_gap))

poor_borough_gaps = []
poor_borough_gaps = [x for x in gap_list if x <= median_gap]
poor_borough_gaps = ['\xa3' + str(x)[:2] + ',' + str(x)[2:] for x in poor_borough_gaps]
print('poor_borough_gaps', poor_borough_gaps)

size_of_poor_boroughs = len(poor_borough_gaps)
print('size_of_poor_boroughs', size_of_poor_boroughs)

df_poor_borough_demographics = df_borough_demographics.loc[df_borough_demographics["Gross Annual Pay, (2015)"].isin(poor_borough_gaps)]
print('df_poor_borough_demographics[\'Gross Annual Pay, (2015)\']', df_poor_borough_demographics['Area name'])


# In[208]:


# Use the poor boroughs
df_borough_demographics = df_poor_borough_demographics

# # Drop null values from borough demographics data frame
# df_borough_demographics.dropna(inplace=True)

# Slice borough names
df_london_boroughs = df_borough_demographics[['Area name']]
print(df_london_boroughs)

# Get list of boroughs in London to an array(list)
borough_list = df_london_boroughs['Area name'].tolist()
df_pubs = df_pubs.rename(columns={'local_authority':'borough'})

# Select all pubs from London, based on the borough names in London
df_london_pubs = df_pubs.loc[df_pubs["borough"].isin(borough_list)]
print ("Pubs that are located in London boroughs:")
df_london_pubs.head()


# In[209]:


df_pub_count_per_borough = df_london_pubs.groupby("borough").nunique()
df_pub_count_per_borough = df_pub_count_per_borough[["fas_id"]]
df_pub_count_per_borough = df_pub_count_per_borough.rename(columns={'fas_id':'pub_count'})
print (df_pub_count_per_borough.head(), '\n')

df_crimes_per_borough = df_crimes.groupby("borough").count()
df_crimes_per_borough = df_crimes_per_borough [['lsoa_code']]
df_crimes_per_borough = df_crimes_per_borough.rename(columns={'lsoa_code':'crime_count'})
print (df_crimes_per_borough.head())


# In[210]:


# Combine data frames
df_pubs_crimes = df_crimes_per_borough.join(df_pub_count_per_borough)
df_pubs_crimes.dropna(inplace=True)
# print(df_pubs_crimes.head(), '\n')

# Create a pub count/crime count ratio variabl, and normalize it
df_pubs_crimes['pc_ratio'] = df_pubs_crimes.apply(lambda row: row.pub_count / row.crime_count, axis=1)
max_value = df_pubs_crimes['pc_ratio'].max()
min_value = df_pubs_crimes['pc_ratio'].min()
df_pubs_crimes['pc_ratio_norm'] = (df_pubs_crimes['pc_ratio'] - min_value) / (max_value - min_value)

df_pubs_crimes


# In[211]:


# Print data frame as bar-graph
ax = df_pubs_crimes.plot(secondary_y='pub_count', rot=90, kind='bar')

# Set Legend labels with 'patch'
crime_patch = mpatches.Patch(color='cornflowerblue', label='Crime Count')
pub_patch = mpatches.Patch(color='orange', label='Pub Count')
ax.legend(handles=[crime_patch,pub_patch], loc=1)

ax.set_xlabel('Poor Boroughs')
ax.set_ylabel('Number of')

ax.set_xticklabels(borough_list)
ax2 = ax.twinx()
ax2.set_yscale('log')

plt.show()


# In[212]:


ax = df_pubs_crimes['pc_ratio'].plot(kind='bar')
ax.set_xlabel('Poor Boroughs')
plt.show()
ax = df_pubs_crimes['pc_ratio_norm'].plot(kind='bar')
ax.set_xlabel('Poor Boroughs')
plt.show()

# statistics.mean(df_pubs_crimes['pc_ratio_norm'])
statistics.stdev(df_pubs_crimes['pc_ratio_norm'])


# In[213]:


statistics.stdev(df_pubs_crimes['pc_ratio_norm'])/math.sqrt(len(df_pubs_crimes))
