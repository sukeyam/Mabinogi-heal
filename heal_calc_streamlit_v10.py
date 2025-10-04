
import streamlit as st
import pandas as pd

# 힐 계수 불러오기
df = pd.read_excel("힐러 스킬별 힐 계수.xlsx")

st.set_page_config(layout="wide")
st.title("마비노기 모바일 시즌1 힐량 계산기")

# 입력값
col1, col2 = st.columns(2)
with col1:
    base_atk = st.number_input("기본 마을 공격력", value=0)
with col2:
    healing_stat = st.number_input("회복력", value=0)

st.markdown("---")

# 룬 카테고리별 체크박스 (% 표시 포함)
st.subheader("공격력 증가 룬 선택")
col1, col2, col3 = st.columns(3)

atk_runes_weapon = {
    "영혼 수확자 (20%)": 0.20, "검무+ (20%)": 0.20, "마지막 자비 (20%)": 0.20, "종언+ (20%)": 0.20
}
atk_runes_armor = {
    "초기+ (20%)": 0.20, "저격+ (15%)": 0.15, "마나격류 (14%)": 0.14, "바위거인 (20%)": 0.20,
    "비열한 일격 (24%)": 0.24, "여명+ (21%)": 0.21, "바위 감시자 (22%)": 0.22, "저무는 달 (20%)": 0.20,
    "땅울림 (30%)": 0.30, "침묵하는 산 (22%)": 0.22, "필사+ (20%)": 0.20, "파멸+ (25%)": 0.25,
    "성역+ (17%)": 0.17, "섬세한 손놀림 (6%)": 0.06, "압도적인 힘 (6%)": 0.06, "붕괴하는 별 (10%)": 0.10,
    "지휘관 (22.5%)": 0.225, "나무 사슴 (12%)": 0.12, "수정 꽃잎 (12%)": 0.12, "어두운 징도 (18%)": 0.18,
    "바스러지는 빛 (27.5%)": 0.275, "이름 없는 혼돈 (40%)": 0.40, "붉은 맹약 (18%)": 0.18
}
atk_runes_emblem = {
    "굳건함+ (10%)": 0.10, "여신의 권능 (13%)": 0.13, "인도하는 빛 (20%)": 0.20,
    "대마법사 (45%)": 0.45, "흩날리는 검 (35%)": 0.35
}

with col1:
    st.markdown("**무기 룬**")
    selected_weapon = [v for k, v in atk_runes_weapon.items() if st.checkbox(k)]
with col2:
    st.markdown("**방어구 룬**")
    selected_armor = [v for k, v in atk_runes_armor.items() if st.checkbox(k)]
with col3:
    st.markdown("**엠블럼 룬**")
    selected_emblem = [v for k, v in atk_runes_emblem.items() if st.checkbox(k)]
    master_emblem = st.checkbox("마스터 엠블렘 착용 (15%)")

# 보정 공격력 계산
atk_bonus_sum = sum(selected_weapon + selected_armor + selected_emblem)
if master_emblem:
    atk_bonus_sum += 0.15 * 0.73
corrected_atk = int(base_atk * (1 + atk_bonus_sum))

# 힐 계수 계산
heal_multiplier = (1.1 + 0) * (1 + healing_stat / 8750)  # 회복량 증가율은 추후 확장 가능

# 힐량 계산
df["기본 힐량"] = (base_atk * df["힐계수"] * heal_multiplier).round()
df["보정 힐량"] = (corrected_atk * df["힐계수"] * heal_multiplier).round()

# 힐량 표 출력
st.markdown("## 힐량 계산 결과 (30레벨 기준)")
st.write(f"**보정 공격력:** :red[**{corrected_atk}**]")
st.dataframe(df[["스킬명", "기본 힐량", "보정 힐량"]], use_container_width=True)

st.markdown(":red[*힐량은 스킬 레벨 30 기준입니다.]")
