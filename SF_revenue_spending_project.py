# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:33:53 2025

@author: alisa
"""

import pandas as pd
import plotly.express as px

# Data taken from https://data.sfgov.org/City-Management-and-Ethics/Spending-and-Revenue/bpnb-jwfb/about_data
df = pd.read_csv('Spending_and_Revenue_{date_of_retrieval}.csv')
df.info()

df['Amount'] = df['Amount'].str.replace(",", "")
df['Amount'] = df['Amount'].astype(float)
df['Department'] = df['Department'].str.replace("  ", " ")
df['Department'] = df['Department'].str.replace("/", "-")
df['Department'] = df['Department'].str.replace(" of ", " Of ")
df['Department'] = df['Department'].str.replace("Gen Svcs Agency-", "GSA - ")
df['Department'] = df['Department'].str.replace("HOMELESSNESS SERVICES", "Homelessness Services")
df['Department'] = df['Department'].str.replace("Administrator", "Admin")
df['Character'] = df['Character'].str.replace("Adjustments-Sources", "Adjustment-Source")
df['Character'] = df['Character'].str.replace("Transfer Adjustment - Uses", "Transfer Adjustments-Uses")

#u1 = df['Department'].unique().tolist()
#u2 = df.groupby(['Program Code', 'Program']).size()
#u3 = df.groupby(['Character Code', 'Character']).size()
#u4 = df.groupby(['Object Code', 'Object']).size()
#u5 = df.groupby(['Fund Type Code', 'Fund Type']).size()
#u6 = df.groupby(['Fund Code', 'Fund']).size()
#u7 = df.groupby(['Fund Category Code', 'Fund Category']).size()

#df.to_csv('Spending_and_Revenue_cleaned.csv', index = False)
#df = pd.read_csv('Spending_and_Revenue_cleaned.csv')


def net_revenue(index_columns):
    pivot_rev_and_spend = df.pivot_table(index = index_columns, columns = 'Revenue or Spending', values = 'Amount', aggfunc = 'sum')
    p = pivot_rev_and_spend.fillna(0)
    p['Net Revenue'] = p['Revenue'] - p['Spending']
    p = p.reset_index().sort_values('Net Revenue', ascending = True)
    return p

# First graph ----------------------------------------------------------------------------------------------------------------
depts = net_revenue(['Department Code', 'Department'])
fig1 = px.bar(depts, x = 'Department Code', y = 'Net Revenue',
             hover_data = ['Department', 'Revenue', 'Spending', 'Net Revenue'],
             template = 'plotly_white')
fig1.show(renderer='browser')
graph1_html = fig1.to_html(full_html = False, include_plotlyjs = 'cdn')

# Second graph ---------------------------------------------------------------------------------------------------------------
groups = net_revenue(['Organization Group', 'Fiscal Year'])
fig2 = px.bar(groups, x = 'Fiscal Year', y = 'Net Revenue', color = 'Organization Group', template = 'plotly_white')
fig2.show(renderer='browser')
graph2_html = fig2.to_html(full_html = False, include_plotlyjs = 'cdn')

# Third graph, not used ------------------------------------------------------------------------------------------------------
years = net_revenue('Fiscal Year')
fig3 = px.bar(years, x = 'Fiscal Year', y = 'Net Revenue')
fig3.show(renderer='browser')

# Forth graph ----------------------------------------------------------------------------------------------------------------
type_hier = df[df['Revenue or Spending'] == 'Spending']
type_hier = type_hier.groupby(['Character', 'Object', 'Sub-object'])['Amount'].sum().reset_index().sort_values(by = 'Amount', ascending = False).head(70)
type_hier['all'] = 'all'
fig5 = px.treemap(type_hier, path = [px.Constant('all'), 'Character', 'Object', 'Sub-object'], values = 'Amount',
                  color = 'Amount', color_continuous_scale = 'Blues')
fig5.show(renderer='browser')
graph5_html = fig5.to_html(full_html = False, include_plotlyjs = 'cdn')
