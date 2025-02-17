import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
from matplotlib import rc
import time

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd()]
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

plt.rcParams['axes.unicode_minus'] = False
system_os = platform.system()
if system_os == "Darwin":  # macOS
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
elif system_os == "Windows":  # Windows
    font_path = "C:/Windows/Fonts/malgun.ttf"
else:  # Linux
    rc('font', family='NanumGothic')

def run_choice():
    fontRegistered()
    plt.rc('font', family='NanumGothic')

    def check_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'register_mode' not in st.session_state:
            st.session_state.register_mode = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = ""

    # 제목
    st.markdown(
        """
        <h2 style="text-align: center; color: #FF4B4B;">
            ☕️ 오늘은 무슨 음료가 좋을까요?
        </h2>
        <p style="font-size: 24px; text-align: center; color: ##4C82C2;">
            <b>탐색적 데이터 분석 기반 스타벅스 메뉴 선택<b>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 데이터 불러오기
    st.info("📌 **기본 데이터** (menu_data.csv) : 원본 데이터셋 한글화 및 한국 메뉴 추가, 컬럼 분리")
    df_drink = pd.read_csv("data/menu_data.csv", index_col=0)
    
    # 데이터프레임 출력
    st.dataframe(df_drink.loc[:, :'카페인 (mg)'], use_container_width=True)

    st.markdown("---")

    # 최대/최소 데이터 확인
    st.info("📌 **각 영양성분별 TOP 5 메뉴는?**")

    menu = ["칼로리 (kcal)", "당류 (g)", "단백질 (g)", "나트륨 (mg)", "포화지방 (g)", "카페인 (mg)"]
    selected_column = st.selectbox("📌 아래 옵션을 선택하고 결과를 확인하세요!", menu)

    # 최댓값 데이터
    st.markdown(f"✅ **고{selected_column} 음료 TOP 5**")
    st.dataframe(df_drink.loc[:, :'카페인 (mg)'].groupby("음료명", as_index=True).max().nlargest(5, selected_column))

    # 최솟값 데이터
    st.markdown(f"✅ **저{selected_column} 음료 TOP 5**")
    st.dataframe(df_drink.loc[:, :'카페인 (mg)'].groupby("음료명", as_index=True).max().nsmallest(5, selected_column))

    st.markdown("---")

    st.markdown(
        "<h3 style='text-align: center; font-weight: bold;'>마음의 준비가 되셨다면, 이제 주문을 해볼까요?</h3>",
        unsafe_allow_html=True
    )

    # 주문 옵션 고르고 주문하기 버튼 누르기
    st.info("📌 **주문 옵션을 선택하고 주문하기 버튼을 눌러주세요!**")

    # 주문 옵션 선택
    st.markdown("### 📝 주문 옵션 선택")

    check_login()

    if not st.session_state.logged_in:

        st.error("로그인이 필요한 서비스입니다. 로그인해주세요.")

        df_user = pd.read_csv('data/user_data.csv')

        if st.session_state.register_mode:
            st.title("📝 회원가입")
            new_username = st.text_input("이름", value="", key="new_username")
            new_id = st.text_input("ID", value="", key="new_id")
            
            if new_id in df_user['ID'].values:
                st.error("❌ 이미 존재하는 ID입니다.")
            
            new_password = st.text_input("새 비밀번호", type="password", value="", key="new_password")
            confirm_password = st.text_input("비밀번호 확인", type="password", value="", key="confirm_password")
            
            if st.button("회원가입 완료"):
                if new_password != confirm_password:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                elif new_id and new_password:
                    new_row = pd.DataFrame([{"이름": new_username, "ID": str(new_id), "비밀번호": str(new_password)}])
                    df_user = pd.concat([df_user, new_row], ignore_index=True)
                    df_user.to_csv('data/user_data.csv', index=False)
                    st.success("✅ 회원가입이 완료되었습니다! 로그인해주세요.")
                    st.session_state.register_mode = False
                    time.sleep(1)
                    st.rerun()
            
            if st.button("뒤로 가기"):
                st.session_state.register_mode = False
                st.rerun()
        
        else:
            st.title("🔐 로그인")
            id = st.text_input("ID", value=st.session_state.user_id, key="username")  # ID 유지
            password = st.text_input("비밀번호", type="password", value="", key="password")

            if st.button("로그인"):
                if id in df_user['ID'].values:
                    if df_user.loc[df_user['ID'] == id, '비밀번호'].values[0] == password:
                        st.session_state.logged_in = True
                        st.session_state.user_id = id
                        name = df_user.loc[df_user['ID'] == id, '이름'].values[0]
                        st.session_state.user_name = name
                        st.success(f"{name}님, 환영합니다! 🎉")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ 비밀번호가 일치하지 않습니다.")   
                else:
                    st.error("❌ 아이디가 존재하지 않습니다.")
            
            if st.button("회원가입"):
                st.session_state.register_mode = True
                st.rerun()

    else :
        id = st.session_state.user_id

        drink_menu = ["-", "콜드 브루 커피", "에스프레소", "브루드 커피", "프라푸치노", "블렌디드", "스타벅스 리프레셔",
                    "스타벅스 피지오", "티(티바나)", "기타 제조 음료", "스타벅스 주스(병음료)"]
        
        category = st.selectbox("음료 유형 선택", drink_menu)   
        drink = st.selectbox("음료 선택", ["-"] + df_drink.loc[df_drink.index == category, '음료명'].drop_duplicates().values.tolist())
        size = st.selectbox("사이즈 선택", ["-"] + df_drink.loc[df_drink['음료명'] == drink, '사이즈'].values.tolist())
        
        is_button_enabled = category != "-" and drink != "-" and size != "-"

        if is_button_enabled :
            st.dataframe(df_drink.loc[(df_drink['음료명'] == drink) & (df_drink['사이즈'] == size), '음료명':'카페인 (mg)'].set_index('음료명'))
            if st.button("주문하기") :    
                df_log = pd.read_csv('data/order_data.csv')
                if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == drink) & (df_log['사이즈'] == size)].empty :
                    dairy = df_drink.loc[df_drink['음료명'] == drink, '유제품'].values[0]
                    data = [[id, drink, size, dairy, 1]]
                    df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                    df_log.to_csv('data/order_data.csv', index=False)
                else :
                    df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == drink) & (df_log['사이즈'] == size), '주문 수'] += 1
                    df_log.to_csv('data/order_data.csv', index=False)

                st.success(f"{drink} 주문이 완료되었습니다! ☕️")

            st.markdown("---")
            
            st.info("""
                어떤 음료를 골라야 할지 고민이라면? 🤔 \n\n
                상단의 **음료 추천 받기** 탭을 클릭해 음료를 추천받으세요! 🎉
                    """)