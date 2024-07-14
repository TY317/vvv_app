import streamlit as st
import pandas as pd
from Top import columns_drive, index_drive, path_drive
from CsvDfClass import CsvDf

##### ページの内容 #####
# 上位ラッシュ中のドライブに関する回数をカウント
# 表記1400枚越えでドライブ確率切り替わるという噂あるので、分けてカウントできるようにする


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
df = CsvDf(columns=columns_drive,
           index=index_drive,
           path=path_drive)
# st.write(df.df)


##############################
##### 上位ラッシュの内容をカウント
##############################
st.subheader("超革命中のハラキリドライブ発生率")
st.caption("・超革命ラッシュのセットゲーム数をカウントし、ハラキリドライブ発生率を算出")
st.caption("・表記1400枚を超えるとドライブ確率が切り替わると言われているので、分けてカウントする機能を追加")
st.write("・設定6で1/4、設定1で1/10～15くらい")
##### 表記1400枚未満のカウント処理
with st.form(key="under1400_drive_count"):
    st.write("表記1400枚未満")

    #カウントボタン
    g10_count_btn = st.form_submit_button("10G",type=button_type)
    g20_count_btn = st.form_submit_button("20G",type=button_type)
    drive_count_btn = st.form_submit_button("ドライブ",type=button_type)

    #ボタンが押されたらカウント処理
    if g10_count_btn:
        df.SelectedCount(selected=df.columns_list[0], minus_check=st.session_state["minus_check"])
    
    elif g20_count_btn:
        df.SelectedCount(selected=df.columns_list[1], minus_check=st.session_state["minus_check"])
    
    elif drive_count_btn:
        df.SelectedCount(selected=df.columns_list[2], minus_check=st.session_state["minus_check"])
    
    #結果の表示
    #1400枚未満だけの表を作ってそれを表示
    df_under1400_result = df.df[[df.columns_list[0],df.columns_list[1], df.columns_list[2]]].copy()
    st.write(df_under1400_result)

    #####ドライブ確率の表示
    #全セット数を取得
    all_count = df_under1400_result.loc[df_under1400_result.index[0]].sum()

    #結果の表示
    st.caption("ドライブ率")
    if df_under1400_result.at[df_under1400_result.index[0],df_under1400_result.columns[2]] == 0:
        st.info("ドライブなし")
    else:
        st.info(f"1/{all_count / df_under1400_result.at[df_under1400_result.index[0],df_under1400_result.columns[2]]:.1f}")

##### 表記1400枚越えのカウント処理
with st.form(key="over1400_drive_count"):
    st.write("表記1400枚越え")

    #カウントボタン
    over1400_g10_count_btn = st.form_submit_button("10G",type=button_type)
    over1400_g20_count_btn = st.form_submit_button("20G",type=button_type)
    over1400_drive_count_btn = st.form_submit_button("ドライブ",type=button_type)

    #ボタンが押されたらカウント処理
    if over1400_g10_count_btn:
        df.SelectedCount(selected=df.columns_list[3], minus_check=st.session_state["minus_check"])
    
    elif over1400_g20_count_btn:
        df.SelectedCount(selected=df.columns_list[4], minus_check=st.session_state["minus_check"])
    
    elif over1400_drive_count_btn:
        df.SelectedCount(selected=df.columns_list[5], minus_check=st.session_state["minus_check"])
    
    #結果の表示
    #1400枚越えだけの表を作ってそれを表示
    df_over1400_result = df.df[[df.columns_list[3],df.columns_list[4], df.columns_list[5]]].copy()
    
    # カラム名を変更
    new_column_names = {"1400枚越え10G": "10G", "1400枚越え20G": "20G", "1400枚越えドライブ": "ドライブ"}
    df_over1400_result.rename(columns=new_column_names, inplace=True)
    
    st.write(df_over1400_result)

    #####ドライブ確率の表示
    #全セット数を取得
    all_count = df_over1400_result.loc[df_over1400_result.index[0]].sum()

    #結果の表示
    st.caption("ドライブ率")
    if df_over1400_result.at[df_over1400_result.index[0],df_over1400_result.columns[2]] == 0:
        st.info("ドライブなし")
    else:
        st.info(f"1/{all_count / df_over1400_result.at[df_over1400_result.index[0],df_over1400_result.columns[2]]:.1f}")

##### トータルの数値表示
st.write("トータル結果")

#トータルの数値が入ったデータフレームを作成
total_result = {df_under1400_result.columns[0]:df_under1400_result[df_over1400_result.columns[0]] + df_over1400_result[df_over1400_result.columns[0]],
                df_under1400_result.columns[1]:df_under1400_result[df_over1400_result.columns[1]] + df_over1400_result[df_over1400_result.columns[1]],
                df_under1400_result.columns[2]:df_under1400_result[df_over1400_result.columns[2]] + df_over1400_result[df_over1400_result.columns[2]]}

#データフレームを作成
total_result_df = pd.DataFrame(total_result)

#データフレームの表示
st.dataframe(total_result_df)

#####ドライブ確率の表示
#全セット数を取得
total_all_count = total_result_df.loc[total_result_df.index[0]].sum()

#結果の表示
st.caption("ドライブ率")
if total_result_df.at[total_result_df.index[0],total_result_df.columns[2]] == 0:
    st.info("ドライブなし")
else:
    st.info(f"1/{total_all_count / total_result_df.at[total_result_df.index[0],total_result_df.columns[2]]:.1f}")


##### マイナスのチェックボックス表示
st.checkbox("マイナスカウント、1行削除", value=st.session_state["minus_check"], on_change=toggle_minus_check)