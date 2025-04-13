import openai
import os
from dotenv import load_dotenv
import streamlit as st


# Dictionary形式でSecretsから取得
api_key = st.secrets["openai"]["OPENAI_API_KEY"]
if not api_key:
    raise ValueError("OPENAI_API_KEY が設定されていません。")
client = openai.OpenAI(api_key=api_key)


# from openai import OpenAI # openAIのchatGPTのAIを活用するための機能をインポート
# import os
# from dotenv import load_dotenv  # pip install python-dotenv

# # .env を読み込む
# load_dotenv()

# # 環境変数から OpenAI API キーを取得
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("OPENAI_API_KEY が設定されていません。")

# # APIキーを明示的に渡して OpenAI クライアントを生成する
# client = OpenAI(api_key=api_key)



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
        最初のステップ: □□ / xx / ☆☆
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

        # ChatCompletion API のレスポンスから返答内容を取得
        suggestion_text = response.choices[0].message.content.strip()
        return suggestion_text
    except Exception as e:
        return f"APIエラーが発生しました: {e}"
