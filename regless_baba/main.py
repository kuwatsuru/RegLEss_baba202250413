import streamlit as st
from db import init_db
import streamlit.components.v1 as components
from PIL import Image


def main():
    st.set_page_config(page_title="RegLess") #ページタイトル

#ロゴ表示
    image = Image.open("regless_baba/images/regless_logo.png")
    st.image(image, use_container_width=False, width=200)  # widthでサイズ調整

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
            <span style='color:black ; font-size: 32px; font-family: Train One''>- 残された時間に 後悔のない毎日を -</span>
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
