import streamlit as st
from db import get_user_by_username, get_wants_by_user, complete_want, update_want

def app():
    st.set_page_config(page_title="RegLess")
    st.header("ダッシュボード")

    # ユーザー名入力
    username = st.text_input("ユーザー名", "")
    
    # セッション状態を初期化
    if "dashboard_shown" not in st.session_state:
        st.session_state.dashboard_shown = False

    # 「ダッシュボードを表示」ボタンが押されたら状態を更新
    if st.button("ダッシュボードを表示"):
        st.session_state.dashboard_shown = True

    # ダッシュボードが表示されている状態なら、内容を表示
    if st.session_state.dashboard_shown:
        user_data = get_user_by_username(username)
        if user_data is None:
            st.error("ユーザーが見つかりません。")
            return
        
        user_id = user_data["id"]
        st.write(f"ユーザー名: {user_data['username']}")
        wants_list = get_wants_by_user(user_id)

        if not wants_list:
            st.info("まだやりたいことが登録されていません。")
        else:
            st.subheader("やりたいこと一覧")
            total_wants = len(wants_list)
            completed_count = 0

            for want in wants_list:
                want_id = want["id"]
                title = want["title"]
                cost = want["cost"]
                period = want["period"]
                first_step = want["first_step"]
                tag = want["tag"]
                deadline = want["deadline"]
                is_completed = want["is_completed"]

                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{title}**")
                    st.write(f"期限: {deadline}")
                    st.write(f"費用：{cost}万円")
                    st.write(f"期間：{period}")
                    st.write(f"1stステップ：{first_step}")
                    st.write(f"タグ: {tag}")
                if st.button("編集", key=f"edit_{want_id}"):
                    st.session_state[f"edit_mode_{want_id}"] = True

                if st.session_state.get(f"edit_mode_{want_id}", False):
                    new_title = st.text_input("タイトル", value=title, key=f"new_title_{want_id}")
                    new_cost = st.text_input("費用", value=cost, key=f"new_cost_{want_id}")
                    new_period = st.text_input("期間", value=period, key=f"new_period_{want_id}")
                    new_first_step = st.text_area("1stステップ", value=first_step, key=f"new_step_{want_id}")
                    new_tag = st.text_input("タグ", value=tag, key=f"new_tag_{want_id}")

                    if st.button("保存する", key=f"save_{want_id}"):
                        from db import update_want  # 🔁 忘れずにインポートしておく

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
                            st.success("やりたいことを更新しました")
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
                    else:
                        st.write("完了済み")

                if is_completed:
                    completed_count += 1

            # 全体進捗
            st.subheader("全体進捗")
            completion_ratio = completed_count / total_wants
            st.write(f"完了率: {completion_ratio * 100:.1f}%")
            
            # ユーザーの残り寿命（カラム順に依存）
            estimated_lifespan = user_data["estimated_lifespan"]
            st.write(f"推定残り寿命: {estimated_lifespan}年")

if __name__ == "__main__":
    app()
