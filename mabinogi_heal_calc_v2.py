
import streamlit as st
import pandas as pd

# 힐 계수 데이터
skill_data = {'스킬': ['라이프 링크', '라이프 링크 (서약 룬)', '팬텀 페인 (억압 룬)', '생명의 고동(물결 룬)', '프로텍션 (감쌈 룬)', '프로텍션-회복량 (광륜 룬)', '프로텍션-지속 회복량 (광륜 룬)', '서먼 루미너스', '윙오브 엔젤'], '30레벨 계수': [0.015964145, 0.015949141, 0.025963149, 0.017593896, 0.019462414, 0.129972591, 0.019482925, 0.023964738, 0.191977183]}

df = pd.DataFrame(skill_data)

st.title("마비노기 모바일 힐량 계산기 (시즌 1)")

# 기본 정보 입력
st.subheader("✅ 기본 정보 입력")
col1, col2 = st.columns(2)
with col1:
    attack = st.number_input("보정 공격력", min_value=0, step=1, value=0)
with col2:
    recovery = st.number_input("회복력 (기본 회복력)", min_value=0, step=1, value=0)

st.caption("※ 시즌 1에서 보정 공격력 값을 구하는 방식이 바뀌었기 때문에, 부득이하게 보정공격력과 회복력(마을에서의 기본 회복력)을 입력해주세요.")
st.caption("※ 보정 공격력은 허수아비를 치면서 모든 버프가 켜진상태에서 스탯창의 공격력이 최고로 증가한 수치를 기입해 주시면 됩니다. (금방합니다)")

# 회복량 증가 룬 체크박스
st.subheader("🧪 회복량 증가 룬 선택")
rune_buff = 0.0
r1 = st.checkbox("집행자 (무기 룬, 회복량 20%)")
r2 = st.checkbox("신성한 수양 (방어구 룬, 회복량 12%)")
r3 = st.checkbox("신성한 칙령 (방어구 룬, 회복량 9%)")

if r1: rune_buff += 0.20
if r2: rune_buff += 0.12
if r3: rune_buff += 0.09

st.caption("※ 신성한 칙령은 아군의 체력 회복 시 공격력 15%, 회복량 9%가 증가하는데, 본인 회복시에도 증가하는지는 검증되지 않았습니다. (룬이 없어서 실험 못해봤어요.)")

# 힐량 계산
st.subheader("📊 힐량 계산 결과 (스킬 30레벨 기준)")
results = []
for i, row in df.iterrows():
    coeff = row["30레벨 계수"]
    final_heal = round(coeff * attack * (1.1 + rune_buff) * (1 + recovery / 8750))
    results.append(final_heal)

df["보정 힐량"] = results
st.dataframe(df[["스킬", "보정 힐량"]], use_container_width=True)
