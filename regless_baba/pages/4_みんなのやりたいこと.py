import streamlit as st
from db import get_wants_by_tag, get_all_wants, add_like, get_likes_count
from auth import get_current_user  # ログイン済みのユーザー取得

def app():
    st.set_page_config(page_title="RegLess")
    st.header("コミュニティ機能 - タグ検索")
    
    current_user = get_current_user()
    if current_user is None:
        st.warning("ログインしてください。")
        return

    user_id = current_user["id"]  # ← UUIDとして取得できる
    username = current_user["username"]  # ユーザー名を取得
    st.write(f"こんにちは、{username}さん")
    st.write("他のユーザーが登録したやりたいことを検索してみましょう。")
    
    # 検索キーワードをセッション状態に保存
    if "search_tag" not in st.session_state:
        st.session_state.search_tag = ""
    if "search_result" not in st.session_state:
        st.session_state.search_result = None

    search_tag = st.text_input("検索したいタグを入力（例：旅行、勉強など）", st.session_state.search_tag)

    # ボタンを横並びに配置
    col1, col2 = st.columns(2)
    
    # タグ検索ボタン
    with col1:
        if st.button("検索"):
            st.session_state.search_tag = search_tag
            if search_tag.strip():
                result = get_wants_by_tag(search_tag.strip())
                st.session_state.search_result = result
                if not result:
                    st.info("該当するやりたいことは見つかりませんでした。")
            else:
                st.warning("タグを入力してください。")
    
    # 全件表示ボタン
    with col2:
        if st.button("全てのデータを表示"):
            result = get_all_wants()  # データベース内の全データを取得する関数
            st.session_state.search_result = result
            st.session_state.search_tag = ""
            if not result:
                st.info("データが見つかりませんでした。")

    # 検索結果または全件結果の表示
    if st.session_state.search_result:
        for want in st.session_state.search_result:
            want_id = want["id"]
            title = want["title"]
            tag = want["tag"]
            deadline = want["deadline"]
            # ここで必要な情報を取得
            # 例: cost, period, first_step など
            st.write(f"**{title}** (タグ: {tag}, 締切: {deadline})")
            like_count = get_likes_count(want_id)
            st.write(f"Like数: {like_count}")

            # Like ボタン（ユーザーIDは固定値: 1 を使用）
            if st.button(f"Like !", key=f"like_{want_id}"):
                add_like(user_id, want_id)
                st.success("Likeを付けました")
                # Like後に表示内容を再取得して更新
                # ※フィルタ条件がタグ検索の場合はそのまま、全件の場合も条件が空になるので問題ありません
                if st.session_state.search_tag:
                    st.session_state.search_result = get_wants_by_tag(st.session_state.search_tag)
                else:
                    st.session_state.search_result = get_all_wants()

if __name__ == "__main__":
    app()
