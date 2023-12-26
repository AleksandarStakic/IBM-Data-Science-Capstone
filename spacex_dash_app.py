# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df.rename(columns={'Launch Site': 'LaunchSite'}, inplace=True)
spacex_df.rename(columns={'Payload Mass (kg)': 'PayloadMass'}, inplace=True)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                         {'label': 'ALL SITES', 'value': 'ALL'},
                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here", 
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                               dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,max=max_payload,step=1000,
                                                value=[min_payload+1000,max_payload-1000],
                                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
	Output(component_id='success-pie-chart', component_property='figure'), 
	Input(component_id='site-dropdown', component_property='value')
	)
def get_pie(site):
	site_df = spacex_df[spacex_df["LaunchSite"] == site].groupby(['LaunchSite', 'class']).size().reset_index(name='class_count')
	if site == "ALL":
		fig = px.pie(data_frame = spacex_df, values = "class", names = "LaunchSite")
		return fig
	else:
		fig = px.pie(data_frame = site_df, values = "class_count", names = "class")
		return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def get_scatter(site, payload):
	payload_df = spacex_df[(spacex_df['PayloadMass']>=payload[0])&(spacex_df['PayloadMass']<=payload[1])]
	site_df = spacex_df.loc[spacex_df['LaunchSite'] == site]
	site_payload_df = site_df[(site_df['PayloadMass']>=payload[0])&(spacex_df['PayloadMass']<=payload[1])]
	if site == "ALL":
		fig = px.scatter(data_frame = payload_df, x = "PayloadMass", y = "class", color="Booster Version Category")
		return fig
	else:
		fig = px.scatter(data_frame = site_payload_df, x = "PayloadMass", y = "class", color="Booster Version Category")
		return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
    
    
    
    
    
    
    
    
