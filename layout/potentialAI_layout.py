import time
import pickle
import math
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px

default_font='Comic Sans Ms'

df = pd.read_csv('./data/prediction/payments/dataset_for_payments.csv', low_memory=False)

# 各モデルを全て読み込んでおく。
# カラー比率
with open('./model/menu_ratio_and_review_points/color_ratio_models.pkl', 'rb') as p:
    color_ratio_models = pickle.load(p)
# トリートメント比率
with open('./model/menu_ratio_and_review_points/treatment_ratio_models.pkl', 'rb') as p:
    treatment_ratio_models = pickle.load(p)
# トリートメント比率
with open('./model/menu_ratio_and_review_points/pama_ratio_models.pkl', 'rb') as p:
    pama_ratio_models = pickle.load(p)
# イルミナ
with open('./model/brand_classification/illumina_classification_models.pkl', 'rb') as p:
    illumina_classification_models = pickle.load(p)    
# アディクシー
with open('./model/brand_classification/addicthy_classification_models.pkl', 'rb') as p:
    addicthy_classification_models = pickle.load(p)
# Aujua
with open('./model/brand_classification/inoa_classification_models.pkl', 'rb') as p:
    inoa_classification_models = pickle.load(p)
# inoa
with open('./model/brand_classification/Aujua_classification_models.pkl', 'rb') as p:
    aujua_classification_models = pickle.load(p)

# 総合
with open('./model/menu_ratio_and_review_points/general_review_models.pkl', 'rb') as p:
    general_review_models = pickle.load(p)
# 雰囲気
with open('./model/menu_ratio_and_review_points/atmosphere_models.pkl', 'rb') as p:
    atmosphere_models = pickle.load(p)
# 接客サービス
with open('./model/menu_ratio_and_review_points/hospitality_models.pkl', 'rb') as p:
    hospitality_models = pickle.load(p)
# 技術・仕上がり
with open('./model/menu_ratio_and_review_points/skills_and_completion_models.pkl', 'rb') as p:
    skills_and_completion_models = pickle.load(p)
# メニュー・料金
with open('./model/menu_ratio_and_review_points/menu_and_price_models.pkl', 'rb') as p:
    menu_and_price_models = pickle.load(p)

