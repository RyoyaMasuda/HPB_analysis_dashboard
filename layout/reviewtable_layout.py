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
                    id='button',
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
                html.P(
                    children='Select a review point',
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
                                id='the_brand',
                                options=[
                                    {'label':'Illumina(WELLA)', 'value':'イルミナメニュー化の有無'},
                                    {'label':'Addicthy(MILBON)', 'value':'addicthyメニュー化の有無'},
                                    {'label':'Inoa(LOREAL)', 'value':'inoaメニュー化の有無'},
                                    {'label':'Aujua(MILBON)', 'value':'Aujuaメニュー化の有無'},
                                ],
                                value='イルミナメニュー化の有無',
                                style={'width':'130px',
                                    'margin':'1px',
                                    'fontSize':15},
                                clearable=False,
                                className='text-dark',
                            ),
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='th_brand',
                                options=[
                                    {'label':'Illumina(WELLA)', 'value':'イルミナメニュー化の有無'},
                                    {'label':'Addicthy(MILBON)', 'value':'addicthyメニュー化の有無'},
                                    {'label':'Inoa(LOREAL)', 'value':'inoaメニュー化の有無'},
                                    {'label':'Aujua(MILBON)', 'value':'Aujuaメニュー化の有無'},
                                ],
                                value='イルミナメニュー化の有無',
                                style={'width':'130px',
                                    'margin':'1px',
                                    'fontSize':15},
                                clearable=False,
                                className='text-dark',
                            ),
                        )
                    ]
                ),
                dbc.Button(
                    id='brand_button',
                    children='Update the Table',
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

content=html.Div(
    []
)

# content = html.Div(
#     [
#         dbc.Row(
#             [   # 1行1列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_1-1",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='gender-ratio',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                 ],
#                 className='bg-info',
#                 style={'padding':'8px'}
#                 ),
#                 # 1行2列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_1-2",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='age-ratio',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],
#                     # 画面のワイドの設定はcol-**で設定した方がいい。横が12だからcol−６で半分
#                     className='bg-info',
#                     style={'padding':'8px'}
#                 ),
#                 # 1行3列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_1-3",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='hair-color-ratio',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],
#                     className='bg-info',
#                     style={'padding':'8px'}
#                 ),
#                 # 1行4列
#                 dbc.Col(  
#                     [   
#                         dcc.Loading(id="loading_1-4",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='treatment-ratio',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],                                          
#                     className='bg-info',
#                     style={'padding':'8px'}
#                 )
#             ],
#             className='bg-primary',
#             style={'height':'30vh'}
#         ),
#         dbc.Row(
#             [   # 2行1列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_2-1",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='cut-only-comparison',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],                    
#                     # className='bg-info',
#                     style={'padding':'8px'},
#                     className='bg-info'
#                 ),
#                 # 2行2列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_2-2",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='cut-and-colr-comparison',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],
#                     style={'padding':'8px'},
#                     className='bg-info'
#                     ),
#                 # 2行3列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_2-3",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='cut-and-colr-and-treatment-comparison',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],                    
#                     style={'padding':'8px'},
#                     className='bg-info'
#                 ),
#                 # 2行4列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_2-4",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='all-menu-comparison',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",},
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],                       
#                     style={'padding':'8px'},
#                     className='bg-info'
#                 )
#             ],
#             # className='bg-secondary',
#             style={'height':'30vh'}
#         ),
#         dbc.Row(
#             [   #3行1列
#                 dbc.Col(
#                     [   
#                         dcc.Loading(id="loading_3-1",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='total_bill_boxplot',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],                    
#                     style={'padding':'8px'},
#                     className='bg-info'
#                     ),
#                 dbc.Col(
# [   
#                         dcc.Loading(id="loading_3-1",
#                             children=[
#                                     html.Div(
#                                         [
#                                             dcc.Graph(
#                                             id='coupon-ranking',
#                                             ), 
#                                         ]
#                                     )
#                             ],
#                             style={"margin": "10%",
#                                     },
#                             type='dot',
#                             color='#ffffb3',
#                             className='bg-info'),
#                     ],
#                     style={'padding':'8px'},
#                     className='light'
#                     ),
#             ],
#             className='bg-info',
#             style={'height':'40vh'}
#         )   
#     ]
# )

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
