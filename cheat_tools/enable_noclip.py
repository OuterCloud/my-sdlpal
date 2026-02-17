#!/usr/bin/env python3
"""
SDLPAL 穿墙功能启用工具

功能：
  - 自动修改源代码启用穿墙功能
  - 支持两种模式：始终开启 / 按键切换
  - 自动备份和恢复

使用方法：
    cd cheat_tools
    python3 enable_noclip.py

作者：AI Assistant
日期：2026-02-17
"""

import os
import shutil
import subprocess
import sys


class NoClipPatcher:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.script_dir)
        self.scene_file = os.path.join(self.project_root, "scene.c")
        self.backup_file = os.path.join(self.project_root, "scene.c.backup")
        self.unix_dir = os.path.join(self.project_root, "unix")

    def check_files(self):
        """检查必要文件是否存在"""
        if not os.path.exists(self.scene_file):
            print(f"❌ 错误: 找不到 scene.c 文件")
            print(f"   路径: {self.scene_file}")
            return False
        return True

    def is_patched(self):
        """检查是否已经打过补丁"""
        with open(self.scene_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return "// NOCLIP PATCH" in content

    def backup(self):
        """备份原始文件"""
        print("📦 备份原始文件...")
        shutil.copy2(self.scene_file, self.backup_file)
        print(f"   备份保存到: {self.backup_file}")

    def restore(self):
        """恢复原始文件"""
        if os.path.exists(self.backup_file):
            shutil.copy2(self.backup_file, self.scene_file)
            print("✓ 已恢复原始版本")
            return True
        else:
            print("❌ 错误: 找不到备份文件")
            return False

    def patch_always_on(self):
        """应用补丁：始终开启穿墙"""
        print("📝 应用补丁：始终开启穿墙...")

        with open(self.scene_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # 找到 PAL_CheckObstacleWithRange 函数
        new_lines = []
        in_function = False
        patched = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            # 检测函数定义
            if "PAL_CheckObstacleWithRange(" in line:
                in_function = True

            # 在函数开始的大括号后插入代码
            if in_function and line.strip() == "{" and not patched:
                new_lines.append(
                    "   // NOCLIP PATCH: Always return FALSE to disable collision\n"
                )
                new_lines.append("   return FALSE;\n")
                new_lines.append("\n")
                patched = True
                in_function = False

        if not patched:
            print("❌ 错误: 无法找到函数插入点")
            return False

        with open(self.scene_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print("✓ 补丁应用成功")
        return True

    def patch_toggle(self):
        """应用补丁：按键切换穿墙"""
        print("📝 应用补丁：按键切换穿墙...")

        with open(self.scene_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # 第一步：在文件顶部添加全局变量
        new_lines = []
        global_added = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            # 在 MAX_SPRITE_TO_DRAW 定义后添加全局变量
            if "#define MAX_SPRITE_TO_DRAW" in line and not global_added:
                new_lines.append("\n")
                new_lines.append("// NOCLIP PATCH: Global noclip toggle\n")
                new_lines.append("static BOOL g_fNoClip = FALSE;\n")
                new_lines.append("\n")
                global_added = True

        if not global_added:
            print("❌ 错误: 无法添加全局变量")
            return False

        # 第二步：在函数中添加检查
        lines = new_lines
        new_lines = []
        in_function = False
        check_added = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            if "PAL_CheckObstacleWithRange(" in line:
                in_function = True

            if in_function and line.strip() == "{" and not check_added:
                new_lines.append("   // NOCLIP PATCH: Check noclip toggle\n")
                new_lines.append("   if (g_fNoClip) return FALSE;\n")
                new_lines.append("\n")
                check_added = True
                in_function = False

        if not check_added:
            print("❌ 错误: 无法添加检查代码")
            return False

        with open(self.scene_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print("✓ 补丁应用成功")
        return True

    def compile(self):
        """重新编译游戏"""
        print("\n🔨 重新编译游戏...")

        try:
            # Clean
            subprocess.run(
                ["make", "clean"],
                cwd=self.unix_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

            # Build
            result = subprocess.run(
                ["make"], cwd=self.unix_dir, capture_output=True, text=True
            )

            if result.returncode == 0:
                return True
            else:
                print("❌ 编译失败:")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"❌ 编译出错: {e}")
            return False

    def run(self):
        """主流程"""
        print("=========================================")
        print("  SDLPAL 穿墙功能启用工具")
        print("=========================================")
        print()

        # 检查文件
        if not self.check_files():
            return

        # 检查是否已打补丁
        if self.is_patched():
            print("⚠️  检测到已经打过穿墙补丁")
            print()
            choice = input("是否要恢复原始版本？(y/n): ").strip().lower()

            if choice == "y":
                if self.restore():
                    if self.compile():
                        print()
                        print("✓ 编译完成！穿墙功能已禁用。")
                    else:
                        print()
                        print("❌ 编译失败，但文件已恢复")
            return

        # 备份
        self.backup()
        print()

        # 选择模式
        print("请选择穿墙模式：")
        print()
        print("1. 始终开启穿墙（最简单）")
        print("   - 游戏中始终可以穿墙")
        print("   - 无需按键切换")
        print()
        print("2. 按键切换穿墙（需要额外修改）")
        print("   - 按 F12 键切换穿墙模式")
        print("   - 需要手动修改 input.c")
        print()
        print("3. 取消")
        print()

        choice = input("请输入选项 (1-3): ").strip()
        print()

        if choice == "1":
            if not self.patch_always_on():
                self.restore()
                return

            if self.compile():
                print()
                print("=========================================")
                print("  ✓ 穿墙功能已成功启用！")
                print("=========================================")
                print()
                print("使用方法：")
                print("  - 直接启动游戏即可穿墙")
                print("  - 可以穿过所有墙壁和障碍物")
                print()
                print("⚠️  警告：")
                print("  - 穿墙可能导致游戏卡住或跳过剧情")
                print("  - 建议使用前备份存档")
                print("  - 如需恢复，再次运行此脚本")
                print()
                print("启动游戏：")
                print("  cd unix && ./sdlpal")
                print()
            else:
                print()
                print("❌ 编译失败，正在恢复原始文件...")
                self.restore()

        elif choice == "2":
            if not self.patch_toggle():
                self.restore()
                return

            print()
            print("⚠️  注意: 还需要手动添加按键处理代码")
            print("   请参考 cheat_tools/enable_noclip.md")
            print("   在 input.c 中添加 F12 键处理")
            print()

            proceed = input("是否继续编译？(y/n): ").strip().lower()
            if proceed != "y":
                print("已取消")
                self.restore()
                return

            if self.compile():
                print()
                print("=========================================")
                print("  ✓ 部分完成")
                print("=========================================")
                print()
                print("下一步：")
                print("  1. 编辑 input.c 添加 F12 键处理")
                print("  2. 重新编译: cd unix && make")
                print("  3. 启动游戏测试")
                print()
            else:
                print()
                print("❌ 编译失败，正在恢复原始文件...")
                self.restore()

        elif choice == "3":
            print("❌ 已取消")
            os.remove(self.backup_file)
        else:
            print("❌ 无效选项")
            os.remove(self.backup_file)


if __name__ == "__main__":
    patcher = NoClipPatcher()
    patcher.run()
