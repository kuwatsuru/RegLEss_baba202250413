import streamlit as st

# ページ設定は最初のStreamlitコマンドとして必ず一度だけ呼び出す
st.set_page_config(page_title="RegLess")

# 以降の Streamlit コマンドは set_page_config の後に記述
import streamlit.components.v1 as components
from PIL import Image


def main():
    # DB 初期化関数を遅延インポート（st.cache_resource 呼び出しより後）
    from db import init_db

    # スクリプトファイルのあるディレクトリを基準に画像パスを解決
    import os
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "images", "regless_logo.png")

    # ロゴ表示
    try:
        image = Image.open(image_path)
        st.image(image, use_container_width=False, width=200)
    except FileNotFoundError:
        st.error(f"ロゴ画像が見つかりません: {image_path}")

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
                @keyframes fadeInUp { 0% { opacity:0; transform:translateY(30px);} 100% { opacity:1; transform:translateY(0);} }
                .fade-in-text { font-family:'Noto Sans JP',sans-serif; font-size:36px; font-weight:500; color:#333; text-align:center; animation:fadeInUp 1.2s ease-out both; }
            </style>
        </head>
        <body>
            <div class="fade-in-text">- 残された時間に 後悔のない毎日を -</div>
        </body>
        """
    )

    st.write("")

    # 操作案内
    components.html(
        """
        <div style='text-align:center;'><p><span style='color:royalblue; font-size:28px; font-weight:bold;'>←サイドバーページから機能を選択してください。</span></p></div>
        """
    )

    # アプリ起動時にDBを初期化（接続確認）
    init_db()


if __name__ == "__main__":
    main()
