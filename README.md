## 概要

自分が持っているスニーカーを記録するバーチャルスニーカーラック. StockXのデータから機械学習を用いたスニーカーのリセール価格予測機能も持つ. 

## 動かし方

1. postgresのdockerfileを作成

- % cd ./sneaker_project/web/
- % python create_postgres_dockerfile.py
- % cd ..

2. Docker containersをビルドして実行

- % docker-compose build
- % docker-compose up -d

3. データベースの作成と初期化

- % docker-compose run --rm web python ./instance/db_create.py

ウェブブラウザで開く:
    localhost:80

## 使用した主なモジュール
### web app
- Flask - ウェブフレームワーク
- Jinga2 - テンプレートエンジン
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - パスワードのハッシュ化
- Flask-Login - ユーザーマネジメントのサポート
- Flask-Migrate - データベースの移行
- Flask-WTF - フォーム作成
- itsdangerous - ユーザーマネジメント、トークン化

### machine learning
- Beautiful Soup - スクレイピング
- Selenium - スクレイピング
- Xception(keras) - 画像の特徴量抽出器. imagenetで学習済み
- 文字レベルCNN(keras) - テキストの特徴量抽出器
- PCA(scikit-learn) - 次元削減
- Xgboost - リセール価格の分類モデル

Python 3.8.0.を使用. データベースにはPostgreSQLを使用. Dockerによるコンテナ型仮想化. 

## Unit Testing

最上位のディレクトリに移動:
    % nose2
