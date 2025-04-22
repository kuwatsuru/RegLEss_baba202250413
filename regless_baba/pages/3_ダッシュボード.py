import streamlit as st
from db import get_user_by_username, get_wants_by_user, complete_want, update_want, insert_want, get_likes_count
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

    # ─── 1-2. 寿命表示 ───
    estimated_lifespan = current_user.get("estimated_lifespan")
    if estimated_lifespan is not None:
        st.metric("推定残り寿命", f"{estimated_lifespan} 年")

    st.markdown("---")


    # ─── 2. 登録済みリストの取得と表示 ───
    st.header("あなたのやりたいこと一覧")
    wants_list = get_wants_by_user(user_id)
    if not wants_list:
        st.info("まだやりたいことが登録されていません。")
        return

    total_wants = len(wants_list)

    # CSS: simple card style ----------------------------------------------------
    st.markdown(
        """
        <style>
        .want-card {
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 0.5rem 1.2rem;
            margin-bottom: 0.2rem;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }
        .want-like {
            padding: 2px 8px;
            border-radius: 8px;
            font-weight: 700;
            margin-left: .3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    #CSS終わり----------------------


    completed_count = 0

    #Like数取得
    for want in wants_list:
        want_id      = want["id"]
        like_count   = get_likes_count(want_id) or 0  # Like 数を取得    

        # ------------------------------------------------------------------ card
        with st.container():
            st.markdown("<div class='want-card'>", unsafe_allow_html=True)

            # ── 3‑A. タイトル行 & Like 数
            head_l, head_r = st.columns([6, 1])
            with head_l:
                st.markdown(f"### {want['title']}")
            with head_r:
                st.write(" ")
                st.markdown(f"👍 <span class='want-like'>{like_count}</span>", unsafe_allow_html=True)

            # ── 3‑B. 詳細情報
            info1, info2, action_col = st.columns([3, 3, 2])
            with info1:
                st.write(f"📅 **期限**: {want['deadline']}")
                st.write(f"💰 **費用**: {want['cost']} 万円")
                st.write(f"🏷️ **タグ**: {want['tag']}")
            with info2:
                st.write(f"⏱️ **期間**: {want['period']}")
                st.write(f"🚀 **アクション**: {want['first_step']}")
            with action_col:
                st.progress(1.0 if want["is_completed"] else 0.0)
                if want["is_completed"]:
                    st.success("達成済み")
                else:
                    if st.button("完了", key=f"complete_{want_id}"):
                        complete_want(want_id)
                        st.rerun()

                # 編集モード切替ボタン
                if st.button("編集", key=f"edit_{want_id}"):
                    st.session_state[f"edit_mode_{want_id}"] = True

            # ── 3‑C. 編集フォーム
            if st.session_state.get(f"edit_mode_{want_id}", False):
                with st.form(f"form_{want_id}"):
                    new_title       = st.text_input("タイトル", value=want["title"])
                    new_cost        = st.number_input("費用 (万円)", value=float(want["cost"]), step=1.0)
                    new_period      = st.text_input("期間", value=want["period"])
                    new_first_step  = st.text_area("アクション", value=want["first_step"])
                    new_tag         = st.text_input("タグ", value=want["tag"])

                    if st.form_submit_button("保存する"):
                        update_want(
                            want_id=want_id,
                            updates={
                                "title": new_title,
                                "cost": new_cost,
                                "period": new_period,
                                "first_step": new_first_step,
                                "tag": new_tag,
                            },
                        )
                        st.success("更新しました！")
                        st.session_state[f"edit_mode_{want_id}"] = False
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            # 完了数カウント
            if want["is_completed"]:
                completed_count += 1

    # ─── 4. 全体進捗表示 ───

    total_wants = len(wants_list)
    if total_wants:
        completion_ratio = completed_count / total_wants
        st.markdown("---")
        st.progress(completion_ratio)
        st.metric("完了率", f"{completion_ratio * 100:.1f}%")



if __name__ == "__main__":
    app()
