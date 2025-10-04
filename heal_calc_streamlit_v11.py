
import streamlit as st
import pandas as pd

# 스킬 계수 데이터 불러오기
excel_file = '힐러 스킬별 힐 계수.xlsx'
df = pd.read_excel(excel_file)

# 스킬 순서 재정렬 및 이름 수정
skill_order = [
    "라이프 링크",
    "라이프 링크 (서약 룬)",
    "팬텀 페인 (억압 룬)",
    "생명의 고동(물결 룬)",
    "프로텍션 (감쌈 룬)",
    "프로텍션-회복량 (광륜 룬)",
    "프로텍션-지속 회복량 (광륜 룬)",
    "서먼 루미너스",
    "윙오브 엔젤"
]
df = df[df['스킬명'].isin(skill_order)]
df['스킬명'] = pd.Categorical(df['스킬명'], categories=skill_order, ordered=True)
df = df.sort_values('스킬명')

# UI 구성
st.title("마비노기 모바일 힐량 계산기")

col1, col2 = st.columns(2)
with col1:
    base_atk = st.number_input("기본 마을 공격력", value=25000)
    heal_stat = st.number_input("회복력", value=2500)
with col2:
    st.markdown("### 마스터 엠블렘")
    master_emblem = st.checkbox("마스터 엠블렘 착용 (+15%)")

st.markdown("## 룬 선택")

# 룬 카테고리 및 항목 구성
weapon_runes = {
    "영혼 수확자 (6성) (+20%)": 0.20,
    "검무+ (8성) (+20%)": 0.20,
    "마지막 자비 (8성) (+20%)": 0.20,
    "종언+ (8성) (+20%)": 0.20
}

armor_runes = {
    "초기+ (6성) (+20%)": 0.20,
    "저격+ (6성) (+15%)": 0.15,
    "마나격류 (6성) (+14%)": 0.14,
    "바위거인 (6성) (+20%)": 0.20,
    "비열한 일격 (6성) (+24%)": 0.24,
    "여명+ (8성) (+21%)": 0.21,
    "바위 감시자 (8성) (+22%)": 0.22,
    "저무는 달 (8성) (+20%)": 0.20,
    "땅울림 (8성) (+30%)": 0.30,
    "침묵하는 산 (8성) (+22%)": 0.22,
    "필사+ (8성) (+20%)": 0.20,
    "파멸+ (8성) (+25%)": 0.25,
    "성역+ (8성) (+17%)": 0.17,
    "섬세한 손놀림 (8성) (+6%)": 0.06,
    "압도적인 힘 (8성) (+6%)": 0.06,
    "붕괴하는 별 (8성) (+10%)": 0.10,
    "지휘관 (8성) (+22.5%)": 0.225,
    "나무 사슴 (8성) (+12%)": 0.12,
    "수정 꽃잎 (8성) (+12%)": 0.12,
    "어두운 징도 (8성) (+18%)": 0.18,
    "바스러지는 빛 (신화) (+27.5%)": 0.275,
    "이름 없는 혼돈 (신화) (+40%)": 0.40,
    "붉은 맹약 (6성) (+18%)": 0.18
}

emblem_runes = {
    "굳건함+ (6성) (+10%)": 0.10,
    "여신의 권능 (6성) (+13%)": 0.13,
    "인도하는 빛 (8성) (+20%)": 0.20,
    "대마법사 (8성) (+45%)": 0.45,
    "흩날리는 검 (8성) (+35%)": 0.35,
}

# 룬 체크박스 UI 표시 및 선택값 수집
total_buff = 0
st.markdown("### 무기 룬")
for name, val in weapon_runes.items():
    if st.checkbox(name):
        total_buff += val

st.markdown("### 방어구 룬")
for name, val in armor_runes.items():
    if st.checkbox(name):
        total_buff += val

st.markdown("### 엠블럼 룬")
for name, val in emblem_runes.items():
    if st.checkbox(name):
        total_buff += val

if master_emblem:
    total_buff += 0.15 * 0.73  # 마스터 엠블렘 보정

# 보정 공격력 계산
final_atk = int(base_atk * (1 + total_buff))

# 힐량 계산
heal_ratio = 1.1 * (1 + heal_stat / 8750)
df['기본 힐량'] = (df['계수'] * base_atk * heal_ratio).round().astype(int)
df['보정 힐량'] = (df['계수'] * final_atk * heal_ratio).round().astype(int)

# 출력
st.markdown("## 힐량 계산 결과 (30레벨 기준)")
st.markdown(f"**보정 공격력: <span style='color:red; font-size:20px'><b>{final_atk}</b></span>**", unsafe_allow_html=True)
st.dataframe(df[['스킬명', '기본 힐량', '보정 힐량']].set_index("스킬명"), use_container_width=True)
