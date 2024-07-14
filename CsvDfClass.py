import streamlit as st
import pandas as pd

class CsvDf:
    def __init__(self,
                 columns=None,
                 index=None,
                 path=None):
        """引数で指定のcsvファイルを読み込み
        ＆データフレームのカラム、インデックスを
        リストで変数化
        
        Parameter
        --------------------------------
        columns:リスト、対象とするDFのカラム名が入ったリスト。基本Top.pyで設定された変数を入れる
        index:リスト、対象とするDFのインデックス名が入ったリスト。基本Top.pyで設定された変数を入れる
        path:文字列、対象とするcsvの相対パス。基本Top.pyで設定された変数を入れる
        """

        #引数の内容をインスタンス変数化
        self.columns_list = columns
        self.index_list= index
        self.path = path

        #csvファイルの読み込み
        try:
            self.df = pd.read_csv(self.path, index_col=0)
        except FileNotFoundError:
            st.caption("Topページで新規作成を押して下さい")
    
    
    ######################################
    ##### 履歴データの保存
    ######################################
    def BonusHistrical(self,
                       add_result=None,
                       minus_check=False):
        """ボーナスやCZの当選履歴を保存する
        
        Parameter
        ------------------------------
        add_result:リスト、セレクトボックスなどで選択された結果をリストにしたものを与える
        minus_check:ブール値、Trueなら1行削除する
        """

        #####マイナスチェックが入っていた場合の処理
        #####最後の1行を削除、1行もデータなければパス
        if minus_check:
            try:
                self.df.drop(self.df.index[-1], inplace=True)
            except IndexError:
                pass
        
        #####マイナスチェックがない場合の処理
        #####選択された結果を最後の1行に追加
        else:
            #現在のインデックス数から新しい行のインデックス値を定義
            new_index = len(self.df)

            #新しい行を追加する
            self.df.loc[new_index] = add_result
        
        #csvに保存する
        self.df.to_csv(self.path)
    

    ###################################
    ##### 終了画面系カウント処理
    ###################################
    def SelectedCount(self,
                   selected=None,
                   minus_check=None):
        """カウント処理。
        引数に設定された選択肢をカウント処理する
        
        Parameter
        --------------------------------
        selected:文字列、カウント処理するカラムを入れる
        minus_check:ブール値、Trueなら1行削除する
        """

        #####マイナスチェックが入っていた場合の処理
        ##### 選択されたものを-1する
        if minus_check:
            #指定のカラムの数値を-1
            self.df.at[self.df.index[0], selected] -= 1

            #結果が0未満になるなら0にしておく
            if self.df.at[self.df.index[0], selected] < 0:
                self.df.at[self.df.index[0], selected] = 0
        
        #####マイナスチェックがない場合の処理
        ##### 選択されたものを+1する
        else:
            self.df.at[self.df.index[0], selected] += 1

        #csvに保存する
        self.df.to_csv(self.path)


    ##################################
    ##### 終了画面系の結果表示
    ##################################
    def CountAndProbabilityResultShow(self,
                                      remarks_list=None):
        """カウント結果と出現確率の表を表示する。
        結果表示用のデータフレームを新規で作成し、それを表示する
        
        Parameter
        -------------------------------------
        remarks_list:リスト、各選択肢の説明、引数の設定なければ追加しない
        """

        #表示用のデータフレームを起こす
        self.df_count_probability_result = self.df.copy()

        #全選択肢のカウント合計値を出しておく
        count_sum = self.df_count_probability_result.loc[self.df_count_probability_result.index[0]].sum()

        #全選択肢の出現確率を格納するリストを準備する
        probability_list = []

        #####各選択肢の出現確率を計算しリストに格納
        for column in self.df_count_probability_result.columns:
            #出現確率の計算
            probability_occurrence = self.df_count_probability_result.at[self.df_count_probability_result.index[0], column] / count_sum

            #％表記の文字列にする
            probability_occurrence = f"{probability_occurrence * 100:.1f}%"

            #リストに追加する
            probability_list.append(probability_occurrence)
        
        #データフレームに追加する
        self.df_count_probability_result.loc["出現確率"] = probability_list

        #選択肢の説明の備考欄を追加する
        if remarks_list == None:
            pass
        else:
            self.df_count_probability_result.loc["備考"] = remarks_list

        st.dataframe(self.df_count_probability_result)