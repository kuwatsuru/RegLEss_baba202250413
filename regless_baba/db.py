import os
import streamlit as st
from supabase import create_client, Client
from utils import get_supabase_client


# Supabase クライアントを取得（キャッシュリソース）
supabase = get_supabase_client()

#データベースの操作に関わる関数を定義

def init_db():
    """
    アプリ起動時にDBを初期化する。
    接続確認用。
    """
    try:
        result = supabase.table("users").select("id").limit(1).execute()
        st.success("✅ Supabaseへの接続成功")
        return True
    except Exception as e:
        st.error(f"❌ Supabase接続エラー: {e}")
        return False

def insert_user(username, birthdate, smoking, drinking, exercise, body_shape, estimated_lifespan):
    """
    ユーザーをDBに登録する処理
    """
    try:
        data = {
            "username": username,
            "birthdate": birthdate,
            "smoking": smoking,
            "drinking": drinking,
            "exercise": exercise,
            "body_shape": body_shape,
            "estimated_lifespan": estimated_lifespan
        }
        result = supabase.table("users").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"ユーザー登録エラー: {e}") 
        return None  


def get_user_by_username(username):
    """
    usernameでユーザーを検索し、そのユーザー情報を返す
    """
    try:
        result = supabase.table('users').select('*').eq('username', username).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.write(f"ユーザー検索エラー: {e}")
        return None


def insert_want(user_id, title, cost, period, first_step, tag, deadline):
    """
    やりたいことをDBに登録する処理
    """
    try:
        data = {
            "user_id": user_id,
            "title": title,
            "cost": cost,
            "period": period,
            "first_step": first_step,
            "tag": tag,
            "deadline": deadline,
            "is_completed": False  # SupabaseではBoolを設定
        }
        result = supabase.table('wants').insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"やりたいこと登録エラー: {e}")
        return None


def get_wants_by_user(user_id):
    """
    ユーザーのやりたいことをすべて取得
    """
    try:
        result = supabase.table('wants').select('*').eq('user_id', user_id).execute()
        return result.data
    except Exception as e:
        print(f"やりたいこと取得エラー: {e}")
        return []


def complete_want(want_id):
    """
    やりたいことを完了状態に更新
    """
    try:
        result = supabase.table('wants').update({"is_completed": True}).eq('id', want_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"やりたいこと更新エラー: {e}")
        return None


def get_wants_by_tag(tag):
    """
    タグで検索してやりたいことリストを取得する
    """
    try:
        # Supabaseでは LIKE の代わりに ilike を使用
        result = supabase.table('wants').select('*').ilike('tag', f"%{tag}%").execute()
        return result.data
    except Exception as e:
        print(f"タグ検索エラー: {e}")
        return []


def add_like(user_id, want_id):
    """
    他人のやりたいことにLikeを追加
    """
    try:
        data = {
            "user_id": user_id,
            "want_id": want_id
        }
        result = supabase.table('likes').insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Like追加エラー: {e}")
        return None


def get_likes_count(want_id):
    """
    指定のやりたいことに対するLike数を取得
    """
    try:
        result = supabase.table('likes').select('*', count='exact').eq('want_id', want_id).execute()
        return result.count
    except Exception as e:
        print(f"Like数取得エラー: {e}")
        return 0


def get_all_wants():
    """
    全てのやりたいことを取得
    """
    try:
        result = supabase.table('wants').select('*').execute()
        return result.data
    except Exception as e:
        print(f"全やりたいこと取得エラー: {e}")
        return []


# －－－－－－－－追加－－－－－－－－
def has_liked(user_id: str, want_id: int) -> bool:
    """そのユーザーが既に like を付けているか"""
    resp = supabase.table("likes") \
        .select("id", count="exact") \
        .eq("want_id", want_id) \
        .eq("user_id", user_id) \
        .execute()
    return (resp.count or 0) > 0


def remove_like(user_id: str, want_id: int):
    """
    いいねを取り消し（削除）
    """
    return supabase.table("likes") \
        .delete() \
        .eq("user_id", user_id) \
        .eq("want_id", want_id) \
        .execute()