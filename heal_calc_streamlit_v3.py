
import streamlit as st

# 룬 정의 (카테고리별 구분)
rune_categories = {
    "무기 룬 (공격력)": {
        "영혼 수확자(6성)": 20, "검무+(8성)": 20, "마지막 자비(8성)": 20, "종언+(8성)": 20
    },
    "방어구 룬 (공격력)": {
        "초기+(6성)": 20, "저격+(6성)": 15, "마나격류(6성)": 14, "바위거인(6성)": 20,
        "비열한 일격(6성)": 24, "여명+(8성)": 21, "바위 감시자(8성)": 22, "저무는 달(8성)": 20,
        "땅울림(8성)": 30, "침묵하는 산(8성)": 22, "필사+(8성)": 20, "파멸+(8성)": 25,
        "성역+(8성)": 17, "섬세한 손놀림(8성)": 6, "압도적인 힘(8성)": 6, "붕괴하는 별(8성)": 10,
        "지휘관(8성)": 22.5, "나무 사슴(8성)": 12, "수정 꽃잎(8성)": 12, "어두운 징도(8성)": 18,
        "바스러지는 빛(신화)": 27.5, "이름 없는 혼돈(신화)": 40
    },
    "엠블럼 (공격력)": {
        "굳건함+(6성)": 10, "여신의 권능(6성)": 13, "인도하는 빛(8성)": 20,
        "대마법사(8성)": 45, "흩날리는 검(8성)": 35
    },
    "무기 룬 (회복량)": {
        "집행자(8성)": 20
    },
    "방어구 룬 (회복량)": {
        "붉은 맹약(6성)": 18
    },
    "방어구 룬 (공격력 + 회복량)": {
        "신성한 수양(6성)": {"attack": 12, "heal": 12},
        "신성한 칙령(8성)": {"attack": 15, "heal": 9}
    }
}

st.title("마비노기 모바일 시즌1 힐량 계산기")

base_atk = st.number_input("기본 마을 공격력", value=15681)
base_heal = st.number_input("회복력", value=2485)

selected_atk_buffs = []
selected_heal_buffs = []
dual_buffs = []

# 마스터 엠블렘 체크박스
st.markdown("### 🧿 추가 옵션")
master_emblem = st.checkbox("마스터 엠블렘 착용 (+15% 공격력)")

# 체크박스 UI 구성
st.markdown("### 📦 룬 선택")
for category, runes in rune_categories.items():
    with st.expander(f"🔹 {category}"):
        for name, value in runes.items():
            if isinstance(value, dict):  # 공격+회복 동시 증가 룬
                if st.checkbox(f"{name} (+{value['attack']}% 공격력 / +{value['heal']}% 회복량)", key=name):
                    dual_buffs.append(value)
            elif "회복량" in category:
                if st.checkbox(f"{name} (+{value}% 회복량)", key=name):
                    selected_heal_buffs.append(value)
            else:
                if st.checkbox(f"{name} (+{value}% 공격력)", key=name):
                    selected_atk_buffs.append(value)

# 계산
total_atk_buff = sum(selected_atk_buffs) + sum(d["attack"] for d in dual_buffs)
if master_emblem:
    total_atk_buff += 15  # 마스터 엠블렘 효과
total_heal_buff = sum(selected_heal_buffs) + sum(d["heal"] for d in dual_buffs)

adjusted_atk = int(base_atk * (1 + total_atk_buff / 100))
heal_rate = 1.1 + total_heal_buff / 100
heal_recovery = 1 + (base_heal / 8750)

st.markdown("---")
st.subheader("💡 힐량 계산 결과 (30레벨 기준)")
st.markdown(f"**🔺 보정 공격력:** `{adjusted_atk}`")

# 스킬별 힐계수 (30레벨 기준, 예시 수치)
skills = {
    "물결": 0.0176,
    "감쌈": 0.024,
    "루미너스": 0.024,
    "빛무리": 0.032,
    "억압": 0.024
}

import pandas as pd

results = []
for skill, coeff in skills.items():
    base_heal_amt = int(base_atk * coeff * 1.1 * heal_recovery)
    max_heal_amt = int(adjusted_atk * coeff * heal_rate * heal_recovery)
    results.append((skill, base_heal_amt, max_heal_amt))

df = pd.DataFrame(results, columns=["스킬", "기본 힐량", "룬 적용 힐량"])
st.table(df)
