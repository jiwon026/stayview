import streamlit as st
import pandas as pd
import altair as alt

# 수정된 CSV 파일 경로 (Streamlit Cloud용 상대 경로)
data_path = "final_all.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

# 도시별 중심 좌표 딕셔너리 추가
region_coords = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "인천": (37.4563, 126.7052),
    "대구": (35.8722, 128.6025),
    "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845),
    "울산": (35.5384, 129.3114),
    "세종": (36.4800, 127.2890),
    "수원": (37.2636, 127.0286),
    "전주": (35.8242, 127.1480),
    "제주": (33.4996, 126.5312),
    "강릉": (37.7519, 128.8761),
    "속초": (38.2044, 128.5912),
    "경주": (35.8562, 129.2247),
    "여수": (34.7604, 127.6622),
    "춘천": (37.8813, 127.7298),
}

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# 지역 선택
regions = df['Location'].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 해당 지역의 호텔 목록 필터링
region_hotels = df[df['Location'] == selected_region]['Hotel'].unique()
selected_region = st.radio("📍 지역을 선택하세요", regions, horizontal=True)

# 선택한 호텔 정보 가져오기
hotel_data = df[(df['Location'] == selected_region) & (df['Hotel'] == selected_hotel)].iloc[0]

# 지역 중심 지도 표시
lat, lon = region_coords.get(hotel_data['Location'], (None, None))

if lat and lon:
    st.subheader("🗺️ 지역 중심 지도")
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
else:
    st.warning("⚠️ 해당 지역의 좌표 정보가 없습니다.")

# 컬럼 나누기
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ 긍정 리뷰 요약")
    st.write(hotel_data['Refined_Positive'])

with col2:
    st.subheader("🚫 부정 리뷰 요약")
    st.write(hotel_data['Refined_Negative'])

# 감성 점수 시각화
st.markdown("---")
st.subheader("📊 항목별 평균 점수")

# 점수 데이터 추출
aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']
aspect_scores = hotel_data[aspect_columns]

# DataFrame으로 변환
score_df = pd.DataFrame({
    '항목': aspect_scores.index,
    '점수': aspect_scores.values
})

# Altair 차트
chart = alt.Chart(score_df).mark_bar().encode(
    x=alt.X('항목', sort=None),
    y='점수',
    color=alt.condition(
        alt.datum.점수 < 0,
        alt.value('crimson'),      # 음수면 빨간색
        alt.value('steelblue') # 양수면 파란색
    )
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)

# Raw 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df[df['Hotel'] == selected_hotel].reset_index(drop=True))
