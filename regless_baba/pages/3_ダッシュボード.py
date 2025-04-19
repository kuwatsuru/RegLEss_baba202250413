import streamlit as st
from db import get_user_by_username, get_wants_by_user, complete_want, insert_want
from auth import get_current_user

def app():
    st.set_page_config(page_title="RegLess")
    st.header("ダッシュボード")

    # ─── 1. ログイン済みユーザーを取得 ───
    current_user = get_current_user()
    if current_user is None:
        st.warning("まずはログインしてください。")
        return
    
    #ユーザーネーム定義して、挨拶
    user_id = current_user["id"]
    username = current_user["username"]
    st.write(f"こんにちは、{username}さん")


    # ─── 2. 登録済みリストの取得と表示 ───
    st.subheader("あなたのやりたいこと一覧")
    wants_list = get_wants_by_user(user_id)
    if not wants_list:
        st.info("まだやりたいことが登録されていません。")
        return

    total_wants = len(wants_list)
    completed_count = 0

    for want in wants_list:
        want_id      = want["id"]
        title        = want["title"]
        cost         = want["cost"]
        period       = want["period"]
        first_step   = want["first_step"]
        tag          = want["tag"]
        deadline     = want["deadline"]
        is_completed = want["is_completed"]

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{title}**")
            st.write(f"期限: {deadline}")
            st.write(f"費用：{cost}円 / 期間：{period}")
            st.write(f"1stステップ：{first_step} / タグ: {tag}")
        with col2:
            st.progress(1.0 if is_completed else 0.0)
        with col3:
            if not is_completed:
                if st.button("完了", key=f"complete_{want_id}"):
                    complete_want(want_id)
                    st.success(f"{title} を完了にしました！")
                    st.rerun()
            else:
                st.write("✅ 完了済み")
        if is_completed:
            completed_count += 1

    # ─── 4. 全体進捗・残り寿命表示 ───
    st.subheader("全体進捗")
    completion_ratio = completed_count / total_wants
    st.write(f"完了率: {completion_ratio * 100:.1f}%")

    estimated_lifespan = current_user.get("estimated_lifespan")
    if estimated_lifespan is not None:
        st.write(f"推定残り寿命: {estimated_lifespan} 年")

if __name__ == "__main__":
    app()
