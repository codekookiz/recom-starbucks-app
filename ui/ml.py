import streamlit as st
import pandas as pd
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

        option_d = ['늘 먹던 걸로.', '피곤해요.. 혈중 카페인 농도 부족!', '그냥 아주 달달한 거 주세요.',
                    '죄책감은 최소로! 맛은 그대로!', '오늘은 새로운 게 궁금해!']
        option_s = ['Short', 'Tall', 'Grande', 'Venti', 'Short Nonfat Milk', '2% Milk', 'Soymilk', 'Tall Nonfat Milk',
                    'Grande Nonfat Milk', 'Venti Nonfat Milk', 'Solo', 'Doppio', 'Whole Milk']

        col1, col2 = st.columns(2)
        with col1 :
            choice = st.selectbox('오늘의 선택은?', option_d)
        with col2 :
            size = st.selectbox('사이즈는?', option_s)

        if st.button('음료 추천 받기') :
            df_log = pd.read_csv('data/order_data.csv')
            df_drink = pd.read_csv('data/menu_data.csv')
            if 'selected' not in st.session_state:
                st.session_state.selected = False

            # 익숙한 맛
            if choice == option_d[0] :
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    st.success(f'늘 한결 같은 당신, 오늘도 {size} 사이즈 {my_num1[0]}로 드리면 될까요?')
                    if st.button('이거 마실래요!') :
                        st.session_state.selected = True
                        st.rerun()
                    elif st.button('다시 고민해볼래요.') :
                        st.session_state.selected = False
                        st.rerun()
                else :
                    st.error('첫 주문이시네요. 음료를 추천해드릴까요?')
                    if st.button('다시 음료 추천 받기') :
                        st.rerun()
                if st.session_state.selected :
                     st.success('제 추천이 마음에 드시길 바래요!')

            # 카페인 부족
            elif choice == option_d[1] :
                mean_caffeine = df_drink['Caffeine (mg)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['Beverage'] == my_num1[0], :]
                    if my_num1_data['Caffeine (mg)'].values[0] >= mean_caffeine :
                        st.success(f'카페인이 부족한 오늘, {size} 사이즈 {my_num1[0]}로 힘내보는 건 어때요?')
                        if st.button('이거 마실래요!') :
                            st.session_state.selected = True
                            st.rerun()
                        elif st.button('다른 건 없어요?') :
                            st.session_state.selected = False
                            pass
                if df_log.loc[df_log['ID'] == id, '음료명':] is None or my_num1_data['Caffeine (mg)'].values[0] < mean_caffeine :
                    caffeine_order = df_drink['Caffeine (mg)'].sort_values(ascending=False).values.tolist()
                    for i in caffeine_order :
                        ideal_drinks = df_drink.loc[(df_drink['Caffeine (mg)'] == i) & (df_drink['Beverage_prep'] == size), :].reset_index()
                        if isinstance(ideal_drinks, pd.DataFrame) :
                            for j in range(len(ideal_drinks)) :
                                best_drink = ideal_drinks[j]
                                st.success(f'카페인이 부족한 오늘, {size} 사이즈 {best_drink['Beverage'].values[0]}로 힘내보는 건 어때요?')
                                if st.button('이거 마실래요!') :
                                    st.session_state.selected = True
                                    st.rerun()
                                elif st.button('다른 건 없어요?') :
                                    st.session_state.selected = False
                                    pass
                                if st.session_state.selected :
                                    break
                        else :
                            st.success(f'카페인이 부족한 오늘, {size} 사이즈 {ideal_drinks['Beverage'].values[0]}로 힘내보는 건 어때요?')
                            if st.button('이거 마실래요!') :
                                st.session_state.selected = True
                                st.rerun()
                            elif st.button('다른 건 없어요?') :
                                st.session_state.selected = False
                                pass
                        if st.session_state.selected :
                            break
                if st.session_state.selected :
                     st.success('제 추천이 마음에 드시길 바래요!')
                else :
                    st.error('추천해드릴 음료가 없어요. 다시 고민해보실래요?')
                    if st.button('다시 선택하기') :
                        st.rerun()

            # 달달한 거
            elif choice == option_d[2] :
                mean_sugar = df_drink['Sugars (g)'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['Beverage'] == my_num1[0], :]
                    if my_num1_data['Sugars (g)'].values[0] >= mean_sugar :
                        st.success(f'달달한 거 너무 좋죠, {size} 사이즈 {my_num1[0]} 한 잔 어때요?')
                        if st.button('이거 마실래요!') :
                            st.session_state.selected = True
                            st.rerun()
                        elif st.button('다른 건 없어요?') :
                            st.session_state.selected = False
                            pass
                if df_log.loc[df_log['ID'] == id, '음료명':] is None or my_num1_data['Sugars (g)'].values[0] < mean_sugar :
                    sugar_order = df_drink['Sugars (g)'].sort_values(ascending=False).values.tolist()
                    for i in sugar_order :
                        ideal_drinks = df_drink.loc[(df_drink['Sugars (g)'] == i) & (df_drink['Beverage_prep'] == size), :].reset_index()
                        if isinstance(ideal_drinks, pd.DataFrame) :
                            for j in range(len(ideal_drinks)) :
                                best_drink = ideal_drinks[j]
                                st.success(f'달달한 거 너무 좋죠, {size} 사이즈 {best_drink['Beverage'].values[0]} 한 잔 어때요?')
                                if st.button('이거 마실래요!') :
                                    st.session_state.selected = True
                                    st.rerun()
                                elif st.button('다른 건 없어요?') :
                                    st.session_state.selected = False
                                    pass
                                if st.session_state.selected :
                                    break
                        else :
                            st.success(f'달달한 거 너무 좋죠, {size} 사이즈 {ideal_drinks['Beverage'].values[0]} 한 잔 어때요?')
                            if st.button('이거 마실래요!') :
                                st.session_state.selected = True
                                st.rerun()
                            elif st.button('다른 건 없어요?') :
                                st.session_state.selected = False
                                pass
                        if st.session_state.selected :
                            break
                if st.session_state.selected :
                     st.success('제 추천이 마음에 드시길 바래요!')
                else :
                    st.error('추천해드릴 음료가 없어요. 다시 고민해보실래요?')
                    if st.button('다시 선택하기') :
                        st.rerun()

            # 저칼로리
            elif choice == option_d[3] :
                mean_calorie = df_drink['Calories'].mean()
                my_drinks = df_log.loc[(df_log['ID'] == id) & (df_log['사이즈'] == size), '음료명':]
                if not my_drinks.empty :
                    my_num1 = my_drinks.value_counts().idxmax()
                    my_num1_data = df_drink.loc[df_drink['Beverage'] == my_num1[0], :]
                    if my_num1_data['Calories'].values[0] >= mean_calorie :
                        st.success(f'칼로리 걱정 말고 {size} 사이즈 {my_num1[0]}로 주문하세요!')
                        if st.button('이거 마실래요!') :
                            st.session_state.selected = True
                            st.rerun()
                        elif st.button('다른 건 없어요?') :
                            st.session_state.selected = False
                            pass
                if df_log.loc[df_log['ID'] == id, '음료명':] is None or my_num1_data['Calories'].values[0] < mean_calorie :
                    calorie_order = df_drink['Calories'].sort_values(ascending=False).values.tolist()
                    for i in calorie_order :
                        ideal_drinks = df_drink.loc[(df_drink['Calories'] == i) & (df_drink['Beverage_prep'] == size), :].reset_index()
                        if isinstance(ideal_drinks, pd.DataFrame) :
                            for j in range(len(ideal_drinks)) :
                                best_drink = ideal_drinks[j]
                                st.success(f'칼로리 걱정 말고 {size} 사이즈 {best_drink['Beverage'].values[0]}로 주문하세요!')
                                if st.button('이거 마실래요!') :
                                    st.session_state.selected = True
                                    st.rerun()
                                elif st.button('다른 건 없어요?') :
                                    st.session_state.selected = False
                                    pass
                                if st.session_state.selected :
                                    break
                        else :
                            st.success(f'칼로리 걱정 말고 {size} 사이즈 {ideal_drinks['Beverage'].values[0]}로 주문하세요!')
                            if st.button('이거 마실래요!') :
                                st.session_state.selected = True
                                st.rerun()
                            elif st.button('다른 건 없어요?') :
                                st.session_state.selected = False
                                pass
                        if st.session_state.selected :
                            break
                if st.session_state.selected :
                     st.success('제 추천이 마음에 드시길 바래요!')
                else :
                    st.error('추천해드릴 음료가 없어요. 다시 고민해보실래요?')
                    if st.button('다시 선택하기') :
                        st.rerun()

            # 신규 추천
            else : 
                pass




        #classifier = joblib.load('model/classifier.pkl')

        #mpaa_dict = {'전체 관람가': 0, '12세 이상 관람가': 1, '15세 이상 관람가': 2, '청소년 관람 불가': 3}
        #genre_dict = {
        #    '액션': 0, '어드벤처': 1, '블랙 코미디': 2, '코미디': 3, '드라마': 4,
        #    '호러': 5, '뮤지컬': 6, '로맨틱 코미디': 7, '스릴러/서스펜스': 8, '서부극': 9
        #}

        #data_classify = np.array([cost, mpaa_dict[mpaa], genre_dict[genre], runtime, year]).reshape(1, 5)
        #new_data_classify = pd.DataFrame(data_classify)

        #st.text('')

                #st.markdown('<p class="sub-header">🔍 예측 결과</p>', unsafe_allow_html=True)

                #pred_group = classifier.predict(new_data_classify)

                #label_group = {0: '미들 마켓', 1: '메가 블록버스터', 2: '블록버스터'}[pred_group[0]]
                #st.success(f'🎬 영화 **"{title}"** 은(는) **{label_group}** 영화군요!')
                
                #with st.spinner('⏳ 수익 예측을 실시하는 중...'):
                #    time.sleep(2)

                #    regressor = joblib.load('model/regressor.pkl')
                #    data_predict = np.array([cost, opening, mpaa_dict[mpaa], genre_dict[genre], runtime, year]).reshape(1, 6)
                #    pred_profit = regressor.predict(data_predict)[0][0]
                #    pred_dom_profit = int(pred_profit.round())

                #    if pred_dom_profit >= 0:
                #        new_dom_profit = format(pred_dom_profit, ',')
                #        st.subheader(f'📈 예상 북미 박스오피스 수익: **{new_dom_profit} 달러**')

                #        time.sleep(1)

                #        wrld_dom_ratio = 2.7
                #        pred_wrld_profit = int((pred_profit * wrld_dom_ratio).round())
                #        new_wrld_profit = format(pred_wrld_profit, ',')
                #        st.subheader(f'🌍 예상 전세계 박스오피스 수익: **{new_wrld_profit} 달러**')

                #        save_df = pd.read_csv('data/result.csv')
                #        new_row = pd.DataFrame([{"영화명":title, "개봉 연도":int(year), "상영 시간":int(runtime), "상영 등급":mpaa, "장르":genre,
                #                                "제작 비용 ($)":int(cost), "개봉 주말 수익 ($)":int(opening), "유형":label_group, "북미 예상 수익 ($)":int(pred_dom_profit),
                #                                "전세계 예상 수익 ($)":int(pred_wrld_profit)}])
                #        print(new_row)

                #        save_df = pd.concat([save_df, new_row], ignore_index=True)
                #        save_df.to_csv('data/result.csv', index=False)

                #    else:
                #        st.error('❌ 예측이 불가능한 데이터입니다.')