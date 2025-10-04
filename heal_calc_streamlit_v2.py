
import streamlit as st

# 룬 정의
attack_buffs = {
    "영혼 수확자(6성)": 20, "검무+(8성)": 20, "마지막 자비(8성)": 20, "종언+(8성)": 20,
    "초기+(6성)": 20, "저격+(6성)": 15, "마나격류(6성)": 14, "바위거인(6성)": 20,
    "비열한 일격(6성)": 24, "여명+(8성)": 21, "바위 감시자(8성)": 22, "저무는 달(8성)": 20,
    "땅울림(8성)": 30, "침묵하는 산(8성)": 22, "필사+(8성)": 20, "파멸+(8성)": 25,
    "성역+(8성)": 17, "섬세한 손놀림(8성)": 6, "압도적인 힘(8성)": 6, "붕괴하는 별(8성)": 10,
    "지휘관(8성)": 22.5, "나무 사슴(8성)": 12, "수정 꽃잎(8성)": 12, "어두운 징도(8성)": 18,
    "바스러지는 빛(신화)": 27.5, "이름 없는 혼돈(신화)": 40,
    "굳건함+(6성)": 10, "여신의 권능(6성)": 13, "인도하는 빛(8성)": 20, "대마법사(8성)": 45, "흩날리는 검(8성)": 35,
}

heal_buffs = {
    "집행자(8성)": 20,
    "붉은 맹약(6성)": 18,
}

dual_buffs = {
    "신성한 수양(6성)": {"attack": 12, "heal": 12},
    "신성한 칙령(8성)": {"attack": 15, "heal": 9},
}

st.title("마비노기 모바일 시즌1 힐량 계산기")

base_atk = st.number_input("기본 마을 공격력", value=10000)
base_heal = st.number_input("회복력", value=2000)

st.markdown("### 🟥 공격력 증가 룬")
selected_atk_buffs = [v for k, v in attack_buffs.items() if st.checkbox(k, key="atk_" + k)]

st.markdown("### 🟦 회복량 증가 룬")
selected_heal_buffs = [v for k, v in heal_buffs.items() if st.checkbox(k, key="heal_" + k)]

st.markdown("### 🟨 공격력 + 회복량 증가 룬")
selected_dual = [v for k, v in dual_buffs.items() if st.checkbox(k, key="dual_" + k)]

total_atk_buff = sum(selected_atk_buffs) + sum(d["attack"] for d in selected_dual)
total_heal_buff = sum(selected_heal_buffs) + sum(d["heal"] for d in selected_dual)

adjusted_atk = int(base_atk * (1 + total_atk_buff / 100))
heal_rate = 1.1 + total_heal_buff / 100
heal_recovery = 1 + (base_heal / 8750)

st.markdown("---")
st.subheader("💡 힐량 계산 결과")
st.markdown(f"**보정 공격력**: `{adjusted_atk}`")
st.markdown(f"**힐 계수 = (1.1 + {total_heal_buff/100:.2f}) × (1 + 회복력 / 8750)` = `{heal_rate:.4f} × {heal_recovery:.4f}`")

# 예시: 스킬 계수 0.02
sample_skill_coeff = 0.02
min_heal = int(base_atk * sample_skill_coeff * 1.1 * heal_recovery)
max_heal = int(adjusted_atk * sample_skill_coeff * heal_rate * heal_recovery)

st.write(f"✔️ **예시 스킬 계수 0.02 기준:**")
st.write(f"- 기본 힐량: `{min_heal}`")
st.write(f"- 룬 적용 최대 힐량: `{max_heal}`")
