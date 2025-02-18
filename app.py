import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

from ui.dev import run_dev
from ui.choice import run_choice
from ui.home import run_home
from ui.info import run_info
from ui.recom import run_recom
from ui.review import run_review
from ui.stat import run_stat


def main():
    # 메인 타이틀
    st.markdown(
        """
        <h1 style='text-align: center; color: color: #4C82C2;'>
            ☕️ 스타벅스 음료 추천 앱
        </h1>
        <h2 style='text-align: center; 'color: #4C82C2;'>
            🤖 데이터 분석 및 딥러닝 기반
        </h2>
        """, unsafe_allow_html=True
    )

    st.markdown("""<hr style="border: none; height: 5px; background: #5B9BD5; box-shadow: 0px 2px 5px rgba(0,0,0,0.2);">""",
                 unsafe_allow_html=True)
    
    # 사이드바
    st.sidebar.image("image/main_sidebar.png")  
    
    # 📅 현재 날짜 & 시간 표시
    utc_now = datetime.now(timezone.utc)  # UTC 시간 가져오기
    kst_now = utc_now + timedelta(hours=9)  # KST 시간으로 변환

    # KST 시간 포맷에 맞게 출력
    now_str = kst_now.strftime("%Y-%m-%d %a %H:%M %p")
    st.sidebar.markdown(f"🕒 **현재 시간:** {now_str}")

    st.sidebar.markdown("---")

    df_drink = pd.read_csv('data/menu_data.csv')
    df_log = pd.read_csv('data/order_data.csv')
    df_review = pd.read_csv('data/review_data.csv')
    count = len(df_drink)
    kcal = int((df_drink['칼로리 (kcal)'].mean()).round())
    best = df_review.groupby('음료명')['별점'].mean().sort_values(ascending=False).to_frame().index[0]
    popular = df_log.groupby('음료명').sum().sort_values('주문 수', ascending=False).iloc[0, :].to_frame().columns[0]

    # 음료 데이터 요약
    st.sidebar.markdown("### 📊 데이터 요약")
    st.sidebar.markdown(
        f"""
        <div style="font-size: 20px; font-weight: bold;">🥤 총 음료</div>
        <div style="font-size: 28px;">{count}개</div>
        """, 
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div style="font-size: 20px; font-weight: bold;">⭐️ 최고 평점 음료</div>
        <div style="font-size: 28px;">{best}</div>
        """, 
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div style="font-size: 20px; font-weight: bold;">💰 최다 판매 음료</div>
        <div style="font-size: 28px;">{popular}</div>
        """, 
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    # 📌 소셜 & 도움말 버튼 추가
    st.sidebar.markdown("### 🔗 유용한 링크")
    st.sidebar.link_button("🔍 GitHub Repository", "https://github.com/codekookiz/recom-starbucks-app")

    if st.sidebar.button("❓ 도움말 보기"):
        st.sidebar.info("이 앱은 사용자의 취향에 따라 스타벅스 음료를 추천하는 딥러닝 기반 앱입니다.")

    st.sidebar.markdown("---")

    # 탭 메뉴
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🏠 홈", "ℹ 앱 상세 정보", "⚒️ 개발 정보", "📌 전체 메뉴 확인하기", "☕️ 음료 추천 받기", "✍️ 리뷰 남기기", "💿 통계 데이터"])

    # 각 탭에 해당하는 기능 실행
    with tab1:
        run_home()

    with tab2:
        run_info()

    #with tab3:
        #run_dev()

    with tab4:
        run_choice()

    with tab5:
        run_recom()

    with tab6:
        run_review()

    with tab7:
        run_stat()

if __name__ == '__main__':
    main()