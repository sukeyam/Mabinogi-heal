
import streamlit as st
import pandas as pd

st.title("마비노기 모바일 시즌1 힐량 계산기")

# 입력값
base_atk = st.number_input("기본 마을 공격력", value=20000)
heal_stat = st.number_input("회복력", value=2000)

st.markdown("### 마스터 엠블렘")
master_emblem = st.checkbox("마스터 엠블렘 착용 (공격력 +15%)")

# 룬 분류
st.markdown("### ✅ 무기 룬 선택")
weapon_runes = {
    "영혼 수확자 (20%)": 0.20,
    "검무+ (20%)": 0.20,
    "마지막 자비 (20%)": 0.20,
    "종언+ (20%)": 0.20,
}
selected_weapon = [r for r in weapon_runes if st.checkbox(r, key=r)]

st.markdown("### ✅ 방어구 룬 선택")
armor_runes = {
    "초기+ (20%)": 0.20,
    "저격+ (15%)": 0.15,
    "마나격류 (14%)": 0.14,
    "바위거인 (20%)": 0.20,
    "비열한 일격 (24%)": 0.24,
    "여명+ (21%)": 0.21,
    "바위 감시자 (22%)": 0.22,
    "저무는 달 (20%)": 0.20,
    "땅울림 (30%)": 0.30,
    "침묵하는 산 (22%)": 0.22,
    "필사+ (20%)": 0.20,
    "파멸+ (25%)": 0.25,
    "성역+ (17%)": 0.17,
    "섬세한 손놀림 (6%)": 0.06,
    "압도적인 힘 (6%)": 0.06,
    "붕괴하는 별 (10%)": 0.10,
    "지휘관 (22.5%)": 0.225,
    "나무 사슴 (12%)": 0.12,
    "수정 꽃잎 (12%)": 0.12,
    "어두운 징도 (18%)": 0.18,
    "바스러지는 빛 (27.5%)": 0.275,
    "이름 없는 혼돈 (40%)": 0.40,
}
selected_armor = [r for r in armor_runes if st.checkbox(r, key=r)]

st.markdown("### ✅ 엠블럼 룬 선택")
emblem_runes = {
    "굳건함+ (10%)": 0.10,
    "여신의 권능 (13%)": 0.13,
    "인도하는 빛 (20%)": 0.20,
    "대마법사 (45%)": 0.45,
    "흩날리는 검 (35%)": 0.35,
}
selected_emblem = [r for r in emblem_runes if st.checkbox(r, key=r)]

# 공격력 증가 총합 (마스터 엠블렘 제외)
total_bonus = sum([weapon_runes[r] for r in selected_weapon]) +               sum([armor_runes[r] for r in selected_armor]) +               sum([emblem_runes[r] for r in selected_emblem])

# 최종 보정 공격력 계산
final_atk = base_atk * (1 + total_bonus * 0.73)
if master_emblem:
    final_atk += base_atk * 0.15  # 예외 적용

# 힐 계수 계산
heal_multiplier = (1.1) * (1 + heal_stat / 8750)

# 스킬 리스트
skills = {
    "라이프 링크": 0.018,
    "라이프 링크 (서약 룬)": 0.021,
    "팬텀 페인 (억압 룬)": 0.024,
    "프로텍션 (감쌈 룬)": 0.024,
    "프로텍션-회복량 (광륜 룬)": 0.016,
    "프로텍션-지속 회복량 (광륜 룬)": 0.008,
    "서먼 루미너스": 0.024,
    "윙 오브 엔젤": 0.032,
    "생명의 고동": 0.020,
}

# 결과 출력
if st.button("힐량 계산하기"):
    st.markdown(f"### ✅ 보정 공격력: <span style='color:red; font-size:20px; font-weight:bold'>{int(final_atk)}</span>", unsafe_allow_html=True)

    data = []
    for skill, coef in skills.items():
        base_heal = int(base_atk * coef * heal_multiplier)
        final_heal = int(final_atk * coef * heal_multiplier)
        data.append([skill, base_heal, final_heal])

    df = pd.DataFrame(data, columns=["스킬명", "기본 힐량", "룬 적용 힐량"])
    st.markdown("### 힐량 계산 결과 (30레벨 기준)")
    st.table(df)
