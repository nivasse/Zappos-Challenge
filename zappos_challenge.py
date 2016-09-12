# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:19:49 2016

@author: nivasseajagane
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

zappos = {}
zappos_nomv = {}

#initializing the tables
zappos['units'] = pd.read_csv("/Users/nivasseajagane/desktop/split_nototalother/Units.csv")
zappos['transactions'] = pd.read_csv("/Users/nivasseajagane/desktop/split_nototalother/Transactions.csv")
zappos['revenue'] = pd.read_csv("/Users/nivasseajagane/desktop/split_nototalother/Revenue.csv")
zappos['buyers'] = pd.read_csv("/Users/nivasseajagane/desktop/split_nototalother/Buyers.csv")
#print(zappos['transactions'].dtypes)
#print(zappos['transactions'].isnull())

#cleaning dataset - removing 4, whitespaces and commas. Removing rows with Nan values for attributes
for key in zappos:
    zappos[key].replace({',':'' , ' ':'' , '\$':''}, regex=True, inplace=True)
    zappos_nomv[key] = zappos[key].dropna()
    zappos_nomv[key] = zappos_nomv[key].set_index('online_retailers')
    zappos_nomv[key] = zappos_nomv[key].apply(pd.to_numeric)
    zappos_nomv[key] = zappos_nomv[key].divide(1000000)
    zappos_nomv[key]['overall']=zappos_nomv[key].sum(axis=1)
 
#creating new attributes for analysis   
zappos_nomv['avgrevenuepertrans'] = pd.DataFrame(0, index=zappos_nomv['revenue'].index, columns=list(zappos_nomv['revenue']))
for col in list(zappos_nomv['units']):
    zappos_nomv['avgrevenuepertrans'][col]= zappos_nomv['revenue'][col]/zappos_nomv['transactions'][col]

zappos_nomv['avgunitspertrans'] = pd.DataFrame(0, index=zappos_nomv['revenue'].index, columns=list(zappos_nomv['revenue']))
for col in list(zappos_nomv['units']):
    zappos_nomv['avgunitspertrans'][col]= zappos_nomv['units'][col]/zappos_nomv['transactions'][col]

zappos_nomv['avgrevenueperunit'] = pd.DataFrame(0, index=zappos_nomv['revenue'].index, columns=list(zappos_nomv['revenue']))
for col in list(zappos_nomv['units']):
    zappos_nomv['avgrevenueperunit'][col]= zappos_nomv['revenue'][col]/zappos_nomv['units'][col]

zappos_nomv['avgtransperbuyer'] = pd.DataFrame(0, index=zappos_nomv['revenue'].index, columns=list(zappos_nomv['revenue']))
for col in list(zappos_nomv['units']):
    zappos_nomv['avgtransperbuyer'][col]= zappos_nomv['transactions'][col]/zappos_nomv['buyers'][col]

for col in list(zappos_nomv['revenue']):
        print(zappos_nomv['revenue'][col].sort_values(ascending=False).head(5))

#plotting graphs for each attribute for each online retailer

ax = {}
sns.set_style("dark")
for key in zappos_nomv:
    
    fig = plt.figure()
    fig.set_size_inches(14.5, 10.5, forward=True)
    fig.suptitle(str.upper(key), y=1.05, fontsize=30)
    for i,col in enumerate(list(zappos_nomv['revenue'])):
        
        ax[i] = fig.add_subplot(4,2,i+1)
        xint = range(5)
        rank = zappos_nomv[key][col].sort_values(ascending=False).head(5)
        t = ax[i].bar(xint, rank)

        for ii,rect in enumerate(t):
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (rank.index[ii]),
                ha='center', va='bottom')
        ax[i].set_title(col)
        ax[i].set_xticks([])
    plt.tight_layout()
    plt.savefig('/Users/nivasseajagane/desktop/images/'+key+'_nomv.png', dpi=300)
    plt.close(fig)

for key in zappos:
    
    fig = plt.figure()
    fig.set_size_inches(14.5, 10.5, forward=True)
    fig.suptitle(str.upper(key), y=1.05, fontsize=30)
    for i,col in enumerate(list(zappos_nomv['revenue'])):
        
        ax[i] = fig.add_subplot(4,2,i+1)
        xint = range(5)
        rank = zappos_nomv[key][col].sort_values(ascending=False).head(5)
        t = ax[i].bar(xint, rank)

        for ii,rect in enumerate(t):
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (rank.index[ii]),
                ha='center', va='bottom')
        ax[i].set_title(col)
        ax[i].set_xticks([])
    plt.tight_layout()
    plt.savefig('/Users/nivasseajagane/desktop/images/'+key+'.png', dpi=300)
    plt.close(fig)

fig = plt.figure()
fig.set_size_inches(14.5, 10.5, forward=True)
labels=['Buyers','Average No: of Transactions per Buyer','Transactions','Revenue','Average Revenue per Unit', 'Average No: of Units per Transaction','Average Revenue per Transaction','Units']
for i,key in enumerate(zappos_nomv):
        
    ax[i] = fig.add_subplot(4,2,i+1)
    xint = range(7)
    rank = zappos_nomv[key].loc['zappos.com']
    
    t = ax[i].bar(xint, rank)
    for ii,rect in enumerate(t):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (rank.index[ii]),
            ha='center', va='bottom')
    ax[i].set_title(labels[i])
    ax[i].set_xticks([])
plt.tight_layout()
plt.savefig('/Users/nivasseajagane/desktop/zappos_internal/zappos.png', dpi=300)
plt.close(fig)