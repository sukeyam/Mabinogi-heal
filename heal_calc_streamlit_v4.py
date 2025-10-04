
import streamlit as st
import pandas as pd

# 스킬별 힐 계수 (30레벨 기준)
skill_df = pd.DataFrame({
    '스킬명': ['물결', '감쌈', '루미너스', '빛무리', '억압'],
    '계수': [0.0176, 0.024, 0.024, 0.032, 0.024]
})

# 룬 데이터: 카테고리별 공격력 증가
rune_data = {
    "무기": {
        "영혼 수확자(6성)": 0.20,
        "검무+(8성)": 0.20,
        "마지막 자비(8성)": 0.20,
        "종언+(8성)": 0.20,
    },
    "방어구": {
        "초기+(6성)": 0.20,
        "저격+(6성)": 0.15,
        "마나격류(6성)": 0.14,
        "바위거인(6성)": 0.20,
        "비열한 일격(6성)": 0.24,
        "여명+(8성)": 0.21,
        "바위 감시자(8성)": 0.22,
        "저무는 달(8성)": 0.20,
        "땅울림(8성)": 0.30,
        "침묵하는 산(8성)": 0.22,
        "필사+(8성)": 0.20,
        "파멸+(8성)": 0.25,
        "성역+(8성)": 0.17,
        "섬세한 손놀림(8성)": 0.06,
        "압도적인 힘(8성)": 0.06,
        "붕괴하는 별(8성)": 0.10,
        "지휘관(8성)": 0.225,
        "나무 사슴(8성)": 0.12,
        "수정 꽃잎(8성)": 0.12,
        "어두운 징도(8성)": 0.18,
        "바스러지는 빛(신화)": 0.275,
        "이름 없는 혼돈(신화)": 0.40,
        "신성한 수양(6성)": 0.12,
        "신성한 칙령(8성)": 0.15,
    },
    "엠블럼": {
        "굳건함+(6성)": 0.10,
        "여신의 권능(6성)": 0.13,
        "인도하는 빛(8성)": 0.20,
        "대마법사(8성)": 0.45,
        "흩날리는 검(8성)": 0.35,
    }
}

# 회복량 증가 룬
heal_buff_data = {
    "집행자(8성)": 0.20,
    "붉은 맹약(6성)": 0.18,
    "신성한 수양(6성)": 0.12,
    "신성한 칙령(8성)": 0.09,
}

# UI 구성
st.title("💉 마비노기 모바일 시즌1 힐량 계산기")

base_atk = st.number_input("기본 마을 공격력", value=26000, step=100)
recovery = st.number_input("회복력", value=2500, step=50)

# 마스터 엠블렘 체크
master_emblem = st.checkbox("✔️ 마스터 엠블렘 착용 (+15%)")

# 공격력 증가 룬 선택
st.subheader("🧱 공격력 증가 룬 선택")
atk_buff_total = 0
for category, options in rune_data.items():
    with st.expander(f"[{category}]"):
        for name, value in options.items():
            if st.checkbox(f"{name} (+{value * 100:.1f}%)", key=name):
                atk_buff_total += value

if master_emblem:
    atk_buff_total += 0.15

# 회복량 증가 룬 선택
st.subheader("💚 회복량 증가 룬 선택")
heal_buff_total = 0
for name, value in heal_buff_data.items():
    if st.checkbox(f"{name} (+{value * 100:.1f}%)", key=f"heal_{name}"):
        heal_buff_total += value

# 보정 공격력 계산 (요청된 방식)
adjusted_atk = base_atk + (base_atk * atk_buff_total)
heal_multiplier = (1.1 + heal_buff_total) * (1 + recovery / 8750)

# 출력
st.markdown(f"### 🔺 보정 공격력: <span style='color:red; font-size:22px'><b>{round(adjusted_atk)}</b></span>", unsafe_allow_html=True)
st.subheader("💧 힐량 계산 결과 (30레벨 기준)")

results = []
for _, row in skill_df.iterrows():
    name = row['스킬명']
    coef = row['계수']
    base_heal = round(base_atk * coef * heal_multiplier)
    max_heal = round(adjusted_atk * coef * heal_multiplier)
    results.append([name, base_heal, max_heal])

result_df = pd.DataFrame(results, columns=["스킬명", "기본 힐량", "최대 힐량 (룬 적용)"])
st.table(result_df)
