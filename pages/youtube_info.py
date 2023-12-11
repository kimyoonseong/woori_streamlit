import streamlit as st
import numpy as np
import pandas as pd  # st은 입력과 출력만 담당할 뿐 실제 로직은 나머지 파이썬 코드로 구현됩니다.
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.sidebar.title('나라 검색')

country=st.sidebar.text_input('궁금한 나라를 검색하세요')

KRvideo = pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\KRvideos.csv")
USvideo = pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\USvideos.csv")
JPvideo = pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\JPvideos.csv")
CAvideo = pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\CAvideos.csv")
MXvideo = pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\MXvideos.csv")
country_list=['한국','미국','일본','캐나다','멕시코']
img_list=['https://i.imgur.com/6BA9OPP.png','https://i.imgur.com/Wct8IbO.png','https://i.imgur.com/EoTAFG4.png','https://i.imgur.com/Mg24HM7.png','https://i.imgur.com/i5Xc7S4.png']
video_list=[KRvideo,USvideo,JPvideo,CAvideo,MXvideo]
for ani_ in country_list:
    if country in ani_:
        idx=country_list.index(ani_)
        
#if country !="":
#   st.image(img_list[idx])
if country=="":
    st.title("없는 나라입니다.")
elif country == country_list[idx]:
    video=video_list[idx]
    st.image(img_list[idx])
else:
    st.title("없는 나라입니다.")
#print(USvideo.columns)
#video=pd.read_csv(r"C:\ITStudy\01_Python\youtube_info\USvideos.csv")
if country!="":
    df = video[["title", "channel_title", "views"]]
    df_sorted = df.sort_values(by='views', ascending=False)
    # 영상제목과 채널명이 둘 다 중복인 영상 제거
    df_sorted_latest = df_sorted.drop_duplicates(['title','channel_title'], keep='first')

    # 채널별 조회수 합계 계산
    df_channel_view_sum = df_sorted_latest.groupby(['channel_title']).sum()
    # 채널별 조회수 내림차순 정렬
    df_channel_view = df_channel_view_sum.sort_values(by='views', ascending=False)
    # 총 2253개의 채널 중 상위 20개 채널만 가져오기
    df_channel_view_top20 = df_channel_view[:20]
    df_channel_view_top20_index = df_channel_view_top20.reset_index()


    df2= video[["category_id",  "views"]]
    df2_sorted=df2.sort_values(by='views', ascending=False)
    df2_channel_view_sum = df2_sorted.groupby(['category_id']).sum()
    df2_channel_view = df2_channel_view_sum.sort_values(by='views', ascending=False)
    df2_category_view_top20 = df2_channel_view[:]
    df2_category_view_top20_index = df2_category_view_top20.reset_index()
    #fig.save("test.png")
    #st.line_chart(x='channel_title', y='views', data=df_channel_view_top20_index)
    #st.bar_chart(df_channel_view_top20_index.set_index('channel_title')['views'])
    if country!="":
        st.title(country +'상위 20위 채널 조회수')
        # 그래프 사이즈 설정
        plt.figure(figsize=(10,10))
        plt.rc('font', family='Malgun Gothic')  
        # seaborn 패키지로 수평막대 그래프 그리기
        plt.xlabel('조회수')  # x축 라벨
        plt.ylabel('채널명')  # y축 라벨
        plt.title('상위 20개 채널 조회수')
        #plt.style.use('Solarize_Light2')
        fig=sns.barplot(x='views', y='channel_title', data=df_channel_view_top20_index, palette="viridis")
        st.pyplot(fig.figure)

        plt.figure(figsize=(10,10))
        plt.rc('font', family='Malgun Gothic')  
        # seaborn 패키지로 수평막대 그래프 그리기
        plt.xlabel('카테고리')  # x축 라벨
        plt.ylabel('조회수')  # y축 라벨
        plt.title('카테고리별 조회수')
        st.title(country+"에서 가장 인기있는 카테고리")
        fig2=sns.barplot(x='category_id', y='views', data=df2_category_view_top20_index, palette="viridis")
        st.pyplot(fig2.figure)
        st.write('모든나라에서 10번과 24번(음악,예능) 카테고리가 가장 인기 있는것을 알 수 있습니다')
