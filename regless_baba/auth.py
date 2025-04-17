from db import supabase


def signup(email, password, username, birthdate, smoking, drinking, exercise, body_shape, estimated_lifespan):
    """
    ユーザー登録（サインアップ）機能
    """
    try:
        #Supabaseの認証を使ってユーザー作成
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        #認証成功したら、ユーザープロフィール作成
        if auth_response.user:
            user_id = auth_response.user.id
            #さらにusersテーブルに追加情報を保存
            user_data = {
                "id": user_id,  # Supabaseの認証IDと同じIDを使用
                "username": username,
                "birthdate": birthdate,
                "smoking": smoking,
                "drinking": drinking,
                "exercise": exercise,
                "body_shape": body_shape,
                "estimated_lifespan": estimated_lifespan
            }
            supabase.table('users').insert(user_data).execute()
            #登録成功の場合メッセージ表示
            return True, "ユーザー登録が完了しました"
        return False, "ユーザー登録に失敗しました"
    except Exception as e:
        return False, f"エラー：{str(e)}"


def login(email, password):
    """
    ログイン機能
    """
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # ユーザー情報を取得
            user_id = auth_response.user.id
            user_data = supabase.table('users').select('*').eq('id', user_id).execute()
            
            return True, user_data.data[0] if user_data.data else None
        return False, "ログインに失敗しました"
    
    except Exception as e:
        return False, f"エラー: {str(e)}"


def logout():
    """
    ログアウト機能
    """
    try:
        supabase.auth.sign_out()
        return True, "ログアウトしました"
    except Exception as e:
        return False, f"エラー: {str(e)}"
    

def get_current_user(): #解説いるやろこれ
    """
    現在ログイン中のユーザー情報を取得
    """
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            user_id = user.user.id
            user_data = supabase.table('users').select('*').eq('id', user_id).execute()
            return user_data.data[0] if user_data.data else None
        return None
    except:
        return None



