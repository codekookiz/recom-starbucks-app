import streamlit as st
import pandas as pd
import numpy as np
import time


def run_recom() :
    
    def check_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'register_mode' not in st.session_state:
            st.session_state.register_mode = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = ""

        
    st.markdown(
    """
    <h2 style="text-align: center; color: #FF4B4B;">
        ☕️ 오늘은 무슨 음료를 마실까?
    </h2>
    <p style="font-size: 24px; text-align: center; color: ##4C82C2;">
        <b>딥러닝 (DL) 데이터를 참고한 음료 추천<b>
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown("---")

    # 큰 제목
    st.markdown('<p style="font-size: 24px; font-weight: bold; color: #333; font-family: Arial, sans-serif;">👆 스타벅스 맞춤 음료 추천</p>', unsafe_allow_html=True)

    # 정보 박스 스타일
    st.markdown('<p style="font-size: 16px; color: #555; font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 15px; border-radius: 8px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1);">아래의 옵션을 선택하시면 오늘의 음료를 추천해드립니다.</p>', unsafe_allow_html=True)
    st.text('')

    if st.button('❓ 음료 추천 예시') :
        col1, col2, col3 = st.columns(3)
        with col1 :
            st.image('image/result_a.png')
        with col2 :
            st.image('image/result_b.png')
        with col3 :
            st.image('image/result_c.png')
            

    # 하위 제목
    st.markdown('<p style="font-size: 22px; font-weight: bold; color: #333; font-family: Arial, sans-serif; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;">📌 당신의 선택은?</p>', unsafe_allow_html=True)
    st.text('')

    check_login()

    if not st.session_state.logged_in:

        st.error("로그인이 필요한 서비스입니다. 로그인해주세요.")

        df_user = pd.read_csv('data/user_data.csv')

        if st.session_state.register_mode:
            st.title("📝 회원가입")
            new_username = st.text_input("이름", value="", key="new_username_recom")
            new_id = st.text_input("ID", value="", key="new_id_recom")
            
            if new_id in df_user['ID'].values:
                st.error("❌ 이미 존재하는 ID입니다.")
            
            new_password = st.text_input("새 비밀번호", type="password", value="", key="new_password_recom")
            confirm_password = st.text_input("비밀번호 확인", type="password", value="", key="confirm_password_recom")
            
            if st.button("회원가입 완료", key="register"):
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
            
            if st.button("뒤로 가기", key="back"):
                st.session_state.register_mode = False
                st.rerun()
        
        else:
            st.title("🔐 로그인")
            id = st.text_input("ID", value=st.session_state.user_id, key="username_recom")  # ID 유지
            password = st.text_input("비밀번호", type="password", value="", key="password_recom")

            if st.button("로그인", key="login"):
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
            
            if st.button("회원가입", key="register"):
                st.session_state.register_mode = True
                st.rerun()

    else:
        id = st.session_state.user_id

        df_log = pd.read_csv('data/order_data.csv')
        df_drink = pd.read_csv('data/menu_data.csv')

        option_d = ['-', '늘 먹던 걸로.', '피곤해요.. 혈중 카페인 농도 부족!', '그냥 아주 달달한 거 주세요.',
                    '죄책감은 최소로! 맛은 그대로!', '오늘은 새로운 게 궁금해!']
        option_m = ["-", "빼주세요.", "우유 든 걸로!"]

        choice = st.selectbox('오늘의 선택은?', option_d)

        col1, col2 = st.columns(2)
        with col1 :
            type = st.selectbox('유제품 선택?', option_m)
        with col2 :
            option_s = []
            if type == '빼주세요.' :
                type = 'X'
                option_s = ["-"] +  sorted(df_drink.loc[df_drink['유제품'] == type, '사이즈'].drop_duplicates().values.tolist(),
                                    key=lambda x: x != "One Size")
            elif type == '우유 든 걸로!' :
                type = 'O'
                option_s = ["-"] + sorted(df_drink.loc[df_drink['유제품'] == type, '사이즈'].drop_duplicates().values.tolist(),
                                    key=lambda x: x != "One Size")
            size = st.selectbox('사이즈는?', option_s)
            
        is_button_enabled = choice != "-" and type != "-" and size != "-"

        if is_button_enabled :
            time.sleep(1)
            selected = False
            answer = False

            # 익숙한 맛
            if choice == option_d[1] :
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size) & (df_log['유제품'] == type), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    st.success(f"""
                                늘 한결 같은 당신, 오늘도
                                {size} 사이즈 {my_num1[0]}로
                                드리면 될까요?
                                """)
                    if st.button('이거 마실래요!') :
                        selected = True
                        answer = True
                        if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size)].empty :
                            dairy = df_drink.loc[df_drink['음료명'] == my_num1[0], '유제품'].values[0]
                            data = [[id, my_num1[0], size, dairy, 1]]
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                        else :
                            df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size), '주문 수'] += 1
                            df_log.to_csv('data/order_data.csv', index=False)
                else :
                    st.info('이 조합의 음료는 처음이시네요.')
                    answer = True
                if selected & answer :
                    st.success('주문이 완료되었습니다. 제 추천이 마음에 드시길 바래요!')

            # 카페인 부족
            elif choice == option_d[2] :
                mean_caffeine = df_drink['카페인 (mg)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size) & (df_log['유제품'] == type), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['음료명'] == my_num1[0], :]
                    if my_num1_data['카페인 (mg)'].values[0] >= mean_caffeine :
                        st.success(f"""
                                카페인이 부족한 오늘,\n\n
                                {size} 사이즈 {my_num1[0]}로\n\n
                                힘내보는 건 어때요?
                                """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈'] == my_num1[1]), '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == my_num1[0], '유제품'].values[0]
                                data = [[id, my_num1[0], size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                if my_drinks.empty or my_num1_data['카페인 (mg)'].values[0] < mean_caffeine :
                    df_drink = df_drink.loc[(df_drink['사이즈'] == size) & (df_drink['카페인 (mg)'] >= mean_caffeine)  & (df_drink['유제품'] == type), :]
                    caffeine_order = df_drink['카페인 (mg)'].sort_values(ascending=False).values.tolist()
                    if caffeine_order :
                        best_caffeine = caffeine_order[0]
                        ideal_drinks = df_drink.loc[df_drink['카페인 (mg)'] == best_caffeine, :].reset_index()
                        final_drink = ideal_drinks.loc[0, '음료명']
                        st.success(f"""
                                    카페인이 부족한 오늘,\n\n
                                    {size} 사이즈 {final_drink}로\n\n
                                    힘내보는 건 어때요?
                                    """)
                        st.dataframe(ideal_drinks.loc[[0], '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == final_drink, '유제품'].values[0]
                                data = [[id, final_drink, size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                    else :
                        st.info('선택하신 옵션의 메뉴 중 카페인 함량이 높은 음료가 없습니다. 새로운 옵션을 선택해주세요.')
                if selected & answer :
                    st.success('주문이 완료되었습니다. 제 추천이 마음에 드시길 바래요!')

            # 달달한 거
            elif choice == option_d[3] :
                mean_sugar = df_drink['당류 (g)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size) & (df_log['유제품'] == type), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['음료명'] == my_num1[0], :]
                    if my_num1_data['당류 (g)'].values[0] >= mean_sugar :
                        st.success(f"""
                                    달달한 거 너무 좋죠,\n\n
                                    {size} 사이즈 {my_num1[0]}\n\n
                                    어때요?
                                    """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈'] == my_num1[1]), '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == my_num1[0], '유제품'].values[0]
                                data = [[id, my_num1[0], size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                if my_drinks.empty or my_num1_data['당류 (g)'].values[0] < mean_sugar :
                    df_drink = df_drink.loc[(df_drink['사이즈'] == size) & (df_drink['당류 (g)'] >= mean_sugar)  & (df_drink['유제품'] == type), :]
                    sugar_order = df_drink['당류 (g)'].sort_values(ascending=False).values.tolist()
                    if sugar_order :
                        best_sugar = sugar_order[0]
                        ideal_drinks = df_drink.loc[df_drink['당류 (g)'] == best_sugar, :].reset_index()
                        final_drink = ideal_drinks.loc[0, '음료명']
                        st.success(f"""
                                    달달한 거 너무 좋죠,\n\n
                                    {size} 사이즈 {final_drink}\n\n
                                    어때요?
                                    """)
                        st.dataframe(ideal_drinks.loc[[0], '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == final_drink, '유제품'].values[0]
                                data = [[id, final_drink, size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                    else :
                        st.info('선택하신 옵션의 메뉴 중 당류 함량이 높은 음료가 없습니다. 새로운 옵션을 선택해주세요.')
                if selected & answer :
                    st.success('주문이 완료되었습니다. 제 추천이 마음에 드시길 바래요!')

            # 저칼로리
            elif choice == option_d[4] :
                mean_calorie = df_drink['칼로리 (kcal)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size) & (df_log['유제품'] == type), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmin()
                    my_num1_data = df_drink.loc[df_drink['음료명'] == my_num1[0], :]
                    if my_num1_data['칼로리 (kcal)'].values[0] < mean_calorie :
                        st.success(f"""
                                    칼로리 걱정 말고,\n\n
                                    {size} 사이즈 {my_num1[0]}로\n\n
                                    주문하세요!
                                    """)
                        st.dataframe(df_drink.loc[(df_drink['음료명'] == my_num1[0]) & (df_drink['사이즈'] == my_num1[1]), '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_my_{my_num1}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == my_num1[0], '유제품'].values[0]
                                data = [[id, my_num1[0], size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == my_num1[0]) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                if my_drinks.empty or my_num1_data['칼로리 (kcal)'].values[0] >= mean_calorie :
                    df_drink = df_drink.loc[(df_drink['사이즈'] == size) & (df_drink['칼로리 (kcal)'] <= mean_calorie)  & (df_drink['유제품'] == type), :]
                    calorie_order = df_drink['칼로리 (kcal)'].sort_values().values.tolist()
                    if calorie_order :
                        best_calorie = calorie_order[0]
                        ideal_drinks = df_drink.loc[df_drink['칼로리 (kcal)'] == best_calorie, :].reset_index()
                        final_drink = ideal_drinks.loc[0, '음료명']
                        st.success(f"""
                                    칼로리 걱정 말고,\n\n
                                    {size} 사이즈 {final_drink}로\n\n
                                    주문하세요!
                                    """)
                        st.dataframe(ideal_drinks.loc[[0], '음료명':'카페인 (mg)'].set_index('음료명'))
                        st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                        if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                            selected = True
                            answer = True
                            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size)].empty :
                                dairy = df_drink.loc[df_drink['음료명'] == final_drink, '유제품'].values[0]
                                data = [[id, final_drink, size, dairy, 1]]
                                df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                                df_log.to_csv('data/order_data.csv', index=False)
                            else :
                                df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size), '주문 수'] += 1
                                df_log.to_csv('data/order_data.csv', index=False)
                    else :
                        st.info('선택하신 옵션의 메뉴 중 칼로리가 낮은 음료가 없습니다. 새로운 옵션을 선택해주세요.')
                if selected & answer :
                    st.success('주문이 완료되었습니다. 제 추천이 마음에 드시길 바래요!')
                
            # 신규 추천
            elif choice == option_d[5] : 
                new_df = df_drink.loc[(df_drink['유제품'] == type) & (df_drink['사이즈'] == size), :]
                not_my_drinks = new_df.loc[~new_df['음료명'].isin(df_log.loc[df_log['ID'] == id, '음료명'])]
                not_my_drinks.sort_values(by='추천 점수', ascending=False, inplace=True)
                if not_my_drinks.empty :
                    st.info('선택하신 옵션과 일치하는 새로운 음료가 없습니다. 새로운 옵션을 선택해주세요.')
                else :
                    random_drink = not_my_drinks.sample()
                    final_drink = random_drink['음료명'].values[0]
                    st.success(f"""
                                오늘은\n\n
                               {size} 사이즈 {final_drink}로\n\n
                                새로운 음료를 시도해보는 건 어떨까요?
                                """)
                    st.dataframe(df_drink.loc[(df_drink['음료명'] == final_drink) & (df_drink['사이즈'] == size), '음료명':'카페인 (mg)'].set_index('음료명'))
                    st.text("아래의 '이거 마실래요!' 버튼을 클릭해 당신의 선택지를 저장하고, 더욱 정확한 예측을 받아보세요!")
                    if st.button('이거 마실래요!', key=f"O_one_{final_drink}") :
                        selected = True
                        answer = True
                        if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size)].empty :
                            dairy = df_drink.loc[df_drink['음료명'] == final_drink, '유제품'].values[0]
                            data = [[id, final_drink, size, dairy, 1]]
                            df_log = pd.concat([df_log, pd.DataFrame(data, columns=df_log.columns)], ignore_index=True)
                            df_log.to_csv('data/order_data.csv', index=False)
                        else :
                            df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == final_drink) & (df_log['사이즈'] == size), '주문 수'] += 1
                            df_log.to_csv('data/order_data.csv', index=False)
                if selected & answer :
                    st.success('주문이 완료되었습니다. 제 추천이 마음에 드시길 바래요!')
            st.info('상단 박스를 조정하여 새로운 추천을 받아보세요!')