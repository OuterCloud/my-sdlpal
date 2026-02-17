#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDLPAL 角色属性修改器
支持修改任意角色的属性

使用方法：
    cd cheat_tools
    python3 modify_role.py ../unix/1.rpg

功能特点：
    1. 支持所有6个角色（李逍遥、赵灵儿、林月如、阿奴、刘晋元、盖罗娇）
    2. 三种修改方式：
       - 全部翻倍（所有属性 × 2）
       - 全部设为指定值（比如全部999）
       - 自定义修改（逐个输入新值）
    3. 自动备份存档（.rolebackup后缀）
    4. 显示修改前后对比
    5. 需要确认才保存

使用示例：

    示例1：给林月如全部翻倍
    $ python3 modify_role.py ../unix/1.rpg
    请选择要修改的角色: 2  (林月如)
    修改方式: 1  (全部翻倍)
    确认修改？y

    示例2：给李逍遥全部设为999
    $ python3 modify_role.py ../unix/1.rpg
    请选择要修改的角色: 0  (李逍遥)
    修改方式: 2  (全部设为指定值)
    请输入目标值: 999
    确认修改？y

    示例3：自定义修改赵灵儿
    $ python3 modify_role.py ../unix/1.rpg
    请选择要修改的角色: 1  (赵灵儿)
    修改方式: 3  (自定义修改)
    修行 [3]: 50  (输入新值)
    体力上限 [220]: 500
    体力 [220]: 500
    ... (其他属性直接回车跳过)
    确认修改？y

注意事项：
    - 游戏中显示的属性 = 基础值 + 装备加成
    - 修改前会自动备份到 .rolebackup 文件
    - 如需恢复：cp unix/1.rpg.rolebackup unix/1.rpg
    - 数值建议不要超过9999

技术信息：
    - PLAYERROLES基址: 0x01FC
    - 角色索引: 0=李逍遥, 1=赵灵儿, 2=林月如, 3=阿奴, 4=刘晋元, 5=盖罗娇
    - 每个属性占2字节(WORD)
