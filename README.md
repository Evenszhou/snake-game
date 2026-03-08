# 🐍 贪吃蛇 - Snake Game

一个使用 Python 和 Pygame 开发的经典贪吃蛇游戏，具有美化的界面、音效和多种游戏功能。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 游戏特性

- ✨ **美化界面**: 渐变色蛇身、动态眼睛、食物动画效果
- 🎵 **音效系统**: 吃食物和游戏结束音效
- 🏆 **计分系统**: 实时分数显示、最高分保存
- 🎯 **等级系统**: 随分数提升，等级和速度增加
- ⭐ **奖励食物**: 10%概率生成奖励食物（20分）
- 🎨 **多种状态**: 主菜单、游戏、暂停、游戏结束画面
- 📊 **HUD显示**: 分数、最高分、等级、速度实时显示

## 🎯 游戏操作

### 基本操作
- **移动**: `方向键` 或 `W/A/S/D`
- **暂停**: `P` 或 `ESC`
- **退出**: `Q`

### 菜单操作
- **主菜单**: `SPACE` 或 `ENTER` 开始游戏
- **游戏结束**: `R` 重新开始, `M` 返回主菜单

## 📦 安装说明

### 方式一：下载可执行文件（推荐）

前往 [Releases](https://github.com/Evenszhou/snake-game/releases) 页面下载对应平台版本：

- **Windows**: `snake-game-windows.zip` → 解压后运行 `snake_game.exe`
- **macOS**: `snake-game-macos.tar.gz` → 解压后运行 `snake_game`
- **Linux**: `snake-game-linux.tar.gz` → 解压后运行 `snake_game`

> 💡 **提示**: 如Releases页面暂无文件，请按照下方"如何发布"章节操作触发自动构建

### 方式二：从源码运行

#### 前置要求
- Python 3.8 或更高版本
- pip 包管理器

#### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/Evenszhou/snake-game.git
cd snake-game
```

2. **创建虚拟环境（可选）**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行游戏**
```bash
python snake_game.py
```

## 🔧 如何打包

如果你想自己打包成 EXE 文件：

### 安装 PyInstaller
```bash
pip install pyinstaller
```

### 打包命令
```bash
# 打包成单个 EXE 文件
pyinstaller --onefile --windowed --name "snake_game" snake_game.py

# 或者使用配置文件
pyinstaller snake_game.spec
```

打包后的 EXE 文件在 `dist/` 目录中。

### 打包参数说明
- `--onefile`: 打包成单个可执行文件
- `--windowed`: 不显示命令行窗口（GUI 程序）
- `--name`: 指定输出文件名
- `--icon`: 可选，指定图标文件（如 `--icon=icon.ico`）

## 🎨 技术栈

- **Python 3.8+**: 主要编程语言
- **Pygame 2.5.0+**: 游戏开发框架
- **PyInstaller**: 打包工具

## 📁 项目结构

```
snake-game/
├── snake_game.py          # 主游戏文件
├── requirements.txt       # 依赖列表
├── README.md             # 项目文档
├── .gitignore            # Git 忽略文件
├── LICENSE               # MIT 许可证
├── highscore.txt         # 最高分记录（运行时生成）
└── .github/
    └── workflows/
        └── build.yml     # GitHub Actions 自动构建配置
```

## 🎯 游戏截图

游戏包含以下界面：

1. **主菜单**: 显示游戏标题和最高分
2. **游戏界面**: 网格背景、美化的蛇和食物
3. **暂停界面**: 半透明遮罩显示暂停状态
4. **游戏结束**: 显示最终得分和新纪录提示

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 开发计划

- [ ] 添加墙壁模式（带边界的地图）
- [ ] 添加障碍物
- [ ] 添加多种难度级别
- [ ] 添加更多音效和背景音乐
- [ ] 添加设置菜单（音量、速度等）
- [ ] 添加排行榜功能
- [ ] 支持多语言

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 [Pygame](https://www.pygame.org/) 提供的游戏开发框架
- 灵感来源于经典的贪吃蛇游戏

## 📧 联系方式

项目地址: [https://github.com/Evenszhou/snake-game](https://github.com/Evenszhou/snake-game)

## 🚀 如何发布新版本

本项目使用 GitHub Actions 自动构建多平台可执行文件。

### 发布流程

1. **更新代码并提交**
```bash
git add .
git commit -m "描述你的更改"
git push
```

2. **创建版本标签**
```bash
git tag v1.0.0  # 使用语义化版本号
git push origin v1.0.0
```

3. **等待自动构建**
   - GitHub Actions 会自动构建 Windows/macOS/Linux 三个版本
   - 构建完成后会在 Releases 页面生成发布包
   - 通常需要 5-10 分钟

4. **下载使用**
   - 前往 [Releases](https://github.com/Evenszhou/snake-game/releases) 页面
   - 下载对应平台的可执行文件

---

**祝你游戏愉快！🎉**
