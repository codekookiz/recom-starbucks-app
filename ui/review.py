from transformers import MarianTokenizer, MarianMTModel
from transformers import pipeline
import torch
import streamlit as st
import pandas as pd
import time
import os
from huggingface_hub import InferenceClient
from huggingface_hub import login


@st.cache_resource
def load_translation_model():
    model_name = "Helsinki-NLP/opus-mt-ko-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)


def run_review():

    def check_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'register_mode' not in st.session_state:
            st.session_state.register_mode = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = ""
    
    def get_huggingface_token() :
        token = os.environ.get('HUGGINGFACE_API_TOKEN')
        if token is None :
            token = st.secrets.get('HUGGINGFACE_API_TOKEN')
        return token

    # 제목
    st.markdown(
        """
        <h2 style="text-align: center; color: #FF4B4B;">
            ☕️ 오늘의 음료, 어떠셨나요?
        </h2>
        <p style="font-size: 24px; text-align: center; color: ##4C82C2;">
            <b>사용자 리뷰 수집 및 딥러닝을 활용한 추천 시스템 개선<b>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.write("""
        오늘의 음료, 어떠셨나요? 🤔\n\n
        여러분이 남겨주시는 리뷰는 추천 시스템의 개선에 큰 도움이 됩니다! 🎉
        """)
    check_login()

    if not st.session_state.logged_in:

        st.error("로그인이 필요한 서비스입니다. 로그인해주세요.")

        df_user = pd.read_csv('data/user_data.csv')

        if st.session_state.register_mode:
            st.title("📝 회원가입")
            new_username = st.text_input("이름", value="", key="new_username_rv")
            new_id = st.text_input("ID", value="", key="new_id_rv")
            
            if new_id in df_user['ID'].values:
                st.error("❌ 이미 존재하는 ID입니다.")
            
            new_password = st.text_input("새 비밀번호", type="password", value="", key="new_password_rv")
            confirm_password = st.text_input("비밀번호 확인", type="password", value="", key="confirm_password_rv")
            
            if st.button("회원가입 완료", key="register_rv"):
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
            
            if st.button("뒤로 가기", key="back_rv"):
                st.session_state.register_mode = False
                st.rerun()
        
        else:
            st.title("🔐 로그인")
            id = st.text_input("ID", value=st.session_state.user_id, key="username_rv")  # ID 유지
            password = st.text_input("비밀번호", type="password", value="", key="password_rv")

            if st.button("로그인", key="login_rv"):
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
            
            if st.button("회원가입", key="register_mode_rv"):
                st.session_state.register_mode = True
                st.rerun()

    else :
        id = st.session_state.user_id
    
        df_drink = pd.read_csv('data/menu_data.csv', index_col=0)
        df_log = pd.read_csv('data/order_data.csv')

        drink_menu = ["-", "콜드 브루 커피", "에스프레소", "브루드 커피", "프라푸치노", "블렌디드", "스타벅스 리프레셔",
                        "스타벅스 피지오", "티(티바나)", "기타 제조 음료", "스타벅스 주스(병음료)"]
        
        category = st.selectbox("음료 유형 선택", drink_menu, key="category")   
        drink = st.selectbox("음료 선택", ["-"] + df_drink.loc[df_drink.index == category, '음료명'].drop_duplicates().values.tolist(), key="drink")
        size = st.selectbox("사이즈 선택", ["-"] + df_drink.loc[df_drink['음료명'] == drink, '사이즈'].values.tolist(), key="size")

        rating = st.radio("별점을 선택하세요:", options=[1, 2, 3, 4, 5],
                        format_func=lambda x: "⭐" * x, horizontal=True)
        review = st.text_area("리뷰를 작성해주세요.", height=100, key="review")

        if st.button("리뷰 제출") :
            if df_log.loc[(df_log['ID'] == id) & (df_log['음료명'] == drink) & (df_log['사이즈'] == size), :].empty :
                st.error("주문한 음료에 대한 리뷰만 작성할 수 있습니다.")
            else :
                df_review = pd.read_csv('data/review_data.csv')
                data = [[id, drink, size, rating, review]]
                prev_rating = 0
                prev_review = ""
                status = ""
                if df_review.loc[(df_review['ID'] == id) & (df_review['음료명'] == drink) & (df_review['사이즈'] == size)].empty :
                    df_review = pd.concat([df_review, pd.DataFrame(data, columns=df_review.columns)], ignore_index=True)
                    df_review.to_csv('data/review_data.csv', index=False)
                    st.success("리뷰가 성공적으로 제출되었습니다! 감사합니다. 🎉")
                    status = 'Create'
                else :
                    prev_rating = df_review.loc[(df_review['ID'] == id) & (df_review['음료명'] == drink) & (df_review['사이즈'] == size), '별점'].values[0]
                    df_review.loc[(df_review['ID'] == id) & (df_review['음료명'] == drink) & (df_review['사이즈'] == size), '별점'] = rating
                    prev_review = df_review.loc[(df_review['ID'] == id) & (df_review['음료명'] == drink) & (df_review['사이즈'] == size), '리뷰'].values[0]
                    df_review.loc[(df_review['ID'] == id) & (df_review['음료명'] == drink) & (df_review['사이즈'] == size), '리뷰'] = review
                    df_review.to_csv('data/review_data.csv', index=False)
                    st.success("리뷰가 성공적으로 수정되었습니다! 감사합니다. 🎉")
                    status = 'Update'

                login(token=get_huggingface_token())
                posneg = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", framework="pt")
                if status == 'Update':
                    tokenizer, model = load_translation_model()
                    prev_result = translate(prev_review, tokenizer, model)
                    prev_result = posneg(prev_result)
                    prev_result.sort(key=lambda x: x['score'], reverse=True)
                    prev_answer = prev_result[0]['label']
                    if prev_answer == 'POSITIVE':
                        df_drink.loc[(df_drink['음료명'] == drink) & (df_drink['사이즈'] == size), '추천 점수'] -= prev_rating
                    elif prev_answer == 'NEGATIVE':
                        df_drink.loc[(df_drink['음료명'] == drink) & (df_drink['사이즈'] == size), '추천 점수'] += (6 - prev_rating)
                tokenizer, model = load_translation_model()
                new_result = translate(review, tokenizer, model)
                new_result = posneg(new_result)
                new_result.sort(key=lambda x: x['score'], reverse=True)
                new_answer = new_result[0]['label']
                if new_answer == 'POSITIVE':
                    df_drink.loc[(df_drink['음료명'] == drink) & (df_drink['사이즈'] == size), '추천 점수'] += rating
                elif new_answer == 'NEGATIVE':
                    df_drink.loc[(df_drink['음료명'] == drink) & (df_drink['사이즈'] == size), '추천 점수'] -= (6 - rating)
                df_drink.to_csv('data/menu_data.csv')