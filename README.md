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

# アプリ起動方法(Documentsディレクトリにてアプリを起動)
linux環境かUnix環境(mac環境)にて実施をしてください。(windowsの場合はWSL2のubuntuにて実施をお勧めします。)  
  
1. Documentsディレクトリに移動します
```
cd ~/Documents
```
2. リポジトリをクローンします。
```
git clone git@github.com:RyoyaMasuda/HPB_analysis_dashboard.git
```
3. modelとdataを削除します。(サンプルデータのため)
sudoは必要ないかもしれない...  
```
sudo rm -rf model data
```
4. 以下のリンクよりmodelとdataをダウンロードします。
https://drive.google.com/drive/folders/115_96jMMp5Vl0aZQIrvy-2ZP8VZgy02m  
![image](https://github.com/RyoyaMasuda/HPB_analysis_dashboard/assets/94744317/53acf4a9-9ad3-470f-99ab-74069b80b3e7)


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
