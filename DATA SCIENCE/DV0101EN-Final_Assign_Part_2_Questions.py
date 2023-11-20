#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

# ---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': '', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
# List of years
year_list = [i for i in range(1980, 2024, 1)]
# ---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={
            'text-align': 'center', 'margin-top': '20px', 'color': '#503D36', 'font-size': '24px'}),
    html.Div([  # TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics',
                    'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px',
                   'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div([  # TASK 2.6: Add another dropdown menu
        html.Label("Select Vehicle Type:"),
        dcc.Dropdown(
            id='select-vehicle-type',
            options=[
                {'label': 'Sedan', 'value': 'sedan'},
                {'label': 'SUV', 'value': 'suv'},
                {'label': 'Truck', 'value': 'truck'}
            ],
            value='sedan',
            placeholder='Select vehicle type'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='',
    )),
    html.Div([  # TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex'})
    ])
])
# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics


@app.callback(
    Output(component_id='select-year', component_property='value'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True
# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        # Perform any additional operations on the recession_data dataframe

    # elif selected_statistics == 'Yearly Statistics':
    #     if selected_year != '':
    #         # Filter the data for the selected year
    #         yearly_data = data[data['Year'] == int(selected_year)]
    #         # Perform any additional operations on the yearly_data dataframe
    #     else:
    #         # Handle the case when no year is selected
    #         yearly_data = pd.DataFrame()

    # # Return the appropriate dataframe based on the selected report type
    # if selected_statistics == 'Recession Period Statistics':
    #     # Filter the data for recession periods
    #     recession_data = data[data['Recession'] == 1]
    #     return recession_data.to_json(orient='records')
    # elif selected_statistics == 'Yearly Statistics':
    #     if selected_year != '':
    #         # Filter the data for the selected year
    #         yearly_data = data[data['Year'] == int(selected_year)]
    #         return yearly_data.to_json(orient='records')
    #     else:
    #         # Handle the case when no year is selected
    #         return pd.DataFrame().to_json(orient='records')
    # else:
    #     return pd.DataFrame().to_json(orient='records')
# TASK 2.5: Create and display graphs for Recession Report Statistics

# Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        # yearly_rec=recession_data.groupby('...')['...'].mean().reset_index()
        yearly_rec = recession_data.groupby(
            'Year')['Automobile_Sales'].mean().reset_index()
        # R_chart1 = dcc.Graph(
        #     figure=px......(.....,
        #         x='....',
        #         y='......',
        #         title="Average Automobile Sales fluctuation over Recession Period"))
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period"))

# Plot 2 Calculate the average number of vehicles sold by vehicle type
        # use groupby to create relevant data for plotting
        # average_sales = ...............mean().reset_index()
        average_sales = recession_data.groupby(
            'Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        # R_chart2  = dcc.Graph(figure=px....................
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                             title='Average Vehicles Sold by Vehicle Type during Recession Period'))

# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        # exp_rec= ....................
        # R_chart3 = .............
        # print all columns
        print(recession_data.columns)
        # print(recession_data.groupby('Vehicle_Type'))
        # print groupby object column
        exp_rec = recession_data.groupby('Vehicle_Type')[
            'Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                             title='Total Advertisement Expenditure by Vehicle Type during Recession Period'))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        # ................
        # ...................
        unemp_rec = recession_data.groupby('Vehicle_Type')[
            'unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_rec, x='Vehicle_Type', y='unemployment_rate',
                             title='Effect of Unemployment Rate on Vehicle Type during Recession Period'))

        # return [
        #     html.Div(className='..........', children=[html.Div(children=R_chart1),html.Div(children=.....)],style={.....}),
        #     html.Div(className='chart-item', children=[html.Div(children=...........),html.Div(.............)],style={....})
        #     ]
        return [
            html.Div(className='chart-item', children=[html.Div(
                children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(
                children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]


# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

# TASK 2.5: Creating Graphs Yearly data

# plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas,
                                            x='Year',
                                            y='Automobile_Sales',
                                            title="Average Automobile Sales fluctuation over Recession Period"))

# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales',
                             title='Total Monthly Automobile Sales in the year {}'.format(input_year)))

        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby(['Vehicle_Type'])[
            'Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                             title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Total Advertisement Expenditure for each vehicle using pie chart
        # exp_data=yearly_data.groupby(..................
        # Y_chart4 = dcc.Graph(...............)
        exp_data = yearly_data.groupby('Vehicle_Type')[
            'Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                             title='Total Advertisement Expenditure by Vehicle Type in the year {}'.format(input_year)))

# TASK 2.6: Returning the graphs for displaying Yearly data
        # return [
        #         html.Div(className='.........', children=[html.Div(....,html.Div(....)],style={...}),
        #         html.Div(className='.........', children=[html.Div(....),html.Div(....)],style={...})
        #         ]
        return [
            html.Div(className='chart-item', children=[html.Div(
                children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(
                children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# %%
