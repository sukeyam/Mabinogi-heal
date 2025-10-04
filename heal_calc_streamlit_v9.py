import streamlit as st
import pandas as pd

# 스킬 데이터 (엑셀 기반, 30레벨 기준 공격력 계수)
skill_data = {
    "라이프 링크": 0.015964,
    "라이프 링크 (서약 룬)": 0.015949,
    "팬텀 페인 (억압 룬)": 0.025963,
    "생명의 고동(물결 룬)": 0.017594,
    "프로텍션 (감쌈 룬)": 0.019462,
    "프로텍션-회복량 (광륜 룬)": 0.129973,
    "프로텍션-지속 회복량 (광륜 룬)": 0.019483,
    "서먼 루미너스": 0.023965,
    "윙오브 엔젤": 0.191977
}

# 공격력 증가 룬
attack_runes = {
    "영혼 수확자(6성)": 0.20, "검무+(8성)": 0.20, "마지막 자비(8성)": 0.20, "종언+(8성)": 0.20,
    "초기+(6성)": 0.20, "저격+(6성)": 0.15, "마나격류(6성)": 0.14, "바위거인(6성)": 0.20,
    "비열한 일격(6성)": 0.24, "여명+(8성)": 0.21, "바위 감시자(8성)": 0.22, "저무는 달(8성)": 0.20,
    "땅울림(8성)": 0.30, "침묵하는 산(8성)": 0.22, "필사+(8성)": 0.20, "파멸+(8성)": 0.25,
    "성역+(8성)": 0.17, "섬세한 손놀림(8성)": 0.06, "압도적인 힘(8성)": 0.06, "붕괴하는 별(8성)": 0.10,
    "지휘관(8성)": 0.225, "나무 사슴(8성)": 0.12, "수정 꽃잎(8성)": 0.12, "어두운 징도(8성)": 0.18,
    "바스러지는 빛(신화)": 0.275, "이름 없는 혼돈(신화)": 0.40,
    "굳건함+(6성)": 0.10, "여신의 권능(6성)": 0.13, "인도하는 빛(8성)": 0.20,
    "대마법사(8성)": 0.45, "흩날리는 검(8성)": 0.35,
    "붉은 맹약(6성)": 0.18
}

# 회복량 증가 룬
heal_runes = {
    "집행자(8성)": 0.20,
    "신성한 수양(6성)": 0.12,
    "신성한 칙령(8성)": 0.09
}

# --- UI 구성 ---
st.title("마비노기 모바일 힐량 계산기 (30레벨 기준)")

atk = st.number_input("기본 마을 공격력", min_value=0, value=15681)
heal = st.number_input("회복력", min_value=0, value=2485)

st.markdown("### 🔘 추가 옵션")
master_emblem = st.checkbox("🟦 마스터 엠블렘 착용 (+15% 공격력)")

st.markdown("### 📦 룬 선택")

def checkbox_group(title, options):
    selected = []
    with st.expander(title):
        for name in options:
            if st.checkbox(name, key=f"{title}-{name}"):
                selected.append(name)
    return selected

weapon_runes = checkbox_group("무기 룬 (공격력)", list(attack_runes.keys())[:4])
armor_runes = checkbox_group("방어구 룬 (공격력)", list(attack_runes.keys())[4:26] + ["붉은 맹약(6성)"])
emblem_runes = checkbox_group("엠블럼 (공격력)", list(attack_runes.keys())[26:-1])
weapon_heal = checkbox_group("무기 룬 (회복량)", list(heal_runes.keys())[:1])
combined_runes = checkbox_group("방어구 룬 (공격력 + 회복량)", list(heal_runes.keys())[1:])

# --- 계산 ---
total_attack_buff = sum(attack_runes[r] for r in weapon_runes + armor_runes + emblem_runes)
if master_emblem:
    total_attack_buff += 0.15
total_attack_buff *= 0.73

corrected_atk = int(atk + atk * total_attack_buff)

total_heal_buff = sum(heal_runes[r] for r in weapon_heal + combined_runes)
if "신성한 수양(6성)" in combined_runes:
    total_heal_buff += 0.12
if "신성한 칙령(8성)" in combined_runes:
    total_heal_buff += 0.09

heal_multiplier = (1.1 + total_heal_buff) * (1 + heal / 8750)

# --- 결과 출력 ---
st.markdown("## 💡 힐량 계산 결과 (30레벨 기준)")
st.markdown(f"🔺 **보정 공격력:** `{corrected_atk}`")

results = []
for skill, coeff in skill_data.items():
    base_heal = int(atk * coeff * (1.1 * (1 + heal / 8750)))
    boosted_heal = int(corrected_atk * coeff * heal_multiplier)
    results.append({
        "스킬": skill,
        "기본 힐량": base_heal,
        "보정 힐량": boosted_heal
    })

st.dataframe(pd.DataFrame(results), use_container_width=True)
