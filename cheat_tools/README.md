# 🎮 SDLPAL 修改器工具

> 仙剑奇侠传存档修改工具 - 完全非侵入式，只修改存档文件

---

## 🚀 快速开始

### 1. 修改属性（体力、真气、武术等）

```bash
cd cheat_tools
python3 sdlpal_cheat_final.py ../unix/1.rpg
```

选择 `1` 一键拉满所有属性，或选择 `2` 自定义修改。

### 2. 查看魔法

```bash
python3 view_magic.py ../unix/1.rpg
```

查看所有角色学会的魔法及其 ID。

### 3. 添加魔法

```bash
python3 add_magic_safe.py ../unix/1.rpg
```

输入已知的魔法 ID 来添加（必须是游戏中真实存在的 ID）。

### 4. 修改金钱

```bash
python3 modify_money.py ../unix/1.rpg
```

查看和修改金钱数量，支持一键拉满。

### 5. 修改角色属性

```bash
# 修改赵灵儿（角色1）等级为99
python3 modify_role.py ../unix/1.rpg 1 99

# 修改李逍遥（角色0）
python3 modify_role.py ../unix/1.rpg 0 99
```

### 6. 启用穿墙功能

```bash
python3 enable_noclip.py
```

自动修改源代码并重新编译，启用穿墙功能。

---

## 📁 可用工具

### 核心工具

- **`sdlpal_cheat_final.py`** - 综合属性修改器
- **`modify_money.py`** - 金钱修改器
- **`modify_role.py`** - 角色等级和属性修改器
- **`view_magic.py`** - 魔法查看器
- **`add_magic_safe.py`** - 魔法添加器
- **`enable_noclip.py`** - 穿墙功能启用器

### 文档

- **`SAVE_FORMAT_DISCOVERED.md`** - 存档格式详解
- **`魔法技能说明.md`** - 魔法系统说明
- **`穿墙使用指南.txt`** - 穿墙功能详细指南
- **`NOCLIP_IMPLEMENTATION.md`** - 穿墙技术实现文档

---

## ✅ 已验证的功能

### 属性修改

| 属性          | 偏移地址      | 状态 |
| ------------- | ------------- | ---- |
| 体力/体力上限 | 0x0268/0x0250 | ✅   |
| 真气/真气上限 | 0x0274/0x025C | ✅   |
| 武术          | 0x02C8        | ✅   |
| 灵力          | 0x02D4        | ✅   |
| 防御          | 0x02E0        | ✅   |
| 身法          | 0x02EC        | ✅   |
| 吉运          | 0x02F8        | ✅   |
| 金钱          | 0x0028        | ✅   |
| 等级          | 0x01FC        | ✅   |

**注意**: 游戏显示值 = 基础值 + 装备加成

---

## 💡 重要提示

### ⚠️ 使用前必读

1. **务必先完全退出游戏再修改存档**

   - 游戏运行时会覆盖存档文件
   - 修改后需要重新启动游戏才能看到效果

2. **务必备份存档**

   ```bash
   cp unix/1.rpg unix/1.rpg.backup
   ```

3. **穿墙功能警告**

   - ⚠️ 不要在主线剧情中使用穿墙
   - 会跳过重要剧情触发点
   - 可能导致剧情无法继续
   - 建议只在探索或刷怪时使用

4. **等级和属性警告**

   - 过高的等级可能导致某些剧情无法触发
   - 建议等级不超过 60
   - 属性建议不超过 999

5. **魔法 ID 必须正确**
   - 不要随意使用未知 ID
   - 先用 `view_magic.py` 查看真实 ID
   - 错误的 ID 会导致显示错误或崩溃

### 恢复存档

```bash
cp unix/1.rpg.backup unix/1.rpg
```

---

## 📊 已知魔法 ID

从游戏存档中发现的真实魔法 ID：

| ID            | 说明                |
| ------------- | ------------------- |
| 295-309       | 基础魔法            |
| 312-332       | 赵灵儿的魔法        |
| 336-337       | 阿奴/林月如的魔法   |
| 352-353       | 刘晋元/盖罗娇的魔法 |
| 374, 389, 394 | 特殊魔法            |

**李逍遥当前魔法**：

- 槽位 5: ID=296 (气疗术)

详细列表请查看 `魔法技能说明.md`

---

## 🔧 技术信息

- **PLAYERROLES 基址**: 0x01FC
- **队伍数据偏移**: 0x002C
- **金钱偏移**: 0x0028
- **存档格式**: WIN95 版本
- **测试平台**: macOS

详细技术信息请查看 `SAVE_FORMAT_DISCOVERED.md`

---

## ⚠️ 已知问题

1. 穿墙功能会跳过剧情触发点，可能导致剧情无法继续
2. 过高的等级可能导致某些剧情无法触发
3. 队伍数据损坏会导致游戏崩溃，建议定期备份存档
4. 修改存档前必须完全退出游戏

---

## 🎉 快速命令

```bash
# 备份存档
cp unix/1.rpg unix/1.rpg.backup

# 修改属性
cd cheat_tools && python3 sdlpal_cheat_final.py ../unix/1.rpg

# 修改金钱
python3 modify_money.py ../unix/1.rpg --max

# 修改角色等级
python3 modify_role.py ../unix/1.rpg 0 60

# 查看魔法
python3 view_magic.py ../unix/1.rpg

# 启用穿墙（修改源代码）
python3 enable_noclip.py

# 恢复存档
cp unix/1.rpg.backup unix/1.rpg
```

---

**祝你游戏愉快！** 🎊
