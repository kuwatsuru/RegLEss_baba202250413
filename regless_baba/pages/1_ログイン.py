import streamlit as st
import datetime
from auth import login, signup, logout, get_current_user
from life_calc import calculate_remaining_life


def app():
    st.set_page_config(page_title="RegLess - ログイン")
    
    # 既にログイン済みかチェック
    current_user = get_current_user()
    
    if current_user:
        st.header(f"こんにちは、{current_user['username']}さん")
        
        if st.button("ログアウト"):
            success, message = logout()
            if success:
                st.success(message)
                st.rerun()  # ページをリロード
            else:
                st.error(message)
    else:
        st.header("ログイン / 新規登録")
        
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
            

            # # 残り寿命の計算と表示（既存のコードを活用）
            # if "estimated_life" in st.session_state:
            #     estimated_life = st.session_state.estimated_life
            # else:
            #     estimated_life = 84  # デフォルト値
            
            # estimated_life_input = st.number_input(
            #     "推定寿命（年）",
            #     min_value=0,
            #     value=estimated_life
            # )
            
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
                    else:
                        st.error(message)
if __name__ == "__main__":
    app()
