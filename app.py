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


def format_number(number):
    """숫자에 콤마를 추가하고 만원 단위로 변환하는 함수"""
    return f"{number / 10000:,.1f}만원"  # 만원 단위 변환


def calculate_insurance(salary, year):
    """
    연도별 4대보험 계산 함수

    Args:
        salary (int): 월 급여
        year (str): 계산할 연도 ("2024년" 또는 "2025년")

    Returns:
        dict: 4대보험 종류별 금액을 담은 딕셔너리
    """
    if year == "2024년":
        national_pension = salary * 0.045  # 국민연금 4.5%
        health_insurance = salary * 0.0709  # 건강보험 7.09%
        long_term_care_insurance = health_insurance * 0.1281  # 장기요양보험 12.81%
        employment_insurance = salary * 0.009  # 고용보험 0.9%
    elif year == "2025년":
        # 2025년 기준 보험료율 (예상 값)
        national_pension = salary * 0.047  # 국민연금 4.7% (예상)
        health_insurance = salary * 0.073  # 건강보험 7.3% (예상)
        long_term_care_insurance = health_insurance * 0.13  # 장기요양보험 13% (예상)
        employment_insurance = salary * 0.008  # 고용보험 0.8% (예상)

    return {
        '국민연금': national_pension,
        '건강보험': health_insurance,
        '장기요양보험': long_term_care_insurance,
        '고용보험': employment_insurance
    }


def calculate_tax(salary, year):
    """
    연도별 세금 계산 함수

    Args:
        salary (int): 월 급여
        year (str): 계산할 연도 ("2024년" 또는 "2025년")

    Returns:
        dict: 세금 종류별 금액을 담은 딕셔너리
    """
    if year == "2024년":
        # 2024년 기준 세율 적용
        taxable_income = salary - 1500000  # 근로소득공제
        if taxable_income <= 14000000:
            tax_rate = 0.06
        elif taxable_income <= 50000000:
            tax_rate = 0.15
        elif taxable_income <= 88000000:
            tax_rate = 0.24
        elif taxable_income <= 150000000:
            tax_rate = 0.35
        elif taxable_income <= 300000000:
            tax_rate = 0.38
        elif taxable_income <= 500000000:
            tax_rate = 0.40
        else:
            tax_rate = 0.42
    elif year == "2025년":
        # 2025년 기준 세율 적용 (예상 값)
        taxable_income = salary - 1700000  # 근로소득공제 (예상)
        if taxable_income <= 15000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.06
        elif taxable_income <= 55000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.16  # 세율 변경 (예상)
        elif taxable_income <= 95000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.25  # 세율 변경 (예상)
        elif taxable_income <= 160000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.36  # 세율 변경 (예상)
        elif taxable_income <= 330000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.39  # 세율 변경 (예상)
        elif taxable_income <= 550000000:  # 과세표준 구간 변경 (예상)
            tax_rate = 0.41  # 세율 변경 (예상)
        else:
            tax_rate = 0.43  # 세율 변경 (예상)

    income_tax = taxable_income * tax_rate
    local_tax = income_tax * 0.1

    return {
        '소득세': income_tax,
        '지방소득세': local_tax
    }


def main():
    st.title('💰 급여 실수령액 계산기')
    st.markdown(
        '#### 연봉/월급을 입력하시면 4대보험과 세금을 공제한 실수령액을 계산해드립니다.'
    )

    # 연도 선택
    year = st.selectbox("계산할 연도를 선택하세요", ["2024년", "2025년"])

    # 입력 섹션
    col1, col2 = st.columns(2)

    with col1:
        salary_type = st.radio("급여 유형 선택", ["연봉", "월급"], horizontal=True)

    with col2:
        if salary_type == "연봉":
            salary = st.number_input(
                "연봉을 입력하세요 (만원)",  # 만원 단위 입력
                min_value=0,
                value=3600,  # 기본값 3600만원
                step=100,  # 100만원 단위 증감
                format="%d"
            )
            monthly_salary = salary * 10000 / 12  # 월급 계산 (원 단위)
        else:
            monthly_salary = st.number_input(
                "월급을 입력하세요 (만원)",  # 만원 단위 입력
                min_value=0,
                value=300,  # 기본값 300만원
                step=10,  # 10만원 단위 증감
                format="%d"
            )
            monthly_salary *= 10000  # 월급 계산 (원 단위)
            salary = monthly_salary * 12  # 연봉 계산 (원 단위)

    if st.button('계산하기', use_container_width=True):
        # 공제액 계산
        insurance = calculate_insurance(monthly_salary, year)
        tax = calculate_tax(monthly_salary, year)

        # 총 공제액 및 실수령액 계산
        total_deduction = sum(insurance.values()) + sum(tax.values())
        net_salary = monthly_salary - total_deduction

        # 결과 표시
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 📊 급여 정보')
            if salary_type == "연봉":
                st.markdown(f'- **연봉**: {format_number(salary)}')
            st.markdown(f'''
                - **월 급여**: {format_number(monthly_salary)}
                - **총 공제액**: {format_number(total_deduction)}
                ''')
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 💵 실수령액')
            st.markdown(f'<p class="big-font">**{format_number(net_salary)}**</p>',
                        unsafe_allow_html=True)
            st.markdown(f'(매월 예상 수령액)')
            st.markdown('</div>', unsafe_allow_html=True)

        # 공제 내역 도넛 차트
        deductions = {**insurance, **tax}
        fig = px.pie(
            values=list(deductions.values()),
            names=list(deductions.keys()),
            title='공제 항목별 비율',
            hole=0.3  # 도넛 차트 가운데 구멍 크기 조절
        )
        st.plotly_chart(fig, use_container_width=True)

        # 상세 공제 내역
        st.markdown('### 📋 상세 공제 내역')
        col1, col2, col3 = st.columns(3)  # 컬럼 3개로 변경

        with col1:
            st.markdown('#### 4대보험')
            for name, value in insurance.items():
                st.markdown(f'- {name}: {format_number(value)}')

        with col2:
            st.markdown('#### 세금')
            for name, value in tax.items():
                st.markdown(f'- {name}: {format_number(value)}')

        with col3:  # 계산식 표시
            st.markdown('#### 계산식')
            st.markdown(f'- **국민연금**: 월 급여 * {0.045 if year == "2024년" else 0.047:.3f}')
            st.markdown(f'- **건강보험**: 월 급여 * {0.0709 if year == "2024년" else 0.073:.3f}')
            st.markdown(f'- **장기요양보험**: 건강보험료 * {0.1281 if year == "2024년" else 0.13:.3f}')
            st.markdown(f'- **고용보험**: 월 급여 * {0.009 if year == "2024년" else 0.008:.3f}')
            st.markdown(f'- **소득세**: (월 급여 - 근로소득공제) * {tax_rate:.2f}')
            st.markdown('- **지방소득세**: 소득세 * 0.1')

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
