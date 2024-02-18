# ホットペッパービューティーの顧客分析ダッシュボード
個人開発として取り組んだダッシュボード開発のソースコードを公開します。

# 画面設定のお願い
window環境において
- 画面サイズ：100%
- 解像度：1920×1080
- ブラウザの倍率：80〜90%

に設定をお願いします。<br>
※その他の環境では画面崩れが生じる可能性があります。適宜調整いただけますと幸いです。

# アプリのURL
~http://hpbdashboard.mydns.jp/~  
(自宅サーバにてURLを公開しておりましたが、現在別用途にて使用しておりますのでアプリの立ち上げ方法を記載します。)

# アプリ起動方法(Documentsディレクトリにてアプリを起動する方法)
1. Documentsディレクトリに移動します
```
cd ~/Documents
```
2. リポジトリをクローンします。
```
git clone git@github.com:RyoyaMasuda/HPB_analysis_dashboard.git
```
3. 

# 開発環境
- AWS VPC
- AWS EC2
- AWS Route53
- AWS ALB
- AWS S3
- docker-compose
- Nginx
- uWSGI
- pyenv
- python3.8.10
- jupyterlab
- Dash
- bootstrap4(dash_bootstrap_component)
- Plotly
- plotly express
- pandas
- numpy
- scikit-learn
- LightGBM

# 本番環境
- ubuntu 22.04 LTS server
- Nginx
- uWSGI
- pyenv
- python3.8.10
- Dash
- bootstrap4(dash_bootstrap_component)
- Plotly
- plotly express
- pandas
- numpy
- scikit-learn
- LightGBM
