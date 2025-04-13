import streamlit as st
from db import init_db
import streamlit.components.v1 as components



def main():
    st.set_page_config(page_title="RegLess") #ページタイトル

    # ロゴ画像のパスまたは URL を指定
    logo_url = "regless_logo.png"

    # HTML を使ってセンタリングして表示
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="{logo_url}" alt="Logo" style="max-width: 50%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    components.html(
    """
    <div style='text-align: center;'>
        <p>
            <span style='color:black ; font-size: 100px; font-family: Courier''>RegLess</span>
        </p>
    </div>
    """
)
    components.html(
    """
    <div style='text-align: center;'>
        <p>
            <span style='color:black ; font-size: 32px; font-family: Yu Mincho''>- 残された時間に 後悔のない毎日を -</span>
        </p>
    </div>
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
