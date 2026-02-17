#!/bin/bash
# 穿墙功能补丁脚本
# 自动修改源代码并重新编译以启用穿墙功能

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCENE_FILE="$PROJECT_ROOT/scene.c"
BACKUP_FILE="$PROJECT_ROOT/scene.c.backup"

echo "========================================="
echo "  SDLPAL 穿墙功能补丁工具"
echo "========================================="
echo ""

# 检查 scene.c 是否存在
if [ ! -f "$SCENE_FILE" ]; then
    echo "❌ 错误: 找不到 scene.c 文件"
    echo "   路径: $SCENE_FILE"
    exit 1
fi

# 检查是否已经打过补丁
if grep -q "// NOCLIP PATCH" "$SCENE_FILE"; then
    echo "⚠️  检测到已经打过穿墙补丁"
    echo ""
    read -p "是否要恢复原始版本？(y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        if [ -f "$BACKUP_FILE" ]; then
            cp "$BACKUP_FILE" "$SCENE_FILE"
            echo "✓ 已恢复原始版本"
            echo ""
            echo "重新编译中..."
            cd "$PROJECT_ROOT/unix"
            make clean > /dev/null 2>&1
            make
            echo ""
            echo "✓ 编译完成！穿墙功能已禁用。"
        else
            echo "❌ 错误: 找不到备份文件"
        fi
    fi
    exit 0
fi

# 备份原始文件
echo "📦 备份原始文件..."
cp "$SCENE_FILE" "$BACKUP_FILE"
echo "   备份保存到: $BACKUP_FILE"
echo ""

# 显示选项
echo "请选择穿墙模式："
echo ""
echo "1. 始终开启穿墙（最简单）"
echo "   - 游戏中始终可以穿墙"
echo "   - 无需按键切换"
echo ""
echo "2. 按键切换穿墙（推荐）"
echo "   - 按 F12 键切换穿墙模式"
echo "   - 可以随时开启/关闭"
echo ""
echo "3. 取消"
echo ""
read -p "请输入选项 (1-3): " mode

case $mode in
    1)
        echo ""
        echo "📝 应用补丁：始终开启穿墙..."
        
        # 在 PAL_CheckObstacleWithRange 函数开头添加 return FALSE
        sed -i.tmp '/^PAL_CheckObstacleWithRange(/,/^{/ {
            /^{/a\
   // NOCLIP PATCH: Always return FALSE to disable collision\
   return FALSE;
        }' "$SCENE_FILE"
        
        rm -f "$SCENE_FILE.tmp"
        echo "✓ 补丁应用成功"
        ;;
        
    2)
        echo ""
        echo "📝 应用补丁：按键切换穿墙..."
        
        # 在文件顶部添加全局变量
        sed -i.tmp '/#define MAX_SPRITE_TO_DRAW/a\
\
// NOCLIP PATCH: Global noclip toggle\
static BOOL g_fNoClip = FALSE;\
' "$SCENE_FILE"
        
        # 在 PAL_CheckObstacleWithRange 函数开头添加检查
        sed -i.tmp2 '/^PAL_CheckObstacleWithRange(/,/^{/ {
            /^{/a\
   // NOCLIP PATCH: Check noclip toggle\
   if (g_fNoClip) return FALSE;
        }' "$SCENE_FILE"
        
        rm -f "$SCENE_FILE.tmp" "$SCENE_FILE.tmp2"
        echo "✓ 补丁应用成功"
        echo ""
        echo "⚠️  注意: 还需要手动添加按键处理代码"
        echo "   请参考 cheat_tools/enable_noclip.md 中的说明"
        echo "   在 input.c 中添加 F12 键处理"
        ;;
        
    3)
        echo ""
        echo "❌ 已取消"
        rm -f "$BACKUP_FILE"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ 无效选项"
        rm -f "$BACKUP_FILE"
        exit 1
        ;;
esac

echo ""
echo "🔨 重新编译游戏..."
cd "$PROJECT_ROOT/unix"

if make clean > /dev/null 2>&1 && make; then
    echo ""
    echo "========================================="
    echo "  ✓ 穿墙功能已成功启用！"
    echo "========================================="
    echo ""
    if [ "$mode" = "1" ]; then
        echo "使用方法："
        echo "  - 直接启动游戏即可穿墙"
        echo "  - 可以穿过所有墙壁和障碍物"
    else
        echo "使用方法："
        echo "  - 启动游戏后按 F12 切换穿墙模式"
        echo "  - （需要先完成 input.c 的修改）"
    fi
    echo ""
    echo "⚠️  警告："
    echo "  - 穿墙可能导致游戏卡住或跳过剧情"
    echo "  - 建议使用前备份存档"
    echo "  - 如需恢复，再次运行此脚本"
    echo ""
    echo "恢复方法："
    echo "  bash cheat_tools/patch_noclip.sh"
    echo ""
else
    echo ""
    echo "❌ 编译失败"
    echo "   正在恢复原始文件..."
    cp "$BACKUP_FILE" "$SCENE_FILE"
    echo "   已恢复原始版本"
    exit 1
fi
