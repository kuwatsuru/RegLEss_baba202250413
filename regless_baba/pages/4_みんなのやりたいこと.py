import streamlit as st
from db import get_wants_by_tag, get_all_wants, add_like, get_likes_count, has_liked, remove_like
from auth import get_current_user  # ログイン済みのユーザー取得

def app():
    st.set_page_config(page_title="RegLess")
    st.header("コミュニティ機能 - タグ検索")
    # 1. 認証 --------------------------------------------------------------    
    current_user = get_current_user()
    if current_user is None:
        st.warning("Homeからログインしてください。")
        return

    user_id = current_user["id"]  # ← UUIDとして取得できる
    username = current_user["username"]  # ユーザー名を取得
    st.write(f"こんにちは、{username}さん")
    st.write("他のユーザーのやりたいことを検索してみましょう。")
    
    # 2. セッション状態の初期化 --------------------------------------------
    defaults = {
        "search_input": "",   # テキスト入力値（ウィジェットと同じ key）
        "search_mode": "none",# none / tag / all
        "search_result": None,
        "_clear_next": False,  # 1 ラン後に入力欄をクリアするフラグ
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # 2‑B. 直前に押されたボタンで「次回レンダリング時に入力欄をクリア」
    if st.session_state["_clear_next"]:
        st.session_state["search_input"] = ""
        st.session_state["_clear_next"]  = False

    # 3. 入力 UI -----------------------------------------------------------
    st.markdown("---")
    st.subheader("🔍 タグ検索")

    # NOTE: text_input の value は session_state["search_input"] にひもづく
    st.text_input(
        "検索したいタグを入力（例：旅行、勉強など）",
        key="search_input",
    )

    col_search, col_all, col_clear = st.columns([1, 2, 1])

    # 3‑A. 検索ボタン ------------------------------------------------------
    with col_search:
        if st.button("検索", key="btn_search"):
            tag = st.session_state["search_input"].strip()
            if tag:
                st.session_state["search_mode"]   = "tag"
                st.session_state["search_result"] = get_wants_by_tag(tag)
            else:
                st.session_state["search_result"] = None
                st.warning("タグを入力してください。")
            st.rerun()

    # 3‑B. 全件表示ボタン --------------------------------------------------
    with col_all:
        if st.button("全てのデータを表示", key="btn_show_all"):
            st.session_state["search_mode"]   = "all"
            st.session_state["search_result"] = get_all_wants()
            # 次回ランで入力欄を空にする
            st.session_state["_clear_next"]  = True
            st.rerun()

    # 3‑C. クリアボタン ----------------------------------------------------
    with col_clear:
        if st.button("クリア", key="btn_clear"):
            for k in ("search_mode", "search_result"):
                st.session_state[k] = defaults[k]
            st.session_state["_clear_next"] = True
            st.rerun()

    st.markdown("---")

    # 4. 結果表示 ----------------------------------------------------------
    results = st.session_state["search_result"]
    mode    = st.session_state["search_mode"]

    if mode == "tag":
        tag = st.session_state["search_input"].strip() or "(不明)"
        st.subheader(f"🎯 タグ『{tag}』の検索結果 ({len(results) if results else 0} 件)")
    elif mode == "all":
        st.subheader(f"📚 全データ一覧 ({len(results) if results else 0} 件)")
    else:
        st.info("タグを入力して検索、または『全てのデータを表示』を押してください。")
        st.stop()

    if results is None:
        st.info("検索結果が空です。タグを変更して再検索してみてください。")
        st.stop()

    if not results:
        st.info("該当するやりたいことは見つかりませんでした。")
        st.stop()

    # 5. カード表示 --------------------------------------------------------
    for want in results:
        want_id  = want["id"]
        like_ct  = get_likes_count(want_id) or 0

        with st.container():
            st.markdown(
                """
                <div style='border:1px solid #e1e4e8;padding:12px;border-radius:10px;margin-bottom:10px;'>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"### {want['title']}")
            st.write(f" **タグ**: {want['tag']}  |   **締切**: {want['deadline']}")
            st.write(f"👍 Like！: {like_ct}")

            # Like ボタン / ラベル
            if has_liked(user_id, want_id):
                st.button("👍 Liked", key=f"liked_{want_id}", disabled=True)
            else:
                if st.button("Like !", key=f"like_{want_id}"):
                    add_like(user_id, want_id)
                    # 最新結果を再取得して即反映
                    if mode == "tag":
                        current_tag = st.session_state["search_input"].strip()
                        st.session_state["search_result"] = get_wants_by_tag(current_tag)
                    else:
                        st.session_state["search_result"] = get_all_wants()
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
