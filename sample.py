import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 파일 경로 (본인의 환경에 맞게 수정하세요)
file_path = 'glucose_shift_work.csv'

# 데이터 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv(file_path)
    return data

data = load_data()

# Streamlit 대시보드 타이틀 설정
st.title('Glucose Level Dashboard')

# 사이드바 필터
st.sidebar.header('Filter Options')
selected_sex = st.sidebar.multiselect('Sex', options=data['sex'].unique(), default=data['sex'].unique())
selected_age = st.sidebar.slider('Age Range', int(data['age'].min()), int(data['age'].max()), (int(data['age'].min()), int(data['age'].max())))
selected_shift = st.sidebar.multiselect('Shift', options=data['shift'].unique(), default=data['shift'].unique())

# 필터 적용
filtered_data = data[(data['sex'].isin(selected_sex)) & (data['age'].between(selected_age[0], selected_age[1])) & (data['shift'].isin(selected_shift))]

# 데이터 표시를 위한 컬럼 생성
col1, col2 = st.columns(2)

# 컬럼1: 필터링된 데이터 표시
with col1:
    st.header('Filtered Data')
    st.write(filtered_data)

# 컬럼2: 근무 시간대 별 평균 혈당 수준 파이 차트
with col2:
    st.header('Average Glucose Level by Shift')
    avg_glucose_per_shift = data.groupby('shift')['glucose'].mean()
    plt.figure(figsize=(6, 6))
    plt.pie(avg_glucose_per_shift, labels=avg_glucose_per_shift.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # 원형 파이 차트를 위해
    st.pyplot(plt)


