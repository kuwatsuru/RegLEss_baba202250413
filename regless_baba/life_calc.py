import datetime
import random

def calculate_remaining_life(birthdate, smoking, drinking, exercise, body_shape):
    """
    独自の指標に基づき残り寿命を計算します。
    あくまで参考情報となりますのでご留意ください。
    """

     # 現在の日付を取得
    today = datetime.date.today()
    
    # 生年月日から年齢を計算
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    # 2. 仮ロジック：生活習慣による加減
    #    アンケート内容に基づいて計算
    life_points = 84  # 日本人の平均寿命
    if smoking == "ほぼ毎日":
        life_points *= 0.90
    elif smoking == "たまに":
        life_points *= 0.96

    if drinking == "ほぼ毎日":
        life_points *= 0.94
    elif drinking == "たまに":
        life_points *= 0.98

    if exercise == "定期的にする":
        life_points *= 1.06
    elif exercise == "不定期":
        life_points *= 1.02

    if body_shape == "肥満":
        life_points *= 0.94
    elif body_shape == "やせ型":
        life_points *= 0.98

    # 3. 実際の年齢を引いて残り寿命をざっくり計算
    remaining = life_points - age

    return max(int(round(remaining)), 0)  # マイナスにならないように



def get_random_message(el):
    """
    残り寿命（年）を受け取り、ランダムにメッセージを返す関数
    """
    messages = [
        f"あなたはあと {int(el * 3)} 回美味しい食事が食べられます。",
        f"あと {el} 年で、どれだけの思い出を作れるでしょうか。",
        f"残りの時間で {el*10} 回映画館に行けます。",
        f"残り時間は約 {el} 年です。これからの計画を考えてみませんか？",
        f"あと {el} 年で、もっと多くの人に会えるでしょう。",
        f"{el} 年の間に、人生で何を達成したいですか？",
        f"あなたには残り {el} 年の冒険が待っています。",
        f"{el} 年後、もっと大切なことを見つけられるでしょう。",
        f"残り {el} 年で何冊の本を読めるか、考えてみてください。",
        f"あなたの残り時間で、どれだけの夢を追いかけられるでしょうか。",
        f"残り {el} 年で、行きたい場所はありますか？",
        f"あと {el} 年の中で最も大切にしたいものは何ですか？",
        f"あと {el} 年、これからもっと素晴らしいことが待っています。",
        f"残り {el} 年で、どんな人間になりたいですか？",
        f"残り {el} 年で、どんな体験をしてみたいですか？",
        f"あと {el} 年のうちにやりたいことをリストアップしてみましょう。",
        f"毎日を感謝と共に。あと {int(el) * 365} 回「ありがとう」と言う機会があります。もっとたくさん伝えましょう！",
        f"あなたの人生の残り {el} 年をどう過ごすかはあなた次第です。",
        f"あなたの寿命は {el} 年。だからこそ、今を大切にしましょう。"
        f"あなたはあと{int(el * 365)}回の日々を過ごせます。",
        f"あなたが楽しめる花金はあと{int(el * 50)}回です。",
        f"あなたはあと{int(el * 1)}回の誕生日を迎えます。",
        f"大切な人と過ごせる週末はあと {int(el) * 50} 回。時間を有効に使いましょう。",
        f"あと{int(el) * 365} 日、新しいことに挑戦するチャンスがあります。",        
        f"あと {el} 回、満開の桜を楽しめます。来年の春も待ち遠しいですね。",
        f"あと {el} 回、太陽が輝く夏を迎えられます。",
        f"あと {el} 回、ご自身の誕生日をお祝いできます。一つ一つの歳を大切に。",
        f"あと {el} 回、心温まるクリスマスを過ごせます。",
        f"色づく紅葉をあと {el} 回、楽しむことができます。",        

    ]

    


    return random.choice(messages)