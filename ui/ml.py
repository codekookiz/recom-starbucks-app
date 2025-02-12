import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time


# 스타일 적용
st.markdown(
    """
    <style>
        .big-font { font-size:30px !important; font-weight: bold; text-align: center; }
        .sub-header { font-size:22px !important; font-weight: bold; }
        .info-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
        .button { font-size:18px; font-weight: bold; color: white; background-color: #ff4b4b; padding: 10px 20px; border-radius: 5px; }
    </style>
    """,
    unsafe_allow_html=True,
)

def run_ml():

    # 세션 상태에서 로그인 여부 확인
    def check_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'register_mode' not in st.session_state:
            st.session_state.register_mode = False

    check_login()

    if not st.session_state.logged_in:
        df = pd.read_csv('data/user_data.csv')
        if st.session_state.register_mode:
            st.title("📝 회원가입")
            new_username = st.text_input("이름", value="", key="new_username")
            new_id = st.text_input("ID", value="", key="new_id")
            if new_id in df['ID'].values :
                    st.error("❌ 이미 존재하는 ID입니다.")
            new_password = st.text_input("새 비밀번호", type="password", value="", key="new_password")
            confirm_password = st.text_input("비밀번호 확인", type="password", value="", key="confirm_password")
            
            if st.button("회원가입 완료"):
                if new_password != confirm_password:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                elif new_password == confirm_password and new_id and new_password:
                    new_row = pd.DataFrame([{"이름":new_username, "ID":str(new_id), "비밀번호":str(new_password)}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv('data/user_data.csv', index=False)
                    st.success("✅ 회원가입이 완료되었습니다! 로그인해주세요.")
                    st.session_state.register_mode = False
                    time.sleep(1)
                    st.rerun()
            
            if st.button("뒤로 가기"):
                st.session_state.register_mode = False
                st.rerun()
        else:
            st.title("🔐 로그인")
            id = st.text_input("ID", value="", key="username")
            password = st.text_input("비밀번호", type="password", value="", key="password")
            
            if st.button("로그인"):
                if (id in df['ID'].value_counts()) == True :
                    if (df.loc[df['ID'] == id, '비밀번호'].values[0]) == password :
                        st.session_state.logged_in = True
                        st.success("로그인 성공! 🎉")
                        time.sleep(1)
                        st.rerun()
                    else :
                        st.error("❌ 비밀번호가 일치하지 않습니다.")   
                else:
                    st.error("❌ 아이디가 존재하지 않습니다.")
            
            if st.button("회원가입"):
                st.session_state.register_mode = True
                st.rerun()
    else:
        st.text('')
        st.text('')

        # 제목 정리
        st.markdown(
            """
            <h2 style="text-align: center; color: #FF4B4B;">
                ☕️ 오늘은 무슨 음료를 마실까?
            </h2>
            <p style="font-size: 24px; text-align: center; color: ##4C82C2;">
                <b>머신 러닝 (ML)<b>
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 큰 제목
        st.markdown('<p style="font-size: 24px; font-weight: bold; color: #333; font-family: Arial, sans-serif;">🎞️ ML 기반 영화 박스오피스 예측</p>', unsafe_allow_html=True)

        # 정보 박스 스타일
        st.markdown('<p style="font-size: 16px; color: #555; font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 15px; border-radius: 8px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1);">영화의 기본 정보를 입력하면 예상 박스오피스 수익을 예측해드립니다.</p>', unsafe_allow_html=True)
        st.text('')

        if st.button('❓ 수익 예측 예시') :
            col1, col2 = st.columns(2)
            with col1 :
                st.image('image/result_a.png')
            with col2 :
                st.image('image/result_b.png')

        # 하위 제목
        st.markdown('<p style="font-size: 22px; font-weight: bold; color: #333; font-family: Arial, sans-serif; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;">📌 영화 정보 입력</p>', unsafe_allow_html=True)
        st.text('')

        menu_rating = ['전체 관람가', '12세 이상 관람가', '15세 이상 관람가', '청소년 관람 불가']
        menu_genre = ['액션', '어드벤처', '블랙 코미디', '코미디', '드라마', '호러', '뮤지컬', '로맨틱 코미디', '스릴러/서스펜스', '서부극']

        title = st.text_input('🎥 영화 제목')
        st.info('* 영화 제목은 데이터 축적 시 영화 간 구분을 위해 사용됩니다.')
        
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input('📅 개봉 연도', min_value=1900, max_value=2040, value=2025)
            runtime = st.number_input('⏳ 상영 시간 (분)', min_value=0, value=120)
        with col2:
            mpaa = st.selectbox('🔖 상영 등급', menu_rating)
            genre = st.selectbox('🎭 장르', menu_genre)

        cost = st.number_input('💰 제작 비용 ($)', step=1000000, value=100000000)
        opening = st.number_input('🎟 개봉 주말 수익 ($)', step=1000000, value=100000000)

        classifier = joblib.load('model/classifier.pkl')

        mpaa_dict = {'전체 관람가': 0, '12세 이상 관람가': 1, '15세 이상 관람가': 2, '청소년 관람 불가': 3}
        genre_dict = {
            '액션': 0, '어드벤처': 1, '블랙 코미디': 2, '코미디': 3, '드라마': 4,
            '호러': 5, '뮤지컬': 6, '로맨틱 코미디': 7, '스릴러/서스펜스': 8, '서부극': 9
        }

        data_classify = np.array([cost, mpaa_dict[mpaa], genre_dict[genre], runtime, year]).reshape(1, 5)
        new_data_classify = pd.DataFrame(data_classify)

        st.text('')

        if st.button('📊 수익 예측', disabled=not title):
            st.markdown('<p class="sub-header">🔍 예측 결과</p>', unsafe_allow_html=True)

            pred_group = classifier.predict(new_data_classify)

            label_group = {0: '미들 마켓', 1: '메가 블록버스터', 2: '블록버스터'}[pred_group[0]]
            st.success(f'🎬 영화 **"{title}"** 은(는) **{label_group}** 영화군요!')
            
            with st.spinner('⏳ 수익 예측을 실시하는 중...'):
                time.sleep(2)

                regressor = joblib.load('model/regressor.pkl')
                data_predict = np.array([cost, opening, mpaa_dict[mpaa], genre_dict[genre], runtime, year]).reshape(1, 6)
                pred_profit = regressor.predict(data_predict)[0][0]
                pred_dom_profit = int(pred_profit.round())

                if pred_dom_profit >= 0:
                    new_dom_profit = format(pred_dom_profit, ',')
                    st.subheader(f'📈 예상 북미 박스오피스 수익: **{new_dom_profit} 달러**')

                    time.sleep(1)

                    # wrld_dom_ratio : domestic gross 대비 worldwide gross의 일반적인 비율
                    # max값이 과도하게 큰 관계로 mean값 대신 median값을 wrld_dom_ratio로 설정 (세부 사항은 ratio_movie.ipynb 참고)
                    wrld_dom_ratio = 2.7
                    pred_wrld_profit = int((pred_profit * wrld_dom_ratio).round())
                    new_wrld_profit = format(pred_wrld_profit, ',')
                    st.subheader(f'🌍 예상 전세계 박스오피스 수익: **{new_wrld_profit} 달러**')

                    save_df = pd.read_csv('data/result.csv')
                    new_row = pd.DataFrame([{"영화명":title, "개봉 연도":int(year), "상영 시간":int(runtime), "상영 등급":mpaa, "장르":genre,
                                            "제작 비용 ($)":int(cost), "개봉 주말 수익 ($)":int(opening), "유형":label_group, "북미 예상 수익 ($)":int(pred_dom_profit),
                                            "전세계 예상 수익 ($)":int(pred_wrld_profit)}])
                    print(new_row)

                    save_df = pd.concat([save_df, new_row], ignore_index=True)
                    save_df.to_csv('data/result.csv', index=False)

                else:
                    st.error('❌ 예측이 불가능한 데이터입니다.')