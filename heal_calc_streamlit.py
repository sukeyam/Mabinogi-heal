
import streamlit as st

# 스킬 계수 테이블
skill_coefficients = {
    "물결":     [0.011, 0.0121, 0.0132, 0.0143, 0.0154, 0.0165, 0.0176],
    "감쌈":     [0.015, 0.0165, 0.018, 0.0195, 0.021, 0.0225, 0.024],
    "루미너스": [0.015, 0.0156, 0.018, 0.0195, 0.021, 0.0225, 0.024],
    "빛무리":   [0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032],
    "억압":     [0.015, 0.0165, 0.018, 0.0195, 0.0205, 0.0225, 0.024]
}

# 스킬별 틱 수
skill_ticks = {
    "물결": 1,
    "감쌈": 15,
    "루미너스": 10,
    "빛무리": 10,
    "억압": 6
}

# 버프 목록과 공격력 증가율
buffs = {
    "영혼수확자 (+20%)": 0.20,
    "마나격류 (+14%)": 0.14,
    "바위거인 (+20%)": 0.20,
    "붉은 맹약 (+18%)": 0.18,
    "비열한 일격 (+24%)": 0.24,
    "신성한 수양 (+12%)": 0.12,
    "저격 (+15%)": 0.15,
}

st.title("마비노기 모바일 힐량 계산기")

# 입력 UI 구성
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    base_attack = st.number_input("기본 마을 공격력", min_value=0, value=15681)
    recovery = st.number_input("회복력", min_value=0, value=2485)
    selected_buffs = [st.checkbox(buff) for buff in buffs]

with col2:
    st.markdown("### 스킬 레벨 선택")
    levels = {}
    for skill in ["물결", "감쌈", "루미너스", "빛무리", "억압"]:
        level = st.selectbox(f"{skill} 레벨", options=[0, 5, 10, 15, 20, 25, 30], index=6)
        levels[skill] = level

with col3:
    if st.button("힐량 계산하기"):
        # 보정 공격력 계산
        total_buff = sum([list(buffs.values())[i] for i, selected in enumerate(selected_buffs) if selected])
        adjusted_attack = round(base_attack * (1 + total_buff))

        # 회복력 보정계수
        recovery_multiplier = 1 + (recovery * 0.0003)

        # 결과 계산
        st.markdown(f"### :red[보정 공격력]: **:red[{adjusted_attack:,}]**", unsafe_allow_html=True)
        st.markdown("### 보정 기준 힐량", unsafe_allow_html=True)

        for skill in ["물결", "감쌈", "루미너스", "빛무리", "억압"]:
            index = levels[skill] // 5
            coeff = skill_coefficients[skill][index]
            tick = skill_ticks[skill]
            base_heal = round(base_attack * coeff * recovery_multiplier)
            total_heal = round(base_heal * tick)
            adjusted_heal = round(adjusted_attack * coeff * recovery_multiplier)
            adjusted_total_heal = round(adjusted_heal * tick)

            st.markdown(
                f"#### {skill} : 기본공격력 기준 {base_heal:,} × {tick} = {total_heal:,} / 보정공격력 기준 {adjusted_heal:,} × {tick} = {adjusted_total_heal:,}"
            )

        st.markdown(
            "<span style='color:red;'>*빛무리, 루미너스, 억압은 정확한 스킬계수를 알 수 없어 수치가 틀릴 확률이 높습니다.</span>",
            unsafe_allow_html=True
        )
