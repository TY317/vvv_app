import streamlit as st
import pandas as pd
from PIL import Image

##### ページの内容 #####
# 参考情報の表示のみ

st.subheader("ラウンド開始画面での示唆")
st.caption("・ラウンド10・20・30・40・50・60の開始画面に高設定濃厚パターンが存在")
st.caption("・参考情報の表示のみ")

#ビーストハイ
beasthigh = Image.open("./image/round_image_beasthigh.jpg")
st.image(beasthigh, width=300)

#リーゼロッテ
reaselotte = Image.open("./image/round_image_reaselotte.jpg")
st.image(reaselotte, width=300)