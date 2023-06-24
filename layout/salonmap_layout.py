import time
import math
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

# px.set_mapbox_access_token(open(".mapbox_token").read())

default_font='Comic Sans Ms'

df = pd.read_csv('./data_for_revise/map/dataframe_for_map.csv', low_memory=False)


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
                           'height': '150px',
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
                           'height': '300px',
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
        ),
        dbc.Row(
            html.P(
                children='Change the brand displayed on the map.',
                style={'margin':'10px', 'fontSize':16},
            ),
            className='bg-secondary'
        ),
        dbc.Row(
            [   
                html.P(
                    children='Select a brand',
                    style={'margin': '10px',
                        #    'width':'140px',
                           'text-decoration':'underline',
                           'fontSize':18},
                    className='font-weight-bold'
                ),
                dcc.Dropdown(
                    id='change_the_brand',
                    options=[
                        {'label':'Illumina(WELLA)', 'value':'イルミナメニュー化の有無'},
                        {'label':'Addicthy(MILBON)', 'value':'addicthyメニュー化の有無'},
                        {'label':'Inoa(LOREAL)', 'value':'inoaメニュー化の有無'},
                        {'label':'Aujua(MILBON)', 'value':'Aujuaメニュー化の有無'},
                    ],
                    value='イルミナメニュー化の有無',
                    style={'width':'300px',
                           'margin-bottom':'1px',
                           'fontSize':15},
                    clearable=False,
                    className='text-dark',
                ),
                dbc.Button(
                    id='change_brand_button',
                    children='Change The Brand',
                    color='info',
                    n_clicks=0,
                    style={'margin':'30px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
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
                                            id='illumina-ratio',
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
                                            id='addicthy-ratio',
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
                                            id='inoa-ratio',
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
                                            id='aujua-ratio',
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
                dcc.Loading(id="loading_2-1",
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='brand_activate_map',
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
            style={'height':'70vh', 
                   'padding':'4px'},
            className='bg-info'
        ),
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
        value = [value]
    return [{'label': x2,'value': x2} for x2 in df[df['県'].isin(value)]['エリア'].unique()]
    
# 1行1列
@callback(
    Output('illumina-ratio', 'figure'),
    Input('salonmap_button', 'n_clicks'),
    [State('multi_dropdown1', 'value'),
     State('multi_dropdown2', 'value'),])
def gender_ratio_figure(n_clicks, multi_dropdown1_value, multi_dropdown2_value):
    
    _df = df.copy()
    
    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]

    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
    elif multi_dropdown2_value == []:
        pass
    else:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    
    _df = _df.groupby('イルミナメニュー化の有無').count().iloc[:,0:1].reset_index()
    _df.loc[_df['イルミナメニュー化の有無']==0, 'イルミナメニュー化の有無'] = '不活性or未導入'
    _df.loc[_df['イルミナメニュー化の有無']==1, 'イルミナメニュー化の有無'] = 'メニュー化'
    _df.rename(columns={'県':'サロン数'}, inplace=True)
    
    figure = px.pie(
        data_frame=_df,
        names='イルミナメニュー化の有無',
        values='サロン数',
        color='イルミナメニュー化の有無',
        title=f'Illumina Color Activated Salon Ratio',
        height=290,
        # width=418,
        color_discrete_map={'メニュー化':'fuchsia','不活性or未導入':'aqua'},
        category_orders={'イルミナメニュー化の有無':['メニュー化', '不活性or未導入']}
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
        # margin={'l':30, 'r':30, 't':50, 'b':10},
        margin={'l':10, 'r':50, 't':40, 'b':20},
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
            title=dict(text='対象ブランド',
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
    Output('addicthy-ratio', 'figure'),
    Input('salonmap_button', 'n_clicks'),
    [State('multi_dropdown1', 'value'),
     State('multi_dropdown2', 'value'),])
def addicthy_ratio_figure(n_clicks, multi_dropdown1_value, multi_dropdown2_value):
    
    _df = df.copy()
    
    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]
    
    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
    elif multi_dropdown2_value == []:
        pass
    else:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    
    _df = _df.groupby('addicthyメニュー化の有無').count().iloc[:,0:1].reset_index()
    _df.loc[_df['addicthyメニュー化の有無']==0, 'addicthyメニュー化の有無'] = '不活性or未導入'
    _df.loc[_df['addicthyメニュー化の有無']==1, 'addicthyメニュー化の有無'] = 'メニュー化'
    _df.rename(columns={'県':'サロン数'}, inplace=True)
    
    figure = px.pie(
        data_frame=_df,
        names='addicthyメニュー化の有無',
        values='サロン数',
        color='addicthyメニュー化の有無',
        title=f'Addicthy Color Activated Salon Ratio',
        height=290,
        # width=418,
        color_discrete_map={'メニュー化':'fuchsia','不活性or未導入':'aqua'},
        category_orders={'addicthyメニュー化の有無':['メニュー化', '不活性or未導入']}
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
        # margin={'l':30, 'r':30, 't':50, 'b':10},
        margin={'l':10, 'r':50, 't':40, 'b':20},
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
            title=dict(text='対象ブランド',
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
    Output('inoa-ratio', 'figure'),
    Input('salonmap_button', 'n_clicks'),
    [State('multi_dropdown1', 'value'),
     State('multi_dropdown2', 'value'),])
def inoa_ratio_figure(n_clicks, multi_dropdown1_value, multi_dropdown2_value):
    
    _df = df.copy()
    
    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]

    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
    elif multi_dropdown2_value == []:
        pass
    else:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    
    _df = _df.groupby('inoaメニュー化の有無').count().iloc[:,0:1].reset_index()
    _df.loc[_df['inoaメニュー化の有無']==0, 'inoaメニュー化の有無'] = '不活性or未導入'
    _df.loc[_df['inoaメニュー化の有無']==1, 'inoaメニュー化の有無'] = 'メニュー化'
    _df.rename(columns={'県':'サロン数'}, inplace=True)
    
    figure = px.pie(
        data_frame=_df,
        names='inoaメニュー化の有無',
        values='サロン数',
        color='inoaメニュー化の有無',
        title=f'inoa Color Activated Salon Ratio',
        height=290,
        # width=418,
        color_discrete_map={'メニュー化':'fuchsia','不活性or未導入':'aqua'},
        category_orders={'inoaメニュー化の有無':['メニュー化', '不活性or未導入']}
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
        # margin={'l':30, 'r':30, 't':50, 'b':10},
        margin={'l':10, 'r':50, 't':40, 'b':20},
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
            title=dict(text='対象ブランド',
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
    Output('aujua-ratio', 'figure'),
    Input('salonmap_button', 'n_clicks'),
        [
            State('multi_dropdown1', 'value'),
            State('multi_dropdown2', 'value'),
    ]
)
def aujua_ratio_figure(n_clicks, multi_dropdown1_value, multi_dropdown2_value):
    
    _df = df.copy()
    
    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]

    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
    elif multi_dropdown2_value == []:
        pass
    else:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    
    _df = _df.groupby('Aujuaメニュー化の有無').count().iloc[:,0:1].reset_index()
    _df.loc[_df['Aujuaメニュー化の有無']==0, 'Aujuaメニュー化の有無'] = '不活性or未導入'
    _df.loc[_df['Aujuaメニュー化の有無']==1, 'Aujuaメニュー化の有無'] = 'メニュー化'
    _df.rename(columns={'県':'サロン数'}, inplace=True)
    
    figure = px.pie(
        data_frame=_df,
        names='Aujuaメニュー化の有無',
        values='サロン数',
        color='Aujuaメニュー化の有無',
        title=f'Aujua Activated Salon Ratio',
        height=290,
        # width=418,
        color_discrete_map={'メニュー化':'fuchsia','不活性or未導入':'aqua'},
        category_orders={'Aujuaメニュー化の有無':['メニュー化', '不活性or未導入']}
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
        # margin={'l':30, 'r':30, 't':50, 'b':10},
        margin={'l':10, 'r':50, 't':40, 'b':20},
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
            title=dict(text='対象ブランド',
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

# 2行1列 最初はイルミナ
@callback(
    Output('brand_activate_map', 'figure', allow_duplicate=True),
    Input('salonmap_button', 'n_clicks'),
    [State('multi_dropdown1', 'value'),
     State('multi_dropdown2', 'value'),
     ],
    prevent_initial_call='initial_duplicate')
def brand_activate_map(n_clicks, multi_dropdown1_value, multi_dropdown2_value):

    brand_name = 'イルミナ'
    _df = df.copy()

    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]

    time.sleep(1)
    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    elif type(multi_dropdown2_value) == list and len(multi_dropdown2_value) > 0:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    elif multi_dropdown2_value == []:
        pass
    

    
    _df.loc[_df['イルミナメニュー化の有無']==0, 'イルミナメニュー化の有無'] = '不活性or未導入'
    _df.loc[_df['イルミナメニュー化の有無']==1, 'イルミナメニュー化の有無'] = 'メニュー化'

    figure = px.scatter_mapbox(_df,
                               title='Map of Salons (Selected brands are being activated.)',
                                lat="緯度",
                                lon="経度",
                                color='イルミナメニュー化の有無',
                                size_max=15,
                                zoom=12,
                                color_discrete_map={'メニュー化':'fuchsia', '不活性or未導入':'aqua'},
                                hover_name='サロン名',
                                hover_data={'緯度':False,
                                            '経度':False,
                                            'イルミナメニュー化の有無':False,
                                            'スタッフ数':True,
                                            'クーポン数':True,
                                            'メニュー数':True, 
                                            'スタイル数':True,
                                            'カット料金':True,
                                            'セット面の数':True,
                                            'ブログ投稿数':True,
                                            '口コミ数':True,
                                },
                                height=710

    )
    figure.update_traces(
        marker=dict(size=16)
    )
    
    figure.update_layout(
        mapbox_style="open-street-map",
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        # margin={'l':30, 'r':30, 't':80, 'b':10},
        margin={'l':10, 'r':50, 't':80, 'b':20},
        title={'font':{'size':26,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=14,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=16,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text=f'対象ブランド: {brand_name}',
                       font=dict(family=default_font,
                                 size=16),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=16,
                      family=default_font,
                      color='slategrey'),
        ),
    )
    
    return figure

# 2行1列
@callback(
    Output('brand_activate_map', 'figure', allow_duplicate=True),
    Input('change_brand_button', 'n_clicks'),
    [State('multi_dropdown1', 'value'),
     State('multi_dropdown2', 'value'),
     State('change_the_brand', 'value')],
    prevent_initial_call='initial_duplicate')
def brand_activate_map(n_clicks, multi_dropdown1_value, multi_dropdown2_value, selected_brand):
    brand_name = selected_brand.split('メニュー')[0]
    
    _df = df.copy()
    
    if type(multi_dropdown1_value) == str:
        multi_dropdown1_value = [multi_dropdown1_value]
    _df = _df[_df['県'].isin(multi_dropdown1_value)]

    if type(multi_dropdown2_value) == str:
        multi_dropdown2_value = [multi_dropdown2_value]
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    elif type(multi_dropdown2_value) == list and len(multi_dropdown2_value) > 0:
        _df = _df[_df['エリア'].isin(multi_dropdown2_value)]
    elif multi_dropdown2_value == []:
        pass
    
    _df.loc[_df[selected_brand]==0, selected_brand] = '不活性or未導入'
    _df.loc[_df[selected_brand]==1, selected_brand] = 'メニュー化'

    figure = px.scatter_mapbox(_df,
                               title='Map of Salons (Selected brands are being activated.)',
                                lat="緯度",
                                lon="経度",
                                color=selected_brand,
                                size_max=15,
                                zoom=12,
                                color_discrete_map={'メニュー化':'fuchsia', '不活性or未導入':'aqua'},
                                hover_name='サロン名',
                                hover_data={'緯度':False,
                                            '経度':False,
                                            selected_brand:False,
                                            'スタッフ数':True,
                                            'クーポン数':True,
                                            'メニュー数':True, 
                                            'スタイル数':True,
                                            'カット料金':True,
                                            'セット面の数':True,
                                            'ブログ投稿数':True,
                                            '口コミ数':True,
                                },
                                height=710

    )
    figure.update_traces(
        marker=dict(size=16,)
    )
    figure.update_layout(
        mapbox_style="open-street-map",
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        # margin={'l':10, 'r':50, 't':40, 'b':20},
        margin={'l':10, 'r':50, 't':80, 'b':20},
        title={'font':{'size':26,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=14,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=16,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text=f'対象ブランド: {brand_name}',
                       font=dict(family=default_font,
                                 size=16),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=16,
                      family=default_font,
                      color='slategrey'),
        ),
    )
    
    return figure