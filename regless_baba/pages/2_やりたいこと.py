import streamlit as st
from db import insert_want, get_user_by_username
from ai_suggest import suggest_ideas, suggest_ideas_with_all_users_rag
from datetime import date, timedelta #期限設定用
from auth import get_current_user

def app():

    st.set_page_config(page_title="RegLess")
    st.header("やりたいこと登録")

    # ─── 1. ログイン済みユーザーを取得 ───
    current_user = get_current_user()
    if current_user is None:
        st.warning("Homeからログインしてください。")
        return
    
    #ユーザーネーム定義して、挨拶
    user_id = current_user["id"]
    username = current_user["username"]
    st.write(f"こんにちは、{username}さん")

    want_title = st.text_input("やりたいこと", "")
    cost = None
    period = None
    first_step = None

    # AIサジェスト
    if st.button("AIサジェスト"):
        if not want_title:
            st.warning("やりたいことを入力してください。")
        else:
            suggestion = suggest_ideas_with_all_users_rag(want_title) #RAGを持たせた
            st.write("**AIサジェスト結果**:")
            st.write(suggestion)

    st.write("**費用、期間、最初のステップを手動で入力する場合**")
    cost = st.number_input("費用（円）", min_value=0, value=0)
    period = st.text_input("必要な期間（例：3ヶ月など）", "")
    first_step = st.text_input("最初のステップ（例：資料を集める、問い合わせをする）", "")

    tag = st.text_input("タグ（カンマ区切りなど）", "")
    deadline = st.date_input("目標期限", date.today() + timedelta(days=365), key="deadline")

    if st.button("登録する"):
        if current_user:  # 現在ログイン中のユーザーのIDを使用
            user_id = current_user['id']
            insert_want(
                user_id=user_id,
                title=want_title,
                cost=cost,
                period=period,
                first_step=first_step,
                tag=tag,
                deadline=str(deadline)
            )
            st.success("やりたいことを登録しました！")
        else:
            st.error("ログイン情報がありません。もう一度ログインしてください。")


def run():
    app()

# ファイルを直接実行した場合に app() を実行する
if __name__ == "__main__":
    app()
