import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


def run_stat() :

    st.text('')
    st.text('')

    st.markdown(
            """
            <h2 style="text-align: center; color: #FF4B4B;">
                💿 통계 데이터
            </h2>
            """, 
            unsafe_allow_html=True
        )

    st.markdown("---")
        
    # 설명 부분 스타일 개선
    st.markdown(
        """
        <p style="font-size: 24px; text-align: center;">
            <b>메뉴 데이터 및 누적된 주문, 리뷰 통계를 표시합니다.<b>
        </p>
        """, 
        unsafe_allow_html=True
    )
    st.text('')

    st.info("📊 **메뉴 데이터**")
    df_drink = pd.read_csv('data/menu_data.csv')
    st.dataframe(df_drink)
    st.write("""
        - 스타벅스 음료의 데이터를 별도의 데이터 테이블에 저장합니다.
            - 음료명, 영양정보, 추천 점수를 표시하여 음료별 정보 및 소비자의 선호도를 확인할 수 있습니다.
        - 앱을 통해 음료 추천 시스템 개선 목적으로 사용될 수 있습니다.
            - 사용자들의 전반적인 선호도를 추천 점수로 변환하여 음료 추천 시스템에 활용 가능
            - 위 데이터 기반으로 사용자 맞춤 음료 추천 시스템 개선 가능
            """)

    st.info("📊 **주문 내역 데이터** (**주문 수**로 내림차순 정렬)")
    df_log = pd.read_csv('data/order_data.csv')
    st.dataframe(df_log.sort_values('주문 수', ascending=False))
    st.write("""
        - 앱 사용자들이 주문한 음료 정보 및 빈도를 별도의 데이터 테이블에 저장합니다.
            - 사용자 ID, 음료 정보, 주문 수량을 표시하여 사용자별 특정 음료의 주문 횟수를 확인할 수 있습니다.
        - 앱을 통해 주문된 음료의 분석 및 추천 성능 개선 목적으로 사용될 수 있습니다.
            - 음료별 주문 횟수, 사용자별 최빈 주문 음료 등 확인 및 분석
            - 위 데이터 기반으로 사용자 맞춤 음료 추천 시스템 개선 가능
            """)

    st.info("📊 **리뷰 데이터** (**별점**으로 내림차순 정렬)")
    df_review = pd.read_csv('data/review_data.csv')
    st.dataframe(df_review.sort_values('별점', ascending=False))
    st.write("""
        - 앱 사용자들이 리뷰한 음료 정보 및 코멘트, 평점을 별도의 데이터 테이블에 저장합니다.
            - 사용자 ID, 음료 정보, 리뷰 데이터를 표시하여 사용자별 특정 음료의 리뷰 정보를 확인할 수 있습니다.
        - 앱을 통해 리뷰된 음료의 분석 및 추천 성능 개선 목적으로 사용될 수 있습니다.
            - 음료별 평점 평균, 사용자별 선호하는 음료 등 확인 및 분석
            - 위 데이터 기반으로 사용자 맞춤 음료 추천 시스템 개선 가능
            """)

    st.markdown("---")

    if not (df_log.empty or df_review.empty) :
        # 음료별 주문 빈도 상위 5개 및 하위 5개
        st.info("📊 **음료별 주문 빈도 상위 5개 및 하위 5개**")
    
        # 음료명별 주문 수 합계 계산
        order_counts = df_log.groupby('음료명')['주문 수'].sum().sort_values(ascending=False)
        
        # df_log에 없는 음료 목록 df_drink에서 가져와서 리스트로 만들기
        drink_list = df_drink['음료명'].tolist()
        for drink in order_counts.index:
            if drink not in drink_list:
                order_counts.drop(drink, inplace=True)
        
        top_5_orders = order_counts.head(5)
        if len(drink_list) in [1, 2, 3, 4]:
            bottom_5_orders = order_counts.tail(5 - len(drink_list))
            list_to_add = [0] * len(drink_list)
            series_from_list = pd.Series(list_to_add, index=drink_list)
            bottom_5_orders = pd.concat([bottom_5_orders, series_from_list])
        elif len(drink_list) == 0:
            bottom_5_orders = order_counts.tail(5)
        else:
            random_drinks = np.random.choice(drink_list, 5, replace=False)
            list_to_add = [0] * 5
            bottom_5_orders = pd.Series(list_to_add, index=random_drinks)

        combined_orders = pd.concat([top_5_orders, pd.Series([0]*5, index=['...']*5), bottom_5_orders])

        fig1, ax1 = plt.subplots()
        combined_orders.plot(kind='bar', ax=ax1, color=['skyblue']*5 + ['white']*5 + ['lightcoral']*5)
        ax1.set_title('음료별 주문 빈도 상위 5개 및 하위 5개')
        ax1.set_ylabel('주문 횟수')
        ax1.set_xticklabels(combined_orders.index)

        # y축 레이블을 정수로 표시
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
        st.pyplot(fig1)
        st.write("""
            - 앱 사용자들의 주문 데이터를 분석하여 가장 많이 주문된 음료와 가장 적게 주문된 음료를 시각화합니다.
                - 높은 주문 빈도를 보이는 음료는 사용자들의 선호도가 높음을 의미할 수 있습니다.
                - 반면 주문 수가 낮은 음료는 마케팅 대상 혹은 개선 대상이 될 수 있습니다.
            - 향후 추천 알고리즘 개선 시 사용자 선호 음료와 비선호 음료의 특성을 반영할 수 있는 근거 자료로 활용됩니다.
            """)
        st.markdown("---")

        # 음료별 평균 평점 상위 5개 및 하위 5개
        st.info("⭐ **음료별 평균 평점 상위 5개 및 하위 5개**")
        avg_ratings = df_review.groupby('음료명')['별점'].mean()
        top_5_ratings = avg_ratings.nlargest(5)
        bottom_5_ratings = avg_ratings.nsmallest(5).sort_values(ascending=False)

        combined_ratings = pd.concat([top_5_ratings, pd.Series([0]*5, index=['...']*5), bottom_5_ratings])

        fig2, ax2 = plt.subplots()
        combined_ratings.plot(kind='bar', ax=ax2, color=['skyblue']*5 + ['white']*5 + ['lightcoral']*5)
        ax2.set_title('음료별 평균 평점 상위 5개 및 하위 5개')
        ax2.set_ylabel('평점')
        st.pyplot(fig2)
        st.write("""
            - 사용자 리뷰 데이터를 기반으로 음료별 평균 평점을 분석하여 상위 5개 및 하위 5개 음료를 시각화합니다.
                - 높은 평점을 받은 음료는 긍정적인 평가를 지속적으로 받았음을 의미합니다.
                - 낮은 평점 음료는 개선 대상이 될 수 있으며, 사용자 피드백 분석에 활용할 수 있습니다.
            - 리뷰 기반 사용자 만족도 분석을 통해 제품 개선 및 추천 신뢰도 향상에 기여합니다.
            """)
        st.markdown("---")

        # 음료별 평균 평점 및 주문 수 분포
        st.info("📈 **음료별 평균 별점 및 주문 수 분포**")
        avg_ratings = df_review.groupby('음료명')['별점'].mean()
        total_orders = df_log.groupby('음료명')['주문 수'].sum()

        merged_df = pd.DataFrame({
            '평점': avg_ratings,
            '주문 수': total_orders
        }).dropna()

        # 중복된 값을 제거하여 하나의 점만 표시
        merged_df = merged_df[~merged_df.duplicated(subset=['평점', '주문 수'])]

        fig3, ax3 = plt.subplots()
        sb.scatterplot(data=merged_df, x='주문 수', y='평점', ax=ax3)

        # 각 점 옆에 음료명과 사이즈 표시
        for i in range(merged_df.shape[0]):
            ax3.annotate(merged_df.index[i], 
                         (merged_df['주문 수'][i], merged_df['평점'][i]), 
                         fontsize=6, 
                         rotation=15,
                         xytext=(5, 0),  # 텍스트를 점에서 약간 떨어뜨림
                         textcoords='offset points')

        ax3.set_title('음료별 평균 별점 및 주문 수 분포')
        ax3.set_xlabel('주문 수')
        ax3.set_ylabel('별점')
        st.pyplot(fig3)
        st.write("""
            - 음료별 평균 평점과 총 주문 수를 산점도로 시각화하여 두 요소 간의 관계를 분석합니다.
                - 평점과 주문 수가 모두 높은 음료는 사용자 만족도와 실제 수요가 일치함을 나타냅니다.
                - 불일치하는 경우에는 마케팅 전략 또는 사용자 경험 개선이 필요할 수 있습니다.
            - 실질적인 소비 패턴과 만족도를 동시에 반영한 분석 자료로 활용됩니다.
            """)