# 穿墙功能实现指南

## 方法一：修改源代码（推荐）

### 步骤

1. **修改碰撞检测函数**

编辑 `scene.c` 文件，找到 `PAL_CheckObstacleWithRange` 函数（约第 522 行），在函数开头添加一个全局开关：

```c
// 在 scene.c 文件顶部添加全局变量
static BOOL g_fNoClip = FALSE;  // 穿墙开关

BOOL
PAL_CheckObstacleWithRange(
    PAL_POS         pos,
    BOOL            fCheckEventObjects,
    WORD            wSelfObject,
    BOOL            fCheckRange
)
{
   // 添加这一行：如果穿墙模式开启，直接返回FALSE（无障碍）
   if (g_fNoClip) {
      return FALSE;
   }

   // 原有代码继续...
   int x, y, h, xr, yr;
   // ...
}
```

2. **添加快捷键切换**

编辑 `input.c` 文件，添加快捷键来切换穿墙模式。找到键盘处理函数，添加：

```c
// 在 input.c 中添加
extern BOOL g_fNoClip;  // 声明外部变量

// 在键盘事件处理中添加（例如按 F12 切换）
if (event.key.keysym.sym == SDLK_F12)
{
   g_fNoClip = !g_fNoClip;
   // 可选：显示提示信息
   printf("穿墙模式: %s\n", g_fNoClip ? "开启" : "关闭");
}
```

3. **重新编译游戏**

```bash
cd unix
make clean
make
```

4. **使用方法**

- 进入游戏后，按 `F12` 键切换穿墙模式
- 开启后可以穿过墙壁和障碍物
- 再次按 `F12` 关闭穿墙模式

## 方法二：简化版（始终开启穿墙）

如果你只想简单地启用穿墙，不需要切换开关：

### 修改 scene.c

找到 `PAL_CheckObstacleWithRange` 函数（约第 522 行），在函数开头直接返回：

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

   // 下面的代码不会执行
   // ...
}
```

### 重新编译

```bash
cd unix
make clean
make
```

## 方法三：配置文件控制（最灵活）

### 1. 修改 palcfg.h

在 `PALCFG_ITEM` 枚举中添加新选项：

```c
typedef enum tagPALCFG_ITEM
{
    // ... 现有选项 ...
    PALCFG_ENABLENOCLIP,  // 添加这一行
    // ...
} PALCFG_ITEM;
```

### 2. 在配置结构中添加字段

在 `palcfg.h` 的 `CONFIGURATION` 结构中添加：

```c
typedef struct tagCONFIGURATION
{
    // ... 现有字段 ...
    BOOL fEnableNoClip;  // 添加这一行
    // ...
} CONFIGURATION;
```

### 3. 修改 scene.c 使用配置

```c
BOOL
PAL_CheckObstacleWithRange(
    PAL_POS         pos,
    BOOL            fCheckEventObjects,
    WORD            wSelfObject,
    BOOL            fCheckRange
)
{
   // 检查配置文件中的穿墙选项
   if (gConfig.fEnableNoClip) {
      return FALSE;
   }

   // 原有代码...
}
```

### 4. 创建配置文件

在游戏目录创建 `sdlpal.cfg` 文件，添加：

```ini
EnableNoClip=True
```

## 注意事项

⚠️ **重要警告**：

1. **游戏逻辑问题**：穿墙可能导致：

   - 跳过必要的剧情触发点
   - 进入未完成的地图区域
   - 卡在无法返回的位置
   - 破坏游戏进度

2. **建议**：

   - 使用前先备份存档
   - 只在需要时临时开启
   - 不要在重要剧情时使用
   - 如果卡住，读取之前的存档

3. **兼容性**：
   - 修改源代码后需要重新编译
   - 确保有完整的开发环境
   - 修改后的版本仅供个人使用

## 快速实现（推荐新手）

最简单的方法是使用**方法二**：

1. 打开 `scene.c` 文件
2. 找到第 522 行的 `PAL_CheckObstacleWithRange` 函数
3. 在函数开头添加 `return FALSE;`
4. 保存文件
5. 运行 `cd unix && make clean && make`
6. 启动游戏，现在可以穿墙了

## 恢复正常模式

如果想恢复正常的碰撞检测：

1. 删除添加的 `return FALSE;` 语句
2. 重新编译：`cd unix && make clean && make`

## 测试

编译完成后：

```bash
cd unix
./sdlpal
```

进入游戏，尝试走向墙壁，如果能穿过去，说明穿墙功能已启用。
