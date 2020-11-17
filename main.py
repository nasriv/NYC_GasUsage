'''
Use 2010 NYC gas usage data from nyc open data
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os

def trunc_val(x):
    if len(x) > 5:
        return x[0:5]
    else:
        return x

def title_change(x):
    if x == 'Large residential' or x=='Large Residential' or x=='Small residential':
        return 'Residential'
    else:
        return x

# import zipcode shape file data from US census bureau
path = os.getcwd()
zip_geo = gpd.read_file(os.path.join(path,"zipcode/ZIP_CODE_040114.shp"))

# import natural gas consumption
ngdf = pd.read_csv("Natural_Gas_Consumption_by_ZIP_Code_-_2010.csv")
ngdf = ngdf.rename(columns={'Zip Code':'ZIPCODE',' Consumption (therms) ':'Consumption(therms)','Building type (service class':'BuildingType'})

# clean zip code data points by truncating
ngdf['ZIPCODE'] = ngdf['ZIPCODE'].apply(trunc_val)

# typecast object zipcode to INT
ngdf['ZIPCODE'] = ngdf['ZIPCODE'].astype(int)
zip_geo['ZIPCODE'] = zip_geo['ZIPCODE'].astype(int)

# consolidate building types definitions
ngdf['BuildingType'] = ngdf['BuildingType'].apply(title_change)

# merge national gas data onto shape file dataframe
merged = zip_geo.merge(ngdf,on='ZIPCODE')

# plot consumptions(therms) data
f, ax = plt.subplots(1,figsize=(10,10))
var = 'Consumption(therms)'

ax = merged.plot(ax=ax,column=var,legend=True,
    legend_kwds = {'label':'Consumption (therms)'},
    cmap='summer',
    edgecolor='black',
    linewidth=0.2)
ax.axis("off")
plt.title('2010 Natural Gas Consumption in NYC by Zip Code',fontsize=18)
plt.tight_layout()
plt.savefig('Gas_Consump_ZIP.png',dpi=300)

# plot utility service distribution
print(ngdf.columns)
f, ax = plt.subplots(1,figsize=(6,6))
ax = sns.countplot(ngdf['Utility/Data Source'])
for p in ax.patches:
    ax.annotate(
        int(p.get_height()),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0,7),
        textcoords='offset points'
        )
plt.title('2010 Utility Provider Ditribution')
plt.tight_layout()

# plot building type count
print(ngdf.columns)
f, ax = plt.subplots(1,figsize=(8,8))
ax = sns.countplot(ngdf['BuildingType'])
for p in ax.patches:
    ax.annotate(
        int(p.get_height()),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0,7),
        textcoords='offset points'
        )
plt.title('2010 Building Type Distribution')
plt.tight_layout()


# plot distribution of gas usage by zipcode
f, ax = plt.subplots(1, figsize=(6,6))
sns.distplot(
    ngdf['Consumption(therms)'],
    kde=False
    )
plt.title('2010 Distribution of Natural Gas Consumption(therms)')

# Gas usage by building type vs zipcode
f, ax = plt.subplots(1, figsize=(8,8))
types = ngdf['BuildingType'].unique()

sns.boxplot(data=ngdf,x="ZIPCODE",y="Consumption(therms)",hue="BuildingType")
