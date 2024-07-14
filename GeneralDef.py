import os
from datetime import datetime, timedelta

def TodayUseCheck(folder_path="./pages/"):
    """csvの最終更新日を確認し、本日内に更新あるかを
    チェックし結果を返す
    
    Parameter
    -------------------------------
    folder_path:文字列、csvファイルが保存されているフォルダの相対パス
    """

    #フォルダ内の全ファイルリストを取得
    files = os.listdir(folder_path)

    #csvファイルのみを対象にしたリストを作る
    csv_files = [file for file in files if file.endswith(".csv")]

    # 最も最近の更新日時を保存する変数を初期化
    most_recent_date = None

    #最も最近の更新日時を取得する
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)

        #最終更新日時を取得
        mtime = os.path.getmtime(file_path)

        #人間が読める形式に変換
        last_modified_date = datetime.fromtimestamp(mtime)

        #9時間を加算して日本時間に変換
        last_modified_date = last_modified_date + timedelta(hours=9)
        # st.write(last_modified_date)

        #更新日時が最も最近だったら変数に入れる
        if most_recent_date is None or last_modified_date > most_recent_date:
            most_recent_date = last_modified_date
        
    #現在日時を取得
    today = datetime.now()

    #9時間を加算して日本時間に変換
    today = today + timedelta(hours=9)

    #本日の日付を取得
    today = today.date()

    #最新更新日が本日と同じなら「本日使用中」、違えば「本日未使用」を表示
    if most_recent_date is not None and most_recent_date.date() == today:
        return True
    else:
        return False