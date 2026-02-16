#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDLPAL 魔法查看器 - 只读模式
用于查看角色的魔法，不会修改任何数据
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
