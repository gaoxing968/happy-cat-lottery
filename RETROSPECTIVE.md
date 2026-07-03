# 开心猫彩票模拟器 · 开发复盘

## 项目概述

| 项目 | 内容 |
|------|------|
| 名称 | 开心猫彩票模拟器 (happy-cat-lottery) |
| 目的 | 娱乐工具，基于星座/心情/日期生成幸运号 |
| 仓库 | https://github.com/gaoxing968/happy-cat-lottery |
| 版本 | v2.0 |

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 桌面版 GUI | Python 3.11 + Tkinter（无需 pip 安装额外依赖）|
| 核心算法 | zodiac_lucky_generator.py（太阳黄经 + 月相 + 星期星体）|
| 网页版 | PWA（HTML/JS，无需构建）|
| 打包 | PyInstaller（--onefile --windowed）|
| 版本管理 | Git + GitHub |

---

## 开发流程

### v2 开发步骤

1. 修改 `lottery_gui_v2.py` 第 173 行，标题"彩票模拟开奖器 2.0" → "开心猫彩票模拟器"
2. 修改第 340 行底部，添加邮箱 `luckycat168968@gmail.com`
3. 创建干净项目目录 `happy-cat-lottery/`
4. 复制 v2 相关文件：
   - `lottery_gui_v2.py`（桌面版主程序）
   - `zodiac_lucky_generator.py`（核心算法）
   - `lottery_pwa/`（网页版目录）
5. 编写 README.md
6. `git init` → `git commit` → `git push`
7. `gh repo create` → GitHub 建仓
8. `pyinstaller --onefile --windowed` 打包 exe
9. `gh release create` 发布 v2.0
10. `gh release upload` 上传 exe 和截图
11. README 顶部嵌入截图
12. 添加 `.github/FUNDING.yml`（待补充 Ko-fi 用户名）

---

## 踩坑记录

### 1. git push 连接失败（443端口）

**症状：** `git push` 一直报 `Failed to connect to github.com port 443`

**原因：** 之前有人配置过 git 全局 rewrite，把所有 GitHub HTTPS 地址强制转成 SSH（`git@github.com:`），但 SSH 密钥未配置。

**解决：**
```bash
git config --global --unset-all url.https://github.com/.insteadof
git config --global --unset-all url.https://gitlab.com/.insteadof
git config --global --unset-all url.https://bitbucket.org/.insteadof
```

**预防：** 新机器先执行 `git config --global -l | grep insteadof`，有输出要先清掉。

### 2. gh release notes 格式问题

**症状：** `--notes` 参数内容包含 Markdown 时解析出错

**解决：** notes 内容用双引号包裹，内部反引号转义，或分开发布后用 `gh release edit` 更新

### 3. cua-driver 无法截取 Tkinter 窗口

**原因：** Tk 窗口不走标准 Accessibility API

**解决：** 用 `PIL.ImageGrab.grab()` 全屏截图，再裁剪

### 4. PyInstaller 打包后窗口闪退

**原因：** `--onefile --windowed` 模式下，console 被隐藏但出错信息看不到

**解决：** 先用 `--console` 模式打包看报错，确认正常后再加 `--windowed`

---

## 经验总结

### 上 GitHub 公开项目标准流程

```
1. 创建干净项目目录
2. 写 README.md（先写，代码后补）
3. git init → commit → push
4. gh repo create --public
5. git push -u origin master
6. pyinstaller 打包 exe
7. gh release create v1.0
8. gh release upload 上传资产
9. gh release edit --notes 更新说明（含截图链接）
10. 添加 FUNDING.yml
```

### 截图发布最佳实践

- 截图文件 commit 进仓库（不用 release assets）
- README 用 `![截图](screenshot.png)` 嵌入（相对路径）
- Release notes 用 raw.githubusercontent.com 链接

### 新机器/新项目 Git 配置检查清单

```bash
# 1. 检查是否有 insteadof 重写
git config --global -l | grep insteadof
# 有输出的话全部 unset

# 2. 检查 gh CLI 登录状态
gh auth status

# 3. 检查 SSH 代理（如果有配置 git SSH）
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

---

## 后续待办

- [ ] 补充 Ko-fi 用户名到 FUNDING.yml
- [ ] 注册爱发电/Buy Me a Coffee（国内/国际打赏平台）
- [ ] 小红书推广引流
- [ ] 掘金/知乎文章（技术原理 + 玩法介绍）
- [ ] 考虑加版本选择功能（让用户可选 v1/v2）

---

## 修改记录

| 日期 | 修改内容 |
|------|---------|
| 2026-07-03 | v2.0 首次发布，标题改名 + 添加邮箱 |
| 2026-07-03 | 上传 GitHub，发布 Release v2.0，打包 exe |
| 2026-07-03 | README 顶部添加 UI 截图，添加 FUNDING.yml |