# 支出金額
with open('./model/payments/payments_models.pkl', 'rb') as p:
    payments_models = pickle.load(p)

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
                    style={'width':'15vw',
                        #    'height':'20px',
                           'margin-bottom':'1px', 'fontSize':15},
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
                    
                    style={'width':'15vw',
                        #    'height':'5px',
                           'margin-bottom':'1px', 'fontSize':15},
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
                                    id='AI_input1',
                                    placeholder='Select...',
                                    
                                    value=3,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=1,
                                    max=30,
                                    step=1,
                                    type='number'
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
                                    
                                    value=100,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    type='text', inputmode='numeric', pattern='[0-9]{1,4}',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
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
                                    
                                    value=150,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                        'margin-bottom':'1px',
                                        #    'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    type='text', inputmode='numeric', pattern='[0-9]{1,4}',
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
                                    
                                    value=4,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                        'margin-bottom':'1px',
                                        #    'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=1,
                                    max=50,
                                    step=1,
                                    type='number',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
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
                                    
                                    value=20,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                            'margin-bottom':'1px',
                                            # 'margin-left':'12px',
                                            'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=1,
                                    max=150,
                                    step=1,
                                    type='number',
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
                                    
                                    value=15,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=1,
                                    max=150,
                                    step=1,
                                    type='number',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
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
                                    
                                    value=100,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                            'margin-bottom':'1px',
                                            # 'margin-left':'12px',
                                            'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    type='text', inputmode='numeric', pattern='[0-9]{1,4}',
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
                                    
                                    value=9,
                                    style={'width':'6vw',
                                        #  'height':'30px',
                                        'margin-bottom':'1px',
                                        # 'margin-left':'12px',
                                        'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=1,
                                    max=40,
                                    step=1,
                                    type='number',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    children='Replay Rate',
                                    style={
                                        'margin-left': '10px',
                                        #    'width':'130px',
                                        'text-decoration':'underline',
                                        'fontSize':16},
                                    className='font-weight-bold'
                                ),
                                dbc.Input(
                                    id='AI_input9',
                                    placeholder='Select...',
                                    
                                    value=70,
                                    style={'width':'6vw',
                                        #    'height':'30px',
                                            'margin-bottom':'1px',
                                            # 'margin-left':'12px',
                                            'fontSize':16},
                                    
                                    className='text-dark',
                                    size='sm',
                                    min=0,
                                    max=100,
                                    step=1,
                                    type='number',
                                ),
                            ]
                        ),
                    ],
                    style={'margin-bottom': '10px'}
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
                                        {'label':'メニュー化', 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'6vw',
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
                                        {'label':'メニュー化', 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'6vw',
                                        'margin-bottom':'1px',
                                        'fontSize':12},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
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
                                        'fontSize':14},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown5',
                                    options=[
                                        {'label':'メニュー化', 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'6vw',
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
                                        'fontSize':14},
                                    className='font-weight-bold'
                                ),
                                dcc.Dropdown(
                                    id='AI_dropdown6',
                                    options=[
                                        {'label':'メニュー化', 'value':1},
                                        {'label':'無', 'value':0},
                                    ],
                                    value=0,
                                    style={'width':'6vw',
                                        'margin-bottom':'1px',
                                        'fontSize':14},
                                    clearable=False,
                                    className='text-dark',
                                ),
                            ]
                        )
                    ],
                    style={'margin-bottom': '10px'}
                ),
                dbc.Button(
                    id='AI_button',
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
        dbc.Row(
            [   # 1行1列
                dbc.Col(
                    [   
                        dcc.Loading(id='tmp_loading_1-1',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='AI-color-ratio',
                                            style={'height':'29vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                ],
                className='bg-info col-3',
                style={'padding':'8px'}
                ),
                # 1行2列
                dbc.Col(
                    [   
                        dcc.Loading(id='tmp_loading_1-2',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='AI_treatment-ratio',
                                            style={'height':'29vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],
                    className='bg-info col-3',
                    style={'padding':'8px'}
                ),
                # 1行3列
                dbc.Col(
                    [   
                        dcc.Loading(id='tmp_loading_1-3',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='AI-pama-ratio',
                                            style={'height':'29vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],
                    className='bg-info col-3',
                    style={'padding':'8px'}
                ),
                # 1行4列
                dbc.Col(  
                    [   
                        dcc.Loading(id='tmp_loading_1-4',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='brand-target',
                                            style={'height':'29vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],                                          
                    className='bg-info col-3',
                    style={'padding':'8px'}
                )
            ],
            className='bg-primary',
            style={'height':'30vh'}
        ),
        dbc.Row(
            [   # 2行1列
                dbc.Col(
                    [   
                        dcc.Loading(id='tmp_loading_2-1',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='review_score_prediction',
                                            style={'height':'68vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],                    
                    style={'padding':'8px'},
                    className='bg-info col-6'
                ),
                # 2行2列
                dbc.Col(
                    [   
                        dcc.Loading(id='tmp_loading_2-2',
                            children=[
                                    html.Div(
                                        [
                                            dcc.Graph(
                                            id='each_price_prediction',
                                            style={'height':'68vh'}
                                            ), 
                                        ]
                                    )
                            ],
                            style={'margin': '10%',
                                    },
                            type='dot',
                            color='#ffffb3',
                            className='bg-info'),
                    ],
                    style={'padding':'8px'},
                    className='bg-info col-6'
                    ),
            ],
            className='bg-info',
            style={'height':'70vh'}
        )   
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

# 1行1列
@callback(
    Output('AI-color-ratio', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def color_ratio_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100
    
    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)
    
    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')
    
    _score = np.mean([model.predict(_df) for model in color_ratio_models])
    _score = round(_score, 2)
    
    _df=pd.DataFrame(data=[['する', _score],
                           ['しない', 1-_score]],
                     columns=['カラー選択','選択割合'])
    
    figure = px.pie(data_frame=_df,
                    names='カラー選択',
                    values='選択割合',
                    color='カラー選択',
                    title=f'Potential Color Ratio',
                    # height=290,
                    # width=418,
                    color_discrete_map={'する':'#fccde5','しない':'#b3de69'},
                    category_orders={'カラー選択':['する','しない']}
                )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            )
        ),
        hovertemplate='カラー選択: %{label}<br>選択割合: %{percent}',
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
        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,
                                  )
                        ),
        paper_bgcolor='lightcyan',
        legend=dict(
            title=dict(text='カラー選択',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行2列
@callback(
    Output('AI_treatment-ratio', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def treatment_ratio_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100
    
    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)
    
    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')
    
    _score = np.mean([model.predict(_df) for model in treatment_ratio_models])
    _score = round(_score, 2)
    
    _df=pd.DataFrame(data=[['する', _score],
                           ['しない', 1-_score]],
                     columns=['トリートメント選択','選択割合'])
    
    figure = px.pie(data_frame=_df,
                    names='トリートメント選択',
                    values='選択割合',
                    color='トリートメント選択',
                    title=f'Potential Treatment Ratio',
                    # height=290,
                    # width=418,
                    color_discrete_map={'する':'#fccde5','しない':'#b3de69'},
                    category_orders={'トリートメント選択':['する','しない']}
                )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            )
        ),
        hovertemplate='トリートメント選択: %{label}<br>選択割合: %{percent}',
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

        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,
                                
                                  )
                        ),
        paper_bgcolor='lightcyan',
        
        legend=dict(
            title=dict(text='トリートメント選択',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure

# 1行3列
@callback(
    Output('AI-pama-ratio', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def pama_ratio_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100

    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)
    
    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')
    
    _score = np.mean([model.predict(_df) for model in pama_ratio_models])
    _score = round(_score, 2)
    
    _df=pd.DataFrame(data=[['する', _score],
                           ['しない', 1-_score]],
                     columns=['パーマ選択','選択割合'])
    figure = px.pie(data_frame=_df,
                    names='パーマ選択',
                    values='選択割合',
                    color='パーマ選択',
                    title=f'Potential Perm Ratio',
                    # height=290,
                    # width=418,
                    color_discrete_map={'する':'#fccde5','しない':'#b3de69'},
                    category_orders={'パーマ選択':['する','しない']}
                )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            )
        ),
        hovertemplate='パーマ選択: %{label}<br>選択割合: %{percent}',
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
        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,                      
                                  )
                        ),
        paper_bgcolor='lightcyan',
        legend=dict(
            title=dict(text='パーマ選択',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
    )
    
    return figure

# 1行4列
@callback(
    Output('brand-target', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def pama_ratio_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100

    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)

    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')

    # 1秒遅らせる処理を入れて原因不明のバグを修正
    time.sleep(1)
    
    illumina_proba = round(np.max([model.predict_proba(_df)[:, 1]*100 for model in illumina_classification_models]), 2)
    addicthy_proba = round(np.max([model.predict_proba(_df)[:, 1]*100 for model in addicthy_classification_models]), 2)
    inoa_proba = round(np.max([model.predict_proba(_df)[:, 1]*100 for model in inoa_classification_models]), 2)
    aujua_proba = round(np.max([model.predict_proba(_df)[:, 1]*100 for model in aujua_classification_models]), 2)

    _df = pd.DataFrame([illumina_proba, addicthy_proba, inoa_proba, aujua_proba], index=['Illumina','Addicthy','Inoa','Aujua'], columns=['メニュー化成功率']).reset_index()
    _df.rename(columns={'index': 'ブランド'}, inplace=True)
    
    xaxes_range_min = 0
    xaxes_range_max = _df['メニュー化成功率'].max() + 10
    
    figure=px.bar(data_frame=_df,
                  y='ブランド',
                  x='メニュー化成功率',
                  color='ブランド',
                  text=[f'{text:,}%' for text in _df['メニュー化成功率']],
                  color_discrete_sequence=plotly.colors.qualitative.Pastel2,
                  title=f'Probability Of Potential Utilizing',
                #   height=290,
                #   width=418,
                )
    
        
    figure.update_traces(
        width=0.6,
        orientation='h',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='ブランド名: %{y}<br>メニュー化成功率: %{x}%',
        marker=dict(
            line=dict(
            color='slategrey',
            width=1.5,
            )
        ),
    )

    figure.update_layout(
        plot_bgcolor='#f7fcf5',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        uniformtext_mode='hide',
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=12,
        ),

        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,
                                  )
                        ),
        paper_bgcolor='lightcyan',
        legend=dict(
            title=dict(text='ブランド',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            borderwidth=1.5,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),   
    )

    figure.update_xaxes(
        ticksuffix='%',
        tickvals=np.arange(xaxes_range_min, xaxes_range_max, 10),
        range=(xaxes_range_min,xaxes_range_max)
    )
    
    figure.update_yaxes(
        title=''
    )    
    
    return figure

# 2行1列
@callback(
    Output('review_score_prediction', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def review_score_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100

    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)
    
    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')

    
    general_score = round(np.min([model.predict(_df) for model in general_review_models]), 2)
    atmosphere_score = round(np.min([model.predict(_df) for model in atmosphere_models]), 2)
    hospitality_score = round(np.min([model.predict(_df) for model in hospitality_models]), 2)
    skills_and_completion_score = round(np.min([model.predict(_df) for model in skills_and_completion_models]), 2)
    menu_and_price_score = round(np.min([model.predict(_df) for model in menu_and_price_models]), 2)
    
    _df = pd.DataFrame([general_score, atmosphere_score, hospitality_score, skills_and_completion_score, menu_and_price_score],
                        index=['総合','雰囲気','接客サービス','技術・仕上がり', 'メニュー・料金'], columns=['レビューの平均点']).reset_index()
    _df.rename(columns={'index': 'レビュー項目'}, inplace=True)

    xaxes_range_min = math.floor(_df['レビューの平均点'].min() - 1)
    xaxes_range_max = 5
    
    figure=px.bar(data_frame=_df,
                  y='レビュー項目',
                  x='レビューの平均点',
                  color='レビュー項目',
                  text=[f'{text:,}' for text in _df['レビューの平均点']],
                  color_discrete_sequence=plotly.colors.qualitative.Set3,
                  title=f'Prediction Of Each Review Score',
                #   height=650,
                #   width=418,
                )
    
        
    figure.update_traces(
        width=0.5,
        orientation='h',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='レビュー項目: %{y}<br>レビューの平均点: %{x}',
        marker=dict(
            line=dict(
            color='slategrey',
            width=1.5,
            )
        ),
    )

    figure.update_layout(   
        plot_bgcolor='#f7fcf5',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        uniformtext_mode='hide',
        margin={'l':30, 'r':30, 't':70, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=12,
        ),
        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,
                                  )
                        ),
        paper_bgcolor='lightcyan',
        legend=dict(
            title=dict(text='レビュー項目',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            borderwidth=1.5,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),   
    )

    figure.update_xaxes(
        tickvals=np.arange(xaxes_range_min, xaxes_range_max, 1),
        range=(xaxes_range_min,xaxes_range_max)
    )
    
    figure.update_yaxes(
        title=''
    )    
    
    return figure

# 2行2列
@callback(
    Output('each_price_prediction', 'figure'),
    Input('AI_button', 'n_clicks'),
    [
        # 県
        State('AI_dropdown1', 'value'),
        # エリア
        State('AI_dropdown2', 'value'),
        # セット面の数
        State('AI_input1', 'value'),
        # ブログ投稿数
        State('AI_input2', 'value'),
        # 口コミ数
        State('AI_input3', 'value'),
        # スタッフ数
        State('AI_input4', 'value'),
        # クーポン数
        State('AI_input5', 'value'),
        # メニュー数
        State('AI_input6', 'value'),
        # スタイル数
        State('AI_input7', 'value'),
        # 駅徒歩
        State('AI_input8', 'value'),
        # コメントへの返信率
        State('AI_input9', 'value'),
        # イルミナメニュー化の有無
        State('AI_dropdown3', 'value'),
        # addicthyメニュー化の有無
        State('AI_dropdown4', 'value'),
        # inoaメニュー化の有無
        State('AI_dropdown5', 'value'),
        # Aujuaメニュー化の有無
        State('AI_dropdown6', 'value'),
    ],
)
def pama_ratio_figure(n_clicks, AI_dropdown1_value, AI_dropdown2_value, 
                       AI_input1_value, AI_input2_value, AI_input3_value, AI_input4_value, AI_input5_value, AI_input6_value, AI_input7_value, AI_input8_value, AI_input9_value,
                       AI_dropdown3_value, AI_dropdown4_value, AI_dropdown5_value, AI_dropdown6_value):
    
    _df = pd.DataFrame(data=[['県', 'エリア', 0, 0.0, 0, 0, 0, 0, 0, 0, 0.0]],
                    columns=['県', 'エリア', 'セット面の数', 'ブログ投稿数', '口コミ数', 'スタッフ数', 'クーポン数', 'メニュー数', 'スタイル数', '駅徒歩', 'コメントへの返信率'])
    _df['県'] = AI_dropdown1_value
    _df['エリア'] = AI_dropdown2_value
    _df['セット面の数'] = AI_input1_value
    _df['ブログ投稿数'] = AI_input2_value
    _df['口コミ数'] = AI_input3_value
    _df['スタッフ数'] = AI_input4_value
    _df['クーポン数'] = AI_input5_value
    _df['メニュー数'] = AI_input6_value
    _df['スタイル数'] = AI_input7_value
    _df['駅徒歩'] = AI_input8_value
    _df['コメントへの返信率'] = AI_input9_value / 100
    _df['カット選択'] = 0
    _df['カラー選択'] = 0
    _df['トリートメント選択'] = 0
    _df['パーマ選択'] = 0
    _df['縮毛矯正選択'] = 0
    _df['その他選択'] = 0
    _df['ヘッドスパ選択'] = 0
    _df['イルミナメニュー化の有無'] = AI_dropdown3_value
    _df['Aujuaメニュー化の有無'] = AI_dropdown6_value
    _df['addicthyメニュー化の有無'] = AI_dropdown4_value
    _df['inoaメニュー化の有無'] = AI_dropdown5_value
    
    _df['ブログ投稿数'] = _df['ブログ投稿数'].astype(int)
    _df['口コミ数'] = _df['口コミ数'].astype(int)
    _df['スタイル数'] = _df['スタイル数'].astype(int)
    
    _df['県'] = _df['県'].astype('category')
    _df['エリア'] = _df['エリア'].astype('category')
    
    cut_df = _df.copy()
    cut_df['カット選択'] = 1
    
    cut_treatment_df = _df.copy()
    cut_treatment_df['カット選択'] = 1
    cut_treatment_df['トリートメント選択'] = 1
    
    cut_color_df = _df.copy()
    cut_color_df['カット選択'] = 1
    cut_color_df['カラー選択'] = 1
    
    cut_color_treatment_df = _df.copy()
    cut_color_treatment_df['カット選択'] = 1
    cut_color_treatment_df['カラー選択'] = 1
    cut_color_treatment_df['トリートメント選択'] = 1
    
    cut_pama_df = _df.copy()
    cut_pama_df['カット選択'] = 1
    cut_pama_df['パーマ選択'] = 1
    
    cut_pama_treatment_df = _df.copy()
    cut_pama_treatment_df['カット選択'] = 1
    cut_pama_treatment_df['パーマ選択'] = 1
    cut_pama_treatment_df['トリートメント選択'] = 1
    
    cut_straight_df = _df.copy()
    cut_straight_df['カット選択'] = 1
    cut_straight_df['縮毛矯正選択'] = 1
    
    cut_straight_treatment_df = _df.copy()
    cut_straight_treatment_df['カット選択'] = 1
    cut_straight_treatment_df['縮毛矯正選択'] = 1
    cut_straight_treatment_df['トリートメント選択'] = 1
    
    cut_color_pama_df = _df.copy()
    cut_color_pama_df['カット選択'] = 1
    cut_color_pama_df['カラー選択'] = 1
    cut_color_pama_df['パーマ選択'] = 1
    
    cut_color_pama_treatment_df = _df.copy()
    cut_color_pama_treatment_df['カット選択'] = 1
    cut_color_pama_treatment_df['カラー選択'] = 1
    cut_color_pama_treatment_df['パーマ選択'] = 1
    cut_color_pama_treatment_df['トリートメント選択'] = 1
    
    cut_color_straight_df = _df.copy()
    cut_color_straight_df['カット選択'] = 1
    cut_color_straight_df['カラー選択'] = 1
    cut_color_straight_df['縮毛矯正選択'] = 1
    
    cut_color_straight_treatment_df = _df.copy()
    cut_color_straight_treatment_df['カット選択'] = 1
    cut_color_straight_treatment_df['カラー選択'] = 1
    cut_color_straight_treatment_df['縮毛矯正選択'] = 1
    cut_color_straight_treatment_df['トリートメント選択'] = 1
    
    cut_score = int(round(np.mean([model.predict(cut_df) for model in payments_models]),-2))
    cut_treatment_score = int(round(np.mean([model.predict(cut_treatment_df) for model in payments_models]),-2))
    cut_color_score = int(round(np.mean([model.predict(cut_color_df) for model in payments_models]),-2))
    cut_color_treatment_score = int(round(np.mean([model.predict(cut_color_treatment_df) for model in payments_models]),-2))
    cut_pama_score = int(round(np.mean([model.predict(cut_pama_df) for model in payments_models]),-2))
    cut_pama_treatment_score = int(round(np.mean([model.predict(cut_pama_treatment_df) for model in payments_models]),-2))
    cut_straight_score = int(round(np.mean([model.predict(cut_straight_df) for model in payments_models]),-2))
    cut_straight_treatment_score = int(round(np.mean([model.predict(cut_straight_treatment_df) for model in payments_models]),-2))
    cut_color_pama_score = int(round(np.mean([model.predict(cut_color_pama_df) for model in payments_models]),-2))
    cut_color_pama_treatment_score = int(round(np.mean([model.predict(cut_color_pama_treatment_df) for model in payments_models]),-2))
    cut_color_straight_score = int(round(np.mean([model.predict(cut_color_straight_df) for model in payments_models]),-2))
    cut_color_straight_treatment_score = int(round(np.mean([model.predict(cut_color_straight_treatment_df) for model in payments_models]),-2))
    
    _df = pd.DataFrame([cut_score, cut_treatment_score, cut_color_score, cut_color_treatment_score, cut_pama_score, cut_pama_treatment_score, cut_straight_score, 
                        cut_straight_treatment_score, cut_color_pama_score, cut_color_pama_treatment_score, cut_color_straight_score, cut_color_straight_treatment_score],
                        index=['カット','カット+Tr','カット+カラー','カット+カラー+Tr', 'カット+パーマ', 'カット+パーマ+Tr','カット+縮毛矯正','カット+縮毛矯正+Tr',
                               'カット+カラー+パーマ','カット+カラー+パーマ+Tr','カット+カラー+縮毛矯正','カット+カラー+縮毛矯正+Tr'],
                        columns=['支出金額']).reset_index()
    _df.rename(columns={'index': 'メニュー'}, inplace=True)

    xaxes_range_min = math.floor((_df['支出金額'].min() - 1000)/1000)*1000
    xaxes_range_max = round(_df['支出金額'].max(), -3)+3000
    figure=px.bar(data_frame=_df,
                  y='メニュー',
                  x='支出金額',
                  color='メニュー',
                  text=[f'¥{text:,}' for text in _df['支出金額']],
                  color_discrete_sequence=plotly.colors.qualitative.Pastel2,
                  title=f'Prediction Of Each Menu Payments',
                #   height=650,
                #   width=418,
                )
    
        
    figure.update_traces(
        width=0.5,
        orientation='h',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='メニュー: %{y}<br>支出金額: %{x}',
        marker=dict(
            line=dict(
            color='slategrey',
            width=1.5,
            )
        ),
    )

    figure.update_layout(
        
        plot_bgcolor='#f7fcf5',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        uniformtext_mode='hide',
        
        margin={'l':30, 'r':30, 't':70, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family=default_font,
            size=12,
        ),

        hoverlabel=dict(font=dict(family='Comic Sans Ms',
                                  size=12,
                                  )
                        ),
        paper_bgcolor='lightcyan',
        legend=dict(
            title=dict(text='メニュー',
                       font=dict(family=default_font,
                                 size=10),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            borderwidth=1.5,
            font=dict(size=10,
                      family=default_font,
                      color='slategrey'),
        ),   
    )

    figure.update_xaxes(
        tickformat=',',
        tickprefix='¥',
        tickvals=np.arange(xaxes_range_min, xaxes_range_max, 3000),
        range=(xaxes_range_min,xaxes_range_max)
    )
    
    figure.update_yaxes(
        title=''
    )    
    
    return figure