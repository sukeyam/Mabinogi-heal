
import streamlit as st
import pandas as pd

# 스킬 계수 하드코딩
skill_data = [
    {"스킬": "라이프 링크", "계수": 0.015964145},
    {"스킬": "라이프 링크 (서약 룬)", "계수": 0.015949141},
    {"스킬": "팬텀 페인 (억압 룬)", "계수": 0.025963149},
    {"스킬": "생명의 고동(물결 룬)", "계수": 0.017593896},
    {"스킬": "프로텍션 (감쌈 룬)", "계수": 0.019462414},
    {"스킬": "프로텍션-회복량 (광륜 룬)", "계수": 0.129972591},
    {"스킬": "프로텍션-지속 회복량 (광륜 룬)", "계수": 0.019482925},
    {"스킬": "서먼 루미너스", "계수": 0.023964738},
    {"스킬": "윙오브 엔젤", "계수": 0.191977183},
]

# UI 입력
st.title("💖 마비노기 모바일 시즌1 힐량 계산기")
atk = st.number_input("기본 마을 공격력", min_value=0, value=15000)
heal = st.number_input("회복력", min_value=0, value=2000)

st.subheader("🧩 추가 옵션")
master_emblem = st.checkbox("마스터 엠블렘 착용 (+15% 공격력)")

# 룬 카테고리별 체크박스 (공격력 증가)
st.subheader("📦 룬 선택")

st.markdown("**무기 룬 (공격력)**")
weapon_runes_atk = {
    "영혼 수확자 (20%)": 0.20,
    "검무+ (20%)": 0.20,
    "마지막 자비 (20%)": 0.20,
    "종언+ (20%)": 0.20,
}
weapon_selected = [r for r in weapon_runes_atk if st.checkbox(r, key=r)]

st.markdown("**방어구 룬 (공격력)**")
armor_runes_atk = {
    "초기+ (20%)": 0.20,
    "저격+ (15%)": 0.15,
    "마나격류 (14%)": 0.14,
    "바위거인 (20%)": 0.20,
    "비열한 일격 (24%)": 0.24,
    "붉은 맹약 (18%)": 0.18,
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
armor_selected = [r for r in armor_runes_atk if st.checkbox(r, key=r)]

st.markdown("**엠블럼 (공격력)**")
emblem_runes = {
    "굳건함+ (10%)": 0.10,
    "여신의 권능 (13%)": 0.13,
    "인도하는 빛 (20%)": 0.20,
    "대마법사 (45%)": 0.45,
    "흩날리는 검 (35%)": 0.35,
}
emblem_selected = [r for r in emblem_runes if st.checkbox(r, key=r)]

# 회복력 증가 룬
st.markdown("**무기 룬 (회복량)**")
healing_runes = {
    "집행자 (20%)": 0.20,
}
healing_selected = [r for r in healing_runes if st.checkbox(r, key=r)]

# 공격력 + 회복력 증가 룬
st.markdown("**방어구 룬 (공격력 + 회복량)**")
dual_runes = {
    "신성한 수양 (공12% 회12%)": (0.12, 0.12),
    "신성한 칙령 (공15% 회9%)": (0.15, 0.09),
}
dual_selected = [r for r in dual_runes if st.checkbox(r, key=r)]

# 계산
atk_bonus = sum([weapon_runes_atk[r] for r in weapon_selected]) +             sum([armor_runes_atk[r] for r in armor_selected]) +             sum([emblem_runes[r] for r in emblem_selected])

if master_emblem:
    atk_bonus += 0.15

atk_bonus += sum([dual_runes[r][0] for r in dual_selected])
final_atk = atk + atk * atk_bonus * 0.73

heal_bonus = sum([healing_runes[r] for r in healing_selected]) +              sum([dual_runes[r][1] for r in dual_selected])

final_heal_multiplier = 1.1 + heal_bonus
heal_coefficient = 1 + heal / 8750

# 출력
st.subheader("💡 힐량 계산 결과 (30레벨 기준)")
st.markdown(f"🔺 **보정 공격력** : `{int(final_atk):,}`")

# 결과 표 생성
result = []
for skill in skill_data:
    coef = skill["계수"]
    base = coef * atk * 1.1 * (1 + heal / 8750)
    boosted = coef * final_atk * final_heal_multiplier * heal_coefficient
    result.append({
        "스킬": skill["스킬"],
        "기본 힐량": int(round(base)),
        "보정 힐량": int(round(boosted))
    })

df_result = pd.DataFrame(result)
st.dataframe(df_result, hide_index=True, use_container_width=True)
