import os
from dotenv import load_dotenv
import streamlit as st
from supabase import create_client, Client

# ローカル起動時に .env を読み込む
load_dotenv()

# ローカル開発時は .env をロード
load_dotenv()

def get_secret(service: str, key: str) -> str:
    """
    1) Streamlit Cloud の st.secrets から
    2) 環境変数から（.env 経由でロード済み）
    の順に値を取得する。
    """
    # 1) Cloud Secrets
    try:
        return st.secrets[service][key]
    except:
        pass
    # 2) 環境変数
    env_key = f"{service.upper()}_{key.upper()}"
    val = os.getenv(env_key)
    if not val:
        raise RuntimeError(f"Secret not found: {service}.{key}")
    return val

@st.cache_resource

def get_supabase_client() -> Client:
    """
    Supabase クライアントを生成
    """
    url = get_secret("supabase", "url")
    anon_key = get_secret("supabase", "anon_key")
    return create_client(url, anon_key)


def require_login():
    """
    ログイン済みでなければエラー表示して停止
    各ページ冒頭で require_login() を呼び出す
    """
    if not st.session_state.get("logged_in", False):
        st.error("※ ログインしてください")
        st.stop()
