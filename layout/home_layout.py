import dash_bootstrap_components as dbc
from dash import html

home_layout = [
    dbc.Row(
        [
            dbc.Col(
                width=3,
            ),
            dbc.Col(
                [
                    html.Div(
                        [   
                            html.Br(),
                            html.H2('ヘアサロン業界の営業様向けアプリの開発'),html.Br(),
                            html.H3('自己紹介',
                                    style={'text-decoration':'underline',}),
                            html.Span('はじめまして。機械学習エンジニア/データサイエンティストの増田燎也と申します。'),html.Br(),
                            html.Span('私はヘアサロン業界で4年、IT業界で1年社会人として経験を積んできました。'),html.Br(),
                            html.Span('ヘアサロン業界ではスーパーバイザー(法人営業)を担当しており、さまざまな美容師様をサポートさせていただきました。'),html.Br(),
                            html.Span('日々の営業活動の中で、こんなアプリ(プラットフォーム)があったら便利だなと感じていたものを今回形にしてみました。'),html.Br(),
                            html.Span('ヘアサロン業界関係者の皆様に本アプリをご活用いただき、フィードバックを頂けますと大変嬉しく思います。'),html.Br(),
                            html.Span('(今回公開しているのは中国四国エリアのみとなります。その他エリアに関しては順次公開していきます。)'),html.Br(),html.Br(),
                            html.H3('機能紹介',
                                    style={'text-decoration':'underline',}),
                            html.Span('本アプリには大きく4つの機能があります。'),html.Br(),html.Br(),
                            html.H5('サロン情報分析ダッシュボード(AnalysisDashboard)',
                                    style={'text-decoration':'underline',}),
                            html.Span('    中国四国エリアのHot Pepper Beautyに登録している全てのサロンの基本情報に加え、カラー比率や単価などの営業様が把握したい情報が確認できます。'),html.Br(),html.Br(),
                            html.H5('サロン-ブランドマップ(SalonMap)',
                                    style={'text-decoration':'underline',}),
                            html.Span('業界でシェアを獲得している主なブランドについて指定エリアごとの活用状況を確認できます。'),html.Br(),
                            html.Span('また指定のブランドを活用しているサロンと活用していないサロンを地図上で確認できます。'),html.Br(),html.Br(), 
                            html.H5('口コミ情報(ReviewTable)',
                                    style={'text-decoration':'underline',}),
                            html.Span('業界でシェアを獲得している主なブランドについて指定エリアごとの活用状況を確認できます。'),html.Br(),html.Br(),
                            html.H5('サロンポテンシャル分析(PotentialAnalysis)',
                                    style={'text-decoration':'underline',}),
                            html.Span('AIアルゴリズムを用いて未知のサロン(これから出店するサロン)が持つポテンシャルを予測します。'),html.Br(),
                            html.Span('既存顧客のサロンのポテンシャルを再分析し、現状と比較することもできます。'),html.Br(),
                            html.Span('(AIの精度は100%ではありませんので日々の営業活動の参考程度にとどめていただけますと幸いです。)'),html.Br(),html.Br(),
                            html.H3('GitHubリポジトリ',
                                    style={'text-decoration':'underline',}),
                            html.Span('GitHubにてソースコードを公開しています。'),html.Br(),
                            html.A('HPB_analysis_dashboard', href='https://github.com/RyoyaMasuda/HPB_analysis_dashboard/', target='_blank'),
                        ]
                    )        
                ]
            ),
            dbc.Col(
                width=3,
            )
        ],
        style={'height':'100vh'}
    ),
]