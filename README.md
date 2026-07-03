# 🎰 开心猫彩票模拟器

基于星座、心情、日期、年龄等元素生成"今日幸运号"的娱乐工具。

**⚠️ 纯属娱乐，无任何预测功能**

---

## 📦 版本说明

| 版本 | 说明 |
|------|------|
| **桌面版（lottery_gui_v2.py）** | Tkinter GUI，支持双色球/大乐透，无需网络 |
| **网页版（lottery_pwa/）** | PWA 应用，可在浏览器中直接打开，支持离线使用 |

---

## 🖥️ 桌面版使用

### 环境要求
- Python 3.8+
- 无需安装额外依赖

### 运行方式
```bash
python lottery_gui_v2.py
```

> Windows 用户双击 `lottery_sim_v2.lnk` 快捷方式即可启动（已包含在发行版中）

---

## 🌐 网页版使用

### 方式一：直接打开
在浏览器中打开 `lottery_pwa/index.html` 即可使用。

### 方式二：本地服务器
```bash
cd lottery_pwa
python server.py
# 访问 http://localhost:8080
```

---

## 🎯 功能

- 输入：姓名、生日、心情、年龄、血型
- 输出：双色球（33红球选6 + 16蓝球选1）或大乐透（前区5个 + 后区2个）
- 模拟开奖：对奖并显示结果
- 多端支持：Windows / Mac / Linux / 手机浏览器

---

## 🔬 算法说明

幸运号基于以下天文学元素生成：
- 太阳黄经（星座位置）
- 星期星体周期
- 月相周期
- 用户输入的心情、年龄、血型作为随机种子

详细原理见 `zodiac_lucky_generator.py`。

---

## 📁 项目结构

```
happy-cat-lottery/
├── lottery_gui_v2.py          # 桌面版主程序
├── zodiac_lucky_generator.py   # 核心算法模块
├── lottery_pwa/               # 网页版
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   └── server.py
└── README.md
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系

Made by luckycat · luckycat168968@gmail.com