"""

import struct
import sys

# 角色列表
ROLES = {
    0: "李逍遥",
    1: "赵灵儿",
    2: "林月如",
    3: "阿奴",
    4: "刘晋元",
    5: "盖罗娇",
}

# 属性偏移
OFFSETS = {
    "level": 72,  # 等级（修行）
    "maxhp": 84,  # 体力上限
    "maxmp": 96,  # 真气上限
    "hp": 108,  # 体力
    "mp": 120,  # 真气
    "attack": 204,  # 武术
    "magic": 216,  # 灵力
    "defense": 228,  # 防御
    "dexterity": 240,  # 身法
    "flee": 252,  # 吉运
}

# 属性中文名
ATTR_NAMES = {
    "level": "修行",
    "maxhp": "体力上限",
    "hp": "体力",
    "maxmp": "真气上限",
    "mp": "真气",
    "attack": "武术",
    "magic": "灵力",
    "defense": "防御",
    "dexterity": "身法",
    "flee": "吉运",
}


def read_role_attrs(data, role_index):
    """读取角色属性"""
    base = 0x01FC
    attrs = {}

    for name, offset in OFFSETS.items():
        pos = base + offset + role_index * 2
        value = struct.unpack_from("<H", data, pos)[0]
        attrs[name] = value

    return attrs


def write_role_attrs(data, role_index, attrs):
    """写入角色属性"""
    base = 0x01FC

    for name, value in attrs.items():
        if name in OFFSETS:
            pos = base + OFFSETS[name] + role_index * 2
            struct.pack_into("<H", data, pos, value)


def display_attrs(attrs, title="属性"):
    """显示属性"""
    print(f"\n{'=' * 70}")
    print(title)
    print("=" * 70)
    for name in [
        "level",
        "maxhp",
        "hp",
        "maxmp",
        "mp",
        "attack",
        "magic",
        "defense",
        "dexterity",
        "flee",
    ]:
        if name in attrs:
            print(f"{ATTR_NAMES[name]:8s}: {attrs[name]:4d}")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 modify_role.py <存档文件>")
        print("示例: python3 modify_role.py ../unix/1.rpg")
        return

    save_file = sys.argv[1]

    # 读取存档
    try:
        with open(save_file, "rb") as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"✗ 无法读取存档: {e}")
        return

    # 备份
    backup_file = save_file + ".rolebackup"
    with open(backup_file, "wb") as f:
        f.write(data)
    print(f"✓ 已备份到 {backup_file}")

    # 选择角色
    print("\n" + "=" * 70)
    print("请选择要修改的角色:")
    print("=" * 70)
    for idx, name in ROLES.items():
        print(f"{idx}. {name}")
    print("=" * 70)

    try:
        role_index = int(input("\n请输入角色编号 [0-5]: ").strip())
        if role_index not in ROLES:
            print("✗ 无效的角色编号")
            return
    except ValueError:
        print("✗ 无效的输入")
        return

    role_name = ROLES[role_index]

    # 读取当前属性
    current = read_role_attrs(data, role_index)
    display_attrs(current, f"{role_name} 当前属性")

    # 选择修改方式
    print("\n" + "=" * 70)
    print("修改方式:")
    print("=" * 70)
    print("1. 全部翻倍")
    print("2. 全部设为指定值")
    print("3. 自定义修改")
    print("=" * 70)

    try:
        choice = input("\n请选择 [1-3]: ").strip()
    except KeyboardInterrupt:
        print("\n\n已取消")
        return

    new_attrs = current.copy()

    if choice == "1":
        # 全部翻倍
        for key in new_attrs:
            new_attrs[key] = current[key] * 2
        print("\n✓ 所有属性翻倍")

    elif choice == "2":
        # 全部设为指定值
        try:
            value = int(input("\n请输入目标值: ").strip())
            for key in new_attrs:
                new_attrs[key] = value
            print(f"\n✓ 所有属性设为 {value}")
        except ValueError:
            print("✗ 无效的数值")
            return

    elif choice == "3":
        # 自定义修改
        print("\n请输入新的属性值（直接回车跳过）:")
        for name in [
            "level",
            "maxhp",
            "hp",
            "maxmp",
            "mp",
            "attack",
            "magic",
            "defense",
            "dexterity",
            "flee",
        ]:
            try:
                value_input = input(
                    f"{ATTR_NAMES[name]:8s} [{current[name]:4d}]: "
                ).strip()
                if value_input:
                    new_attrs[name] = int(value_input)
            except ValueError:
                print("  ✗ 无效的数值，保持原值")
            except KeyboardInterrupt:
                print("\n\n已取消")
                return
    else:
        print("✗ 无效的选择")
        return

    # 显示修改对比
    print("\n" + "=" * 70)
    print("修改对比")
    print("=" * 70)
    for name in [
        "level",
        "maxhp",
        "hp",
        "maxmp",
        "mp",
        "attack",
        "magic",
        "defense",
        "dexterity",
        "flee",
    ]:
        old = current[name]
        new = new_attrs[name]
        if old != new:
            print(f"{ATTR_NAMES[name]:8s}: {old:4d} → {new:4d}")

    # 确认
    confirm = input("\n确认修改？(y/n): ").strip().lower()
    if confirm != "y":
        print("已取消")
        return

    # 写入
    write_role_attrs(data, role_index, new_attrs)

    # 保存
    with open(save_file, "wb") as f:
        f.write(data)

    print("\n" + "=" * 70)
    print("✅ 修改完成！")
    print("=" * 70)
    print("\n💡 提示：")
    print("  - 游戏中显示的属性可能包含装备加成")
    print(f"  - 如需恢复：cp {backup_file} {save_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback

        traceback.print_exc()
