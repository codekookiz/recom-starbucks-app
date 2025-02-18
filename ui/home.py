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
            ☕️ 스타벅스의 최신 음료 영양정보 데이터를 기반으로 <b>사용자 취향에 맞는 음료를 추천</b>하는 앱입니다.<br>
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
        🔹 **[starbucks_drinkMenu_expanded.csv](https://www.kaggle.com/datasets/noorunnishabegum1996/starbucks-drinkmenu-expanded)** (출처: Kaggle)\n
        * 2019년 기준 미국 스타벅스에서 판매하는 음료의 영양성분 데이터입니다.\n
        🔹 **스타벅스 영양성분.csv** (영문 데이터 번역 및 한국 스타벅스 음료 데이터 추가)\n
        * 2025년 2월 기준 한국 스타벅스 매장에서 판매하는 음료 데이터를 추가하고, 영문 컬럼명 및 데이터를 한글로 번역하였습니다.\n
            * **영문 컬럼명 및 데이터명**: "Beverage", "Caffè Latte"\n
            * **한글 컬럼명 및 데이터명**: "음료명", "카페 라떼"\n
        * [스타벅스 코리아](https://www.starbucks.co.kr/menu/drink_list.do) 홈페이지에 업로드된 데이터를 일부 활용해 직접 제작한 데이터셋입니다.\n
            * Tall 사이즈를 제외한 음료의 영양 정보는 [스타벅스 모바일 앱](https://www.starbucks.co.kr/util/app_tip.do)을 통해 추가하였습니다.\n
        * **사이즈 및 유제품** 컬럼을 분리 및 간소화하여 상세 분류가 가능하게 하고, 가독성을 개선하였습니다.\n
            * 기존 데이터 : "(Beverage_prep) Short Nonfat Milk"\n
            * 변경 데이터 : "(사이즈) Short", "(유제품) O"\n
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
        - **📌 전체 메뉴 확인하기**: 스타벅스 음료의 영양정보를 한눈에 확인
        - **☕️ 음료 추천 받기**: 사용자의 취향에 맞는 음료 추천
            - **🛒 음료 주문 시스템**: 원하는 음료를 주문하고, 칼로리 정보 확인
        - **✍️ 리뷰 남기기**: 구매한 음료에 대한 리뷰 작성 및 확인
        - **💿 통계 데이터**: 주문 통계 및 인기 음료 확인
        """
    )

    st.markdown("---")

    # 📢 활용 예시
    st.markdown("### 📢 **이렇게 활용할 수 있어요!**")
    st.markdown(
        """
        - **👤 고객**: 스타벅스 음료의 영양정보를 확인하고, 추천 음료를 찾아보세요.
        - **🏢 스타벅스**: 사용자의 음료 주문 데이터를 분석하여, 추후 음료 개발 및 마케팅에 활용할 수 있습니다.
        """)

    st.markdown("---")