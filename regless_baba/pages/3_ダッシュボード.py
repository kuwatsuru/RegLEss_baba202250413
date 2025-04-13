import streamlit as st
from db import get_user_by_username, get_wants_by_user, complete_want

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
        
        user_id = user_data[0]
        wants_list = get_wants_by_user(user_id)

        if not wants_list:
            st.info("まだやりたいことが登録されていません。")
        else:
            st.subheader("やりたいこと一覧")
            total_wants = len(wants_list)
            completed_count = 0

            for want in wants_list:
                want_id = want[0]
                user_id_fk = want[1]
                title = want[2]
                cost = want[3]
                period = want[4]
                first_step = want[5]
                tag = want[6]
                deadline = want[7]
                is_completed = want[8]

                # 完了ボタンを含むレイアウト
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{title}**")
                    st.write(f"期限: {deadline}")
                    st.write(f"費用：{cost}円")
                    st.write(f"期間：{period}")
                    st.write(f"1stステップ：{first_step}")
                    st.write(f"タグ: {tag}")
                with col2:
                    st.progress(1.0 if is_completed else 0.0)
                with col3:
                    if not is_completed:
                        if st.button("完了", key=f"complete_{want_id}"):
                            complete_want(want_id)
                            st.success(f"{title}完了にしますか？")
                    else:
                        st.write("完了済み")

                if is_completed:
                    completed_count += 1

            # 全体進捗
            st.subheader("全体進捗")
            completion_ratio = completed_count / total_wants
            st.write(f"完了率: {completion_ratio * 100:.1f}%")
            
            # ユーザーの残り寿命（カラム順に依存）
            estimated_lifespan = user_data[8]
            st.write(f"推定残り寿命: {estimated_lifespan}年")

if __name__ == "__main__":
    app()
