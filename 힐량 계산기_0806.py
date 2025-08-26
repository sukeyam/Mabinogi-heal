import tkinter as tk
from tkinter import ttk, messagebox

BUFFS = {
    "영혼수확자": 0.20,
    "마나격류": 0.14,
    "바위거인": 0.20,
    "붉은 맹약": 0.18,
    "비열한 일격": 0.24,
    "신성한 수양": 0.12,
    "저격": 0.15
}

# 스킬 순서 정의
SKILL_ORDER = ["물결", "감쌈", "루미너스", "빛무리", "억압"]

SKILL_TABLE = {
    "물결":     [0.011, 0.0121, 0.0132, 0.0143, 0.0154, 0.0165, 0.0176],
    "루미너스": [0.015, 0.0156, 0.018, 0.0195, 0.021, 0.0225, 0.024],
    "빛무리":   [0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032],
    "억압":     [0.015, 0.0165, 0.018, 0.0195, 0.0205, 0.0225, 0.024],
    "감쌈":     [0.015, 0.0165, 0.018, 0.0195, 0.021, 0.0225, 0.024]
}

SKILL_TICKS = {
    "물결": 15,
    "루미너스": 10,
    "빛무리": 10,
    "억압": 6,
    "감쌈": 15
}

def get_skill_coef(skill, level):
    index = level // 5
    return SKILL_TABLE[skill][index]

def calculate_heals():
    try:
        base_atk = float(entry_atk.get())
        heal_stat = float(entry_heal.get())
        heal_boost = 1 + (heal_stat * 0.0003)
        buff_total = sum(BUFFS[name] for name in BUFFS if buff_vars[name].get())
        corrected_atk = round(base_atk * (1 + buff_total))

        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"[보정 공격력: {corrected_atk:,} (버프 적용 {int(buff_total*100)}%)]\n\n", "redbold")

        result_text.insert(tk.END, "[기본 기준 힐량]\n", "bold")
        for skill in SKILL_ORDER:
            level = int(skill_levels[skill].get())
            coef = get_skill_coef(skill, level)
            ticks = SKILL_TICKS[skill]
            base_tick = round(base_atk * coef * heal_boost)
            base_total = round(base_tick * ticks)
            result_text.insert(tk.END, f"{skill} (Lv.{level}): 틱당 {base_tick:,} / 총 {base_total:,}\n", "default")

        result_text.insert(tk.END, "\n[보정 기준 힐량]\n", "boldbig")
        for skill in SKILL_ORDER:
            level = int(skill_levels[skill].get())
            coef = get_skill_coef(skill, level)
            ticks = SKILL_TICKS[skill]
            corr_tick = round(corrected_atk * coef * heal_boost)
            corr_total = round(corr_tick * ticks)
            result_text.insert(tk.END, f"{skill} (Lv.{level}): 틱당 {corr_tick:,} / 총 {corr_total:,}\n", "default")

        result_text.insert(tk.END, "\n*빛무리, 루미너스, 억압은 정확한 스킬계수를 알 수 없어 수치가 틀릴 확률이 높습니다.", "warning")
        result_text.config(state='disabled')

    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 정확히 입력해주세요.")

# GUI 구성
root = tk.Tk()
root.title("마비노기 모바일 힐량 계산기")
root.geometry("980x600")

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

buff_frame = tk.Frame(root)
buff_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

level_frame = tk.Frame(root)
level_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=10, sticky="n")

result_frame = tk.Frame(root)
result_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="n")

tk.Label(input_frame, text="기본 마을 공격력:").pack(anchor="w")
entry_atk = tk.Entry(input_frame, width=15)
entry_atk.pack()
entry_atk.insert(0, "15681")

tk.Label(input_frame, text="회복력:").pack(anchor="w", pady=(10, 0))
entry_heal = tk.Entry(input_frame, width=15)
entry_heal.pack()
entry_heal.insert(0, "2485")

tk.Label(buff_frame, text="버프 선택:").pack(anchor="w", pady=(10, 5))
buff_vars = {}
for name in BUFFS:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(buff_frame, text=f"{name} (+{int(BUFFS[name]*100)}%)", variable=var)
    cb.pack(anchor="w")
    buff_vars[name] = var

tk.Label(level_frame, text="스킬 레벨 선택 (0~30, 5단위):").pack(anchor="w", pady=(10, 5))
skill_levels = {}
LEVEL_OPTIONS = [str(i) for i in range(0, 31, 5)]
for skill in SKILL_ORDER:
    tk.Label(level_frame, text=skill).pack(anchor="w")
    combo = ttk.Combobox(level_frame, values=LEVEL_OPTIONS, state="readonly", width=5)
    combo.set("30")
    combo.pack(anchor="w")
    skill_levels[skill] = combo

tk.Button(result_frame, text="힐량 계산하기", command=calculate_heals).pack(pady=5)
result_text = tk.Text(result_frame, height=30, width=50, wrap="word")
result_text.pack()
result_text.tag_configure("redbold", foreground="red", font=("Helvetica", 12, "bold"))
result_text.tag_configure("bold", font=("Helvetica", 11, "bold"))
result_text.tag_configure("boldbig", font=("Helvetica", 13, "bold"))
result_text.tag_configure("default", font=("Helvetica", 10))
result_text.tag_configure("warning", foreground="red", font=("Helvetica", 9))
result_text.config(state='disabled')

root.mainloop()
