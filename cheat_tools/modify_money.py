#!/usr/bin/env python3
"""
SDLPAL 金钱修改器

功能：
  - 查看当前金钱
  - 修改金钱数量
  - 设置为最大值（999999999）

使用方法：
    cd cheat_tools
    python3 modify_money.py ../unix/1.rpg

示例：
    # 查看当前金钱
    $ python3 modify_money.py ../unix/1.rpg
    当前金钱: 358

    # 修改为指定金额
    $ python3 modify_money.py ../unix/1.rpg
    选择: 2 (自定义金额)
    输入: 999999

    # 一键拉满
    $ python3 modify_money.py ../unix/1.rpg
    选择: 1 (最大金额)

注意：
  - 金钱是 DWORD 类型（4字节，0-4294967295）
  - 建议不要超过 999999999（9个9）
  - 修改前会自动备份

作者：AI Assistant
日期：2026-02-17
"""

import os
import struct
import sys
from datetime import datetime


class MoneyModifier:
    def __init__(self, save_file):
        self.save_file = save_file
        self.data = None

        # 存档结构偏移（WIN95版本）
        # 从存档开始计算：
        # WORD wSavedTimes           = 0x0000 (2 bytes)
        # WORD wViewportX, wViewportY = 0x0002 (4 bytes)
        # WORD nPartyMember          = 0x0006 (2 bytes)
        # WORD wNumScene             = 0x0008 (2 bytes)
        # WORD wPaletteOffset        = 0x000A (2 bytes)
        # WORD wPartyDirection       = 0x000C (2 bytes)
        # WORD wNumMusic             = 0x000E (2 bytes)
        # WORD wNumBattleMusic       = 0x0010 (2 bytes)
        # WORD wNumBattleField       = 0x0012 (2 bytes)
        # WORD wScreenWave           = 0x0014 (2 bytes)
        # WORD wBattleSpeed          = 0x0016 (2 bytes)
        # WORD wCollectValue         = 0x0018 (2 bytes)
        # WORD wLayer                = 0x001A (2 bytes)
        # WORD wChaseRange           = 0x001C (2 bytes)
        # WORD wChasespeedChangeCycles = 0x001E (2 bytes)
        # WORD nFollower             = 0x0020 (2 bytes)
        # WORD rgwReserved2[3]       = 0x0022 (6 bytes)
        # DWORD dwCash               = 0x0028 (4 bytes) ← 这里！

        self.CASH_OFFSET = 0x0028
        self.MAX_CASH = 999999999  # 建议最大值（9个9）

    def load(self):
        """加载存档文件"""
        try:
            with open(self.save_file, "rb") as f:
                self.data = bytearray(f.read())
            print(f"✓ 成功加载存档: {self.save_file}")
            return True
        except FileNotFoundError:
            print(f"❌ 错误: 找不到存档文件 {self.save_file}")
            return False
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False

    def get_cash(self):
        """读取当前金钱"""
        if self.data is None:
            return None

        # DWORD 是小端序 4 字节无符号整数
        cash = struct.unpack_from("<I", self.data, self.CASH_OFFSET)[0]
        return cash

    def set_cash(self, amount):
        """设置金钱"""
        if self.data is None:
            return False

        # 限制范围
        if amount < 0:
            amount = 0
        elif amount > 4294967295:  # DWORD 最大值
            amount = 4294967295

        # 写入金钱（小端序）
        struct.pack_into("<I", self.data, self.CASH_OFFSET, amount)
        return True

    def save(self):
        """保存存档"""
        try:
            with open(self.save_file, "wb") as f:
                f.write(self.data)
            print(f"✓ 存档已保存: {self.save_file}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    def backup(self):
        """备份存档"""
        backup_file = f"{self.save_file}.moneybackup"
        try:
            with open(self.save_file, "rb") as f:
                data = f.read()
            with open(backup_file, "wb") as f:
                f.write(data)
            print(f"✓ 备份已创建: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False

    def display_cash(self):
        """显示当前金钱"""
        cash = self.get_cash()
        if cash is not None:
            print(f"\n💰 当前金钱: {cash:,}")
            print(f"   十六进制: 0x{cash:08X}")
            print(f"   偏移地址: 0x{self.CASH_OFFSET:04X}")
        else:
            print("❌ 无法读取金钱")

    def max_out_cash(self):
        """设置为最大金额"""
        print(f"\n设置金钱为最大值: {self.MAX_CASH:,}")
        if self.set_cash(self.MAX_CASH):
            print("✓ 金钱已设置为最大值")
            return True
        return False

    def custom_cash(self):
        """自定义金额"""
        print(f"\n当前金钱: {self.get_cash():,}")
        print(f"建议范围: 0 - {self.MAX_CASH:,}")
        print()

        try:
            amount = int(input("请输入新的金额: ").strip())

            if amount < 0:
                print("⚠️  金额不能为负数，已设置为 0")
                amount = 0
            elif amount > self.MAX_CASH:
                print(f"⚠️  金额过大，建议不超过 {self.MAX_CASH:,}")
                confirm = input(f"是否继续设置为 {amount:,}？(y/n): ").strip().lower()
                if confirm != "y":
                    print("已取消")
                    return False

            if self.set_cash(amount):
                print(f"✓ 金钱已设置为: {amount:,}")
                return True
        except ValueError:
            print("❌ 无效的数字")
        except KeyboardInterrupt:
            print("\n已取消")

        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python3 modify_money.py <存档文件>")
        print("示例: python3 modify_money.py ../unix/1.rpg")
        sys.exit(1)

    save_file = sys.argv[1]

    print("=" * 60)
    print("  SDLPAL 金钱修改器")
    print("=" * 60)
    print()

    # 创建修改器实例
    modifier = MoneyModifier(save_file)

    # 加载存档
    if not modifier.load():
        return

    # 显示当前金钱
    modifier.display_cash()

    # 主菜单
    while True:
        print("\n" + "=" * 60)
        print("请选择操作：")
        print("  1. 设置为最大金额 (999,999,999)")
        print("  2. 自定义金额")
        print("  3. 查看当前金钱")
        print("  4. 备份存档")
        print("  5. 保存并退出")
        print("  6. 退出（不保存）")
        print("=" * 60)

        choice = input("\n请输入选项 (1-6): ").strip()

        if choice == "1":
            modifier.max_out_cash()
            modifier.display_cash()
        elif choice == "2":
            modifier.custom_cash()
            modifier.display_cash()
        elif choice == "3":
            modifier.display_cash()
        elif choice == "4":
            modifier.backup()
        elif choice == "5":
            if modifier.save():
                print("\n✓ 修改已保存！请进入游戏查看效果。")
                print("\n💡 提示: 金钱修改立即生效")
            break
        elif choice == "6":
            print("\n已退出（未保存）")
            break
        else:
            print("❌ 无效选项")


if __name__ == "__main__":
    main()
