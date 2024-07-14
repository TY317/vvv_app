import streamlit as st
import pandas as pd
from GeneralDef import TodayUseCheck

st.title("革命機ヴァルヴレイヴ")

################################################
##### データフレームの定義 #######################
################################################

# CZ初当り用
columns_cz = ["液晶ゲーム数ゾーン", "CZキャラ", "ボーナス"]
index_cz = []
data_cz = []
path_cz = "./pages/cz_df.csv"

#CZ、ボーナス終了画面用
columns_bonus_pic = ["白(2人)","白(3人)","白(4人)","紫(男性集合)","紫(水着)","赤(ドルシア軍5人)","赤(ドルシア軍6人)","金(パイロット)"]
index_bonus_pic = ["出現回数"]
data_bonus_pic = [[0,0,0,0,0,0,0,0]]
path_bonus_pic = "./pages/bonus_pic_count_df.csv"

#ハラキリドライブのカウント用
columns_drive = ["10G","20G","ドライブ","1400枚越え10G","1400枚越え20G","1400枚越えドライブ"]
index_drive = ["出現回数"]
data_drive = [[0,0,0,0,0,0]]
path_drive = "./pages/drive_count_df.csv"

#マリエ覚醒のカウント用
columns_marie = ["マリエ覚醒"]
index_marie = ["出現回数"]
data_marie = [[0]]
path_marie = "./pages/marie_count_df.csv"

##################################################
##### 新規作成ボタンを押すとデータをすべてリセットする
##################################################

#フォームの作成
with st.form(key='new_play'):

    #説明書き
    st.caption("※ 新規作成ボタンを押すとデータがすべて0リセットされます!")
    st.caption("※ 同時に他の人が利用しているとその人のデータも0リセットされます!恨みっこなしです!")
    st.caption("※ データの最終更新が本日だと「本日使用中」表示になります")

    #データの最終更新日が本日かをチェック
    today_use_check_result = TodayUseCheck()
    # st.write(today_use_check_result)

    #チェック結果に応じて表示
    if today_use_check_result:
        st.markdown(":red-background[本日使用中]")
    else:
        st.markdown(":green-background[本日未使用]")

    #新規作成ボタンの設定
    start_btn = st.form_submit_button("新規作成")

    #ボタンが押されたらcsvファイルをリセットし保存
    if start_btn:

        #########################################
        ##### csvファイルの作成 ##################
        #########################################

        ##### CZ初当り用
        cz_df = pd.DataFrame(data_cz,
                                             index=index_cz,
                                             columns=columns_cz)
        cz_df.to_csv(path_cz)
        # st.dataframe(cz_df)

        ##### CZ、ボーナス終了画面用
        bonus_pic_df = pd.DataFrame(data_bonus_pic,
                                             index=index_bonus_pic,
                                             columns=columns_bonus_pic)
        bonus_pic_df.to_csv(path_bonus_pic)
        # st.dataframe(bonus_pic_df)

        #####ハラキリドライブのカウント用
        drive_df = pd.DataFrame(data_drive,
                                             index=index_drive,
                                             columns=columns_drive)
        drive_df.to_csv(path_drive)
        # st.dataframe(drive_df)

        #####マリエ覚醒のカウント用
        marie_df = pd.DataFrame(data_marie,
                                             index=index_marie,
                                             columns=columns_marie)
        marie_df.to_csv(path_marie)


########################################
##### バージョン情報 ####################
########################################
st.caption("ver2.1.0")
st.caption("   ・マリエ覚醒のページを追加")
st.caption("   ・ドライブ確率の参考情報を追記")
st.caption("   ・ミミズの情報を追記")
st.caption("ver2.0.0")
st.caption("   ・新規作成")