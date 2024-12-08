import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="급여 실수령액 계산기",
    page_icon="💰",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .big-font {
        font-size: 24px !important;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def calculate_insurance(salary):
    # 4대보험 계산 (2024년 기준)
    national_pension = salary * 0.045  # 국민연금 4.5%
    health_insurance = salary * 0.0709  # 건강보험 7.09%
    long_term_care = health_insurance * 0.1281  # 장기요양보험 12.81%
    employment_insurance = salary * 0.009  # 고용보험 0.9%
    
    return {
        '국민연금': national_pension,
        '건강보험': health_insurance,
        '장기요양보험': long_term_care,
        '고용보험': employment_insurance
    }

def calculate_tax(salary):
    # 간단한 세금 계산 (실제 세금은 더 복잡한 계산식 사용)
    income_tax = salary * 0.06  # 소득세 약 6% (간단화)
    local_tax = income_tax * 0.1  # 지방소득세 (소득세의 10%)
    
    return {
        '소득세': income_tax,
        '지방소득세': local_tax
    }

def main():
    st.title('💰 급여 실수령액 계산기')
    st.markdown('#### 연봉/월급을 입력하시면 4대보험과 세금을 공제한 실수령액을 계산해드립니다.')
    
    # 입력 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        salary_type = st.radio(
            "급여 유형 선택",
            ["연봉", "월급"],
            horizontal=True
        )
    
    with col2:
        if salary_type == "연봉":
            salary = st.number_input(
                "연봉을 입력하세요 (원)",
                min_value=0,
                value=36000000,
                step=1000000,
                format="%d"
            )
            monthly_salary = salary / 12
        else:
            monthly_salary = st.number_input(
                "월급을 입력하세요 (원)",
                min_value=0,
                value=3000000,
                step=100000,
                format="%d"
            )
            salary = monthly_salary * 12
    
    if st.button('계산하기', use_container_width=True):
        # 공제액 계산
        insurance = calculate_insurance(monthly_salary)
        tax = calculate_tax(monthly_salary)
        
        # 총 공제액 및 실수령액 계산
        total_deduction = sum(insurance.values()) + sum(tax.values())
        net_salary = monthly_salary - total_deduction
        
        # 결과 표시
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 📊 급여 정보')
            if salary_type == "연봉":
                st.markdown(f'- **연봉**: {salary:,}원')
            st.markdown(f'''
            - **월 급여**: {monthly_salary:,}원
            - **총 공제액**: {total_deduction:,.0f}원
            ''')
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 💵 실수령액')
            st.markdown(f'<p class="big-font">**{net_salary:,.0f}원**</p>', unsafe_allow_html=True)
            st.markdown(f'(매월 예상 수령액)')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 공제 내역 도넛 차트
        deductions = {**insurance, **tax}
        fig = px.pie(
            values=list(deductions.values()),
            names=list(deductions.keys()),
            title='공제 항목별 비율'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 상세 공제 내역
        st.markdown('### 📋 상세 공제 내역')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('#### 4대보험')
            for name, value in insurance.items():
                st.markdown(f'- {name}: {value:,.0f}원')
        
        with col2:
            st.markdown('#### 세금')
            for name, value in tax.items():
                st.markdown(f'- {name}: {value:,.0f}원')
        
        # 주의사항
        st.info('''
        #### ℹ️ 참고사항
        - 이 계산기는 개략적인 예상 금액을 계산합니다.
        - 실제 공제액은 회사 정책, 부양가족 수, 각종 공제 항목에 따라 달라질 수 있습니다.
        - 정확한 금액은 회사 급여담당자나 세무사와 상담하시기 바랍니다.
        ''')
        
        # 블로그 링크 섹션
        st.markdown('---')
        st.markdown('''
        ### 🔍 더 자세한 정보가 필요하신가요?
        
        급여 계산과 관련된 더 자세한 정보를 확인해보세요:
        
        - ✍️ [급여 실수령액 계산 상세 가이드](https://lzhakko.tistory.com/)
        - 📚 [4대보험 계산 방법 완벽 가이드](https://lzhakko.tistory.com/)
        - 💡 [자주 묻는 급여 계산 질문과 답변](https://lzhakko.tistory.com/)
        
        ### 💪 추천 콘텐츠
        - ✨ 퇴직금 계산기
        - 📊 연차수당 계산기
        - 📈 연봉 인상률 계산기
        
        더 많은 유용한 정보는 [개발하는 나무](https://lzhakko.tistory.com/)에서 확인하세요!
        ''')

if __name__ == '__main__':
    main()
