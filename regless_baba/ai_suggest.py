import openai
import os
from dotenv import load_dotenv
import streamlit as st
from utils import get_secret
from db import get_all_wants
from auth import get_current_user


# APIキーを環境（st.secrets or .env）から一元取得
api_key = get_secret("openai", "api_key")
if not api_key:
    raise ValueError("OPENAI_API_KEY が設定されていません。")

# OpenAI クライアントを生成
client = openai.OpenAI(api_key=api_key)


def suggest_ideas(want_title):
    """
    want_title（やりたいことの名称）に対してAIサジェストする例。
    
    """
    try:
        prompt = f"""
        私は「{want_title}」を実現したいと考えています。
        以下の3項目を日本語で簡潔に出力してください：
        - 費用（int形式、単位は万円）
        - 期間（例：3ヶ月）
        - 最初のステップ（例：まずは本を買って基礎を学ぶ/学校に通う）
        - タグ（例：旅行,趣味,勉強,夢,仕事など）

        出力は次の形式でお願いします：
        費用:〇〇万円
        期間: △△
        最初のステップ: □□ / xx /
        タグ:タグ1, タグ2
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはユーザーのやりたいことを具体的に分析するアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        # レスポンスから文章部分を抽出
        suggestion_text = response.choices[0].message.content.strip()
        return suggestion_text
    except Exception as e:
        return f"APIエラーが発生しました: {e}"


#wantsリストの中身をRAGとして渡したうえでサジェストさせる
def suggest_ideas_with_all_users_rag(want_title):
    """
    全ユーザーの「やりたいこと」情報をRAGとして渡してサジェストを生成する
    """
    try:
        # 全ユーザーの「やりたいこと」リストを取得
        all_wants = get_all_wants()
        
        # 過去のやりたいことリストをプロンプトに組み込む
        all_wants_text = "\n".join([f"ユーザーID: {want['user_id']}, タイトル: {want['title']}, 費用: {want['cost']}, 期間: {want['period']}" for want in all_wants])

        prompt = f"""
        参考情報として、他のユーザーの関連するやりたいことの事例を以下に示します：
        {all_wants_text}
        ---参考情報終わり---（もし参考情報がない場合や関連性が低い場合は、上記の参考事例セクションは無視してください）
        新しく「{want_title}」を実現したいと考えています。
        上記の参考情報や一般的な知識を考慮して、「{want_title}」を実現するための以下の3項目を日本語で簡潔に出力してください。参考事例と全く同じにする必要はなく、あくまでアイデアや相場感の参考にしてください。
        - 費用 〇〇万円※1万円未満の場合1
        - 期間（例：3ヶ月）
        - 最初のステップ（例：まずは本を買って基礎を学ぶ/学校に通う）
        - タグ（例：旅行,趣味,勉強,夢,仕事など）

        出力は次の形式でお願いします：
        費用:〇〇万円
        期間: △△
        最初のステップ: □□ / xx /
        タグ:タグ1, タグ2
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはユーザーのやりたいことを具体的に分析するアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        # レスポンスから文章部分を抽出
        suggestion_text = response.choices[0].message.content.strip()
        return suggestion_text
    except Exception as e:
        return f"APIエラーが発生しました: {e}"
