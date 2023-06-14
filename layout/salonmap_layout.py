import time
import math
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

default_font='Comic Sans Ms'

df = pd.read_csv('./data/for_map_df_tmp.csv', low_memory=False)

sidebar = html.Div(
    [
        dbc.Row(
            html.P(
                children='Select the parameters.',
                style={'margin':'10px', 'fontSize':22},
            ),
            className='bg-secondary'
        ),
        dbc.Row(
            [
                html.P(
                    children='Select some prefecture',
                    style={'margin': '10px',
                        #    'width':'175px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='multi_dropdown1',
                    options=[
                        {'label':x, 'value':x} for x in df['県'].unique()
                    ],
                    value='広島',
                    style={'width':'300px',
                           'height': '80px',
                           'margin-bottom':'1px', 'fontSize':15},
                    clearable=True,
                    multi=True,
                    className='text-dark'
                ),
                html.P(
                    children='Select some region',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='multi_dropdown2',
                    options = [{'label':x, 'value':x} for x in df['県'].unique()],
                    style={'width':'300px',
                           'height': '80px',
                           'margin-bottom':'1px',
                           'fontSize':15},
                    clearable=True,
                    multi=True,
                    value='八丁堀・幟町・胡町',
                    className='text-dark',
                ),
                dbc.Button(
                    id='salonmap_button',
                    children='Apply',
                    color='info',
                    n_clicks=0,
                    style={'margin':'30px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
                html.Hr(),
                html.Br(),
            ]
        )
    ],
    style={'font-family': default_font}
)

content = html.Div(
    [
        dbc.Row(
            [   # 1行1列
                dbc.Col(
                    [   
                        dcc.Loading(id="loading_1-1",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='gender-ratio',
                                            ), 
                                        ]
                                    )
                            ],
                            style={"margin": "10%",
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                ],
                className='bg-info',
                style={'padding':'8px'}
                ),
                # 1行2列
                dbc.Col(
                    [   
                        dcc.Loading(id="loading_1-2",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='age-ratio',
                                            ), 
                                        ]
                                    )
                            ],
                            style={"margin": "10%",
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],
                    # 画面のワイドの設定はcol-**で設定した方がいい。横が12だからcol−６で半分
                    className='bg-info',
                    style={'padding':'8px'}
                ),
                # 1行3列
                dbc.Col(
                    [   
                        dcc.Loading(id="loading_1-3",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='hair-color-ratio',
                                            ), 
                                        ]
                                    )
                            ],
                            style={"margin": "10%",
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],
                    className='bg-info',
                    style={'padding':'8px'}
                ),
                # 1行4列
                dbc.Col(  
                    [   
                        dcc.Loading(id="loading_1-4",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='treatment-ratio',
                                            ), 
                                        ]
                                    )
                            ],
                            style={"margin": "10%",
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],                                          
                    className='bg-info',
                    style={'padding':'8px'}
                )
            ],
            className='bg-primary',
            style={'height':'30vh'}
        ),
        dbc.Row(
            [   
            ],
            style={'height':'30vh'}
        ),
        # 3行
        dbc.Row(
            [   #3行1列
            ],
            className='bg-info',
            style={'height':'40vh'}
        )   
    ]
)

salonmap_layout = [
    dbc.Row(
        [
            dbc.Col(
                children=sidebar,
                width=2,
                className='bg-primary'
            ),
            dbc.Col(
                children=content,
                width=10,
                className='bg-info'
            )
        ],
        style={'height':'95vh'}
    )
]


@callback(
    Output('multi_dropdown2', 'options'),
    Input('multi_dropdown1', 'value')
)
def update_area(value):
    if type(value) == str:
        return [{'label': x2,'value': x2} for x2 in df[df['県']==value]['エリア'].unique()]    
    if type(value) == list:
        return [{'label': x2,'value': x2} for x2 in df[df['県'].isin(value)]['エリア'].unique()]