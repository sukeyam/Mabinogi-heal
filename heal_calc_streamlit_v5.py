
import streamlit as st

# 힐 스킬별 계수 (30레벨 기준)
skill_data = {
    "라이프 링크": 0.018,
    "라이프 링크 (서약 룬)": 0.021,
    "팬텀 페인 (억압 룬)": 0.024,
    "프로텍션 (감쌈 룬)": 0.024,
    "프로텍션-회복량 (광륜 룬)": 0.016,
    "프로텍션-지속 회복량 (광륜 룬)": 0.008,
    "서먼 루미너스": 0.024,
    "윙 오브 엔젤": 0.032
}

# 공격력 증가 룬 사전 (이름: 수치)
attack_runes = {
    "마스터 엠블렘": 0.15,
    "영혼 수확자(6성)": 0.20,
    "검무+(8성)": 0.20,
    "마지막 자비(8성)": 0.20,
    "종언+(8성)": 0.20,
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
    "굳건함+(6성)": 0.10,
    "여신의 권능(6성)": 0.13,
    "인도하는 빛(8성)": 0.20,
    "대마법사(8성)": 0.45,
    "흩날리는 검(8성)": 0.35,
    "신성한 수양(6성)": 0.12,
    "신성한 칙령(8성)": 0.15
}

# 회복력 증가 룬
heal_runes = {
    "집행자(8성)": 0.20,
    "붉은 맹약(6성)": 0.18,
    "신성한 수양(6성) - 회복량": 0.12,
    "신성한 칙령(8성) - 회복량": 0.09
}

# Streamlit UI
st.title("마비노기 모바일 힐량 계산기 (시즌1 기준)")
base_attack = st.number_input("기본 마을 공격력", min_value=0, value=26000)
base_heal = st.number_input("회복력", min_value=0, value=2500)

# 룬 선택 체크박스
st.subheader("공격력 증가 룬 선택")
selected_attack_runes = []
for rune in attack_runes:
    if st.checkbox(rune):
        selected_attack_runes.append(rune)

st.subheader("회복량 증가 룬 선택")
selected_heal_runes = []
for rune in heal_runes:
    if st.checkbox(rune):
        selected_heal_runes.append(rune)

# 보정 공격력 계산
attack_bonus = sum(attack_runes[r] for r in selected_attack_runes if r in attack_runes)
adjusted_attack = int(base_attack * (1 + attack_bonus * 0.73))

# 보정 회복력 증가량
heal_bonus = sum(heal_runes[r] for r in selected_heal_runes if r in heal_runes)
total_multiplier = (1.1 + heal_bonus) * (1 + base_heal / 8750)

# 출력
st.markdown(f"### ✅ 보정 공격력: **:red[{adjusted_attack}]**")
st.markdown(f"### ✅ 힐량 계산 결과 (30레벨 기준)")

for skill, coefficient in skill_data.items():
    base_heal_amount = int(base_attack * coefficient * total_multiplier)
    boosted_heal_amount = int(adjusted_attack * coefficient * total_multiplier)
    st.markdown(f"**{skill}**")
    st.markdown(f"- 기본 힐량: {base_heal_amount}")
    st.markdown(f"- 룬 적용 최대 힐량: {boosted_heal_amount}")
