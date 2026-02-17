#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDLPAL 安全魔法添加器
基于实际游戏数据的魔法ID

使用方法：
    cd cheat_tools
    python3 add_magic_safe.py ../unix/1.rpg

使用步骤：
    1. 运行脚本
    2. 查看已知魔法ID列表
    3. 输入要添加的魔法ID
    4. 自动备份并添加
    5. 进入游戏验证

推荐流程：
    第一步：查看其他角色的魔法
    $ python3 view_magic.py ../unix/1.rpg

    第二步：选择要添加的魔法ID
    比如看到赵灵儿有ID=312的魔法

    第三步：添加到李逍遥
    $ python3 add_magic_safe.py ../unix/1.rpg
    请输入要添加的魔法ID: 312

    第四步：进入游戏验证

已知魔法ID：
    295-309   : 基础魔法
    312-332   : 赵灵儿的魔法
    336-337   : 阿奴/林月如的魔法
    352-353   : 刘晋元/盖罗娇的魔法
    374,389,394: 特殊魔法

注意事项：
    - 只能使用游戏中真实存在的魔法ID
    - 错误的ID会导致显示错误或崩溃
    - 每个角色最多32个魔法槽位
    - 自动备份到 .magic_backup 文件
    - 如需恢复：cp unix/1.rpg.magic_backup unix/1.rpg

关于酒神：
    酒神是李逍遥的专属技能，需要在游戏中学会后才能知道ID
    学会后用 view_magic.py 查看李逍遥的魔法列表即可找到
"""

import struct
import sys

# 从其他角色学到的真实魔法ID
KNOWN_MAGICS = {
    295: "阿奴的魔法1",
    296: "气疗术 (李逍遥)",
    297: "赵灵儿的魔法2",
    298: "林月如/盖罗娇的魔法",
    299: "阿奴/刘晋元的魔法",
    302: "阿奴/刘晋元/盖罗娇的魔法",
    303: "赵灵儿的魔法",
    304: "阿奴/刘晋元/盖罗娇的魔法",
    305: "刘晋元的魔法",
    306: "赵灵儿的魔法",
    307: "赵灵儿的魔法",
    308: "阿奴/刘晋元/盖罗娇的魔法",
    309: "赵灵儿的魔法",
    312: "赵灵儿的魔法1",
    315: "阿奴的魔法",
    316: "赵灵儿的魔法",
    318: "刘晋元的魔法",
    320: "阿奴的魔法",
    321: "赵灵儿的魔法",
    323: "盖罗娇的魔法",
    325: "阿奴的魔法",
    327: "赵灵儿的魔法",
    329: "刘晋元/盖罗娇的魔法",
    332: "赵灵儿的魔法",
    336: "阿奴的魔法",
    337: "林月如的魔法",
    352: "刘晋元的魔法",
    353: "刘晋元/盖罗娇的魔法",
    374: "盖罗娇的魔法",
    389: "阿奴的魔法",
    394: "刘晋元的魔法",
}


def add_magic_to_lixiaoyao(save_file, magic_id):
    """给李逍遥添加一个魔法"""

    try:
        with open(save_file, "rb") as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"✗ 无法读取存档: {e}")
        return False

    base = 0x01FC
    magic_offset = 384
    lixiaoyao_magic_start = base + magic_offset

    # 找到第一个空槽位
    for slot in range(32):
        offset = lixiaoyao_magic_start + slot * 6 * 2 + 0 * 2
        if offset < len(data) - 1:
            current_id = struct.unpack_from("<H", data, offset)[0]
            if current_id == 0:
                # 找到空槽位，添加魔法
                struct.pack_into("<H", data, offset, magic_id)

                # 保存
                with open(save_file, "wb") as f:
                    f.write(data)

                magic_name = KNOWN_MAGICS.get(magic_id, "未知魔法")
                print(f"✓ 已添加魔法ID {magic_id} ({magic_name}) 到槽位 {slot}")
                return True

    print("✗ 魔法槽位已满")
    return False


def main():
    print("=" * 70)
    print("SDLPAL 安全魔法添加器")
    print("=" * 70)
    print()

    if len(sys.argv) > 1:
        save_file = sys.argv[1]
    else:
        save_file = "../unix/1.rpg"

    print("已知的魔法ID（从其他角色学到的）:")
    print()
    for magic_id, name in sorted(KNOWN_MAGICS.items()):
        print(f"  {magic_id:3d} - {name}")

    print()
    print("=" * 70)
    print("💡 建议:")
    print("  1. 先在游戏中学会一个新魔法")
    print("  2. 用 view_magic.py 查看它的ID")
    print("  3. 然后用这个工具添加相同类型的魔法")
    print()
    print("  例如：如果赵灵儿有治疗术，可以把它的ID添加给李逍遥")
    print("=" * 70)
    print()

    magic_id_input = input("请输入要添加的魔法ID (直接回车取消): ").strip()

    if not magic_id_input:
        print("已取消")
        return

    try:
        magic_id = int(magic_id_input)

        # 备份
        import shutil

        backup_file = save_file + ".magic_backup"
        shutil.copy(save_file, backup_file)
        print(f"✓ 已备份到: {backup_file}")
        print()

        add_magic_to_lixiaoyao(save_file, magic_id)

        print()
        print("请进入游戏查看效果。")
        print(f"如果不对，可以恢复: cp {backup_file} {save_file}")

    except ValueError:
        print("✗ 无效的魔法ID")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
