import streamlit as st
from db import get_wants_by_tag, add_like, get_likes_count

def app():
    st.set_page_config(page_title="RegLess")
    st.header("コミュニティ機能 - タグ検索")

    # 検索キーワードをセッション状態に保存
    if "search_tag" not in st.session_state:
        st.session_state.search_tag = ""
    if "search_result" not in st.session_state:
        st.session_state.search_result = None

    search_tag = st.text_input("検索したいタグを入力（例：旅行、勉強など）", st.session_state.search_tag)
    if st.button("検索"):
        st.session_state.search_tag = search_tag
        if search_tag.strip():
            result = get_wants_by_tag(search_tag.strip())
            st.session_state.search_result = result
            if not result:
                st.info("該当するやりたいことは見つかりませんでした。")
        else:
            st.warning("タグを入力してください。")

    # 検索結果の表示（セッション状態に検索結果がある場合）
    if st.session_state.search_result:
        for want in st.session_state.search_result:
            want_id = want[0]
            title = want[2]
            tag = want[6]
            deadline = want[7]
            st.write(f"**{title}** (タグ: {tag}, 締切: {deadline})")
            like_count = get_likes_count(want_id)
            st.write(f"Like数: {like_count}")

            # Like ボタン
            if st.button(f"Like !", key=f"like_{want_id}"):
                # 実際にはログインユーザーのidを使うべきですが、今回は固定値で
                add_like(1, want_id)
                st.success("Likeを付けますか？")
                # Like後に再度結果を更新する例：
                st.session_state.search_result = get_wants_by_tag(st.session_state.search_tag)

if __name__ == "__main__":
    app()
