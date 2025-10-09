#! /usr/bin/env python3

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# create list of all relevant months
monthlist = pd.date_range('2022-05-01', pd.Timestamp.today() + pd.offsets.MonthEnd(-1), 
              freq='MS').strftime("%Y-%m").tolist()

# pull month end data for all completed months
monthend = pd.DataFrame()
for i in monthlist[:] :
    url = r"https://raw.githubusercontent.com/anacedragon/pf-funding-data/refs/heads/main/funds-"+ i +".csv"
    monthdata = pd.read_csv( url ) #.loc[ : , ['Date' , 'Goal' , 'Funds'] ]
    lastday = monthdata[-1:]
    monthend = pd.concat([monthend , lastday] , ignore_index = True)

# drop November 2023 (Emergency Fundraiser)
monthend = monthend.loc[ monthend['Date'] !='2023-11-29 21:01:00-05:00' ]
# calculate net income
monthend['Net Income'] = monthend['Funds'] - monthend['Goal']

# create monthly funds vs. goal graph
month_balance_graph = px.bar(monthend , x='Date' , y=['Funds' , 'Goal'] , 
                             barmode = 'overlay' , color_discrete_sequence = ['#00cc96' , '#ef553b'] , opacity=0.75
                            )
month_balance_graph.show(config={'modeBarButtonsToRemove': ['zoomIn', 'zoomOut' , 'lasso' , 'select']})

# create net income graph
month_netincome_graph = px.bar(monthend , x='Date' , y='Net Income' , 
                             barmode = 'overlay' , color_discrete_sequence = ['#636efa'] , opacity=0.75
                            )
month_netincome_graph.show(config={'modeBarButtonsToRemove': ['zoomIn', 'zoomOut' , 'lasso' , 'select']})

# reformat graphs and styling
start_date = '2024-01-15'
end_date = pd.Timestamp.today() + pd.DateOffset(5)
min_date = '2022-05-01'
max_date = end_date
raisedmin = '0'
raisedmax = '7600'
netincomemin = '-1250'
netincomemax = '1100'

fig = make_subplots(rows=2 , cols=1 ,
                     row_heights=[0.6, 0.4] ,
                     shared_xaxes=True ,
                     vertical_spacing=0.1 ,
                     subplot_titles=("Funds Raised vs. Goal" , "Net Income")
                    )
fig.add_traces(month_balance_graph.data, 1, 1)
fig.add_traces(month_netincome_graph.data , 2, 1 )

fig.update_layout(
    font=dict(
        family="Trebuchet MS" ,
        color="white"
    ),
    paper_bgcolor="#27182B" ,
    plot_bgcolor="#392340" ,
    title=dict(
        text=None,
    ),
    xaxis=dict(
        title=None,
        minallowed=min_date,
        maxallowed=max_date,
        showticklabels=True,
    ),
    yaxis=dict(
        title=None,
        tickprefix='$',
        tickformat=',.0f',
        fixedrange=False,
        range=[ raisedmin , raisedmax ],
        minallowed=0,
    ),
    xaxis2=dict(
        title=None,
    ),
    yaxis2=dict(
        title=None,
        tickprefix='$',
        tickformat=',.0f',
        range=[ netincomemin , netincomemax ]
    ),
    showlegend=True,
    legend=dict(
        title=None,
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=0.13,
    ),
    margin=dict(
        l=20, r=20, t=5, b=20
    ),
    barmode='overlay',
    hoversubplots='axis',
    hovermode='x unified' ,
    hoverlabel=dict(
       bgcolor= "#472C59",
       bordercolor= "#000000",
    ),
    dragmode='pan' ,
)
fig.update_xaxes(
    type="date", range=[start_date , end_date],
    dtick="M1", tick0="2025-01-1", tickformat="%b\n%Y" , ticklabelmode='period' , ticklabelshift=20
)
fig.update_traces(
    hovertemplate="Net Income: $%{y:,.0f}"
)

# export graph to html
fig.write_html(
    'auto_monthly_graph.html' ,
    include_plotlyjs='cdn',    # Use CDN
    include_mathjax=False,     # Exclude MathJax
    config={
        'modeBarButtonsToRemove': ['lasso' , 'select']
    }
)
