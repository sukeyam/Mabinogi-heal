
import streamlit as st
import pandas as pd

# 힐 계수 정의
heal_coefficients = {
    "라이프 링크": 0.011,
    "라이프 링크 (서약 룬)": 0.0132,
    "팬텀 페인 (억압 룬)": 0.015,
    "프로텍션 (감쌈 룬)": 0.015,
    "프로텍션-회복량 (광륜 룬)": 0.02,
    "프로텍션-지속 회복량 (광륜 룬)": 0.008,
    "서먼 루미너스": 0.015,
    "윙 오브 엔젤": 0.02,
    "물결": 0.0176,
    "감쌈": 0.024,
    "루미너스": 0.024,
    "빛무리": 0.032,
    "억압": 0.024,
    "생명의 고동": 0.015
}

# 룬 옵션
runes = {
    "무기 룬 (공격력)": {
        "영혼 수확자(6성)": 0.20,
        "검무+(8성)": 0.20,
        "마지막 자비(8성)": 0.20,
        "종언+(8성)": 0.20
    },
    "방어구 룬 (공격력)": {
        "붉은 맹약(6성)": 0.18,
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
        "이름 없는 혼돈(신화)": 0.40
    },
    "엠블럼 (공격력)": {
        "굳건함+(6성)": 0.10,
        "여신의 권능(6성)": 0.13,
        "인도하는 빛(8성)": 0.20,
        "대마법사(8성)": 0.45,
        "흩날리는 검(8성)": 0.35
    },
    "무기 룬 (회복량)": {
        "집행자(8성)": 0.20
    },
    "방어구 룬 (회복량)": {
    },
    "방어구 룬 (공격력 + 회복량)": {
        "신성한 수양(6성)": (0.12, 0.12),
        "신성한 칙령(8성)": (0.15, 0.09)
    }
}

st.title("마비노기 모바일 시즌1 힐량 계산기")

atk = st.number_input("기본 마을 공격력", value=15681, step=1)
heal = st.number_input("회복력", value=2485, step=1)

st.markdown("### 🔘 추가 옵션")
master_emblem = st.checkbox("🛡️ 마스터 엠블렘 착용 (+15% 공격력)")

st.markdown("### 📦 룬 선택")
selected_atk_runes = []
selected_heal_runes = []
atk_buff = 0
heal_buff = 0

for category, options in runes.items():
    with st.expander(f"▶ {category}"):
        for label, value in options.items():
            if isinstance(value, tuple):  # 공격력 + 회복력
                checked = st.checkbox(f"{label} (+{int(value[0]*100)}% 공격력, +{int(value[1]*100)}% 회복력)", key=label)
                if checked:
                    atk_buff += value[0]
                    heal_buff += value[1]
            elif "공격력" in category:
                checked = st.checkbox(f"{label} (+{int(value*100)}%)", key=label)
                if checked:
                    atk_buff += value
            elif "회복량" in category:
                checked = st.checkbox(f"{label} (+{int(value*100)}%)", key=label)
                if checked:
                    heal_buff += value

if master_emblem:
    atk_buff += 0.15

# 실 게임 기준 보정 계수 적용
total_atk = int(atk + atk * atk_buff * 0.73)
heal_rate = (1.1 + heal_buff) * (1 + heal / 8750)

# 결과 계산
data = []
for skill, coef in heal_coefficients.items():
    base_heal = round(atk * coef * heal_rate)
    buffed_heal = round(total_atk * coef * heal_rate)
    data.append((skill, base_heal, buffed_heal))

df = pd.DataFrame(data, columns=["스킬", "기본 힐량", "룬 적용 힐량"])

st.markdown("---")
st.markdown("💡 **힐량 계산 결과 (30레벨 기준)**")
st.markdown(f"🔺 **보정 공격력 : <span style='color:red; font-size:20px'><b>{total_atk}</b></span>**", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
