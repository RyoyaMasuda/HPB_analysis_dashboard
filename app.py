import math
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

from navber import navber
from layout.home_layout import home_layout

default_font='Comic Sans Ms'

app = Dash(__name__,
           suppress_callback_exceptions=True,
           prevent_initial_callbacks=False,
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

@app.callback(
    [Output('layout', 'children')],
    [Input('url', 'pathname')]
)
def update_page(href):
    if href == '/':
        return home_layout
    
if __name__ == '__main__':
    app.run_server(debug=True, port=7001)