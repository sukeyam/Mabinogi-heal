
import streamlit as st
import pandas as pd

st.set_page_config(page_title="마비노기 모바일 힐량 계산기", layout="centered")

st.title("💊 마비노기 모바일 힐량 계산기 (S1 기준)")

# 입력
st.header("기본 정보 입력")
col1, col2 = st.columns(2)
with col1:
    base_power = st.number_input("보정 공격력", min_value=0, value=15000, step=100)
with col2:
    heal_stat = st.number_input("회복력", min_value=0, value=2000, step=100)

st.header("회복량 증가 룬 선택")
col1, col2, col3 = st.columns(3)
buff_run_1 = col1.checkbox("집행자 (무기 룬, +20%)")
buff_run_2 = col2.checkbox("신성한 수양 (방어구 룬, +12%)")
buff_run_3 = col3.checkbox("신성한 칙령 (방어구 룬, +9%)")

# 회복량 보정 계산
heal_buff = 0.0
if buff_run_1:
    heal_buff += 0.20
if buff_run_2:
    heal_buff += 0.12
if buff_run_3:
    heal_buff += 0.09

heal_ratio = (1.1 + heal_buff) * (1 + heal_stat / 8750)

# 스킬 계수 테이블
skill_data = [
    ["라이프 링크", 0.015964145],
    ["라이프 링크 (서약 룬)", 0.015949141],
    ["팬텀 페인 (억압 룬)", 0.025963149],
    ["생명의 고동(물결 룬)", 0.017593896],
    ["프로텍션 (감쌈 룬)", 0.019462414],
    ["프로텍션-회복량 (광륜 룬)", 0.129972591],
    ["프로텍션-지속 회복량 (광륜 룬)", 0.019482925],
    ["서먼 루미너스", 0.023964738],
    ["윙오브 엔젤", 0.191977183],
]

# 힐량 계산 결과
st.subheader("💡 힐량 계산 결과 (30레벨 기준)")
st.markdown(f"🔧 보정 공격력: **{base_power}**, 회복력 보정 계수: **{heal_ratio:.4f}**")

results = []
for name, coef in skill_data:
    base_heal = round(base_power * coef)
    final_heal = round(base_power * coef * heal_ratio)
    results.append((name, base_heal, final_heal))

df = pd.DataFrame(results, columns=["스킬", "기본 힐량", "보정 힐량"])
st.table(df)
