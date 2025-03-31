import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

# 수정된 CSV 파일 경로 (Streamlit Cloud용 상대 경로)
data_path = "hotel_fin_0331_1.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

# 도시별 중심 좌표 딕셔너리 추가
region_coords = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8722, 128.6025),
    "전주": (35.8242, 127.1480),
    "제주": (33.4996, 126.5312),
    "강릉": (37.7519, 128.8761),
    "속초": (38.2044, 128.5912),
    "경주": (35.8562, 129.2247),
    "여수": (34.7604, 127.6622),
}

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# 지역 선택
regions = df['Location'].unique()
selected_region = st.radio("📍 지역을 선택하세요", regions, horizontal=True)

# 지역 필터링
region_df = df[df['Location'] == selected_region]
region_hotels = region_df['Hotel'].unique()

# 호텔 선택
selected_hotel = st.selectbox("🏨 호텔을 선택하세요", ["전체 보기"] + list(region_hotels))

# 색상 컬럼 추가
def get_color(hotel):
    if selected_hotel == "전체 보기":
        return [30, 144, 255]  # 파란색
    elif hotel == selected_hotel:
        return [255, 0, 0]  # 빨간색
    else:
        return [180, 180, 180]  # 회색

region_df["color"] = region_df["Hotel"].apply(get_color)

# 지도 표시
layer = pdk.Layer(
    "ScatterplotLayer",
    data=region_df,
    get_position='[Longitude, Latitude]',
    get_color="color",
    get_radius=80,
    pickable=True,
)

mid_lat = region_df["Latitude"].mean()
mid_lon = region_df["Longitude"].mean()

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=11,
    pitch=0
)

st.subheader(f"🗺️ {selected_region} 지역 호텔 지도")
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Hotel}"}
))

# 리뷰 요약 및 감성 점수 시각화
if selected_hotel == "전체 보기":
    map_df = region_df[['Latitude', 'Longitude']].dropna()
    map_df.columns = ['lat', 'lon']
    st.subheader(f"🗺️ {selected_region} 지역 호텔 지도")
    st.map(map_df)

else:
    # 선택된 호텔 정보만 표시
    hotel_data = region_df[region_df['Hotel'] == selected_hotel].iloc[0]
    st.subheader(f"🗺️ '{selected_hotel}' 위치")
    st.map(pd.DataFrame({
        'lat': [hotel_data['Latitude']],
        'lon': [hotel_data['Longitude']]
    }))

    # 요약 출력
    st.markdown("### ✨ 선택한 호텔 요약")
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
    if selected_hotel == "전체 보기":
        st.dataframe(region_df.reset_index(drop=True))
    else:
        st.dataframe(region_df[region_df['Hotel'] == selected_hotel].reset_index(drop=True))
