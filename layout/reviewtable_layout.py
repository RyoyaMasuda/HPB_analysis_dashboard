import time
import math
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

default_font='Comic Sans Ms'

df = pd.read_csv('./data_for_revise/tmp_merge_df.csv', low_memory=False)

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
                    id='table_dropdown1',
                    options=[
                        {'label':x, 'value':x} for x in df['県'].unique()
                    ],
                    value='広島',
                    style={'width':'300px', 'margin-bottom':'1px', 'fontSize':15},
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
                    id='table_dropdown2',
                    # options = callbackで返ってくる。
                    style={'width':'300px', 'margin-bottom':'1px', 'fontSize':15},
                    clearable=True,
                    value='八丁堀・幟町・胡町',
                    className='text-dark',
                ),
                html.P(
                    children='Select a salon',
                    style={'margin': '10px',
                        #    'width':'130px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='table_dropdown3',
                    # options = callbackで返ってくる。
                    value='ATENA　AVEDA　広島三越店 【アテナアヴェダ】',
                    style={'width':'300px', 'margin-bottom':'1px', 'fontSize':12},
                    clearable=True,
                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                    optionHeight=55,
                    className='text-dark'
                ),
                html.P(
                    children='Select gender',
                    style={'margin': '10px',
                        #    'width':'130px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Checklist(
                    id='table_checklist1',
                    # options = callbackで返ってくる。
                    value=['女性', '未設定', '男性'],
                    inline=True,
                    inputStyle={'margin':'8px'}
                ),
                dbc.Button(
                    id='table_button',
                    children='Apply',
                    color='info',
                    n_clicks=0,
                    style={'margin':'20px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
                html.Hr(),
                html.Br(),
            ],
        ),
        dbc.Row(
            html.P(
                children='Select the review criteria to display.',
                style={'margin':'10px', 'fontSize':16},
            ),
            className='bg-secondary'
        ),
        dbc.Row(
            [   
                html.P(
                    children='Select a review item',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='review_item_dropdown',
                    options=[
                        {'label':'総合', 'value':'総合'},
                        {'label':'雰囲気', 'value':'雰囲気'},
                        {'label':'接客サービス', 'value':'接客サービス'},
                        {'label':'技術・仕上がり', 'value':'技術・仕上がり'},
                        {'label':'メニュー・料金', 'value':'メニュー・料金'},
                    ],
                    value='総合',
                    style={'width':'300px',
                           'margin-bottom':'1px',
                           'fontSize':15},
                    clearable=False,
                    className='text-dark',
                ),
                html.P(
                    children='Select a review point and range',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id='review_points',
                                value='5',
                                style={'width':'135px',
                                    'margin':'1px',
                                    'fontSize':15},
                                clearable=False,
                                className='text-dark',
                            ),
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='review_point_range',
                                options=[
                                    {'label':'のみ', 'value':'only'},
                                    {'label':'以上', 'value':'more_than'},
                                    {'label':'以下', 'value':'less_than'},
                                ],
                                value='only',
                                style={'width':'135px',
                                    # 'margin':'1px',
                                    'fontSize':15},
                                clearable=False,
                                className='text-dark',
                            ),
                        )
                    ]
                ),
                dbc.Button(
                    id='review_point_button',
                    children='Update the Table',
                    color='info',
                    n_clicks=0,
                    style={'margin':'20px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
                html.Hr(),
                html.Br(),
            ]
        ),
        dbc.Row(
            html.P(
                children='Download Review Table',
                style={'margin':'10px', 'fontSize':20,
                    #    'textAlign':'center'
                       },
            ),
            className='bg-secondary'
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Button(
                            id='button_csv',
                            children='Download csv',
                            color='info',
                            n_clicks=0,
                            style={'margin-top':'20px',
                                   'margin-left':'20px',
                                   'margin-right':'20px',
                                   },
                            className='d-grid gap-2 col-6 mx-auto',
                            ),
                        dcc.Download(id='download-dataframe-csv'),
                    ]
                ),
                html.Div(
                    [
                        html.Hr(),
                        # html.Br(),
                        html.Div(
                            id='salon_url',
                        )
                    ]
                )    
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
                                            id='total-ratio',
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
                                            id='atmosphere-ratio',
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
                                            id='service-ratio',
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
                                            id='skill-ratio',
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
                # 1行5列
                dbc.Col(  
                    [   
                        dcc.Loading(id="loading_1-4",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='menu_and_price-ratio',
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
            ],
            className='bg-primary',
            style={'height':'30vh'}
        ),
        dbc.Row(
            [   
                dcc.Loading(id="loading_2-1",
                            children=[
                                    html.Div(
                                        children=[
                                            html.P(
                                                children='Review Point and Contents',
                                                style={'textAlign':'center',
                                                       'padding-top':'20px',
                                                       'color':'grey',
                                                       'fontSize':25,
                                                       'font-family':default_font
                                                       }    
                                            ),
                                            html.Div(
                                                id='review_table',
                                                # children = dash_table(hogehoge) コールバックで返ってくる
                                                style={'padding':'20px',
                                                       'color':'grey',
                                                       'backgroundColor':'lightcyan'}
                                                ),
                                            
                                            ],
                                        style={'backgroundColor':'lightcyan',
                                               'height':'720px'}
                                    ),
                            ],
                            style={"margin": "10%",
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
            ],
            style={'height':'70vh', 
                   'padding':'6px'},
            className='bg-info'
        ),
    ]
)

reviewtable_layout = [
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
    Output('table_dropdown2', 'options'),
    Input('table_dropdown1', 'value')
)
def update_area(value):
    return [{'label': x2,'value': x2} for x2 in df[df['県'] == value]['エリア'].unique()]

@callback(
    Output('table_dropdown3', 'options'),
    Input('table_dropdown2', 'value')
)
def update_salon(value):
    return [{'label': x3,'value': x3} for x3 in df[df['エリア'] == value]['サロン名'].unique()]

# 県を削除したときにサロン名も消える処理
@callback(
    Output('table_dropdown3', 'value'),
    Input('table_dropdown1', 'value'),
    prevent_initial_call=True
)
def update_area(value):
    if value is None:
        return ''

@callback(
    Output('table_checklist1', 'options'),
    Input('table_dropdown3', 'value'),
    Input('table_dropdown2', 'value'),
    #
)
def update_gender(dropdown3_value, dropdown2_value):
    
    _df = df.copy()
    _df = df[df['エリア'] == dropdown2_value]
    
    if dropdown3_value is None:
        dropdown3_value = _df['サロン名'].unique()
    else:
        dropdown3_value = [dropdown3_value]
    
    _df = _df[_df['サロン名'].isin(dropdown3_value)]
    
    return [{'label': x3,'value': x3} for x3 in _df['性別'].unique()]

# 評価点を選択するためのコールバック
@callback(
    Output('review_points', 'options'),
    Input('table_dropdown1', 'value'),
    Input('table_dropdown2', 'value'),
    Input('table_dropdown3', 'value'),
    Input('table_checklist1', 'value'),
    Input('review_item_dropdown', 'value'),
)
def narrow_review_points(table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value, review_item_dropdown_value):
    
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    return [{'label':point, 'value':point} for point in sorted(_df[review_item_dropdown_value].unique())]

# サイドバーのサロンインフォメーション
@callback(
    Output('salon_url', 'children'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def salon_url(n_clicks, table_dropdown1_value, table_dropdown2_value, tabledropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県']==table_dropdown1_value]
    _df = _df[_df['エリア']==table_dropdown2_value]
    _df = _df[_df['サロン名']==tabledropdown3_value]
    
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    link = _df['URL'].unique()[0]
    
    children = [

                html.P(children='Link to Hot Pepper Beauty :',
                        style={
                            # 'margin':'10px',
                               'fontSize':18,
                               'text-decoration':'underline'},
                        className='font-weight-bold'
                    ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                html.A(children='HPBのページへ飛ぶ',
                                        href=link,
                                        target='_blank',
                                        style={'text-decoration':'underline',
                                               'fontSize':16
                                                # 'margin-top':'15px'
                                        },
                                    ),
                                ]
                            ),
                        width={"size": 6, "offset": 3},
                    ),
                    style={'margin-top':'15px'}
                ),
            ]
    
    return children

# 1行1列
@callback(
    Output('total-ratio', 'figure'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df.loc[_df['総合'] <= 3, '総合']='3以下'
    _df['総合'] = _df['総合'].astype(str)
    _df = pd.DataFrame(_df['総合'].value_counts()).reset_index()
    _df = _df.rename(columns={'index':'点数', '総合':'客数(口コミ数)'})
    figure = px.pie(
        data_frame=_df,
        names='点数',
        values='客数(口コミ数)',
        color='点数',
        title=f'Total Review Points Ratio',
        height=290,
        width=335,
        color_discrete_map={'5':'#fccde5','4':'#ffffb3','3以下':'#80b1d3'},
        category_orders={'点数':['5','4','3以下']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='点数',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行2列
@callback(
    Output('atmosphere-ratio', 'figure'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def general_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df.loc[_df['雰囲気'] <= 3, '雰囲気']='3以下'
    _df['雰囲気'] = _df['雰囲気'].astype(str)
    _df = pd.DataFrame(_df['雰囲気'].value_counts()).reset_index()
    _df = _df.rename(columns={'index':'点数', '雰囲気':'客数(口コミ数)'})
    figure = px.pie(
        data_frame=_df,
        names='点数',
        values='客数(口コミ数)',
        color='点数',
        title=f'General Score Ratio',
        height=290,
        width=335,
        color_discrete_map={'5':'#fccde5','4':'#ffffb3','3以下':'#80b1d3'},
        category_orders={'点数':['5','4','3以下']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='点数',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行3列
@callback(
    Output('service-ratio', 'figure'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def Hospitality_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df.loc[_df['接客サービス'] <= 3, '接客サービス']='3以下'
    _df['接客サービス'] = _df['接客サービス'].astype(str)
    _df = pd.DataFrame(_df['接客サービス'].value_counts()).reset_index()
    _df = _df.rename(columns={'index':'点数', '接客サービス':'客数(口コミ数)'})
    figure = px.pie(
        data_frame=_df,
        names='点数',
        values='客数(口コミ数)',
        color='点数',
        title=f'Hospitality Review Score Ratio',
        height=290,
        width=335,
        color_discrete_map={'5':'#fccde5','4':'#ffffb3','3以下':'#80b1d3'},
        category_orders={'点数':['5','4','3以下']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='点数',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行4列
@callback(
    Output('skill-ratio', 'figure'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df.loc[_df['技術・仕上がり'] <= 3, '技術・仕上がり']='3以下'
    _df['技術・仕上がり'] = _df['技術・仕上がり'].astype(str)
    _df = pd.DataFrame(_df['技術・仕上がり'].value_counts()).reset_index()
    _df = _df.rename(columns={'index':'点数', '技術・仕上がり':'客数(口コミ数)'})
    figure = px.pie(
        data_frame=_df,
        names='点数',
        values='客数(口コミ数)',
        color='点数',
        title=f'Hairdresser Skills & Quality Ratio',
        height=290,
        width=335,
        color_discrete_map={'5':'#fccde5','4':'#ffffb3','3以下':'#80b1d3'},
        category_orders={'点数':['5','4','3以下']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='点数',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行5列
@callback(
    Output('menu_and_price-ratio', 'figure'),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')]
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df.loc[_df['メニュー・料金'] <= 3, 'メニュー・料金']='3以下'
    _df['メニュー・料金'] = _df['メニュー・料金'].astype(str)
    _df = pd.DataFrame(_df['メニュー・料金'].value_counts()).reset_index()
    _df = _df.rename(columns={'index':'点数', 'メニュー・料金':'客数(口コミ数)'})
    figure = px.pie(
        data_frame=_df,
        names='点数',
        values='客数(口コミ数)',
        color='点数',
        title=f'Menu & Price Score Ratio',
        height=290,
        width=335,
        color_discrete_map={'5':'#fccde5','4':'#ffffb3','3以下':'#80b1d3'},
        category_orders={'点数':['5','4','3以下']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='点数',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 2行1列
@callback(
    Output('review_table', 'children', allow_duplicate=True),
    Input('table_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value')],
    prevent_initial_call='initial_duplicate'
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    _df = _df[['サロン名', '名前', '投稿日時', '総合', '雰囲気', '接客サービス', '技術・仕上がり', 'メニュー・料金', '選択されたクーポン', 'メニューの種類', '口コミ本文']]
    columns=[{'name': 'サロン名', 'id': 'サロン名'},
             {'name': '名前', 'id': '名前'},
             {'name': '投稿日時', 'id': '投稿日時'},
             {'name': '総合', 'id': '総合'},
             {'name': '雰囲気', 'id': '雰囲気'},
             {'name': '接客サービス', 'id': '接客サービス'},
             {'name': '技術・仕上がり', 'id': '技術・仕上がり'},
             {'name': 'メニュー・料金', 'id': 'メニュー・料金'},
             {'name': '選択されたクーポン', 'id': '選択されたクーポン'},
             {'name': 'メニューの種類', 'id': 'メニューの種類'},
             {'name': '口コミ本文', 'id': '口コミ本文'},
             ]
    children = dash_table.DataTable(_df.to_dict('records'),
                                    columns=columns,
                                    style_cell={'color':'grey',
                                                # 'height':'300px',
                                                'textAlign':'left',
                                                },
                                    style_table={
                                        # 'height':'700px',
                                                #  'overflowY':'scroll',
                                                #  'overflowX':'scroll',
                                                 },
                                    fixed_rows={'headers':True},
                                    # fixed_columns={'headers':True},
                                    style_header={
                                        'backgroundColor': '#fee391',
                                                  'fontWeight': 'bold',
                                                  },
                                    style_data={
                                        'backgroundColor': '#ffffe5',
                                                'whiteSpace':'normal',
                                                'minWidth':'120px',
                                                'maxWidth':'500px'},
                                    # export_format='csv'
                                    # 縦スクロール時にヘッダーを固定

                                    )
    
    return children
    
    

 
                    # id='review_item_dropdown',
                    #             id='review_points',
                    #             id='review_point_range',    
    
# 2行1列 更新する
@callback(
    Output('review_table', 'children', allow_duplicate=True),
    Input('review_point_button', 'n_clicks'),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value'),
    State('review_item_dropdown', 'value'), # 総合とか雰囲気とか
    State('review_points', 'value'), # 54321
    State('review_point_range', 'value'), # 以上、以下、のみ
    ],
    prevent_initial_call='initial_duplicate'
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value, 
                       review_item_dropdown_value, review_points_value, review_point_range_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    if review_point_range_value == 'only':
        _df = _df[_df[review_item_dropdown_value] == review_points_value]
    elif review_point_range_value == 'more_than':
        _df = _df[_df[review_item_dropdown_value] >= review_points_value]
    elif review_point_range_value == 'less_than':
        _df = _df[_df[review_item_dropdown_value] <= review_points_value]
    
    _df = _df[['サロン名', '名前', '投稿日時', '総合', '雰囲気', '接客サービス', '技術・仕上がり', 'メニュー・料金', '選択されたクーポン', 'メニューの種類', '口コミ本文']]
    columns=[{'name': 'サロン名', 'id': 'サロン名'},
             {'name': '名前', 'id': '名前'},
             {'name': '投稿日時', 'id': '投稿日時'},
             {'name': '総合', 'id': '総合'},
             {'name': '雰囲気', 'id': '雰囲気'},
             {'name': '接客サービス', 'id': '接客サービス'},
             {'name': '技術・仕上がり', 'id': '技術・仕上がり'},
             {'name': 'メニュー・料金', 'id': 'メニュー・料金'},
             {'name': '選択されたクーポン', 'id': '選択されたクーポン'},
             {'name': 'メニューの種類', 'id': 'メニューの種類'},
             {'name': '口コミ本文', 'id': '口コミ本文'},
             ]
    children = dash_table.DataTable(_df.to_dict('records'),
                                    columns=columns,
                                    style_cell={
                                        'color':'grey',
                                                # 'height':'300px',
                                                'textAlign':'left',
                                                # 'backgroundColor': '#fee391'
                                                },
                                    style_table={
                                        # 'height':'700px',
                                                #  'overflowY':'scroll',
                                                #  'overflowX':'scroll',
                                                 },
                                    fixed_rows={'headers':True},
                                    # fixed_columns={'headers':True},
                                    style_header={
                                        'backgroundColor': '#fee391',
                                                  'fontWeight': 'bold',
                                                  },
                                    style_data={
                                        'backgroundColor': '#ffffe5',
                                                'whiteSpace':'normal',
                                                'minWidth':'120px',
                                                'maxWidth':'500px'},
                                    # export_format='csv'
                                    # 縦スクロール時にヘッダーを固定

                                    )
    
    return children

# 2行1列のデータフレームをダウンロードする。
@callback(
    Output("download-dataframe-csv", "data"),
    Input("button_csv", "n_clicks"),
    [State('table_dropdown1', 'value'),
    State('table_dropdown2', 'value'),
    State('table_dropdown3', 'value'),
    State('table_checklist1', 'value'),
    State('review_item_dropdown', 'value'), # 総合とか雰囲気とか
    State('review_points', 'value'), # 54321
    State('review_point_range', 'value'), # 以上、以下、のみ
    ],
    # prevent_initial_call='initial_duplicate',
    prevent_initial_call=True,
)
def total_ratio_figure(n_clicks, table_dropdown1_value, table_dropdown2_value, table_dropdown3_value, table_checklist1_value, 
                       review_item_dropdown_value, review_points_value, review_point_range_value):
    _df = df.copy()
    _df = _df[_df['県'] == table_dropdown1_value]
    _df = _df[_df['エリア'] == table_dropdown2_value]
    _df = _df[_df['サロン名'] == table_dropdown3_value]
    _df = _df[_df['性別'].isin(table_checklist1_value)]
    
    if review_point_range_value == 'only':
        _df = _df[_df[review_item_dropdown_value] == review_points_value]
    elif review_point_range_value == 'more_than':
        _df = _df[_df[review_item_dropdown_value] >= review_points_value]
    elif review_point_range_value == 'less_than':
        _df = _df[_df[review_item_dropdown_value] <= review_points_value]
    
    _df = _df[['サロン名', '名前', '投稿日時', '総合', '雰囲気', '接客サービス', '技術・仕上がり', 'メニュー・料金', '選択されたクーポン', 'メニューの種類', '口コミ本文']]
    
    range={'only':'のみ', 'more_than':'以上', 'less_than':'以下'}
    
    return dcc.send_data_frame(_df.to_csv, f"{table_dropdown3_value}_評価{review_points_value}点{range[review_point_range_value]}の口コミ.csv")
# @callback(
#     ,
#     Input("button_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")

# 'download-dataframe-csv'