from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

nav_contens = [
    dbc.NavItem(
        dbc.NavLink(
            id='home',
            children='Home',
            href='/',
            external_link=True,
            style={'fontSize':18,},
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='analysis_dashboard',
            children='AnalysisDashboard',
            href='/analysis_dashboard',
            external_link=True,
            style={'fontSize':18,},
            active='partial'
            
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='salon_map',
            children='SalonMap',
            href='/salon_map',
            external_link=True,
            style={'fontSize':18,},
            active='partial'
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='review_table',
            children='ReviewTable',
            href='/review_table',
            external_link=True,
            style={'fontSize':18,},
            active='partial'
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='potential_analysis',
            children='PotentialAnalysis(AI)',
            href='/potential_analysis',
            external_link=True,
            style={'fontSize':18,},
            active='partial'
        )
    )
]

navber = dbc.NavbarSimple(
        children=[
            dcc.Location(id='url'),
            dbc.Nav(
                children=nav_contens,
                pills=False,
                fill=False,
                style={'font-family':'Comic Sans Ms'}
            ),
            html.Img(
                src='assets/og_beauty.png',
                style={'height':40,
                       'padding':'5px'
                    }
            )
        ],
        brand='Hot Pepper Beauty Review Analysis Dashboard',
        brand_href='/',
        brand_style={'fontSize':30, 'font-family':'Comic Sans Ms'},
        className='bg-dark font-weight-bold text-warning',
        dark=True,
        fluid=True,
)