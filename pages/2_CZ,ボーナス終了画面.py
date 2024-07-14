import streamlit as st
import pandas as pd
from Top import columns_bonus_pic, index_bonus_pic, path_bonus_pic
from CsvDfClass import CsvDf
from PIL import Image

##### ページの内容 #####
# CZ,ボーナス終了画面のメモ

########################################
##### マイナス、1行削除のための変数・関数定義
########################################

#マイナス、1行削除のチェック状態用の変数
if "minus_check" not in st.session_state:
    st.session_state["minus_check"] = False
    minus_check = st.session_state["minus_check"]

def toggle_minus_check():
    st.session_state["minus_check"] = not st.session_state["minus_check"]

#ボタンの表示文字列の設定
if st.session_state["minus_check"]:
    button_str = "1行削除"
    button_type = "primary"
else:
    button_str = "登録"
    button_type = "secondary"


#############################
##### csvデータを読み込み
#############################
df = CsvDf(columns=columns_bonus_pic,
           index=index_bonus_pic,
           path=path_bonus_pic)
# st.write(df.df)


#################################
##### ボーナス後画面のカウント
#################################
st.subheader("CZ,ボーナス終了画面")
st.caption("・CZ,ボーナス終了画面で示唆を確認")
st.caption("・ベットボタンで飛ばさないよう注意")

#画面の選択肢をセッション管理するための変数設定
if "pic_select" not in st.session_state:
    st.session_state.pic_select = ""

#セレクトボックスを作成
st.session_state.pic_select = st.selectbox("終了画面", df.columns_list)

#選択肢に合わせて画像を表示
im_path = f"./image/bonus_image_{st.session_state.pic_select}.jpg"
im = Image.open(im_path)
st.image(im, width=300)

#登録ボタン
submit_btn = st.button(button_str, type=button_type)

#カウント処理
if submit_btn:
    df.SelectedCount(selected=st.session_state.pic_select,
                  minus_check=st.session_state["minus_check"])
# st.dataframe(df.df)

#結果の表示
remarks_list = ["デフォルト", "奇数示唆", "偶数示唆", "高設定示唆 弱", "高設定示唆 強", "設定2以上", "設定4以上", "設定6"]
df.CountAndProbabilityResultShow(remarks_list=remarks_list)


##################################
##### 解析情報の表示 #########
##################################
st.caption("解析値")

#解析値データフレームの作成
columns_list_theoretical = df.columns_list
index_list_theoretical = ["設定1", "設定2", "設定3", "設定4", "設定5", "設定6"]
data_list_theoretical = [["79%","10%","8%","2%", "1%", "-", "-", "-"],
                         ["77%","8%","10%","2%", "1%", "-", "-", "-"],
                         ["75%","10%","7%","4%", "2%", "2%", "-", "-"],
                         ["75%","5%","10%","4%", "2%", "2%", "2%", "-"],
                         ["75%","10%","5%","4%", "2%", "2%", "2%", "-"],
                         ["74%","5%","10%","4%", "3%", "2%", "1%", "1%"]]
df_theoretical = pd.DataFrame(data_list_theoretical, index=index_list_theoretical, columns=columns_list_theoretical)

#解析値の表示
st.dataframe(df_theoretical)


##### マイナスのチェックボックス表示
st.checkbox("マイナスカウント、1行削除", value=st.session_state["minus_check"], on_change=toggle_minus_check)