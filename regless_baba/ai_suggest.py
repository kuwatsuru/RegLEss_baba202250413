import openai
import os
from dotenv import load_dotenv
import streamlit as st
from utils import get_secret

# # デプロイ時はこっち
# # Dictionary形式でSecretsから取得
# api_key = st.secrets["openai"]["OPENAI_API_KEY"]
# if not api_key:
#     raise ValueError("OPENAI_API_KEY が設定されていません。")

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
        - 費用（例：5万円）
        - 期間（例：3ヶ月）
        - 最初のステップ（例：まずは本を買って基礎を学ぶ/学校に通う）

        出力は次の形式でお願いします：

        費用: ○○
        期間: △△
        最初のステップ: □□ / xx /・・・
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
