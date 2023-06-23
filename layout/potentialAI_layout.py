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

df = pd.read_csv('./data_for_revise/prediction/payments/dataset_for_payments.csv', low_memory=False)
print(df.columns)

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
                    children='Select a prefecture',
                    style={'margin': '10px',
                        #    'width':'175px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='AI_dropdown1',
                    options=[
                        {'label':x, 'value':x} for x in df['県'].unique()
                    ],
                    value='広島',
                    style={'width':'300px',
                        #    "height":"20px",
                           'margin-bottom':'1px', 'fontSize':16},
                    clearable=True,
                    className='text-dark'
                ),
                html.P(
                    children='Select a region',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='AI_dropdown2',
                    # options = callbackで返ってくる。
                    style={'width':'300px',
                        #    "height":"5px",
                           "margin-bottom":'1px', 'fontSize':16},
                    clearable=True,
                    value='八丁堀・幟町・胡町',
                    className='text-dark',
                ),
                html.P(
                    children='Select the number for items below',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Seats',
                                    style={
                                        'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input',
                                    placeholder="Select...",
                                    # options = callbackで返ってくる。
                                    value=3,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    min=1,
                                    max=30,
                                    step=1,
                                    type="number"
                                ),
                            ]    
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Blog Posts',
                                    style={'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input2',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=100,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    type="text", inputmode="numeric", pattern="[0-9]*",
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Review',
                                    style={'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input3',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=150,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        #    'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    type="text", inputmode="numeric", pattern="[0-9]*",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Staff',
                                    style={'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input4',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=4,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        #    'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    min=1,
                                    max=50,
                                    step=1,
                                    type="number",
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Coupon',
                                    style={
                                        'margin-left': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input5',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=20,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                            'margin-bottom':'1px',
                                            # 'margin-left':'12px',
                                            'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    min=1,
                                    max=150,
                                    step=1,
                                    type="number",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Menu',
                                    style={
                                        'margin-left': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input6',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=15,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    min=1,
                                    max=150,
                                    step=1,
                                    type="number",
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Style',
                                    style={
                                        'margin-left': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input7',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=100,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                            'margin-bottom':'1px',
                                            # 'margin-left':'12px',
                                            'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    type="text", inputmode="numeric", pattern="[0-9]*",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Time from station(walk)',
                                    style={
                                        'margin-left': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':11},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input8',
                                    placeholder='Select...',
                                    # options = callbackで返ってくる。
                                    value=9,
                                    style={'width':'135px',
                                        #    "height":"30px",
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                                    className='text-dark',
                                    size="sm",
                                    min=1,
                                    max=40,
                                    step=1,
                                    type="number",
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                html.P(
                    children='Select utilizing of brands below',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Illumina(WELLA)',
                                    style={
                                        'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':14},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown3',
                                    options=[
                                        {'label':"メニュー化", 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'135px',
                                        'margin-bottom':'1px',
                                        'fontSize':14},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]    
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Addicthy(MILBON)',
                                    style={'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':12},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown4',
                                    options=[
                                        {'label':"メニュー化", 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'135px',
                                        'margin-bottom':'1px',
                                        'fontSize':14},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Inoa(LOREAL)',
                                    style={
                                        'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown5',
                                    options=[
                                        {'label':"メニュー化", 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'135px',
                                        'margin-bottom':'1px',
                                        'fontSize':14},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]    
                        ),
                        dbc.Col(
                            [
                                html.Span(
                                    children='Aujua(MILBON)',
                                    style={'margin': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown6',
                                    options=[
                                        {'label':"メニュー化", 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'135px',
                                        'margin-bottom':'1px',
                                        'fontSize':14},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]
                        )
                    ],
                    style={"margin-bottom": "10px"}
                ),
                dbc.Button(
                    id='tmp_button',
                    children='Predict',
                    color='info',
                    n_clicks=0,
                    style={'margin':'20px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
                html.Hr(),
                html.Br(),
            ]
        ),
    ],
    style={'font-family': default_font}
)

content = html.Div(
    [
        # dbc.Row(
        #     [   # 1行1列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_1-1",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_gender-ratio',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #         ],
        #         className='bg-info',
        #         style={'padding':'8px'}
        #         ),
        #         # 1行2列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_1-2",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_age-ratio',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],
        #             # 画面のワイドの設定はcol-**で設定した方がいい。横が12だからcol−６で半分
        #             className='bg-info',
        #             style={'padding':'8px'}
        #         ),
        #         # 1行3列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_1-3",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_hair-color-ratio',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],
        #             className='bg-info',
        #             style={'padding':'8px'}
        #         ),
        #         # 1行4列
        #         dbc.Col(  
        #             [   
        #                 dcc.Loading(id="tmp_loading_1-4",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_treatment-ratio',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],                                          
        #             className='bg-info',
        #             style={'padding':'8px'}
        #         )
        #     ],
        #     className='bg-primary',
        #     style={'height':'30vh'}
        # ),
        # dbc.Row(
        #     [   # 2行1列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_2-1",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_cut-only-comparison',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],                    
        #             # className='bg-info',
        #             style={'padding':'8px'},
        #             className='bg-info'
        #         ),
        #         # 2行2列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_2-2",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_cut-and-colr-comparison',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],
        #             style={'padding':'8px'},
        #             className='bg-info'
        #             ),
        #         # 2行3列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_2-3",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_cut-and-colr-and-treatment-comparison',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],                    
        #             style={'padding':'8px'},
        #             className='bg-info'
        #         ),
        #         # 2行4列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_2-4",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_all-menu-comparison',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",},
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],                       
        #             style={'padding':'8px'},
        #             className='bg-info'
        #         )
        #     ],
        #     # className='bg-secondary',
        #     style={'height':'30vh'}
        # ),
        # dbc.Row(
        #     [   #3行1列
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_3-1",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_total_bill_boxplot',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],                    
        #             style={'padding':'8px'},
        #             className='bg-info'
        #             ),
        #         dbc.Col(
        #             [   
        #                 dcc.Loading(id="tmp_loading_3-1",
        #                     children=[
        #                             html.Div(
        #                                 [
        #                                     dcc.Graph(
        #                                     id='tmp_coupon-ranking',
        #                                     ), 
        #                                 ]
        #                             )
        #                     ],
        #                     style={"margin": "10%",
        #                             },
        #                     type='dot',
        #                     color='#ffffb3',
        #                     className='bg-info'),
        #             ],
        #             style={'padding':'8px'},
        #             className='light'
        #             ),
        #     ],
        #     className='bg-info',
        #     style={'height':'40vh'}
        # )   
    ]
)

potensialAI_layout = [
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
    Output('AI_dropdown2', 'options'),
    Input('AI_dropdown1', 'value')
)
def update_area(value):
    return [{'label': x2,'value': x2} for x2 in df[df['県'] == value]['エリア'].unique()]

# @callback(
#     Output('dropdown3', 'options'),
#     Input('dropdown2', 'value')
# )
# def update_salon(value):
#     return [{'label': x3,'value': x3} for x3 in df[df['エリア'] == value]['サロン名'].unique()]

# # 県を削除したときにサロン名も消える処理
# @callback(
#     Output('dropdown3', 'value'),
#     Input('dropdown1', 'value'),
#     prevent_initial_call=True
# )
# def update_area(value):
#     if value is None:
#         return ''

# @callback(
#     Output('checklist1', 'options'),
#     Input('dropdown3', 'value'),
#     Input('dropdown2', 'value'),
#     #
# )
# def update_gender(dropdown3_value, dropdown2_value):
    
#     _df = df.copy()
#     _df = df[df['エリア'] == dropdown2_value]
    
#     if dropdown3_value is None:
#         dropdown3_value = _df['サロン名'].unique()
#     else:
#         dropdown3_value = [dropdown3_value]
    
#     _df = _df[_df['サロン名'].isin(dropdown3_value)]
    
#     return [{'label': x3,'value': x3} for x3 in _df['性別'].unique()]

# # サイドバーのサロンインフォメーション
# @callback(
#     Output('salon_infomation', 'children'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def salon_infomation(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
#     salon_name = _df['サロン名'].unique()[0]
#     salon_adress = _df['住所'].unique()[0]
#     num_of_seat = _df['セット面の数'].unique()[0]
#     num_of_staff = _df['スタッフ数'].unique()[0]
#     num_of_review = _df['口コミ数'].unique()[0]
#     num_of_coupon = _df['クーポン数'].unique()[0]
#     num_of_menu = _df['メニュー数'].unique()[0]
#     link = _df['URL'].unique()[0]
    
#     children = [
#                     html.P(children='Salon Information',
#                             style={'text-align':'center',
#                                     'fontSize':20},
#                             className='bg-light col-10 mx-auto'),
#                     html.P(children='Salon Name :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=salon_name,
#                             style={'text-align':'center',
#                                     'fontSize': 18,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Salon Address :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=salon_adress,
#                             style={'text-align':'center',
#                                     'fontSize': 16,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Number Of Sheets :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=f'{num_of_seat}席',
#                             style={'text-align':'center',
#                                     'fontSize': 18,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Number Of Staff :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=f'{num_of_staff}人',
#                             style={'text-align':'center',
#                                     'fontSize': 18,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Number Of Review :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=f'{num_of_review}口コミ',
#                             style={'text-align':'center',
#                                     'fontSize': 18,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Number Of Coupon & Menu :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children=f'クーポン数={num_of_coupon} メニュー数={num_of_menu}',
#                             style={'text-align':'center',
#                                     'fontSize': 18,
#                                     'text-decoration':'underline'},
#                             className='font-weight-bold'
#                         ),
#                     html.P(children='Link to Hot Pepper Beauty :',
#                             style={'margin':'5px'},
#                             className='font-weight-bold'
#                         ),
#                     dbc.Row(
#                         dbc.Col(
#                             html.Div(
#                                 [
#                                     html.A(children='HPBのページへ飛ぶ',
#                                             href=link,
#                                             target='_blank',
#                                             style={'text-decoration':'underline',
#                                                     'margin':'5px'
#                                             },
#                                         ),
#                                     ]
#                                 ),
#                             width={"size": 6, "offset": 3},
#                         )
#                     ),
#                 ]
    
    
#     return children
    

# # 1行1列
# @callback(
#     Output('gender-ratio', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def gender_ratio_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
#     _df =_df.groupby('性別').count().iloc[:,0:1].reset_index()
#     _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
#     figure = px.pie(
#         data_frame=_df,
#         names='性別',
#         values='客数(口コミ数)',
#         color='性別',
#         title=f'Gender Ratio',
#         height=290,
#         width=418,
#         color_discrete_map={'女性':'skyblue','男性':'peachpuff','未設定':'palegreen'},
#     )
    
#     figure.update_traces(
#         textinfo='percent+label',
#         textposition='inside',
#         marker=dict(
#             line=dict(
#                 color='slategrey',
#                 width=2.0
#             ),
#         )
#     )
    
#     figure.update_layout(
#         uniformtext_mode='hide',
#         uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='性別',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#         ),
        
#     )
    
#     return figure

# # 1行2列
# @callback(
#     Output('age-ratio', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def age_ratio_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
#     _df = _df.groupby('年齢').count().iloc[:,0:1].reset_index()
#     _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
#     figure = px.pie(
#         data_frame=_df,
#         names='年齢',
#         values='客数(口コミ数)',
#         color='年齢',
#         title='Age Ratio',
#         height=290,
#         width=418,
#         # color_discrete_map={'女性':'cornflowerblue','男性':'hotpink','未設定':'darkorange'},
#         color_discrete_sequence=plotly.colors.qualitative.Set3,
#         category_orders={'年齢':['～10代前半', '10代後半', '20代前半', '20代後半', '30代前半', '30代後半', '40代', '50代', '60代', '70代～', '未設定']}
#     )
    
#     figure.update_traces(
#         textinfo='percent+label',
#         textposition='inside',
#         marker=dict(
#             line=dict(
#                 color='slategrey',
#                 width=2.0
#             ),
#         ),
#     )
    
#     figure.update_layout(
#         uniformtext_mode='hide',
#         uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # ユーザーによって未定義にされたレイアウトの幅や高さを、各リレーアウトで初期化するかどうかを決定します。この属性に関係なく、未定義のレイアウトの幅や高さは、plotの最初の呼び出しで常に初期化されることに注意してください。
#         # autosize=True,
#         legend=dict(
#             title=dict(text='年齢',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # valign='top',
#             # ↓多分いらない。itemsizing=
#             # itemsizing='constant'
#         ),
        
#     )
    
#     return figure

# # 1行3列
# @callback(
#     Output('hair-color-ratio', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def hair_color_ratio_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
#     _df =_df.groupby('カラー選択').count().iloc[:,0:1].reset_index()
#     _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
#     _df.loc[_df['カラー選択']==0, 'カラー選択'] = 'カラー未実施'
#     _df.loc[_df['カラー選択']==1, 'カラー選択'] = 'カラー実施'

#     figure = px.pie(
#         data_frame=_df,
#         names='カラー選択',
#         values='客数(口コミ数)',
#         color='カラー選択',
#         title=f'Percentage Of Color Selected',
#         height=290,
#         width=418,
#         color_discrete_map={'カラー実施':'#fccde5','カラー未実施':'#b3de69'},
#         category_orders={'カラー選択':['カラー実施', 'カラー未実施']}
#     )
    
#     figure.update_traces(
#         textinfo='percent+label',
#         textposition='inside',
#         marker=dict(
#             line=dict(
#                 color='slategrey',
#                 width=2.0
#             ),
#         )
#     )
    
#     figure.update_layout(
#         uniformtext_mode='hide',
#         uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='カラー選択の有無',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#         ),
        
#     )
    
#     return figure

# # 1行4列
# @callback(
#     Output('treatment-ratio', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def treatment_ratio_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
#     _df =_df.groupby('トリートメント選択').count().iloc[:,0:1].reset_index()
#     _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
#     _df.loc[_df['トリートメント選択']==0, 'トリートメント選択'] = 'Tr未実施'
#     _df.loc[_df['トリートメント選択']==1, 'トリートメント選択'] = 'Tr実施'

#     figure = px.pie(
#         data_frame=_df,
#         names='トリートメント選択',
#         values='客数(口コミ数)',
#         color='トリートメント選択',
#         title=f'Percentage Of Treatment Selected',
#         height=290,
#         width=418,
#         color_discrete_map={'Tr実施':'#fccde5','Tr未実施':'#b3de69'},
#         category_orders={'トリートメント選択':['Tr実施', 'Tr未実施']}
#     )
    
#     figure.update_traces(
#         textinfo='percent+label',
#         textposition='inside',
#         marker=dict(
#             line=dict(
#                 color='slategrey',
#                 width=2.0
#             ),
#         )
#     )
    
#     figure.update_layout(
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,
#         uniformtext_mode='hide',
#         uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='Tr選択の有無',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#         ),
        
#     )
    
#     return figure


# # 2行1列
# @callback(
#     Output('cut-only-comparison', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def cut_only_compare_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):

#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]

#     _df_prefecture = _df.copy()
#     prefecture_mean = int(round(_df_prefecture.loc[
#         ((_df_prefecture['カット選択']==1)&(_df_prefecture['カラー選択']==0)&(_df_prefecture['トリートメント選択']==0)&(_df_prefecture['パーマ選択']==0)&\
#         (_df_prefecture['縮毛矯正選択']==0)&(_df_prefecture['その他選択']==0)&(_df_prefecture['ヘッドスパ選択']==0)&(_df_prefecture['ヘアセット選択']==0)&\
#         (_df_prefecture['エクステ選択']==0)&(_df_prefecture['着付け選択']==0)&(_df_prefecture['メニュー無し選択']==0)&(_df_prefecture['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['エリア'] == dropdown2_value]

#     _df_area = _df.copy()
#     area_mean = int(round(_df_area.loc[
#         ((_df_area['カット選択']==1)&(_df_area['カラー選択']==0)&(_df_area['トリートメント選択']==0)&(_df_area['パーマ選択']==0)&\
#         (_df_area['縮毛矯正選択']==0)&(_df_area['その他選択']==0)&(_df_area['ヘッドスパ選択']==0)&(_df_area['ヘアセット選択']==0)&\
#         (_df_area['エクステ選択']==0)&(_df_area['着付け選択']==0)&(_df_area['メニュー無し選択']==0)&(_df_area['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['サロン名'] == dropdown3_value]
#     _df = _df[_df['性別'].isin(checklist1_value)]

#     _df_salon = _df.copy()
#     try:
#         salon_mean = int(round(_df_salon.loc[
#             ((_df_salon['カット選択']==1)&(_df_salon['カラー選択']==0)&(_df_salon['トリートメント選択']==0)&(_df_salon['パーマ選択']==0)&\
#             (_df_salon['縮毛矯正選択']==0)&(_df_salon['その他選択']==0)&(_df_salon['ヘッドスパ選択']==0)&(_df_salon['ヘアセット選択']==0)&\
#             (_df_salon['エクステ選択']==0)&(_df_salon['着付け選択']==0)&(_df_salon['メニュー無し選択']==0)&(_df_salon['支出金額']!=0)),
#             ['支出金額']].mean()))
#     except ValueError:
#         try:
#             salon_mean = int(_df['カット料金'].unique()[0])
#         except Exception:
#             salon_mean = 0
        
#     __df1 = pd.DataFrame(data=[salon_mean, area_mean, prefecture_mean], index=['サロン', 'エリア', '県'], columns=['単価(平均価格)'])
#     __df1 = __df1.reset_index().rename(columns={'index':'算出レンジ'})

#     xaxes_range_min = int(round(__df1['単価(平均価格)'].min()/2, -3))
#     range_max = int(math.ceil(__df1['単価(平均価格)'].max()))
#     xaxes_range_max = math.ceil(range_max/1000) * 1000 + 1000

#     # 1秒遅らせる処理を入れて原因不明のバグを修正
#     time.sleep(1)
#     figure=px.bar(data_frame=__df1,
#                   y='算出レンジ',
#                   x='単価(平均価格)',
#                   color='算出レンジ',
#                   color_discrete_map={'サロン':'#8dd3c7','エリア':'#ffffb3','県':'#fdb462'},
#                   category_orders={'算出レンジ':['サロン', 'エリア', '県']},
#                   text=[f'¥{text:,}' for text in __df1['単価(平均価格)']],
#                   title=f'Cut Unit Price',
#                   height=290,
#                   width=418,
#                 )
    
        
#     figure.update_traces(
#         width=0.6,
#         orientation='h',
#         # texttemplate=,
#         textposition='outside',
#         textfont=dict(size=12),
#         hovertemplate='単価(平均価格): ¥%{x:,}<br>算出レンジ: %{y}',
#         marker=dict(
#             line=dict(
#             color='slategrey',
#             width=1.5,
#             )
#         ),
#         # showlegend=False
#     )

#     figure.update_layout(
#         # uniformtext_minsize=8,
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,
#         uniformtext_mode='hide',
#         margin={'l':0, 'r':50, 't':40, 'b':20},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='算出範囲',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=1.5,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # tracegroupgap=1,
#             # itemsizing='constant'
#         ),   
#     )

#     figure.update_xaxes(
#         # rangemode='tozero',
#         tickformat=',',
#         tickprefix='¥',
#         tickvals=np.arange(xaxes_range_min, xaxes_range_max, 1000),
#         range=(xaxes_range_min,xaxes_range_max)
#     )
    
#     figure.update_yaxes(
#         title=''
#     )    
    
#     return figure

# # 2行2列
# @callback(
#     Output('cut-and-colr-comparison', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def cut_and_color_compare_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):

#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]

#     _df_prefecture = _df.copy()
#     prefecture_mean = int(round(_df_prefecture.loc[
#         ((_df_prefecture['カット選択']==1)&(_df_prefecture['カラー選択']==1)&(_df_prefecture['トリートメント選択']==0)&(_df_prefecture['パーマ選択']==0)&\
#         (_df_prefecture['縮毛矯正選択']==0)&(_df_prefecture['その他選択']==0)&(_df_prefecture['ヘッドスパ選択']==0)&(_df_prefecture['ヘアセット選択']==0)&\
#         (_df_prefecture['エクステ選択']==0)&(_df_prefecture['着付け選択']==0)&(_df_prefecture['メニュー無し選択']==0)&(_df_prefecture['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['エリア'] == dropdown2_value]

#     _df_area = _df.copy()
#     area_mean = int(round(_df_area.loc[
#         ((_df_area['カット選択']==1)&(_df_area['カラー選択']==1)&(_df_area['トリートメント選択']==0)&(_df_area['パーマ選択']==0)&\
#         (_df_area['縮毛矯正選択']==0)&(_df_area['その他選択']==0)&(_df_area['ヘッドスパ選択']==0)&(_df_area['ヘアセット選択']==0)&\
#         (_df_area['エクステ選択']==0)&(_df_area['着付け選択']==0)&(_df_area['メニュー無し選択']==0)&(_df_area['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['サロン名'] == dropdown3_value]
#     _df = _df[_df['性別'].isin(checklist1_value)]

#     _df_salon = _df.copy()
#     try:
#         salon_mean = int(round(_df_salon.loc[
#             ((_df_salon['カット選択']==1)&(_df_salon['カラー選択']==1)&(_df_salon['トリートメント選択']==0)&(_df_salon['パーマ選択']==0)&\
#             (_df_salon['縮毛矯正選択']==0)&(_df_salon['その他選択']==0)&(_df_salon['ヘッドスパ選択']==0)&(_df_salon['ヘアセット選択']==0)&\
#             (_df_salon['エクステ選択']==0)&(_df_salon['着付け選択']==0)&(_df_salon['メニュー無し選択']==0)&(_df_salon['支出金額']!=0)),
#             ['支出金額']].mean()))
#     except ValueError:
#         salon_mean = 0
    
#     __df2 = pd.DataFrame(data=[salon_mean, area_mean, prefecture_mean], index=['サロン', 'エリア', '県'], columns=['単価(平均価格)'])
#     __df2 = __df2.reset_index().rename(columns={'index':'算出レンジ'})

#     xaxes_range_min = int(round(__df2['単価(平均価格)'].min()/2, -3))
#     range_max = int(math.ceil(__df2['単価(平均価格)'].max()))
#     xaxes_range_max = math.ceil(range_max/1000) * 1000 + 2000

#     #１秒遅らせる処理を入れて原因不明のバグを修正
#     time.sleep(1)
#     figure=px.bar(data_frame=__df2,
#                   y='算出レンジ',
#                   x='単価(平均価格)',
#                   color='算出レンジ',
#                   color_discrete_map={'サロン':'#8dd3c7','エリア':'#ffffb3','県':'#fdb462'},
#                   category_orders={'算出レンジ':['サロン', 'エリア', '県']},
#                   text=[f'¥{text:,}' for text in __df2['単価(平均価格)']],
#                   title=f'Cut & Color Unit Price',
#                   height=290,
#                   width=418,
#                 )
    
                
#     figure.update_traces(
#         width=0.6,
#         orientation='h',
#         # texttemplate=,
#         textposition='outside',
#         textfont=dict(size=12),
#         hovertemplate='単価(平均価格): ¥%{x:,}<br>算出レンジ: %{y}',
#         marker=dict(
#             line=dict(
#             color='slategrey',
#             width=1.5,
#             )
#         ),
#         # showlegend=False
#     )

#     figure.update_layout(
#         uniformtext_mode='hide',
#         uniformtext_minsize=8,
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,
#         margin={'l':0, 'r':50, 't':40, 'b':20},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='算出範囲',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=1.5,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # tracegroupgap=1,
#             # itemsizing='constant'
#         ),   
#     )

#     figure.update_xaxes(
#         # rangemode='tozero',
#         tickformat=',',
#         tickprefix='¥',
#         tickvals=np.arange(xaxes_range_min, xaxes_range_max, 2000),
#         range=(xaxes_range_min,xaxes_range_max),
#     )
    
#     figure.update_yaxes(
#         title=''
#     )    
    
#     return figure
    


# # 2行3列
# @callback(
#     Output('cut-and-colr-and-treatment-comparison', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def cut_and_color_and_treatment_compare_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):

#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]

#     _df_prefecture = _df.copy()
#     prefecture_mean = int(round(_df_prefecture.loc[
#         ((_df_prefecture['カット選択']==1)&(_df_prefecture['カラー選択']==1)&(_df_prefecture['トリートメント選択']==1)&(_df_prefecture['パーマ選択']==0)&\
#         (_df_prefecture['縮毛矯正選択']==0)&(_df_prefecture['その他選択']==0)&(_df_prefecture['ヘッドスパ選択']==0)&(_df_prefecture['ヘアセット選択']==0)&\
#         (_df_prefecture['エクステ選択']==0)&(_df_prefecture['着付け選択']==0)&(_df_prefecture['メニュー無し選択']==0)&(_df_prefecture['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['エリア'] == dropdown2_value]

#     _df_area = _df.copy()
#     area_mean = int(round(_df_area.loc[
#         ((_df_area['カット選択']==1)&(_df_area['カラー選択']==1)&(_df_area['トリートメント選択']==1)&(_df_area['パーマ選択']==0)&\
#         (_df_area['縮毛矯正選択']==0)&(_df_area['その他選択']==0)&(_df_area['ヘッドスパ選択']==0)&(_df_area['ヘアセット選択']==0)&\
#         (_df_area['エクステ選択']==0)&(_df_area['着付け選択']==0)&(_df_area['メニュー無し選択']==0)&(_df_area['支出金額']!=0)),
#         ['支出金額']].mean()))

#     _df = _df[_df['サロン名'] == dropdown3_value]
#     _df = _df[_df['性別'].isin(checklist1_value)]

#     _df_salon = _df.copy()
#     try:
#         salon_mean = int(round(_df_salon.loc[
#             ((_df_salon['カット選択']==1)&(_df_salon['カラー選択']==1)&(_df_salon['トリートメント選択']==1)&(_df_salon['パーマ選択']==0)&\
#             (_df_salon['縮毛矯正選択']==0)&(_df_salon['その他選択']==0)&(_df_salon['ヘッドスパ選択']==0)&(_df_salon['ヘアセット選択']==0)&\
#             (_df_salon['エクステ選択']==0)&(_df_salon['着付け選択']==0)&(_df_salon['メニュー無し選択']==0)&(_df_salon['支出金額']!=0)),
#             ['支出金額']].mean()))
#     except ValueError:
#         salon_mean = 0
        
#     __df = pd.DataFrame(data=[salon_mean, area_mean, prefecture_mean], index=['サロン', 'エリア', '県'], columns=['単価(平均価格)'])
#     __df = __df.reset_index().rename(columns={'index':'算出レンジ'})

#     xaxes_range_min = int(round(__df['単価(平均価格)'].min()/2, -3))
#     range_max = int(math.ceil(__df['単価(平均価格)'].max()))
#     xaxes_range_max = math.ceil(range_max/1000) * 1000 + 2000

#     figure=px.bar(data_frame=__df,
#                   y='算出レンジ',
#                   x='単価(平均価格)',
#                   color='算出レンジ',
#                   color_discrete_map={'サロン':'#8dd3c7','エリア':'#ffffb3','県':'#fdb462'},
#                   category_orders={'算出レンジ':['サロン', 'エリア', '県']},
#                   text=[f'¥{text:,}' for text in __df['単価(平均価格)']],
#                   title=f'Cut & Color & Treatment Unit Price',
#                   height=290,
#                   width=418,
#                 )
    
        
#     figure.update_traces(
#         width=0.6,
#         orientation='h',
#         # texttemplate=,
#         textposition='outside',
#         textfont=dict(size=12),
#         hovertemplate='単価(平均価格): ¥%{x:,}<br>算出レンジ: %{y}',
#         marker=dict(
#             line=dict(
#             color='slategrey',
#             width=1.5,
#             )
#         ),
#         # showlegend=False
#     )

#     figure.update_layout(
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,
#         uniformtext_mode='hide',
#         uniformtext_minsize=8,
#         margin={'l':0, 'r':50, 't':40, 'b':20},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='算出範囲',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=1.5,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # tracegroupgap=1,
#             # itemsizing='constant'
#         ),   
#     )

#     figure.update_xaxes(
#         # rangemode='tozero',
#         tickformat=',',
#         tickprefix='¥',
#         tickvals=np.arange(xaxes_range_min, xaxes_range_max, 2000),
#         range=(xaxes_range_min,xaxes_range_max),
#     )
    
#     figure.update_yaxes(
#         title=''
#     )    
    
#     return figure
    
# # 2行4列
# @callback(
#     Output('all-menu-comparison', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def all_menu_compare_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):

#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]

#     _df_prefecture = _df.copy()
#     prefecture_mean = int(round(_df_prefecture.loc[_df_prefecture['支出金額']!=0, ['支出金額']].mean()))

#     _df = _df[_df['エリア'] == dropdown2_value]

#     _df_area = _df.copy()
#     area_mean = int(round(_df_area.loc[_df_area['支出金額']!=0, ['支出金額']].mean()))

#     _df = _df[_df['サロン名'] == dropdown3_value]
#     _df = _df[_df['性別'].isin(checklist1_value)]

#     _df_salon = _df.copy()
#     try:
#         salon_mean = int(round(_df_salon.loc[_df_salon['支出金額']!=0, ['支出金額']].mean()))
#     except ValueError:
#         salon_mean = 0
        
#     __df = pd.DataFrame(data=[salon_mean, area_mean, prefecture_mean], index=['サロン', 'エリア', '県'], columns=['単価(平均価格)'])
#     __df = __df.reset_index().rename(columns={'index':'算出レンジ'})

#     xaxes_range_min = int(round(__df['単価(平均価格)'].min()/2, -3))
#     range_max = int(math.ceil(__df['単価(平均価格)'].max()))
#     xaxes_range_max = math.ceil(range_max/1000) * 1000 + 2000

#     figure=px.bar(data_frame=__df,
#                   y='算出レンジ',
#                   x='単価(平均価格)',
#                   color='算出レンジ',
#                   color_discrete_map={'サロン':'#8dd3c7','エリア':'#ffffb3','県':'#fdb462'},
#                   category_orders={'算出レンジ':['サロン', 'エリア', '県']},
#                   text=[f'¥{text:,}' for text in __df['単価(平均価格)']],
#                   title=f'All Menu Unit Price',
#                   height=290,
#                   width=418,
#                 )
                
#     figure.update_traces(
#         width=0.6,
#         orientation='h',
#         # texttemplate=,
#         textposition='outside',
#         textfont=dict(size=12),
#         hovertemplate='単価(平均価格): ¥%{x:,}<br>算出レンジ: %{y}',
#         marker=dict(
#             line=dict(
#             color='slategrey',
#             width=1.5,
#             )
#         ),
#         # showlegend=False
#     )

#     figure.update_layout(
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,        
#         uniformtext_mode='hide',
#         uniformtext_minsize=8,
#         margin={'l':0, 'r':50, 't':40, 'b':20},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # autosize=True,
#         legend=dict(
#             title=dict(text='算出範囲',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=1.5,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # tracegroupgap=1,
#             # itemsizing='constant'
#         ),   
#     )

#     figure.update_xaxes(
#         # rangemode='tozero',
#         tickformat=',',
#         tickprefix='¥',
#         tickvals=np.arange(xaxes_range_min, xaxes_range_max, 2000),
#         range=(xaxes_range_min,xaxes_range_max),
#     )
    
#     figure.update_yaxes(
#         title=''
#     )    
    
#     return figure
   
# # 3行1列
# @callback(
#     Output('total_bill_boxplot', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def total_bill_box_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
    
    
#     _df = _df[['サロン名','年齢', '支出金額', '名前', 'メニューの種類', '性別', '職業', '投稿日時','総合','雰囲気','接客サービス',	'技術・仕上がり', 'メニュー・料金']][_df['支出金額']!=0]
    
#     figure = px.box(
#         data_frame=_df,
#         y="支出金額", 
#         x="年齢",
#         color="年齢",
#         points="all",
#         hover_data=_df.columns, title='Distribution of Payments by Age',
#         color_discrete_sequence=plotly.colors.qualitative.T10,
#         category_orders={'年齢':['～10代前半', '10代後半', '20代前半', '20代後半', '30代前半', '30代後半', '40代', '50代', '60代', '70代～', '未設定']},
#         height=400,
#         width=852
#         )

#     figure.update_traces(
#         # 箱ひげ図の太さを調整。
#         width=0.4,
#         marker=dict(
#             line=dict(
#                 color='grey',
#                 width=1.0
#             ),
#             size=5,
#             opacity=0.9
#         ),
#     )

#     figure.update_yaxes(
#         rangemode='tozero',
#         tickformat=',',
#         tickprefix='¥',
#         tickvals=[0,2500,5000,7500,10000,12500,15000,17500,20000,25000,30000,40000,50000,60000]
#     )

#     figure.update_layout(
#         plot_bgcolor='#f7fcf5',
#         xaxis_showgrid=False,
#         yaxis_showgrid=True,        
#         uniformtext_mode='hide',
#         uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                        'color':'grey'},
#                'x':0.5,
#                'y':0.95,
#                'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                   size=12,
#                                 #   color="white"
#                                   )
#                         ),
#         paper_bgcolor='lightcyan',
#         # ユーザーによって未定義にされたレイアウトの幅や高さを、各リレーアウトで初期化するかどうかを決定します。この属性に関係なく、未定義のレイアウトの幅や高さは、plotの最初の呼び出しで常に初期化されることに注意してください。
#         # autosize=True,
#         legend=dict(
#             title=dict(text='年齢',
#                        font=dict(family=default_font,
#                                  size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                       family=default_font,
#                       color='slategrey'),
#             # valign='top'
#             # itemsizing='constant'
#         ),
        
#     )
    
#     return figure

# # 3行2列
# @callback(
#     Output('coupon-ranking', 'figure'),
#     Input('button', 'n_clicks'),
#     [State('dropdown1', 'value'),
#      State('dropdown2', 'value'),
#      State('dropdown3', 'value'),
#      State('checklist1', 'value')])
# def coupon_ranking_table_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
#     _df = df.copy()
#     _df = _df[_df['県']==dropdown1_value]
#     _df = _df[_df['エリア']==dropdown2_value]
#     _df = _df[_df['サロン名']==dropdown3_value]
    
#     _df = _df[_df['性別'].isin(checklist1_value)]
#     _df = _df[(_df['投稿日時'].str.startswith('2023'))|(_df['投稿日時'].str.startswith('2022'))]
#     _df = _df.groupby(['選択されたクーポン']).count().reset_index().iloc[:,0:2]
#     _df.rename(columns={'県':'顧客数'}, inplace=True)
#     total_customer = _df['顧客数'].sum()
#     _df['割合']=_df['顧客数'].apply(lambda x: f'{round((x/total_customer)*100, 2)}%')
#     _df = _df.sort_values(by='顧客数', ascending=False).head(10).reset_index(drop=True)
    
#     ranking = []
#     for i in range(len(_df)):
#         ranking.append(f'{i+1}位')
    
#     _df.insert(0,'ランキング', ranking)
    
#     figure = go.Figure(
#         data=go.Table(
#             columnorder = [1,2,3,4],
#             columnwidth = [60,400,50,50],
#             header={'values':_df.columns,
#                     'fill_color':'#fee391',
#                     'line_color':'lightgrey',
#                     'font_size':14,
#                     'height':30,},
#             cells={'values':[_df[col].tolist() for col in _df.columns],
#                    'fill_color':'#ffffe5',
#                    'line_color':'lightgrey',
#                    'font_size':14,
#                    'height':30,},
#         ),
#         layout=go.Layout(title='Coupon Ranking Table',
#                          height=400,
#                          width=852)
#     )
    
#     figure.update_layout(
#         # uniformtext_mode='hide',
#         # uniformtext_minsize=10,
#         margin={'l':30, 'r':30, 't':50, 'b':10},
#         title={'font':{'size':20,
#                         'color':'grey'},
#                 'x':0.5,
#                 'y':0.95,
#                 'xanchor':'center'},
#         font=dict(
#             family=default_font,
#             size=10,
#         ),
#         # hoverlabel: hoverdataの中の指定
#         hoverlabel=dict(font=dict(family="Comic Sans Ms",
#                                     size=12,
#                                 #   color="white"
#                                     )
#                         ),
#         paper_bgcolor='lightcyan',
#         # ユーザーによって未定義にされたレイアウトの幅や高さを、各リレーアウトで初期化するかどうかを決定します。この属性に関係なく、未定義のレイアウトの幅や高さは、plotの最初の呼び出しで常に初期化されることに注意してください。
#         # autosize=True,
#         legend=dict(
#             title=dict(text='年齢',
#                         font=dict(family=default_font,
#                                     size=12),
#             ),
#             bgcolor='aliceblue',
#             bordercolor='grey',
#             #bordercolorを指定したらborderwidthも指定しないといけない。
#             borderwidth=2,
#             font=dict(size=12,
#                         family=default_font,
#                         color='slategrey'),
#             # valign='top'
#             # itemsizing='constant'
#     ),
    
# )

#     return figure