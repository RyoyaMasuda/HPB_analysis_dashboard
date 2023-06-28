import dash_bootstrap_components as dbc
from dash import html

contact_layout = [
    dbc.Row(
        [
            dbc.Col(
                width=4,
            ),
            dbc.Col(
                [
                    html.Div(
                        [  
                            html.Br(),
                            html.H2('お問い合わせ先'),
                            html.H3('メールアドレス',
                                    style={'text-decoration':'underline',}),
                            html.Span('メールアドレス: despocampi.foot@gmail.com'),html.Br(),html.Br(),
                            html.H3('LINE',
                                    style={'text-decoration':'underline',}),
                            html.Td(html.Img(src='./assets/IMG_4074.png')),
                        ],
                        style={'fontSize':16}
                    )        
                ],
                
            ),
            dbc.Col(
                width=3,
            )
        ],
        style={'height':'100vh'}
    ),
]
