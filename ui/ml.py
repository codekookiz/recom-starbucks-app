import streamlit as st
import pandas as pd
import numpy as np
import time

def run_ml() :

    def check_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'register_mode' not in st.session_state:
            st.session_state.register_mode = False
        if 'user_id' not in st.session_state:  # 로그인한 ID 저장
            st.session_state.user_id = ""

    check_login()

    if not st.session_state.logged_in:
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
                        st.success(f"{df_user.loc[df_user['ID'] == id, '이름'].values[0]}님, 환영합니다! 🎉")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ 비밀번호가 일치하지 않습니다.")   
                else:
                    st.error("❌ 아이디가 존재하지 않습니다.")
            
            if st.button("회원가입"):
                st.session_state.register_mode = True
                st.rerun()

    else:
        id = st.session_state.user_id

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
        st.markdown('<p style="font-size: 24px; font-weight: bold; color: #333; font-family: Arial, sans-serif;">🎞️ ML 기반 스타벅스 맞춤 음료 추천</p>', unsafe_allow_html=True)

        # 정보 박스 스타일
        st.markdown('<p style="font-size: 16px; color: #555; font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 15px; border-radius: 8px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1);">아래의 옵션을 선택시면 오늘의 음료를 추천해드립니다.</p>', unsafe_allow_html=True)
        st.text('')

        if st.button('❓ 음료 추천 예시') :
            col1, col2 = st.columns(2)
            with col1 :
                st.image('image/result_a.png')
            with col2 :
                st.image('image/result_b.png')

        # 하위 제목
        st.markdown('<p style="font-size: 22px; font-weight: bold; color: #333; font-family: Arial, sans-serif; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;">📌 당신의 선택은?</p>', unsafe_allow_html=True)
        st.text('')

        option_d = ['-', '늘 먹던 걸로.', '피곤해요.. 혈중 카페인 농도 부족!', '그냥 아주 달달한 거 주세요.',
                    '죄책감은 최소로! 맛은 그대로!', '오늘은 새로운 게 궁금해!']
        option_m = ["-", "없음", '무지방 우유', "저지방 우유", "두유", "일반 우유"]

        choice = st.selectbox('오늘의 선택은?', option_d)

        col1, col2 = st.columns(2)
        with col1 :
            type = st.selectbox('유제품 선택?', option_m)
        with col2 :
            option_s = []
            if type == '없음' :
                option_s = ["-", "Solo", "Doppio", "Short", "Tall", "Grande", "Venti"]
            if type in ['무지방 우유', '저지방 우유', '두유'] :
                option_s = ["-", "Short", "Tall", "Grande", "Venti"]
            if type == '일반 우유' :
                option_s = ["-", "Tall", "Grande", "Venti"]
            size = st.selectbox('사이즈는?', option_s)
            
        is_button_enabled = choice != "-" and type != "-" and size != "-"

        if is_button_enabled :
            time.sleep(1)
            df_log = pd.read_csv('data/order_data.csv')
            df_drink = pd.read_csv('data/menu_data.csv')
            selected = False
            answer = False

            if type == "없음" :
                print_size = f"{size} "
            else :
                print_size = f"{type}가 들어간 {size} "
                size = f"{size} {type}"

            # 익숙한 맛
            if choice == option_d[1] :
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    st.success(f"""
                               늘 한결 같은 당신, 오늘도
                               {print_size} 사이즈 {my_num1[0]}로
                               드리면 될까요?
                               """)
                    col1, col2 = st.columns(2)
                    with col1 :
                        if st.button('이거 마실래요!') :
                            selected = True
                            answer = True
                            data = np.array([id, my_num1[0], size]).reshape(1, 3)
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                    with col2 :
                        if st.button('다시 고민해보실래요?') :
                            answer = True
                else :
                    st.info('이 조합의 음료는 처음이시네요. 음료를 추천해드릴까요?')
                    if st.button('다른 음료 추천 받기') :
                        answer = True
                if selected & answer :
                     st.success('제 추천이 마음에 드시길 바래요!')
                elif answer :
                    st.info('상단 박스를 조정하여 새로운 추천을 받아보세요!')

            # 카페인 부족
            elif choice == option_d[2] :
                mean_caffeine = df_drink['카페인 (mg)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈 및 유제품'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['Beverage'] == my_num1[0], :]
                    if my_num1_data['카페인 (mg)'].values[0] >= mean_caffeine :
                        st.success(f"""
                               카페인이 부족한 오늘,\n\n
                               {print_size} 사이즈 {my_num1[0]}로\n\n
                               힘내보는 건 어때요?
                               """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈 및 유제품'] == my_num1[1]), 'Beverage':].set_index('Beverage'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            data = np.array([id, my_num1[0], size]).reshape(1, 3)
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                        if st.button('다시 고민해보실래요?') :
                            answer = True
                if my_drinks.empty or my_num1_data['카페인 (mg)'].values[0] < mean_caffeine :
                    df_drink = df_drink.loc[df_drink['사이즈 및 유제품'] == size, :]
                    caffeine_order = df_drink['카페인 (mg)'].sort_values(ascending=False).values.tolist()
                    best_caffeine = caffeine_order[0]
                    ideal_drinks = df_drink.loc[df_drink['카페인 (mg)'] == best_caffeine, :].reset_index()
                    final_drink = ideal_drinks.loc[0, '음료명']
                    st.success(f"""
                               카페인이 부족한 오늘,\n\n
                               {print_size} 사이즈 {final_drink}로\n\n
                               힘내보는 건 어때요?
                               """)
                    st.dataframe(ideal_drinks.loc[[0], '음료명':].set_index('음료명'))
                    st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                    if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                        selected = True
                        answer = True
                        data = np.array([id, final_drink, size]).reshape(1, 3)
                        df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                        df_log.to_csv('data/order_data.csv', index=False)
                    if st.button('다시 고민해보실래요?') :
                        answer = True
                if selected & answer :
                     st.success('제 추천이 마음에 드시길 바래요!')
                elif answer :
                    st.info('상단 박스를 조정하여 새로운 추천을 받아보세요!')

            # 달달한 거
            elif choice == option_d[3] :
                mean_sugar = df_drink['당류 (g)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈 및 유제품'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['음료명'] == my_num1[0], :]
                    if my_num1_data['당류 (g)'].values[0] >= mean_sugar :
                        st.success(f"""
                                   달달한 거 너무 좋죠,\n\n
                                   {print_size} 사이즈 {my_num1[0]}\n\n
                                   한 잔 어때요?
                                   """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈 및 유제품'] == my_num1[1]), '음료명':].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            data = np.array([id, my_num1[0], size]).reshape(1, 3)
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                        if st.button('다시 고민해보실래요?') :
                            answer = True
                if my_drinks.empty or my_num1_data['당류 (g)'].values[0] < mean_sugar :
                    df_drink = df_drink.loc[df_drink['사이즈 및 유제품'] == size, :]
                    sugar_order = df_drink['당류 (g)'].sort_values(ascending=False).values.tolist()
                    best_sugar = sugar_order[0]
                    ideal_drinks = df_drink.loc[df_drink['당류 (g)'] == best_sugar, :].reset_index()
                    final_drink = ideal_drinks.loc[0, '음료명']
                    st.success(f"""
                               달달한 거 너무 좋죠,\n\n
                               {print_size} 사이즈 {final_drink}\n\n
                               한 잔 어때요?
                               """)
                    st.dataframe(ideal_drinks.loc[[0], '음료명':].set_index('음료명'))
                    st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                    if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                        selected = True
                        answer = True
                        data = np.array([id, final_drink, size]).reshape(1, 3)
                        df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                        df_log.to_csv('data/order_data.csv', index=False)
                    if st.button('다시 고민해보실래요?') :
                        answer = True
                if selected & answer :
                     st.success('제 추천이 마음에 드시길 바래요!')
                elif answer :
                    st.info('상단 박스를 조정하여 새로운 추천을 받아보세요!')

            # 저칼로리
            elif choice == option_d[4] :
                mean_calorie = df_drink['열량'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈 및 유제품'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmin()
                    my_num1_data = df_drink.loc[df_drink['음료명'] == my_num1[0], :]
                    if my_num1_data['열량'].values[0] <= mean_calorie :
                        st.success(f"""
                                   칼로리 걱정 말고,\n\n
                                   {print_size} 사이즈 {my_num1[0]}로\n\n
                                   주문하세요!
                                   """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈 및 유제품'] == my_num1[1]), '음료명':].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            data = np.array([id, my_num1[0], size]).reshape(1, 3)
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                        if st.button('다시 고민해보실래요?') :
                            answer = True
                if my_drinks.empty or my_num1_data['열량'].values[0] > mean_calorie :
                    df_drink = df_drink.loc[df_drink['사이즈 및 유제품'] == size, :]
                    calorie_order = df_drink['열량'].sort_values().values.tolist()
                    best_calorie = calorie_order[0]
                    ideal_drinks = df_drink.loc[df_drink['열량'] == best_calorie, :].reset_index()
                    final_drink = ideal_drinks.loc[0, '음료명']
                    st.success(f"""
                               칼로리 걱정 말고,\n\n
                               {print_size} 사이즈 {final_drink}로\n\n
                               주문하세요!
                               """)
                    st.dataframe(ideal_drinks.loc[[0], '음료명':].set_index('음료명'))
                    st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                    if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                        selected = True
                        answer = True
                        data = np.array([id, final_drink, size]).reshape(1, 3)
                        df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                        df_log.to_csv('data/order_data.csv', index=False)
                    if st.button('다시 고민해보실래요?') :
                        answer = True
                if selected & answer :
                     st.success('제 추천이 마음에 드시길 바래요!')
                elif answer :
                    st.info('상단 박스를 조정하여 새로운 추천을 받아보세요!')
                
            # 신규 추천
            elif choice == option_d[5] : 
                pass

