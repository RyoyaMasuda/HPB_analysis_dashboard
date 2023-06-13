from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

nav_contens = [
    dbc.NavItem(
        dbc.NavLink(
            id='home',
            children='Home',
            href='/',
            external_link=True,
            style={'fontSize':18}
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='dashboard',
            children='Dashboard',
            href='/',
            external_link=True,
            style={'fontSize':18}
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='map',
            children='Map',
            href='/',
            external_link=True,
            style={'fontSize':18}
        )
    ),
    dbc.NavItem(
        dbc.NavLink(
            id='hoge',
            children='hoge',
            href='/',
            external_link=True,
            style={'fontSize':18}
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
        fluid=True
)