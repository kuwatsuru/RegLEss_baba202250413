# RegLEss_baba202250413

＜構成＞
regless/
├── main.py                   # Streamlitのエントリーポイント
├── iamages/                  #ロゴとか
├── pages/
│   ├── 0_ログイン.py                     # ログイン、ユーザー登録ページ
│   ├── 2_やりたいこと.py                  # やりたいこと登録ページ
│   ├── 3_ダッシュボード.py                # ダッシュボードページ
│   └── 4_みんなのやりたいこと.py          # コミュニティ機能ページ
├── db.py                    # DB関連の処理モジュール
├── auth.py                  #ログイン関連のモジュール
├── life_calc.py             # 残り寿命を計算するモジュール
├── ai_suggest.py            # AIサジェスト（GPT API）関連
├── requirements.txt         # 必要パッケージ一覧
├── README.md                # 簡易説明
└── utils.py                 #共通モジュール
