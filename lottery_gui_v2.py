#!/usr/bin/env python3
"""
彩票模拟开奖器 2.0 - 重写版
基于心情、日期、星座、年龄等元素生成"今日幸运号"
⚠️ 纯属娱乐，无任何预测功能
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import hashlib

# ==================== 核心逻辑 ====================

ZODIAC_SIGNS = [
    ("白羊座", 3, 21, 4, 19), ("金牛座", 4, 20, 5, 20),
    ("双子座", 5, 21, 6, 20), ("巨蟹座", 6, 21, 7, 22),
    ("狮子座", 7, 23, 8, 22), ("处女座", 8, 23, 9, 22),
    ("天秤座", 9, 23, 10, 22), ("天蝎座", 10, 23, 11, 21),
    ("射手座", 11, 22, 12, 21), ("摩羯座", 12, 22, 1, 19),
    ("水瓶座", 1, 20, 2, 18), ("双鱼座", 2, 19, 3, 20),
]

MOODS = [
    ("😊", "超开心", "happy"),
    ("😄", "很开心", "very_happy"),
    ("🙂", "心情不错", "good"),
    ("😐", "一般般", "normal"),
    ("😔", "有点低落", "sad"),
    ("😤", "生气中", "angry"),
    ("🤔", "在思考", "thinking"),
]

BLOOD_TYPES = ["A", "B", "O", "AB", "不知道", "其他"]

from zodiac_lucky_generator import generate_zodiac_lucky_numbers

def get_zodiac(day, month):
    for name, m1, d1, m2, d2 in ZODIAC_SIGNS:
        if (month == m1 and day >= d1) or (month == m2 and day <= d2):
            return name
    return "未知"

def hash_md5(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % (10**10)

def generate_lucky(name, birth, zodiac, mood, age, blood, count, ball_min, ball_max, exclude=None):
    """根据用户信息生成幸运号（天文学版）

    exclude: 可选，已排除的号码列表（如大乐透前区已用的号码）
    """
    today = datetime.date.today()
    seed_text = f"{name}_{birth}_{zodiac}_{mood}_{age}_{blood}_{today}"
    base_seed = hash_md5(seed_text)

    rng = random.Random(base_seed)

    # 排除列表
    exclude = exclude or []

    # 用天文学方式生成星座幸运号（每日不同）
    zodiac_pool, _ = generate_zodiac_lucky_numbers(zodiac, today, 5, ball_min, ball_max)

    # 随机选最多3个作为首选
    zp_size = min(3, count, len(zodiac_pool))
    zp = rng.sample(zodiac_pool, zp_size)

    remaining = count - len(zp)
    others = []
    for _ in range(remaining * 5):
        num = rng.randint(ball_min, ball_max)
        if num not in zp and num not in others and num not in exclude:
            others.append(num)
        if len(others) >= remaining:
            break

    return sorted(zp + others[:count])

def ssq_lucky(name, birth, zodiac, mood, age, blood):
    red = generate_lucky(name, birth, zodiac, mood, age, blood, 6, 1, 33)
    blue_seed = hash_md5(f"{name}_{birth}_{zodiac}_{mood}_{age}_{blood}_blue")
    blue = random.Random(blue_seed).randint(1, 16)
    return red, blue

def dlt_lucky(name, birth, zodiac, mood, age, blood):
    today = datetime.date.today()
    # 前区先生成（1-35）
    front = generate_lucky(name, birth, zodiac, mood, age, blood, 5, 1, 35)
    # 后区：用天文学方式生成（1-12），取在范围内的星座幸运数
    back_pool, _ = generate_zodiac_lucky_numbers(zodiac, today, 5, 1, 12)
    back_lucky = [x for x in back_pool if x not in front]
    back_lucky_pick = random.sample(back_lucky, min(2, len(back_lucky))) if len(back_lucky) >= 2 else (back_lucky[:1] if back_lucky else [])

    # 随机补满后区
    rng_seed = hash_md5(f"{name}_back_{birth}_{zodiac}_{mood}_{age}_{blood}_{today}")
    rng = random.Random(rng_seed)
    remaining = 2 - len(back_lucky_pick)
    others = []
    for _ in range(remaining * 10):
        num = rng.randint(1, 12)
        if num not in front and num not in back_lucky_pick and num not in others:
            others.append(num)
        if len(others) >= remaining:
            break
    back = sorted(back_lucky_pick + others)
    while len(back) < 2:
        num = rng.randint(1, 12)
        if num not in back:
            back.append(num)
    return front, sorted(back[:2])

def ssq_draw():
    return sorted(random.sample(range(1, 34), 6)), random.randint(1, 16)

def dlt_draw():
    return sorted(random.sample(range(1, 36), 5)), sorted(random.sample(range(1, 13), 2))

def ssq_check(ur, ub, wr, wb):
    rh = len(set(ur) & set(wr))
    bh = (ub == wb)
    if rh == 6 and bh: return 1, "🏆 一等奖（6红+蓝）", "#f1c40f"
    elif rh == 6: return 2, "🏆 二等奖（6红）", "#f39c12"
    elif rh == 5 and bh: return 3, "🏆 三等奖（5红+蓝）", "#e67e22"
    elif rh == 5 or (rh == 4 and bh): return 4, "🎉 四等奖", "#27ae60"
    elif rh == 4 or (rh == 3 and bh): return 5, "👌 五等奖", "#2ecc71"
    elif bh: return 6, "🎯 六等奖（蓝球）", "#3498db"
    else: return 0, "未中奖", "#95a5a6"

def dlt_check(uf, ub, wf, wb):
    fh = len(set(uf) & set(wf))
    bh = len(set(ub) & set(wb))
    if fh == 5 and bh == 2: return 1, "🏆 一等奖（5前+2后）", "#f1c40f"
    elif fh == 5 and bh == 1: return 2, "🏆 二等奖（5前+1后）", "#f39c12"
    elif fh == 5: return 3, "🏆 三等奖（5前）", "#e67e22"
    elif fh == 4 and bh == 2: return 4, "🎉 四等奖（4前+2后）", "#27ae61"
    elif fh == 4 and bh == 1: return 5, "👌 五等奖（4前+1后）", "#2ecc71"
    elif fh == 4: return 6, "六等奖（4前）", "#3498db"
    elif fh == 3 and bh == 2: return 7, "🎯 七等奖（3前+2后）", "#9b59b6"
    else: return 0, "未中奖", "#95a5a6"

# ==================== GUI ====================

BG = "#1a1a2e"
PANEL_BG = "#16213e"
ENTRY_BG = "#0f3460"
TEXT_FG = "#eaf6ff"
ACCENT = "#3498db"
BTN_GREEN = "#27ae60"
BTN_RED = "#e74c3c"

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("开心猫彩票模拟器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg=BG)

        self.lottery_type = tk.StringVar(value="ssq")
        self.mood = tk.StringVar(value="normal")
        self.blood = tk.StringVar(value="O")
        self.info_ready = False
        self.cached_lucky = None  # 缓存幸运号，开奖时复用

        self.build_ui()

    def build_ui(self):
        # 标题
        hdr = tk.Frame(self.root, bg=PANEL_BG, height=60)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🎰 开心猫彩票模拟器",
                 font=('微软雅黑', 22, 'bold'), fg=TEXT_FG, bg=PANEL_BG).pack(pady=12)

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=15)

        # ===== 左侧面板 =====
        left = tk.LabelFrame(main, text=" ✏️ 今日幸运信息",
                             font=('微软雅黑', 13, 'bold'), fg=TEXT_FG,
                             bg=PANEL_BG, bd=0, labelanchor='n', padx=15, pady=10)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))

        row = 0

        # 名字
        tk.Label(left, text="👤 名字:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)
        self.name_ent = tk.Entry(left, font=('微软雅黑', 11), bg=ENTRY_BG, fg='white',
                                  insertbackground='white', bd=0, width=18)
        self.name_ent.grid(row=row, column=1, sticky='w', padx=10, pady=8)
        self.name_ent.insert(0, "幸运用户")

        row += 1

        # 生日
        tk.Label(left, text="📅 生日:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)
        self.birth_ent = tk.Entry(left, font=('微软雅黑', 11), bg=ENTRY_BG, fg='white',
                                   insertbackground='white', bd=0, width=18)
        self.birth_ent.grid(row=row, column=1, sticky='w', padx=10, pady=8)
        self.birth_ent.insert(0, "1993-12-13")
        tk.Label(left, text="格式：YYYY-MM-DD", font=('微软雅黑', 9), fg='#7f8c8d', bg=PANEL_BG) \
            .grid(row=row, column=2, sticky='w', padx=5)

        row += 1

        # 星座（自动显示）
        tk.Label(left, text="♈ 星座:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)
        self.zodiac_lbl = tk.Label(left, text="（输入生日后自动计算）",
                                   font=('微软雅黑', 11), fg=ACCENT, bg=PANEL_BG)
        self.zodiac_lbl.grid(row=row, column=1, sticky='w', padx=10, pady=8)

        row += 1

        # 心情
        tk.Label(left, text="😐 心情:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)

        mood_frm = tk.Frame(left, bg=PANEL_BG)
        mood_frm.grid(row=row, column=1, columnspan=2, sticky='w', padx=10, pady=8)
        self.mood_btns = {}
        for emoji, label, key in MOODS:
            item_frm = tk.Frame(mood_frm, bg=PANEL_BG)
            item_frm.pack(side='left', padx=3, pady=2)
            b = tk.Button(item_frm, text=emoji, font=('微软雅黑', 14),
                          bg=ENTRY_BG, fg='white', activebackground=ACCENT,
                          activeforeground='white', relief='flat', cursor='hand2',
                          width=3, height=1, command=lambda k=key: self.set_mood(k))
            b.pack()
            lbl = tk.Label(item_frm, text=label, font=('微软雅黑', 8), fg='#bdc3c7', bg=PANEL_BG)
            lbl.pack()
            self.mood_btns[key] = b
        self.mood_btns["normal"].config(bg=ACCENT)

        row += 1

        # 年龄
        tk.Label(left, text="🎂 心情年龄:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)
        self.age_ent = tk.Entry(left, font=('微软雅黑', 11),
                                bg=ENTRY_BG, fg='white', insertbackground='white',
                                bd=0, width=16)
        self.age_ent.grid(row=row, column=1, sticky='w', padx=10, pady=8)
        self.age_ent.insert(0, "30")
        tk.Label(left, text="岁（感觉今年像…）", font=('微软雅黑', 9), fg='#7f8c8d', bg=PANEL_BG) \
            .grid(row=row, column=2, sticky='w', padx=5)

        row += 1

        # 血型
        tk.Label(left, text="🅰️ 血型:", font=('微软雅黑', 12), fg=TEXT_FG, bg=PANEL_BG) \
            .grid(row=row, column=0, sticky='ne', padx=10, pady=8)

        blood_frm = tk.Frame(left, bg=PANEL_BG)
        blood_frm.grid(row=row, column=1, columnspan=2, sticky='w', padx=10, pady=8)
        self.blood_btns = {}
        for i, bt in enumerate(BLOOD_TYPES):
            col = i % 3
            brow = i // 3
            b = tk.Button(blood_frm, text=bt, font=('微软雅黑', 10, 'bold'),
                         width=5, bg=ENTRY_BG, fg='white', activebackground=BTN_RED,
                         activeforeground='white', relief='flat', cursor='hand2',
                         command=lambda t=bt: self.set_blood(t))
            b.grid(row=brow, column=col, padx=3, pady=3)
            self.blood_btns[bt] = b
        self.blood_btns["O"].config(bg=BTN_RED)

        row += 1

        # 确认按钮
        confirm_btn = tk.Button(left, text="✅ 确认信息，生成幸运号",
                                font=('微软雅黑', 13, 'bold'), bg=BTN_GREEN, fg='white',
                                activebackground='#1e8449', relief='flat', cursor='hand2',
                                command=self.on_confirm)
        confirm_btn.grid(row=row, column=0, columnspan=3, pady=20, padx=10, ipady=8)

        # ===== 右侧面板 =====
        right = tk.LabelFrame(main, text=" 🎯 开奖结果",
                              font=('微软雅黑', 13, 'bold'), fg=TEXT_FG,
                              bg=PANEL_BG, bd=0, labelanchor='n', padx=15, pady=10)
        right.pack(side='right', fill='both', expand=True)

        # 玩法切换
        switch = tk.Frame(right, bg=PANEL_BG)
        switch.pack(pady=10)
        tk.Radiobutton(switch, text="双色球", variable=self.lottery_type, value='ssq',
                       font=('微软雅黑', 12), bg=PANEL_BG, fg=TEXT_FG,
                       activebackground=PANEL_BG, selectcolor=ENTRY_BG,
                       command=self.on_type_change).pack(side='left', padx=10)
        tk.Radiobutton(switch, text="大乐透", variable=self.lottery_type, value='dlt',
                       font=('微软雅黑', 12), bg=PANEL_BG, fg=TEXT_FG,
                       activebackground=PANEL_BG, selectcolor=ENTRY_BG,
                       command=self.on_type_change).pack(side='left', padx=10)

        self.rule_lbl = tk.Label(right, text="33红球选6 + 16蓝球选1",
                                  font=('微软雅黑', 10), fg='#7f8c8d', bg=PANEL_BG)
        self.rule_lbl.pack()

        sep = tk.Frame(right, bg='#2c3e50', height=2, width=380)
        sep.pack(pady=12)

        # 幸运号标题
        tk.Label(right, text="您的今日幸运号",
                 font=('微软雅黑', 14, 'bold'), fg='#f39c12', bg=PANEL_BG).pack(pady=(5, 5))
        self.lucky_lbl = tk.Label(right, text="（请先确认信息）",
                                   font=('微软雅黑', 13), fg='#bdc3c7', bg=PANEL_BG,
                                   wraplength=380)
        self.lucky_lbl.pack()

        sep2 = tk.Frame(right, bg='#2c3e50', height=2, width=380)
        sep2.pack(pady=12)

        # 开奖号码标题
        tk.Label(right, text="模拟开奖号码",
                 font=('微软雅黑', 14, 'bold'), fg=BTN_RED, bg=PANEL_BG).pack(pady=(5, 5))
        self.win_lbl = tk.Label(right, text="（点击开奖）",
                                 font=('微软雅黑', 13), fg='#bdc3c7', bg=PANEL_BG,
                                 wraplength=380)
        self.win_lbl.pack()

        # 开奖按钮
        draw_btn = tk.Button(right, text="🎲 开奖",
                             font=('微软雅黑', 16, 'bold'), bg=BTN_RED, fg='white',
                             activebackground='#c0392b', activeforeground='white',
                             relief='flat', cursor='hand2', width=16, height=2,
                             command=self.on_draw)
        draw_btn.pack(pady=15)

        # 结果
        self.result_lbl = tk.Label(right, text="",
                                    font=('微软雅黑', 15, 'bold'), bg=PANEL_BG)
        self.result_lbl.pack(pady=5)

        # 底部
        tk.Label(self.root, text="⚠️ 本程序仅供娱乐，彩票为公益事业，理性购彩",
                 font=('微软雅黑', 9), fg='#555555', bg=BG).pack(side='bottom', pady=5)
        tk.Label(self.root, text="Made by luckycat  ·  luckycat168968@gmail.com",
                 font=('微软雅黑', 8), fg='#888888', bg=BG).pack(side='bottom', pady=2)

    def set_mood(self, key):
        self.mood.set(key)
        for k, b in self.mood_btns.items():
            b.config(bg=ENTRY_BG if k != key else ACCENT)

    def set_blood(self, t):
        self.blood.set(t)
        for k, b in self.blood_btns.items():
            b.config(bg=ENTRY_BG if k != t else BTN_RED)

    def on_type_change(self):
        t = self.lottery_type.get()
        if t == 'ssq':
            self.rule_lbl.config(text="33红球选6 + 16蓝球选1")
        else:
            self.rule_lbl.config(text="35前区选5 + 12后区选2")

        if self.info_ready:
            self.on_confirm()

    def on_confirm(self):
        """确认信息，生成幸运号"""
        try:
            birth_str = self.birth_ent.get().strip()
            parts = birth_str.split('-')
            if len(parts) != 3:
                messagebox.showerror("格式错误", "生日格式应为 YYYY-MM-DD，例如：1990-05-15")
                return

            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            zodiac = get_zodiac(day, month)
            self.zodiac_lbl.config(text=f"{zodiac}")

            name = self.name_ent.get().strip() or "匿名用户"
            mood = self.mood.get()
            blood = self.blood.get()
            # 心情年龄：用户自行输入
            try:
                age = int(self.age_ent.get())
                age = max(1, min(120, age))
            except:
                age = 30

            t = self.lottery_type.get()
            if t == 'ssq':
                red, blue = ssq_lucky(name, birth_str, zodiac, mood, age, blood)
                self.cached_lucky = ('ssq', red, blue)
                self.lucky_lbl.config(
                    text=f"红球：{' '.join(f'[{x:02d}]' for x in red)}  蓝球：[{blue:02d}]",
                    fg='#f39c12'
                )
            else:
                front, back = dlt_lucky(name, birth_str, zodiac, mood, age, blood)
                self.cached_lucky = ('dlt', front, back)
                self.lucky_lbl.config(
                    text=f"前区：{' '.join(f'[{x:02d}]' for x in front)}  后区：{' '.join(f'[{x:02d}]' for x in back)}",
                    fg='#f39c12'
                )

            self.info_ready = True
            self.win_lbl.config(text="点击开奖查看结果", fg='#bdc3c7')
            self.result_lbl.config(text="")

        except Exception as e:
            import traceback
            messagebox.showerror("出错啦", f"错误：{e}\n\n{traceback.format_exc()}")

    def on_draw(self):
        """开奖"""
        if not self.info_ready or not self.cached_lucky:
            messagebox.showinfo("提示", "请先点击上方「确认信息」按钮生成幸运号！")
            return

        try:
            t = self.lottery_type.get()
            win_red, win_blue = ssq_draw()
            win_front, win_back = dlt_draw()

            if t == 'ssq':
                _, lucky_red, lucky_blue = self.cached_lucky
                self.lucky_lbl.config(
                    text=f"红球：{' '.join(f'[{x:02d}]' for x in lucky_red)}  蓝球：[{lucky_blue:02d}]",
                    fg='#f39c12'
                )

                for i in range(4):
                    self.win_lbl.config(text=f"🎲 抽奖中{'.' * i}")
                    self.root.update()
                    self.root.after(100)

                self.win_lbl.config(
                    text=f"红球：{' '.join(f'[{x:02d}]' for x in win_red)}  蓝球：[{win_blue:02d}]",
                    fg=BTN_RED
                )

                _, result, color = ssq_check(lucky_red, lucky_blue, win_red, win_blue)
                self.result_lbl.config(text=result, fg=color)

            else:
                _, lucky_front, lucky_back = self.cached_lucky
                self.lucky_lbl.config(
                    text=f"前区：{' '.join(f'[{x:02d}]' for x in lucky_front)}  后区：{' '.join(f'[{x:02d}]' for x in lucky_back)}",
                    fg='#f39c12'
                )

                for i in range(4):
                    self.win_lbl.config(text=f"🎲 抽奖中{'.' * i}")
                    self.root.update()
                    self.root.after(100)

                self.win_lbl.config(
                    text=f"前区：{' '.join(f'[{x:02d}]' for x in win_front)}  后区：{' '.join(f'[{x:02d}]' for x in win_back)}",
                    fg=BTN_RED
                )

                _, result, color = dlt_check(lucky_front, lucky_back, win_front, win_back)
                self.result_lbl.config(text=result, fg=color)

        except Exception as e:
            import traceback
            messagebox.showerror("出错啦", f"错误：{e}\n\n{traceback.format_exc()}")

def main():
    root = tk.Tk()
    LotteryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()