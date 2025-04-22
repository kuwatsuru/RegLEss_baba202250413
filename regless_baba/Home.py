import streamlit as st

# ページ設定は最初のStreamlitコマンドとして必ず一度だけ呼び出す
st.set_page_config(page_title="RegLess")

# 以降の Streamlit コマンドは set_page_config の後に記述
import streamlit.components.v1 as components
from PIL import Image
import datetime
from auth import login, signup, logout, get_current_user
from life_calc import calculate_remaining_life, get_random_message

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
            <p>          
            <span
            style='
              font-family:Courier;
              font-size:100px;
              text-shadow: 0 0 10px rgba(255,255,255,2);
            '

          >RegLess</span></p>
        </div>
        """
    )

    # サブタイトル（フェードインアニメーション）
    components.html(
        """
        <head>
        <link
            href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500&display=swap"
            rel="stylesheet"
        >
        <style>
            @keyframes fadeInUp {
            0%   { opacity:0; transform:translateY(30px); }
            100% { opacity:1; transform:translateY(0); }
            }
            .fade-in-text {
            font-family:'Noto Sans JP',sans-serif;
            font-size:36px;
            font-weight:500;
            text-align:center;
            text-shadow: 0 0 10px rgba(255,255,255,1);
            animation:fadeInUp 1.2s ease-out both;
            }
        </style>
        </head>
        <body>
        <div class="fade-in-text">
            - 残された人生に 後悔のない毎日を -
        </div>
        </body>
        """
    )



    # アプリ起動時にDBを初期化（接続確認）
    init_db()

#----- ここからログイン機能ｰｰｰｰ###

    # 既にログイン済みかチェック
    current_user = get_current_user()
    
    # ログアウト時間の設定
    SESSION_TIMEOUT_MINUTES = 15

    #　自動ログアウト設定
    if "login_time" in st.session_state:
        elapsed = datetime.datetime.now() - st.session_state["login_time"]
        if elapsed.total_seconds() > SESSION_TIMEOUT_MINUTES * 60:
            logout()
            st.session_state.clear()
            st.warning("一定時間操作がなかったため、自動ログアウトされました。")
            st.rerun()


    if current_user:
        st.header(f"こんにちは、{current_user['username']}さん")

        # --- ログイン成功後に残り寿命メッセージを表示 ---
        # current_user (ユーザー情報) に 'estimated_life' キーが含まれていると仮定
        estimated_life = current_user.get("estimated_lifespan")# キーが存在しない場合を考慮

        if estimated_life is not None:
            # 残り寿命からランダムメッセージを取得
            life_message = get_random_message(estimated_life)
            # メッセージを表示 (例としてst.infoを使用)
            st.subheader(life_message)
            st.write("")
        else:
            # estimated_life がユーザー情報に含まれていない場合の処理
            st.warning("ユーザーの推定寿命情報が見つかりません。プロフィールを更新してください。")
        ###
        
        if st.button("ログアウト"):
            success, message = logout()
            if success:
                st.success(message)
                st.session_state.clear()
                st.rerun()  # ページをリロード
            else:
                st.error(message)
    else:
        
        
        tab1, tab2 = st.tabs(["ログイン", "新規登録"])
        
        with tab1:
            st.subheader("ログイン")
            email = st.text_input("メールアドレス", key="login_email")
            password = st.text_input("パスワード", type="password", key="login_password")
            
            if st.button("ログイン", key="login_button"):
                if not email or not password:
                    st.error("メールアドレスとパスワードを入力してください")
                else:
                    success, result = login(email, password)
                    if success:
                        # セッションにユーザー情報を保存
                        st.session_state["user"] = result
                        st.session_state["login_time"] = datetime.datetime.now() 
                        st.success("ログインしました！")
                        st.rerun()  # ページをリロード
                    else:
                        st.write("未登録の場合は”新規登録”から登録を行ってください。")
                        st.error(result)
                    
        
        with tab2:
            st.subheader("新規登録")
            email = st.text_input("メールアドレス", key="signup_email")
            password = st.text_input("パスワード", type="password", key="signup_password")
            username = st.text_input("ユーザー名（他ユーザーとの重複不可）", key="signup_username")
            
            # 現在のユーザー登録と同じ追加情報を収集
            birthdate_input = st.date_input("生年月日", datetime.date(1990,1,1))
            smoking = st.selectbox("タバコを吸うか", ["ほぼ毎日", "たまに", "吸わない"])
            drinking = st.selectbox("お酒を飲むか", ["ほぼ毎日", "たまに", "飲まない"])
            exercise = st.selectbox("運動の習慣", ["定期的にする", "不定期", "しない"])
            body_shape = st.selectbox("体型", ["肥満", "普通", "やせ型"])

            # 残り寿命の提示
            if st.button("残り寿命を計算する"):
                birthdate_str = birthdate_input.strftime("%Y-%m-%d")
                estimated_life = calculate_remaining_life(
                birthdate_input, smoking, drinking, exercise, body_shape
            )
                st.session_state["estimated_life"] = estimated_life
                st.success(f"推定残り寿命: {estimated_life}年")
            # 推定寿命の登録を確認
            estimated_life_input = st.number_input(
                "推定寿命を手動で変更可能（年）",
                min_value=0,    
                value=st.session_state.get("estimated_life", 84)
            )

            
            if st.button("登録する", key="signup_button"):
                if not email or not password or not username:
                    st.error("必須項目を入力してください")
                else:
                    birthdate_str = birthdate_input.strftime("%Y-%m-%d")
                    success, message = signup(
                        email, 
                        password, 
                        username, 
                        birthdate_str, 
                        smoking, 
                        drinking,
                        exercise, 
                        body_shape, 
                        estimated_life_input
                    )
                    
                    if success:
                        st.success(message)
                        st.info("ログインページからログインしてください")
                        st.rerun()  # ページをリロード    
                    else:
                        st.error(message)


if __name__ == "__main__":
    main()
