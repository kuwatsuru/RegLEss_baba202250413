import streamlit as st
from db import insert_want, get_user_by_username
from ai_suggest import suggest_ideas
from datetime import date, timedelta #期限設定用

def app():

    st.set_page_config(page_title="RegLess")
    st.header("やりたいこと登録")
 
    # セッション初期化（最初だけ）
    for key in ["cost", "period", "first_step"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # 暫定的にユーザー名を入力して、そのユーザーIDを取得する仕組み
    # 実際にはログインしてセッションからユーザーIDを取得するのが望ましい
    username = st.text_input("登録済みのユーザー名を入力してください")

    want_title = st.text_input("やりたいこと", "")
    cost = None
    period = None
    first_step = None

    # AIサジェスト
    if st.button("AIサジェスト"):
        if not want_title:
            st.warning("やりたいことを入力してください。")
        else:
            suggestion = suggest_ideas(want_title)
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
                        st.session_state["cost"] = int("".join(filter(str.isdigit, value)))  # 数字だけ抽出
                    elif key == "期間":
                        st.session_state["period"] = value
                    elif key == "最初のステップ":
                        st.session_state["first_step"] = value
            st.success("AIサジェストをフォームに反映しました！")


    st.write("**費用、期間、最初のステップを手動で入力する場合**")
    # 入力フォームにセッションの内容を反映
    cost = st.number_input("費用（万円）", min_value=0, value=int(st.session_state.get("cost", 0) or 0), key="cost_input")
    period = st.text_input("必要な期間（例：3ヶ月など）", value=st.session_state.get("period", ""), key="period_input")
    first_step = st.text_input("最初のステップ（例：資料を集める、問い合わせをする）", value=st.session_state.get("first_step", ""), key="first_step_input")

    tag = st.text_input("タグ（カンマ区切りなど）", "")
    deadline = st.date_input("目標期限", date.today() + timedelta(days=365), key="deadline")

    if st.button("登録する"):
        user_data = get_user_by_username(username)
        if user_data is None:
            st.error("ユーザーが存在しません。先にユーザー登録を行ってください。")
        else:
            user_id = user_data["id"]
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
            # フォームリセット（オプション）
            for key in ["cost", "period", "first_step"]:
                st.session_state[key] = ""
def run():
    app()

# ファイルを直接実行した場合に app() を実行する
if __name__ == "__main__":
    app()
