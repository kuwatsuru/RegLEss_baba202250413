import streamlit as st
import os
from PIL import Image
import streamlit.components.v1 as components
from db import init_db

# ページ設定は最初に一度だけ
st.set_page_config(page_title="RegLess")


def main():
    # スクリプトファイルの所在ディレクトリを基準に画像パスを解決
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "images", "regless_logo.png")

    # ロゴ表示
    try:
        image = Image.open(image_path)
        st.image(image, use_container_width=False, width=200)
    except FileNotFoundError:
        st.error(f"ロゴ画像が見つかりません: {image_path}") #エラー時のメッセージ追加

    # 大見出し
    components.html(
        """
        <div style='text-align:center;'>
            <p><span style='color:black; font-size:100px; font-family:Courier'>RegLess</span></p>
        </div>
        """
    )
    # サブタイトル（フェードインアニメーション）
    components.html(
    """
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500&display=swap" rel="stylesheet">
        <style>
            @keyframes fadeInUp {
                0% {
                    opacity: 0;
                    transform: translateY(30px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .fade-in-text {
                font-family: 'Noto Sans JP', sans-serif;
                font-size: 36px;
                font-weight: 500;
                color: #333;
                text-align: center;
                animation: fadeInUp 1.2s ease-out both;
                margin-top: 0px;
            }
        </style>
    </head>

    <body>
        <div class="fade-in-text">
            - 残された時間に 後悔のない毎日を -
        </div>
    </body>
    """
)
    
    st.write("")


    components.html(
    """
    <div style='text-align: center;'>
        <p>
            <span style='color:royalblue ; font-size: 28px; font-weight: bold;''>←サイドバーページから機能を選択してください。</span>
        </p>
    </div>
    """
)

        # アプリ起動時にDBを初期化
    init_db()

if __name__ == "__main__":
    main()
