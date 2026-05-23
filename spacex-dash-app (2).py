import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Min and max payload
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create app
app = Dash(__name__)

# Layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center'}
    ),

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),

    dcc.Graph(id='success-payload-scatter-chart')

])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for site {entered_site}'
        )

        return fig

# Callback for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_chart(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome for All Sites'
        )

        return fig

    else:

        site_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome for {selected_site}'
        )

        return fig

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060, debug=True)
