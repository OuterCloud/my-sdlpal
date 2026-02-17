# 穿墙功能实现记录

## 实现日期

2026-02-17

## 需求

用户询问："我可以穿墙吗"

## 分析

### 碰撞检测机制

通过分析源代码，发现游戏的碰撞检测主要在 `scene.c` 文件中实现：

1. **核心函数**: `PAL_CheckObstacleWithRange()`

   - 位置: `scene.c` 第 522 行
   - 功能: 检查指定位置是否有障碍物
   - 返回值: TRUE=有障碍, FALSE=无障碍

2. **调用位置**:
   - `PAL_UpdateParty()` - 玩家移动时检查
   - `script.c` - NPC 移动时检查
   - `play.c` - 其他场景检查

### 实现方案

#### 方案对比

| 方案           | 难度   | 优点             | 缺点                               |
| -------------- | ------ | ---------------- | ---------------------------------- |
| 修改源代码     | 简单   | 永久有效，可编译 | 需要重新编译                       |
| 运行时内存补丁 | 困难   | 不需要重新编译   | 需要调试器，macOS 限制多           |
| 存档修改       | 不可行 | -                | 碰撞检测在运行时，无法通过存档修改 |

#### 选择方案

修改源代码（最简单可靠）

## 实现细节

### 方法一：始终开启穿墙（最简单）

修改 `scene.c` 中的 `PAL_CheckObstacleWithRange()` 函数：

```c
BOOL
PAL_CheckObstacleWithRange(
    PAL_POS         pos,
    BOOL            fCheckEventObjects,
    WORD            wSelfObject,
    BOOL            fCheckRange
)
{
   // 直接返回FALSE，禁用所有碰撞检测
   return FALSE;

   // 原有代码不会执行...
}
```

### 方法二：按键切换穿墙（更灵活）

1. 添加全局变量：

```c
static BOOL g_fNoClip = FALSE;
```

2. 修改检测函数：

```c
BOOL PAL_CheckObstacleWithRange(...)
{
   if (g_fNoClip) return FALSE;
   // 原有代码...
}
```

3. 添加按键处理（需要修改 `input.c`）：

```c
if (event.key.keysym.sym == SDLK_F12)
{
   g_fNoClip = !g_fNoClip;
}
```

### 方法三：配置文件控制（最灵活）

1. 在 `palcfg.h` 中添加配置项
2. 在 `CONFIGURATION` 结构中添加字段
3. 在碰撞检测中读取配置
4. 通过配置文件控制

## 创建的工具

### 1. enable_noclip.py

Python 自动化脚本，功能：

- 自动备份原始代码
- 自动应用补丁
- 自动编译游戏
- 支持一键恢复

### 2. patch_noclip.sh

Bash 版本脚本（备用）

### 3. 文档

- `enable_noclip.md` - 详细技术文档
- `穿墙使用指南.txt` - 快速使用指南
- `NOCLIP_IMPLEMENTATION.md` - 本文档

## 使用方法

### 快速启用

```bash
cd cheat_tools
python3 enable_noclip.py
# 选择模式 1（始终开启）
# 等待编译完成
cd ../unix
./sdlpal
```

### 恢复正常

```bash
cd cheat_tools
python3 enable_noclip.py
# 选择恢复原始版本 (y)
```

## 技术要点

### 1. 碰撞检测流程

```
用户按方向键
  ↓
PAL_UpdateParty()
  ↓
计算目标位置
  ↓
PAL_CheckObstacleWithRange()
  ↓
检查地图障碍 + 事件对象
  ↓
返回 TRUE/FALSE
  ↓
决定是否移动
```

### 2. 修改点

只需要修改 `PAL_CheckObstacleWithRange()` 的返回值，让它始终返回 FALSE（无障碍）。

### 3. 编译命令

```bash
cd unix
make clean
make
```

## 注意事项

### ⚠️ 警告

1. **游戏逻辑问题**：

   - 可能跳过必要的剧情触发点
   - 可能进入未完成的地图区域
   - 可能卡在无法返回的位置

2. **使用建议**：

   - 使用前备份存档
   - 只在探索时使用
   - 不要在重要剧情时使用
   - 如果卡住，读取之前的存档

3. **技术限制**：
   - 需要重新编译游戏
   - 需要完整的开发环境
   - 修改后的版本仅供个人使用

## 测试

### 测试环境

- 系统: macOS
- 编译器: gcc/clang
- SDL 版本: SDL2

### 测试步骤

1. 运行 `enable_noclip.py`
2. 选择模式 1
3. 等待编译完成
4. 启动游戏
5. 尝试走向墙壁
6. 验证是否能穿过

### 预期结果

- ✅ 能够穿过墙壁
- ✅ 能够穿过障碍物
- ✅ 能够穿过 NPC
- ✅ 不影响其他游戏功能

## 未来改进

### 可能的增强

1. **更智能的穿墙**：

   - 只穿墙壁，不穿 NPC
   - 自动避免卡住的位置

2. **更好的控制**：

   - 游戏内菜单切换
   - 热键快速切换
   - 配置文件持久化

3. **安全机制**：
   - 检测危险位置
   - 自动保存位置
   - 一键返回安全点

## 相关文件

### 源代码

- `scene.c` - 碰撞检测主文件
- `scene.c.backup` - 自动备份（运行脚本后生成）
- `input.c` - 按键处理（方法二需要）
- `palcfg.h` - 配置定义（方法三需要）

### 工具脚本

- `cheat_tools/enable_noclip.py` - Python 自动化脚本
- `cheat_tools/patch_noclip.sh` - Bash 脚本（备用）

### 文档

- `cheat_tools/enable_noclip.md` - 详细技术文档
- `cheat_tools/穿墙使用指南.txt` - 快速指南
- `cheat_tools/README.md` - 主文档（已更新）
- `cheat_tools/使用指南.txt` - 使用指南（已更新）

## 总结

穿墙功能通过修改游戏源代码中的碰撞检测函数实现，是一个简单但有效的方案。提供了自动化工具和详细文档，用户可以轻松启用和恢复。

主要优点：

- ✅ 实现简单
- ✅ 效果可靠
- ✅ 易于恢复
- ✅ 完全自动化

主要限制：

- ⚠️ 需要重新编译
- ⚠️ 可能影响游戏体验
- ⚠️ 需要谨慎使用

---

**实现者**: AI Assistant  
**日期**: 2026-02-17  
**状态**: ✅ 完成
