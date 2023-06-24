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
                            html.Span('現在は都内のIT企業で異常音検知のシステム開発に携わっています。'),html.Br(),
                            html.Span('機械学習エンジニアとして業務だけでなく業務外でも何かのアウトプットがしたいと思い、個人開発に取り組みました。'),html.Br(),
                            html.Span('今回のテーマは4年間お世話になったヘアサロン業界でさまざまな美容師様をサポートさせていただいた中でこんなアプリ(プラットフォーム)があったら便利だなと感じていたものです。'),html.Br(),
                            html.Span('ヘアサロン業界関係者の皆様に本アプリをご活用いただき、フィードバックを頂けますと大変嬉しく思います。'),html.Br(),
                            html.Span('(今回公開しているのは中国四国エリアのみとなります。その他エリアに関しては順次公開していきます。)'),html.Br(),html.Br(),
                            html.H3('機能紹介',
                                    style={'text-decoration':'underline',}),
                            html.Span('本アプリには大きく4つの機能があります。'),html.Br(),html.Br(),
                            html.H5('1.サロン情報分析ダッシュボード(AnalysisDashboard)',
                                    style={'text-decoration':'underline',}),
                            html.Span('中国四国エリアのHot Pepper Beautyに登録している全てのサロンの基本情報に加え、カラー比率や単価などの情報が確認できます。'),html.Br(),html.Br(),
                            html.H5('2.サロン-ブランドマップ(SalonMap)',
                                    style={'text-decoration':'underline',}),
                            html.Span('業界でシェアを獲得している主なブランドについて指定エリアごとの活用状況を確認できます。'),html.Br(),
                            html.Span('また指定のブランドを活用しているサロンと活用していないサロンを地図上で確認できます。'),html.Br(),html.Br(), 
                            html.H5('3.口コミ情報(ReviewTable)',
                                    style={'text-decoration':'underline',}),
                            html.Span('指定したサロンの口コミ点数の割合と口コミを表示できます。'),html.Br(),
                            html.Span('また口コミは点数の条件を指定して表示することができます。'),html.Br(),
                            html.Span('指定した条件で絞り込んだ口コミをcsvファイルでダウンロードできます。'),html.Br(),html.Br(),
                            html.H5('4.サロンポテンシャル分析(PotentialAnalysis)',
                                    style={'text-decoration':'underline',}),
                            html.Span('AI(Microsoftが開発したLightGBMを採用)を用いて未知のサロン(これから出店するサロン)が持つポテンシャルを予測します。'),html.Br(),
                            html.Span('既存顧客のサロンのポテンシャルを再分析し、現状と比較することもできます。'),html.Br(),
                            html.Span('(AIの精度は100%ではありませんので日々の営業活動の参考程度にとどめていただけますと幸いです。)'),html.Br(),html.Br(),
                            html.H3('画面設定',
                                    style={'text-decoration':'underline',}),
                            html.Span('画面サイズ100%, 解像度1920×1080, ブラウザの倍率:80%~90%に設定の上ご使用ください。'),html.Br(),
                            html.Span('※設定条件次第で画面が崩れる可能性があります。上記を目安に適宜調整いただけますと幸いです。'),html.Br(),html.Br(),
                            html.H3('GitHubリポジトリ',
                                    style={'text-decoration':'underline',}),
                            html.Span('GitHubにてソースコードを公開しています。'),html.Br(),
                            html.A('RyoyaMasuda/HPB_analysis_dashboard', href='https://github.com/RyoyaMasuda/HPB_analysis_dashboard/', target='_blank'),
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