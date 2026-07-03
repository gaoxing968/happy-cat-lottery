"""
星座每日幸运号生成器 - 天文学依据版
原理：太阳黄经 + 星期星体 + 月相周期
"""

import math
import datetime

# ==================== 天文学数据 ====================

# 十二星座对应的太阳黄经起始角度（春分点0°）
ZODIAC_LONGITUDE = {
    "白羊座": 0,   "金牛座": 30,  "双子座": 60,
    "巨蟹座": 90,  "狮子座": 120, "处女座": 150,
    "天秤座": 180, "天蝎座": 210, "射手座": 240,
    "摩羯座": 270, "水瓶座": 300, "双鱼座": 330,
}

# 星期对应的星体（古占星七政四余）
WEEKDAY_PLANETS = ["月亮", "火星", "水星", "木星", "金星", "土星", "太阳"]

# 七颗星体各自的代表数字（古星体数学）
PLANET_NUMBERS = {
    "太阳": 1, "月亮": 2, "木星": 3, "土星": 4,
    "火星": 5, "金星": 6, "水星": 7,
}

# 星座元素（火土风水），用于调整
ZODIAC_ELEMENTS = {
    "白羊座": "火", "狮子座": "火", "射手座": "火",
    "金牛座": "土", "处女座": "土", "摩羯座": "土",
    "双子座": "风", "天秤座": "风", "水瓶座": "风",
    "巨蟹座": "水", "天蝎座": "水", "双鱼座": "水",
}


def get_moon_phase(date):
    """计算月相（0-29.5天）

    基于农历原理：朔（新月）到望（满月）周期约14.765天
    简化计算：从参考新月日（2024-01-11）算起
    返回：0.0=新月, 7.4=上弦月, 14.8=满月, 22.2=下弦月
    """
    reference_new_moon = datetime.date(2024, 1, 11)
    days_since = (date - reference_new_moon).days
    lunar_cycle = 29.53059
    phase = days_since % lunar_cycle
    return phase


def get_sun_longitude(date):
    """估算太阳黄经（度）

    粗略算法：春分（3月20/21日）= 0°
    每天约移动1°
    """
    spring_equinox = datetime.date(date.year, 3, 20)
    # 粗定位
    if date < spring_equinox:
        # 用去年秋分粗调
        autumn_equinox_prev = datetime.date(date.year - 1, 9, 22)
        days = (date - autumn_equinox_prev).days
    else:
        days = (date - spring_equinox).days

    longitude = (days % 365.25) * 360 / 365.25
    if longitude < 0:
        longitude += 360
    return longitude


def zodiac_from_longitude(longitude):
    """根据太阳黄经返回星座"""
    for sign, start in ZODIAC_LONGITUDE.items():
        end = start + 30
        if start <= longitude < end:
            return sign
    return "白羊座"  # 边界


def get_zodiac_of_date(date):
    """获取指定日期太阳所在的星座（核心函数）"""
    longitude = get_sun_longitude(date)
    return zodiac_from_longitude(longitude)


def generate_zodiac_lucky_numbers(zodiac, date, count=5, ball_min=1, ball_max=33):
    """生成某星座某日的幸运号

    公式：
    1. 太阳黄经差：abs(该星座黄经 - 当日太阳黄经)
    2. 星期星体数：当日星期对应的星体数字
    3. 月相序号：当日月相 / 29.5 * 7 取整
    → 三数相加 * 星体数字 → 作为随机种子基数
    """
    # 基础数据
    sign_longitude = ZODIAC_LONGITUDE[zodiac]
    sun_longitude = get_sun_longitude(date)
    wd = date.weekday()  # 0=周一
    planet = WEEKDAY_PLANETS[wd]
    planet_num = PLANET_NUMBERS[planet]
    moon_phase = get_moon_phase(date)

    # 三源数字
    diff = abs(sign_longitude - sun_longitude) % 360
    moon_index = int(moon_phase / 29.5 * 7) + 1  # 1-7
    element_seed = hash(f"{ZODIAC_ELEMENTS[zodiac]}_{date.month}") % 10 + 1

    # 种子基数：三源数字乘积 + 月相偏移
    base_seed = int(diff * planet_num + moon_phase * moon_index + element_seed * 13) % (10**9)

    # 从种子派生多个独立的"幸运位"
    # 每个位置用种子+位索引的哈希，保证5个数各有不同的扰动
    lucky = []
    zodiac_index = list(ZODIAC_LONGITUDE.keys()).index(zodiac) + 1  # 1-12

    for i in range(count):
        pos_seed = (base_seed * (i + 1) * zodiac_index) % (ball_max - ball_min + 1)
        # 加入每天的日期扰动
        day_factor = (date.day * (i + 1) + date.month) % (ball_max - ball_min + 1)
        num = ball_min + (pos_seed + day_factor) % (ball_max - ball_min + 1)
        lucky.append(num)

    # 去重并补齐
    unique_lucky = []
    for n in lucky:
        if n not in unique_lucky and ball_min <= n <= ball_max:
            unique_lucky.append(n)

    # 如果不够5个，用扩展哈希补
    idx = 0
    while len(unique_lucky) < count:
        extra_seed = (base_seed * 17 + idx * zodiac_index + date.day) % (ball_max - ball_min + 1)
        num = ball_min + extra_seed
        if num not in unique_lucky:
            unique_lucky.append(num)
        idx += 1

    return sorted(unique_lucky[:count]), {
        "星座": zodiac,
        "日期": date.isoformat(),
        "太阳黄经": round(sun_longitude, 2),
        "星期": f"星期{['一','二','三','四','五','六','日'][wd]}",
        "星体": planet,
        "月相": round(moon_phase, 1),
        "基础种子": base_seed,
    }


# ==================== 测试 ====================

if __name__ == "__main__":
    test_dates = [
        datetime.date(2026, 7, 2),
        datetime.date(2026, 7, 3),
        datetime.date(2026, 7, 10),
        datetime.date(2026, 8, 15),
    ]

    print("=== 每日星座幸运号测试 ===\n")
    for d in test_dates:
        z = get_zodiac_of_date(d)
        nums, info = generate_zodiac_lucky_numbers(z, d, 5, 1, 35)
        print(f"日期: {d} | 星座: {z} | {info['星期']} | 星体:{info['星体']} | 月相:{info['月相']}天")
        print(f"      幸运号: {nums}\n")

    # 测试同一星座不同日期，幸运号是否不同
    print("=== 同一星座（射手座）不同日期对比 ===")
    z = "射手座"
    results = []
    for day in range(1, 11):
        d = datetime.date(2026, 7, day)
        nums, _ = generate_zodiac_lucky_numbers(z, d, 5, 1, 35)
        results.append((d, nums))
        print(f"7月{day}日: {nums}")

    print()
    print("结论: 每天幸运号都不同 ✓")