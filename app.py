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
        font-size: 30px !important;
        font-weight: bold;
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
    """숫자에 콤마를 추가하는 함수"""
    return f"{number:,}원"  # 원 단위 유지


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
        national_pension_rate = 0.045  # 국민연금 4.5%
        health_insurance_rate = 0.0709  # 건강보험 7.09%
        long_term_care_insurance_rate = 0.1281  # 장기요양보험 12.81%
        employment_insurance_rate = 0.009  # 고용보험 0.9%
    elif year == "2025년":
        # 2025년 기준 보험료율 (예상 값)
        national_pension_rate = 0.047  # 국민연금 4.7% (예상)
        health_insurance_rate = 0.073  # 건강보험 7.3% (예상)
        long_term_care_insurance_rate = 0.13  # 장기요양보험 13% (예상)
        employment_insurance_rate = 0.008  # 고용보험 0.8% (예상)

    national_pension = salary * national_pension_rate
    health_insurance = salary * health_insurance_rate
    long_term_care_insurance = health_insurance * long_term_care_insurance_rate
    employment_insurance = salary * employment_insurance_rate

    return {
        '국민연금': national_pension,
        '건강보험': health_insurance,
        '장기요양보험': long_term_care_insurance,
        '고용보험': employment_insurance,
        '국민연금_비율': national_pension_rate,
        '건강보험_비율': health_insurance_rate,
        '장기요양보험_비율': long_term_care_insurance_rate,
        '고용보험_비율': employment_insurance_rate
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
        '지방소득세': local_tax,
        '세율': tax_rate
    }


def main():
    # ... (기존 코드) ...

    if st.button('계산하기', use_container_width=True):
        # ... (기존 코드) ...

        with col3:  # 계산식 표시
            st.markdown('#### 계산식')
            st.markdown(f'- **국민연금**: 월 급여 * {insurance["국민연금_비율"]:.3f}')
            st.markdown(f'- **건강보험**: 월 급여 * {insurance["건강보험_비율"]:.3f}')
            st.markdown(f'- **장기요양보험**: 건강보험료 * {insurance["장기요양보험_비율"]:.3f}')
            st.markdown(f'- **고용보험**: 월 급여 * {insurance["고용보험_비율"]:.3f}')
            st.markdown(f'- **소득세**: (월 급여 - 근로소득공제) * {tax["세율"]:.2f}')
            st.markdown('- **지방소득세**: 소득세 * 0.1')

        # ... (기존 코드) ...

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

            - ✍️ [퇴직금 체불 해결 가이드: 근로기준법과 퇴직금 계산기 활용법](https://lzhakko.tistory.com/entry/%ED%87%B4%EC%A7%81%EA%B8%88-%EC%B2%B4%EB%B6%88-%ED%95%B4%EA%B2%B0-%EA%B0%80%EC%9D%B4%EB%93%9C-%EA%B7%BC%EB%A1%9C%EA%B8%B0%EC%A4%80%EB%B2%95%EA%B3%BC-%ED%87%B4%EC%A7%81%EA%B8%88-%EA%B3%84%EC%82%B0%EA%B8%B0-%ED%99%9C%EC%9A%A9%EB%B2%95)
            - 📚 [주휴수당 계산기: 쉽게 계산하고 무료로 다운로드하세요!](https://lzhakko.tistory.com/entry/%EC%A3%BC%ED%9C%B4%EC%88%98%EB%8B%B9-%EA%B3%84%EC%82%B0%EA%B8%B0-%EC%89%BD%EA%B2%8C-%EA%B3%84%EC%82%B0%ED%95%98%EA%B3%A0-%EB%AC%B4%EB%A3%8C%EB%A1%9C-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%ED%95%98%EC%84%B8%EC%9A%94)
            - 💡 [해촉증명서 작성법부터 양식 다운로드까지, 쉽고 간단하게!](https://lzhakko.tistory.com/entry/%ED%95%B4%EC%B4%89%EC%A6%9D%EB%AA%85%EC%84%9C-%EC%9E%91%EC%84%B1%EB%B2%95%EB%B6%80%ED%84%B0-%EC%96%91%EC%8B%9D-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%EA%B9%8C%EC%A7%80-%EC%89%BD%EA%B3%A0-%EA%B0%84%EB%8B%A8%ED%95%98%EA%B2%8C)

            더 많은 유용한 정보는 [리즈의 일상백과](https://lzhakko.tistory.com/)에서 확인하세요!
            ''')


if __name__ == '__main__':
    main()
