
import streamlit as st
import pandas as pd

# 스킬 계수 하드코딩
skill_data = {
    "스킬명": [
        "라이프 링크",
        "라이프 링크 (서약 룬)",
        "팬텀 페인 (억압 룬)",
        "생명의 고동(물결 룬, 괄호 안의 수치는 자힐 수치)",
        "프로텍션 (감쌈 룬)",
        "프로텍션-회복량 (광륜 룬)",
        "프로텍션-지속 회복량 (광륜 룬)",
        "서먼 루미너스",
        "윙오브 엔젤"
    ],
    "30레벨 계수": [
        0.015964145,
        0.015949141,
        0.025963149,
        0.017593896,
        0.019462414,
        0.129972591,
        0.019482925,
        0.023964738,
        0.191977183
    ]
}
df_skills = pd.DataFrame(skill_data)

st.set_page_config(page_title="마비노기 모바일 힐량 계산기 (시즌 1)", layout="centered")

# 타이틀
st.markdown("<h1 style='text-align: center; color: gold;'>💉 마비노기 모바일 힐량 계산기 (시즌 1)</h1>", unsafe_allow_html=True)

# 기본 입력
st.subheader("📌 기본 정보 입력")
col1, col2 = st.columns(2)
with col1:
    attack = st.number_input("보정 공격력", min_value=0, value=15000, step=100)
with col2:
    recovery = st.number_input("회복력", min_value=0, value=2500, step=50)

# 안내 문구
st.markdown("""
<div style='font-size: 14px; color: #CCCCCC;'>
※ 시즌 1에서 보정 공격력 값을 구하는 방식이 바뀌었기 때문에, 부득이하게 보정공격력과 회복력(마을에서의 기본 회복력)을 입력해주세요. 

※ 보정 공격력은 허수아비를 치면서 모든 버프가 켜진상태에서 스탯창의 공격력이 최고로 증가한 수치를 기입해 주시면 됩니다. (금방합니다) 

※ 만약 보정 힐량이 다르게 나온다면, 본인의 스킬레벨이 30레벨이 아닐겁니다. (힐 스킬 계수를 정확하게 입력했기 때문에 비슷하게라도 나와야 정상입니다. / 보통 허수아비에서 생명의 고동 자힐로 체크하시면 됩니다.)
</div>
""", unsafe_allow_html=True)

# 회복량 증가 룬
st.subheader("💠 회복량 증가 룬 선택")
col1, col2, col3 = st.columns(3)
with col1:
    rune_1 = st.checkbox("집행자 (무기 룬, 회복량 20%)")
with col2:
    rune_2 = st.checkbox("신성한 수양 (방어구 룬, 회복량 12%)")
with col3:
    rune_3 = st.checkbox("신성한 칙령 (방어구 룬, 회복량 9%)")

st.markdown("""
<div style='font-size: 13px; color: #999999; margin-bottom: 20px;'>
※ 신성한 칙령은 아군의 체력 회복 시 공격력 15%, 회복량 9%가 증가하는데, 본인 회복시에도 증가하는지는 검증되지 않았습니다. (룬이 없어서 실험 못해봤어요.)
</div>
""", unsafe_allow_html=True)

# 회복량 증가율 계산
healing_multiplier = 1.1
if rune_1:
    healing_multiplier += 0.20
if rune_2:
    healing_multiplier += 0.12
if rune_3:
    healing_multiplier += 0.09

# 힐량 계산
def calculate_heal(coeff, atk, recov, mult):
    return round(coeff * atk * mult * (1 + recov / 8750))

# 결과 계산
result = []
for idx, row in df_skills.iterrows():
    base_heal = calculate_heal(row["30레벨 계수"], attack, recovery, healing_multiplier)
    if "생명의 고동" in row["스킬명"]:
        result.append(f"{base_heal:,} ({round(base_heal/2):,})")
    else:
        result.append(f"{base_heal:,}")

df_skills["보정 힐량"] = result

# 결과 출력
st.subheader("📊 힐량 계산 결과 (스킬 30레벨 기준)")
st.dataframe(df_skills[["스킬명", "보정 힐량"]], use_container_width=True)
