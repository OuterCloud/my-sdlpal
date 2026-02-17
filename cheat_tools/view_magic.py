#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDLPAL 魔法查看器 - 只读模式
用于查看角色的魔法，不会修改任何数据

使用方法：
    cd cheat_tools
    python3 view_magic.py ../unix/1.rpg

功能：
    - 查看所有6个角色学会的魔法
    - 显示魔法ID和槽位号
    - 只读模式，完全安全
    - 不会修改存档文件

输出示例：
    🔮 李逍遥
    ----------------------------------------------------------------------
      槽位  5: 魔法ID = 296 (0x0128)

    🔮 赵灵儿
    ----------------------------------------------------------------------
      槽位  0: 魔法ID = 312 (0x0138)
      槽位  1: 魔法ID = 316 (0x013C)
      ...

用途：
    1. 查看角色当前学会的魔法
    2. 找到魔法的真实ID
    3. 为添加魔法做准备

注意：
    - 李逍遥的气疗术ID是296
    - 魔法ID范围通常在295-400之间
    - 不同角色可能有相同的魔法
"""

import struct
import sys


def view_magics(save_file):
    """查看所有角色的魔法"""

    try:
        with open(save_file, "rb") as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"✗ 无法读取存档: {e}")
        return

    base = 0x01FC
    magic_offset = 384

    roles = [
        (0, "李逍遥"),
        (1, "赵灵儿"),
        (2, "林月如"),
        (3, "阿奴"),
        (4, "刘晋元"),
        (5, "盖罗娇"),
    ]

    print("=" * 70)
    print("SDLPAL 魔法查看器 - 只读模式")
    print("=" * 70)
    print()

    for role_index, role_name in roles:
        magic_start = base + magic_offset

        magics = []
        for slot in range(32):
            offset = magic_start + slot * 6 * 2 + role_index * 2
            if offset < len(data) - 1:
                magic_id = struct.unpack_from("<H", data, offset)[0]
                if magic_id > 0:
                    magics.append((slot, magic_id))

        if magics:
            print(f"🔮 {role_name}")
            print("-" * 70)
            for slot, magic_id in magics:
                print(f"  槽位 {slot:2d}: 魔法ID = {magic_id:3d} (0x{magic_id:04X})")
            print()

    print("=" * 70)
    print("💡 提示:")
    print("  - 这是只读模式，不会修改存档")
    print("  - 要添加魔法，请先在游戏中学会，然后记录ID")
    print("  - 气疗术的ID是296")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        save_file = sys.argv[1]
    else:
        save_file = "../unix/1.rpg"

    view_magics(save_file)
