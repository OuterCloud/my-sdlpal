#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDLPAL 存档修改器 - 最终验证版
基于实际游戏测试的准确偏移地址

测试日期: 2026-02-16
测试平台: macOS
存档版本: WIN95格式
"""

import struct
import sys


class SDLPALCheat:
    """SDLPAL存档修改器 - 实测验证版"""

    # PLAYERROLES结构基址（李逍遥数据起始位置）
    PLAYERROLES_BASE = 0x01FC

    # 李逍遥各属性偏移（相对于PLAYERROLES基址）
    # 每个PLAYERS数组包含6个角色，李逍遥是第0个（偏移+0）
    OFFSETS = {
        # 基础属性
        "level": 72,  # 等级
        "maxhp": 84,  # 体力上限
        "maxmp": 96,  # 真气上限
        "hp": 108,  # 体力
        "mp": 120,  # 真气
        # 战斗属性（注意：游戏显示值 = 基础值 + 装备加成）
        "attack": 204,  # 武术（攻击力）
        "magic": 216,  # 灵力（魔法攻击）
        "defense": 228,  # 防御
        "dexterity": 240,  # 身法
        "flee": 252,  # 吉运（逃跑率）
    }

    def __init__(self, save_file):
        self.save_file = save_file
        self.data = None
        self.backup_file = save_file + ".backup"

    def load(self):
        """加载存档文件"""
        try:
            with open(self.save_file, "rb") as f:
                self.data = bytearray(f.read())
            print(f"✓ 已加载存档: {self.save_file} ({len(self.data)} 字节)")
            return True
        except FileNotFoundError:
            print(f"✗ 找不到存档文件: {self.save_file}")
            return False
        except Exception as e:
            print(f"✗ 加载失败: {e}")
            return False

    def save(self):
        """保存存档文件"""
        try:
            with open(self.save_file, "wb") as f:
                f.write(self.data)
            print(f"✓ 已保存到: {self.save_file}")
            return True
        except Exception as e:
            print(f"✗ 保存失败: {e}")
            return False

    def backup(self):
        """备份存档"""
        try:
            with open(self.save_file, "rb") as f:
                backup_data = f.read()
            with open(self.backup_file, "wb") as f:
                f.write(backup_data)
            print(f"✓ 已备份到: {self.backup_file}")
            return True
        except Exception as e:
            print(f"✗ 备份失败: {e}")
            return False

    def read_word(self, offset):
        """读取一个WORD（2字节）"""
        return struct.unpack_from("<H", self.data, offset)[0]

    def write_word(self, offset, value):
        """写入一个WORD（2字节）"""
        struct.pack_into("<H", self.data, offset, value)

    def get_stats(self):
        """获取李逍遥当前属性"""
        base = self.PLAYERROLES_BASE
        return {
            "level": self.read_word(base + self.OFFSETS["level"]),
            "maxhp": self.read_word(base + self.OFFSETS["maxhp"]),
            "hp": self.read_word(base + self.OFFSETS["hp"]),
            "maxmp": self.read_word(base + self.OFFSETS["maxmp"]),
            "mp": self.read_word(base + self.OFFSETS["mp"]),
            "attack": self.read_word(base + self.OFFSETS["attack"]),
            "magic": self.read_word(base + self.OFFSETS["magic"]),
            "defense": self.read_word(base + self.OFFSETS["defense"]),
            "dexterity": self.read_word(base + self.OFFSETS["dexterity"]),
            "flee": self.read_word(base + self.OFFSETS["flee"]),
        }

    def set_stats(self, **kwargs):
        """设置李逍遥属性

        参数:
            level: 等级
            maxhp: 体力上限
            hp: 体力
            maxmp: 真气上限
            mp: 真气
            attack: 武术
            magic: 灵力
            defense: 防御
            dexterity: 身法
            flee: 吉运
        """
        base = self.PLAYERROLES_BASE

        for key, value in kwargs.items():
            if key in self.OFFSETS and value is not None:
                self.write_word(base + self.OFFSETS[key], value)

    def display_stats(self):
        """显示当前属性"""
        stats = self.get_stats()
        print("\n" + "=" * 60)
        print("🗡️  李逍遥当前属性（存档基础值）")
        print("=" * 60)
        print(f"等级: {stats['level']}")
        print(f"体力: {stats['hp']:4d} / {stats['maxhp']:4d}")
        print(f"真气: {stats['mp']:4d} / {stats['maxmp']:4d}")
        print(f"武术: {stats['attack']:4d}  (游戏显示可能+装备加成)")
        print(f"灵力: {stats['magic']:4d}")
        print(f"防御: {stats['defense']:4d}  (游戏显示可能+装备加成)")
        print(f"身法: {stats['dexterity']:4d}  (游戏显示可能+装备加成)")
        print(f"吉运: {stats['flee']:4d}")
        print("=" * 60)
        print("\n💡 提示: 游戏中显示的属性 = 基础值 + 装备加成")

    def max_out_all(self):
        """一键拉满所有属性"""
        print("\n正在修改李逍遥属性...")
        self.set_stats(
            maxhp=9999,
            hp=9999,
            maxmp=9999,
            mp=9999,
            attack=999,
            magic=999,
            defense=999,
            dexterity=999,
            flee=999,
        )
        print("✓ 所有属性已拉满！")

    def custom_modify(self):
        """自定义修改"""
        print("\n当前属性:")
        self.display_stats()
        print("\n请输入新的属性值（直接回车跳过）:")

        try:
            inputs = {}

            level_input = input("等级     [回车跳过]: ").strip()
            inputs["level"] = int(level_input) if level_input else None

            maxhp_input = input("体力上限 [回车跳过]: ").strip()
            inputs["maxhp"] = int(maxhp_input) if maxhp_input else None

            hp_input = input("体力     [回车跳过]: ").strip()
            inputs["hp"] = int(hp_input) if hp_input else None

            maxmp_input = input("真气上限 [回车跳过]: ").strip()
            inputs["maxmp"] = int(maxmp_input) if maxmp_input else None

            mp_input = input("真气     [回车跳过]: ").strip()
            inputs["mp"] = int(mp_input) if mp_input else None

            attack_input = input("武术     [回车跳过]: ").strip()
            inputs["attack"] = int(attack_input) if attack_input else None

            magic_input = input("灵力     [回车跳过]: ").strip()
            inputs["magic"] = int(magic_input) if magic_input else None

            defense_input = input("防御     [回车跳过]: ").strip()
            inputs["defense"] = int(defense_input) if defense_input else None

            dexterity_input = input("身法     [回车跳过]: ").strip()
            inputs["dexterity"] = int(dexterity_input) if dexterity_input else None

            flee_input = input("吉运     [回车跳过]: ").strip()
            inputs["flee"] = int(flee_input) if flee_input else None

            self.set_stats(**inputs)
            print("\n✓ 修改完成！")

        except ValueError:
            print("\n✗ 输入无效，请输入数字")
        except KeyboardInterrupt:
            print("\n\n已取消")


def main():
    print("=" * 60)
    print("    SDLPAL 存档修改器 - 实测验证版")
    print("=" * 60)
    print("    基于实际游戏测试的准确偏移地址")
    print("    测试日期: 2026-02-16")
    print("=" * 60)
    print()

    # 检查命令行参数
    if len(sys.argv) > 1:
        save_file = sys.argv[1]
    else:
        save_file = input("请输入存档文件路径 [默认: ../unix/1.rpg]: ").strip()
        if not save_file:
            save_file = "../unix/1.rpg"

    # 创建修改器实例
    cheat = SDLPALCheat(save_file)

    # 加载存档
    if not cheat.load():
        return

    # 显示当前属性
    cheat.display_stats()

    # 主菜单
    while True:
        print("\n" + "=" * 60)
        print("请选择操作:")
        print("=" * 60)
        print("1. 一键拉满（所有属性）")
        print("2. 自定义修改")
        print("3. 查看当前属性")
        print("4. 备份存档")
        print("5. 保存并退出")
        print("0. 退出（不保存）")
        print("=" * 60)

        choice = input("\n请输入选项 [1-5, 0]: ").strip()

        if choice == "1":
            cheat.max_out_all()
            cheat.display_stats()
        elif choice == "2":
            cheat.custom_modify()
            cheat.display_stats()
        elif choice == "3":
            cheat.display_stats()
        elif choice == "4":
            cheat.backup()
        elif choice == "5":
            if cheat.save():
                print("\n✓ 修改已保存！请进入游戏读取存档查看效果。")
                print("\n💡 提示: 游戏中显示的属性可能包含装备加成")
                print("   例如: 武术999 → 显示1001 (装备+2)")
            break
        elif choice == "0":
            print("\n已退出，未保存修改。")
            break
        else:
            print("\n✗ 无效选项，请重新选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback

        traceback.print_exc()
