import streamlit as st
from db import get_user_by_username, get_wants_by_user, complete_want, update_want, insert_want
from auth import get_current_user

def app():
    st.set_page_config(page_title="RegLess")
    st.header("ダッシュボード")

    # ─── 1. ログイン済みユーザーを取得 ───
    current_user = get_current_user()
    if current_user is None:
        st.warning("Homeからログインしてください。")
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
            st.write(f"{deadline}")
            st.write(f"費用：{cost}円")
            st.write(f" 期間：{period}")
            st.write(f"アクション：{first_step}")
            st.write(f"タグ：{tag}")

            if st.button("編集", key=f"edit_{want_id}"):
                st.session_state[f"edit_mode_{want_id}"] = True

            if st.session_state.get(f"edit_mode_{want_id}", False):
                new_title = st.text_input("タイトル", value=title, key=f"new_title_{want_id}")
                new_cost = st.text_input("費用", value=cost, key=f"new_cost_{want_id}")
                new_period = st.text_input("期間", value=period, key=f"new_period_{want_id}")
                new_first_step = st.text_area("1stステップ", value=first_step, key=f"new_step_{want_id}")
                new_tag = st.text_input("タグ", value=tag, key=f"new_tag_{want_id}")

                if st.button("保存する", key=f"save_{want_id}"):
                    from db import update_want  # 忘れずにインポート
                    update_result = update_want(
                        want_id=want_id,
                        updates={
                            "title": new_title,
                            "cost": new_cost,
                            "period": new_period,
                            "first_step": new_first_step,
                            "tag": new_tag
                        }
                    )
                    if update_result:
                        st.success("やりたいことを更新しました！")
                        st.session_state[f"edit_mode_{want_id}"] = False
                        st.rerun()
                    else:
                        st.error("更新に失敗しました")

        with col2:
            st.progress(1.0 if is_completed else 0.0)

        with col3:
            if not is_completed:
                if st.button("完了", key=f"complete_{want_id}"):
                    complete_want(want_id)
                    st.success(f"{title} を完了にしますか？")
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
