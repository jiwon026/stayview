import streamlit as st
import pandas as pd

# 수정된 CSV 파일 경로 (Streamlit Cloud용 상대 경로)
data_path = "final_all.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# 호텔 선택
df = df.dropna(subset=['Hotel'])  # 혹시 모를 NaN 방지
hotels = df['Hotel'].unique()
selected_hotel = st.selectbox("호텔을 선택하세요", hotels)

# 선택한 호텔 정보 필터링
hotel_data = df[df['Hotel'] == selected_hotel].iloc[0]

# 컬럼 나누기
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ 긍정 요약")
    st.write(hotel_data['Refined_Positive'])

with col2:
    st.subheader("🚫 부정 요약")
    st.write(hotel_data['Refined_Negative'])

# 감성 점수 시각화
st.markdown("---")
st.subheader("📊 항목별 평균 점수")

aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']
aspect_scores = hotel_data[aspect_columns]
st.bar_chart(aspect_scores)

# Raw 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df[df['Hotel'] == selected_hotel].reset_index(drop=True))
