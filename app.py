import math
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

from navber import navber
from layout import dashboard_layout, salonmap_layout, reviewtable_layout, potentialAI_layout

default_font='Comic Sans Ms'

app = Dash(__name__,
           suppress_callback_exceptions=True,
           prevent_initial_callbacks='initial_duplicate',
           external_stylesheets=[dbc.themes.DARKLY],
           update_title=None,
           )
app.title = "Hot Pepper Beauty Review Analysis Dashboard"

app.layout = dbc.Container(
    [
        dbc.Row(
            children=navber
        ),
        html.Div(
            id='layout',
            # children=update_page()の返り値
        )
    ],
    fluid=True
)

home_layout = [
    html.Div(
        children='aaa'
    )
]

@app.callback(
    [Output('layout', 'children')],
    [Input('url', 'pathname')]
)
def update_page(href):
    if href == '/':
        return home_layout
    if href == '/analysis_dashboard':
        return dashboard_layout.dashboard_layout
    if href == '/salon_map':
        return salonmap_layout.salonmap_layout
    if href == '/review_table':
        return reviewtable_layout.reviewtable_layout
    if href == '/potential_analysis':
        return potentialAI_layout.potensialAI_layout
    
if __name__ == '__main__':
    app.run_server(debug=True, port=7016)