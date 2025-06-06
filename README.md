# Spring-Hackathon-2025-04-05

**起動方法**
```
docker compose up
```

**ブラウザで確認**
```
http://localhost:55001
```

**サンプルアプリの該当箇所を変更**
・.env
　→10行目：FLASK_PORT=56000

・docker-compose.yml
　→5行目：container_name: MySQL_sample
　→42行目：container_name: Flask_sample
　→54行目：- "${FLASK_PORT}:5600"


**ディレクトリ構成図**
<pre>
Desktop/
└── work_space/ 　　#←親ディレクトリ（ここでgit initと git clone初回のみ）
    ├── .git
    └── Spring-Hackathon-2025-04-05/　# 作業ディレクトリ（修正作業やpushを行う）
        ├── .git                         # ★ここで作業ブランチに変更する
        ├── ChatApp
        │   ├── __init__.py
        │   ├── app.py
        │   ├── models.py
        │   ├── static /                  # 画像などの静的ファイル用ディレクトリ
        │   ├── templates /               # Template(HTML)用ディレクトリ
        │   │   ├──auth /                 # ログインやサインアップ関係のhtmlファイル
        │   │   ├──error /                # エラー関係
        │   │   ├──model /                # チャットルーム関係
        │   │   └──util /                 # ヘッダーやサイドバーなど            
        ├── Docker/
        │   ├── Flask/
        │   │   └── Dockerfile           # Flask(Python)用Dockerファイル
        │   └── MySQL /
        │       ├── Dockerfile           # MySQL用Dockerファイル
        │       ├── init.sql             # MySQL初期設定ファイル
        │       └── my.cnf
        ├── .env
        ├── docker-compose.yml         # Spring-Hackathon用Docker-composeファイル
        ├── .gitignore
        ├── README.md
        └── requirements.txt           # Spring-Hackathon用requirements.txt
</pre>
