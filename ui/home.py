import streamlit as st

def run_home():

    st.text('')
    st.text('')

    # 제목
    st.markdown(
        """
        <h2 style="text-align: center; color: #FF4B4B;">
            🥤 스타벅스 음료 주문 및 추천 시스템 개요
        </h2>
        """, 
        unsafe_allow_html=True
    )

    st.text('')

    # 설명
    st.markdown(
        """
        <p style="font-size: 18px; text-align: center;">
            ☕️ 스타벅스의 최신 음료 영양정보 데이터를 기반으로 <b>사용자의 취향에 맞는 음료를 추천</b>하는 앱입니다.<br>
            음료 주문 데이터와 딥러닝 모델을 통해 <b>나의 취향에 맞는 음료</b>를 추천 받아보세요.</b>
        </p>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 📌 데이터 출처 및 구성
    st.markdown("### 📌 **사용 데이터**")
    st.info(
        """
        🔹 **[starbucks_drinkMenu_expanded.csv](https://www.kaggle.com/datasets/noorunnishabegum1996/starbucks-drinkmenu-expanded)** (출처: Kaggle)  
        * 2019년 기준 미국 스타벅스에서 판매하는 음료의 영양성분 데이터입니다.\n\n 
        🔹 **스타벅스 영양성분.csv** (영문 데이터 번역 및 한국 스타벅스 음료 데이터 추가)\n\n
        * 2025년 2월 기준 한국 스타벅스 매장에서 판매하는 음료 데이터를 추가하고, 영문 컬럼명 및 데이터를 한글로 번역하였습니다.\n\n
        * [스타벅스 코리아](https://www.starbucks.co.kr/menu/drink_list.do) 홈페이지에 업로드된 데이터를 활용해 직접 제작한 데이터셋입니다.\n\n
        * **사이즈 및 유제품** 컬럼을 분리하여 가독성 개선
        """
    )

    st.markdown("---")

    # 이미지 추가
    st.image("image/main_home.png")

    st.markdown("---")

    # ⚡ 기능 소개
    st.markdown("### ⚡ **탭별 주요 기능**")
    st.markdown(
        """
        - 📊 **과거 데이터 확인하기**: 기존 영화 데이터를 시각적으로 분석하고, 트렌드를 파악  
        - 🔍 **앱 상세 정보**: 이 앱의 개요와 기능을 한눈에 확인
        - 📈 **영화 수익 예측하기**: 입력한 영화 정보를 바탕으로 AI 모델이 예상 수익을 예측  
        - ⚒️ **통계 데이터**: 관리자 전용 페이지로 추가적인 분석 기능 제공  
        """
    )

    st.markdown("---")

    # 📢 활용 예시
    st.markdown("### 📢 **이렇게 활용할 수 있어요!**")
    st.markdown(
        """
        - 🎬 **영화 제작사** → 제작 전 예상 수익을 분석하여 투자 결정  
        - 🎞 **배급사** → 마케팅 전략을 세우기 전 예상 흥행 여부 판단  
        - 📺 **영화 애호가** → 과거 데이터를 통해 어떤 영화가 성공했는지 확인  
        """
    )

    st.markdown("---")