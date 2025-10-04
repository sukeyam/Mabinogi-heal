import streamlit as st
import pandas as pd

# 힐 계수 데이터 (30레벨 기준)
heal_data = {
    "라이프 링크": 0.015964,
    "라이프 링크 (서약 룬)": 0.015949,
    "팬텀 페인 (억압 룬)": 0.025963,
    "생명의 고동(물결 룬)": 0.017594,
    "프로텍션 (감쌈 룬)": 0.019462,
    "프로텍션-회복량 (광륜 룬)": 0.129973,
    "프로텍션-지속 회복량 (광륜 룬)": 0.019483,
    "서먼 루미너스": 0.023965,
    "윙오브 엔젤": 0.191978
}

st.set_page_config(page_title="마비노기 모바일 힐량 계산기", layout="centered")

# 타이틀
st.title("💖 마비노기 모바일 힐량 계산기 (시즌 1)")

# 입력 영역
st.subheader("📌 기본 정보 입력")

adjusted_atk = st.number_input("보정 공격력", min_value=0, value=0, step=100)
recovery = st.number_input("회복력", min_value=0, value=0, step=100)

st.markdown("""
> ※ 시즌 1에서 보정 공격력 값을 구하는 방식이 바뀌었기 때문에, 부득이하게 보정공격력과 회복력(마을에서의 기본 회복력)을 입력해주세요.  
> ※ 보정 공격력은 허수아비를 치면서 모든 버프가 켜진상태에서 스탯창의 공격력이 최고로 증가한 수치를 기입해 주시면 됩니다. (금방합니다)
""")

# 룬 체크박스
st.subheader("📦 회복량 증가 룬 선택")
rune1 = st.checkbox("🗡 집행자 (무기 룬, 치유량 20% 증가)")
rune2 = st.checkbox("🛡 신성한 수양 (방어구 룬, 회복량 12% 증가)")
rune3 = st.checkbox("✨ 신성한 칙령 (회복량 9% 증가)")

st.markdown("""
> ※ 신성한 칙령은 아군의 체력 회복 시 공격력 15%, 회복량 9%가 증가하는데, 본인 회복시에도 증가하는지는 검증되지 않았습니다.  
> (룬이 없어서 실험 못해봤어요.)
""")

# 힐 증가율 계산
heal_bonus = 0.0
if rune1:
    heal_bonus += 0.20
if rune2:
    heal_bonus += 0.12
if rune3:
    heal_bonus += 0.09

# 결과 계산
st.subheader("💡 힐량 계산 결과 (스킬 30레벨 기준)")

results = []
for skill, coeff in heal_data.items():
    heal = coeff * adjusted_atk * (1.1 + heal_bonus) * (1 + recovery / 8750)
    results.append({
        "스킬명": skill,
        "보정 힐량": round(heal)
    })

df_result = pd.DataFrame(results)
st.table(df_result)
