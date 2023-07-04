from flask import Flask
from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
from navber import navber
from layout import dashboard_layout, salonmap_layout, reviewtable_layout, potentialAI_layout, home_layout, contact_layout

default_font='Comic Sans Ms'

app = Dash(__name__,
           suppress_callback_exceptions=True,
           prevent_initial_callbacks='initial_duplicate',
           external_stylesheets=[dbc.themes.DARKLY],
           update_title=None,
           )
server = app.server

app.title = "Hot Pepper Beauty Review Analysis Dashboard"

app.layout = dbc.Container(
    [
        dbc.Row(
            children=navber
        ),
        html.Div(
            id='layout',
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
        return home_layout.home_layout
    if href == '/analysis_dashboard':
        return dashboard_layout.dashboard_layout
    if href == '/salon_map':
        return salonmap_layout.salonmap_layout
    if href == '/review_table':
        return reviewtable_layout.reviewtable_layout
    if href == '/potential_analysis':
        return potentialAI_layout.potensialAI_layout
    if href=='/contact':
        return contact_layout.contact_layout
    
if __name__ == '__main__':
    app.run(debug=True,
            #  host='0.0.0.0',
               port=8029)
