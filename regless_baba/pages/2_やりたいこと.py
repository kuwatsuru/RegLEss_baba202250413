import streamlit as st
from db import insert_want, get_user_by_username
from ai_suggest import suggest_ideas, suggest_ideas_with_all_users_rag
from datetime import date, timedelta #期限設定用
from auth import get_current_user
import time

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

    # ★① セッションステート初期化
    for key in ["cost", "period", "first_step", "tag"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    want_title = st.text_input("やりたいこと", "")

    # AIサジェスト
    if st.button("AIサジェスト"):
        if not want_title.strip():
            st.warning("やりたいことを入力してください。")
        else:
            suggestion = suggest_ideas_with_all_users_rag(want_title) #RAGを持たせた
            st.write("**AIサジェスト結果**:")
            st.write(suggestion)

            # セッションに反映
            lines = suggestion.splitlines()
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "費用":
                        st.session_state["cost"] = "".join(filter(str.isdigit, value)) or "0"
                    elif key == "期間":
                        st.session_state["period"] = value
                    elif key == "最初のステップ":
                        st.session_state["first_step"] = value
                    elif key == "タグ": # タグも追加
                        st.session_state["tag"] = value
            #st.success("AIサジェストをフォームに反映しました！")

    st.write("**費用、期間、最初のステップを手動で入力する場合**")

    # ★③ 入力欄にセッション値を反映
    cost = st.number_input(
        "費用（万円）",
        min_value=0,
        value=int(st.session_state.get("cost", 0) or 0),  # int変換エラー防止
        key="cost_input"
    )
    period = st.text_input("必要な期間（例：3ヶ月など）", value=st.session_state.get("period", ""), key="period_input")
    first_step = st.text_input("最初のステップ（例：資料を集める、問い合わせをする）", value=st.session_state.get("first_step", ""), key="first_step_input")
    tag = st.text_input("タグ（カンマ区切りなど）", value=st.session_state.get("tag", ""), key="tag_input") #
    deadline = st.date_input("目標期限", date.today() + timedelta(days=365), key="deadline")

    if st.button("登録する"):
        if not want_title.strip():
            st.warning("やりたいことを入力してください。")
            st.stop()
        elif current_user:  # 現在ログイン中のユーザーのIDを使用
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
            # ★セッションステートをリセット
            for key in ["cost", "period", "first_step", "tag"]:
                if key in st.session_state: # 存在チェックを追加（より安全）
                    st.session_state[key] = ""
            # 登録成功後も再描画を促してフォームをクリア
            # 登録成功後、0.3秒待ってから再描画を促す
            time.sleep(1) #1秒待つ
            st.rerun() 
        else:
            st.error("ログイン情報がありません。もう一度ログインしてください。")


def run():
    app()

# ファイルを直接実行した場合に app() を実行する
if __name__ == "__main__":
    app()
