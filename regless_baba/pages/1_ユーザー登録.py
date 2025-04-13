import streamlit as st
import datetime
from db import insert_user, get_user_by_username
from life_calc import calculate_remaining_life

def app():
    st.set_page_config(page_title="RegLess")
    st.header("ユーザー登録")

    st.write("**アカウント情報の入力**")
    username = st.text_input("ユーザー名（他ユーザーとの重複不可）", "")
    password = st.text_input("パスワード", type="password")

    # 生年月日入力（date型）
    st.write("**ユーザー情報の入力**")
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
        value=st.session_state.get("estimated_life", 80)
    )

    if st.button("ユーザー登録"):
        # ユーザー名がすでに存在するかチェック
        existing_user = get_user_by_username(username)
        if existing_user:
            st.error("このユーザー名は既に使われています。別の名前を入力してください。")
        else:
            birthdate_str = birthdate_input.strftime("%Y-%m-%d")
            insert_user(
                username,
                password,
                birthdate_str,
                smoking,
                drinking,
                exercise,
                body_shape,
                estimated_life_input
            )
            st.success("ユーザー登録が完了しました！")

def run():
    """
    Streamlitでpagesフォルダ内のファイルを認識させるためのエントリーポイント。
    直接このファイルを呼び出すときは app() を実行。
    """
    app()


# ファイルを直接実行した場合に app() を実行する
if __name__ == "__main__":
    app()