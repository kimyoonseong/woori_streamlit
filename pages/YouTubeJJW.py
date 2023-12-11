import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Streamlit 페이지 설정
st.header('년도별(1월~12월) 가장 인기가 많았던 예능 채널!')
st.sidebar.markdown('년도를 입력하세요!')

# 사용자로부터 년도 입력받기
selected_year = st.sidebar.text_input("년도 (예: 2023)")
accept = st.sidebar.button("확인")
# 데이터 불러오기 및 처리 함수
def load_data(year):
    # 데이터 불러오기
    df = pd.read_csv(f'C:\\Users\\dinoqos\\Downloads\\KR_youtube_trending_data.csv')

    # 'publishedAt'과 'trending_date' 열을 datetime 객체로 변환
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['trending_date'] = pd.to_datetime(df['trending_date'])

    # 'publishedAt'에서 년도와 월 추출
    df['year'] = df['publishedAt'].dt.year
    df['month'] = df['publishedAt'].dt.month

    # 특정 년도의 데이터만 필터링
    df_year = df[df['year'] == year]

    # 카테고리 24에 속하는 동영상만 필터링
    category_24_data = df_year[df_year['categoryId'] == 24]

    # 각 월별로 가장 많은 'likes'를 받은 동영상 추출
    top_videos_per_month = category_24_data.groupby('month').apply(lambda x: x.loc[x['likes'].idxmax()])

    # 필요한 열만 선택
    top_video_titles = top_videos_per_month[['month', 'title', 'view_count', 'channelTitle', 'likes']]
    top_video_titles.reset_index(drop=True, inplace=True)

    # 각 월별로 가장 많은 'view_count'를 기록한 상위 5개 채널 추출
# 각 월별로 가장 많은 'view_count'를 기록한 상위 5개 채널 추출
    top_channels_per_month = category_24_data.groupby(['month', 'channelTitle'])\
        ['view_count'].sum().reset_index()  # 'view_count'만을 합산

    top_channels_per_month = top_channels_per_month.groupby('month')\
        .apply(lambda x: x.nlargest(5, 'view_count')).reset_index(drop=True)

    # 데이터프레임 정렬
    top_channels_per_month.sort_values(by=['month', 'view_count'], ascending=[True, False], inplace=True)
    top_channels_per_month.reset_index(drop=True, inplace=True)

    return top_video_titles, top_channels_per_month


# 'best 채널 확인' 버튼이 눌렸을 때의 동작
if accept:
    if selected_year:
        try:
            year = int(selected_year)

            # 한글 폰트 설정
            plt.rc('font', family='Malgun Gothic')

            # load_data 함수로부터 두 개의 데이터프레임을 받는다.
            top_video_titles, top_channels_per_month = load_data(year)

            # MrBeast 채널 제거
            top_channels_without_mrbeast = top_channels_per_month[top_channels_per_month['channelTitle'] != 'MrBeast']

            # 각 월별 상위 5개 채널 추출
            top_5_channels_by_month = top_channels_without_mrbeast.groupby('month').apply(lambda x: x.nlargest(5, 'view_count')).reset_index(drop=True)

            # 시각화
            plt.figure(figsize=(20, 15))
            for month in range(1, 13):
                plt.subplot(4, 3, month)
                monthly_data = top_5_channels_by_month[top_5_channels_by_month['month'] == month]
                sns.barplot(x='channelTitle', y='view_count', data=monthly_data, palette='viridis')
                plt.title(f'{month}월 Top 5 채널')
                plt.xlabel('채널')
                plt.ylabel('조회수')
                plt.xticks(rotation=45)
            plt.tight_layout()

            # Streamlit에 그래프 표시
            st.pyplot(plt)

        except ValueError:
            st.error("유효한 년도를 입력해주세요.")
    else:
        st.error("년도를 입력해주세요.")
