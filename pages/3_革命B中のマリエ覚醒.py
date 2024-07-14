import streamlit as st
import pandas as pd
from Top import columns_marie, index_marie, path_marie, columns_cz, index_cz, path_cz
from CsvDfClass import CsvDf

##### ページの内容 #####
# 革命ボーナス中のマリエ覚醒の回数をカウント
# 革命ボーナスの回数は別ページで記録した結果を引用


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
    button_str = "マイナス"
    button_type = "primary"
else:
    button_str = "カウント"
    button_type = "secondary"


#############################
##### csvデータを読み込み
#############################
#マリエ覚醒回数のcsvを読み込み
df = CsvDf(columns=columns_marie, index=index_marie, path=path_marie)

#CZ、ボーナス履歴のcsvを読み込み
bonus_df = CsvDf(columns=columns_cz, index=index_cz, path=path_cz)


##############################
##### マリエ覚醒の回数をカウント
##############################
st.subheader("マリエ覚醒の発生率")
st.caption("・革命ボーナス当選時に確定するマリエ覚醒の確率に設定差あり")
st.caption("・HOLDが一度も発生せずに出てきたマリエ覚醒が対象")
st.caption("(通常は最低保証で1回はHOLDが出る。内部的にマリエ覚醒確定時のみ最低保証が出ない)")

#マリエ覚醒の回数カウント
with st.form(key="marie_count"):

    #2列に画面分割
    col1, col2 = st.columns(2)

    ##### 左画面
    with col1:
        st.caption("マリエ覚醒回数カウント")

        #カウントボタン
        marie_count_btn = st.form_submit_button(button_str,type=button_type)

        #カウント処理
        if marie_count_btn:
            df.SelectedCount(selected=columns_marie[0],minus_check=st.session_state["minus_check"])

    ##### 右画面
    with col2:
        #現在回数の表示
        st.caption("マリエ覚醒回数")
        st.info(df.df.at[df.df.index[0], df.df.columns[0]])

#############################################
##### 当選確率の算出と表示 ####################
#############################################

#革命ボーナスの回数を取得
bonus_counts = bonus_df.df[bonus_df.columns_list[2]].value_counts()
kakumei_counts = bonus_counts.get("革命",0)
# st.write(kakumei_counts)

#2列に表示分割
col1, col2 = st.columns(2)

#####左画面
with col1:
    #マリエ覚醒の確率を算出
    marie_ratio = df.df.at[df.df.index[0], df.df.columns[0]] / kakumei_counts

    #算出結果の表示
    st.caption("マリエ覚醒発生率")
    st.info(f"{marie_ratio*100:.1f}%")

#####右画面
with col2:
    st.caption("解析値")

    #解析値のデータフレーム作成
    columns_list_theoretical = ["マリエ覚醒発生率"]
    index_list_theoretical = ["設定1", "設定2", "設定3", "設定4", "設定5", "設定6"]
    data_list_theoretical = [["5%"],
                            ["6%"],
                            ["7%"],
                            ["9%"],
                            ["10%"],
                            ["13%"]]
    df_theoretical = pd.DataFrame(data_list_theoretical, index=index_list_theoretical, columns=columns_list_theoretical)

    #データフレームの表示
    st.dataframe(df_theoretical)


##### マイナスのチェックボックス表示
st.checkbox("マイナスカウント、1行削除", value=st.session_state["minus_check"], on_change=toggle_minus_check)