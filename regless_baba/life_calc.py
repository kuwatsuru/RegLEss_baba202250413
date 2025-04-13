import datetime

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
    #    ここでは単純なポイント方式で寿命を加減してみる
    life_points = 84  # 日本人の平均寿命
    if smoking == "ほぼ毎日":
        life_points -= 5
    elif smoking == "たまに":
        life_points -= 2

    if drinking == "ほぼ毎日":
        life_points -= 3
    elif drinking == "たまに":
        life_points -= 1

    if exercise == "定期的にする":
        life_points += 3
    elif exercise == "不定期":
        life_points += 1

    if body_shape == "肥満":
        life_points -= 3
    elif body_shape == "やせ型":
        life_points -= 1

    # 3. 実際の年齢を引いて残り寿命をざっくり計算
    remaining = life_points - age

    return max(remaining, 0)  # 0を下回らないようにする

#寿命計算は　マイナスではなく0.95×とかでもいいかも。