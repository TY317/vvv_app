import streamlit as st
import pandas as pd
from Top import columns_cz, index_cz, path_cz
from CsvDfClass import CsvDf

##### ページの内容 #####
# CZに当選した液晶ゲーム数ゾーンとキャラ、CZの結果（ボーナス種類）をメモ
# 上記から滞在モードを推測していく
# 革命と決戦の比率を算出

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
df = CsvDf(columns=columns_cz,
           index=index_cz,
           path=path_cz)
# st.write(df.columns)
# st.write(df.index)
# st.write(df.path)
# st.write(df.df)

#######################################
##### CZ初当りのデータメモ
#######################################
st.subheader("CZ当選ゾーンとキャラ、結果のメモ")
st.caption("・CZに当選した液晶ゲーム数のゾーンとCZキャラをメモ")
st.caption("・ゾーンから滞在モードを推測し良し悪し判断。考え方はページ後方を参照")
st.caption("・革命と決戦の比率を算出")

#選択肢のリストを変数として設定
zone_select_list = ["100未満", "100G台", "200G台", "300G台", "400G台", "500G台", "600G台", "700G台", "800G台", "900G台"]
character_select_list = ["キューマ", "ライゾウ", "サキ", "アキラ", "マリエ", "3人共闘"]
bonus_select_list = ["革命", "決戦", "はずれ"]

##### 初当りのデータを入力し、登録するフォーム
with st.form(key='cz_data_input'):
    st.caption("CZ当選データと結果の入力")

    #3列のカラムを作成
    col1, col2, col3 = st.columns(3)

    #当選ゾーンの入力
    with col1:
        zone_result = st.selectbox(df.columns_list[0], zone_select_list)
    
    #CZキャラの入力
    with col2:
        character_result = st.selectbox(df.columns_list[1], character_select_list)
    
    #ボーナス結果の入力
    with col3:
        bonus_result = st.selectbox(df.columns_list[2], bonus_select_list)

    #登録ボタン
    submit_btn = st.form_submit_button(button_str, type=button_type)

    ##### 結果を保存
    #選択された結果をまとめたリストを定義
    selected_list = [zone_result, character_result, bonus_result]

    #結果の保存処理
    if submit_btn:
        df.BonusHistrical(add_result=selected_list,
                        minus_check=st.session_state["minus_check"])

#####################################
##### 結果の表示
#####################################

##### 履歴データの表示
st.caption("CZ履歴データ")
st.dataframe(df.df)

##### 革命と決戦の比率結果
st.caption("革命・決戦 比率")

#2列に表示分割
col1, col2 = st.columns(2)

#比率算出結果の表示
with col1:
    st.caption("革命比率")
    #ボーナスカラムの中身全体をカウントする
    bonus_counts = df.df[df.columns_list[2]].value_counts()

    #革命と決戦の回数を取得する
    kakumei_counts = bonus_counts.get(bonus_select_list[0],0)
    kessen_counts = bonus_counts.get(bonus_select_list[1], 0)

    #革命の比率を算出して表示
    try:
        kakumei_ratio = kakumei_counts / (kakumei_counts + kessen_counts)
        st.info(f"{kakumei_ratio*100:.1f}%")
    except ZeroDivisionError:
        st.info("ボーナスなし")


#革命比率の参考情報を表示
with col2:
    st.caption("解析値(※実戦値)")

    #解析値のデータフレーム作成
    columns_list_theoretical = ["設定6"]
    index_list_theoretical = ["革命", "決戦"]
    data_list_theoretical = [["65%"],
                            ["35%"]]
    df_theoretical = pd.DataFrame(data_list_theoretical, index=index_list_theoretical, columns=columns_list_theoretical)

    #データフレームの表示
    st.dataframe(df_theoretical)


##### マイナスのチェックボックス表示
st.checkbox("マイナスカウント、1行削除", value=st.session_state["minus_check"], on_change=toggle_minus_check)


##################################
##### CZに関する噂のまとめ
##################################
st.subheader("モード・CZに関する噂まとめ")
st.caption("・基本白マスで前兆が発生したらモードA以外")
st.caption("・ただし、朝イチは前兆の状態がむちゃくちゃ")
st.caption("・朝イチのはまりはそれほど気にしなくてもいいが、やっぱり高設定は朝も早いことが多い")
st.caption("・モードはATか革命ボーナス引くまで変わらない")
st.caption("・モード移行に設定差があると言われている")
st.caption("・CZのキャラは基本設定差なし")
st.caption("　しかし、モードC,Dにいるときはいいキャラ出る説がある")
st.caption("　→いいキャラがでる → いいモードにいる可能性UP → モード移行がいい可能性UP → 高設定の期待UP")
