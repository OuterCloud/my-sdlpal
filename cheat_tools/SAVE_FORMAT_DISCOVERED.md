# 🎮 SDLPAL 存档格式实测发现

> 通过实际游戏测试验证的存档结构 - 2026 年 2 月 16 日

## ⚠️ 重要说明

本文档记录的是通过**实际游戏测试**验证的存档文件偏移地址。这些地址是通过以下方法发现的：

1. 在游戏中查看角色当前属性值
2. 在存档文件中搜索这些值
3. 修改存档并在游戏中验证效果
4. 反复测试确认准确性

---

## 📊 PLAYERROLES 结构基址

**基址**: `0x01FC`

这是李逍遥（第 0 个角色）数据在存档文件中的起始位置。

---

## 🗡️ 李逍遥属性偏移表

### 基础属性

| 属性名称             | 偏移地址 | 相对偏移 | 测试值 | 游戏显示 | 状态    |
| -------------------- | -------- | -------- | ------ | -------- | ------- |
| **体力上限** (MaxHP) | 0x0250   | +84      | 999    | 999      | ✅ 验证 |
| **体力** (HP)        | 0x0268   | +108     | 999    | 999      | ✅ 验证 |
| **真气上限** (MaxMP) | 0x025C   | +96      | 999    | 999      | ✅ 验证 |
| **真气** (MP)        | 0x0274   | +120     | 999    | 999      | ✅ 验证 |

### 战斗属性

| 属性名称                  | 偏移地址 | 相对偏移 | 测试值 | 游戏显示 | 装备加成 | 状态      |
| ------------------------- | -------- | -------- | ------ | -------- | -------- | --------- |
| **武术** (AttackStrength) | 0x02C8   | +204     | 999    | 1001     | +2       | ✅ 验证   |
| **灵力** (MagicStrength)  | 0x02D4   | +216     | 999    | 999      | +0       | ✅ 验证   |
| **防御** (Defense)        | 0x02E0   | +228     | 999    | 1008     | +9       | ✅ 验证   |
| **身法** (Dexterity)      | 0x02EC   | +240     | 999    | 1002     | +3       | ✅ 验证   |
| **吉运** (FleeRate)       | 0x02F8   | +252     | 999    | ?        | ?        | 🔄 待验证 |

### 其他字段

| 字段名称             | 偏移地址 | 相对偏移 | 说明                |
| -------------------- | -------- | -------- | ------------------- |
| rgwAvatar            | 0x01FC   | +0       | 头像 ID             |
| rgwSpriteNumInBattle | 0x0208   | +12      | 战斗精灵            |
| rgwSpriteNum         | 0x0214   | +24      | 场景精灵            |
| rgwName              | 0x0220   | +36      | 名字 ID             |
| rgwLevel             | 0x0244   | +72      | 等级                |
| rgwEquipment         | 0x0258   | +132     | 装备数据（72 字节） |

---

## 📝 测试记录

### 测试 1: 体力和真气

- **日期**: 2026-02-16
- **测试内容**: 修改体力和真气为 999
- **结果**: ✅ 成功
- **发现**:
  - 最初在 0x024E 找到 MaxHP，但那不是正确位置
  - 通过搜索 HP=150 找到正确的基址 0x01FC
  - 真气在 0x025C（相对基址+96）

### 测试 2: 战斗属性

- **日期**: 2026-02-16
- **测试内容**: 修改武术、灵力、防御、身法为 999
- **结果**: ✅ 成功
- **发现**:
  - 游戏显示值 = 基础值 + 装备加成
  - 武术+2, 防御+9, 身法+3 来自装备
  - 灵力没有装备加成

### 测试 3: 吉运

- **日期**: 2026-02-16
- **测试内容**: 修改吉运为 999
- **结果**: 🔄 待验证
- **发现**: 吉运在 0x02F8（相对基址+252）

---

## 🔍 发现过程

### 方法 1: 直接搜索已知值

1. 在游戏中查看李逍遥 HP=150
2. 在存档文件中搜索值 150
3. 找到多个匹配位置
4. 通过修改验证正确位置

### 方法 2: 基于结构反推

1. 根据源代码中的 PLAYERROLES 结构定义
2. 计算各字段的理论偏移
3. 从已知的 HP 位置反推基址
4. 验证其他字段是否匹配

### 方法 3: 装备加成分析

- 游戏显示值 = 存档基础值 + 装备加成
- 通过对比差值可以验证修改是否生效
- 例如: 武术 999 → 显示 1001，说明装备+2

---

## 💡 使用建议

### 推荐修改值

- **体力/真气**: 999-9999（不要太大）
- **战斗属性**: 500-999（保持游戏平衡）
- **等级**: 不建议修改（可能影响剧情）

### 注意事项

1. **务必备份存档**：修改前先备份
2. **数值合理**：不要设置过大的值
3. **装备加成**：最终显示值会包含装备加成
4. **存档版本**：本文档基于 WIN95 版本测试

---

## 🛠️ 快速修改脚本

```python
import struct

def modify_lixiaoyao(save_file, hp=None, mp=None, attack=None, magic=None, defense=None, dexterity=None, flee=None):
    """修改李逍遥属性"""
    with open(save_file, 'rb') as f:
        data = bytearray(f.read())

    base = 0x01FC

    if hp is not None:
        struct.pack_into('<H', data, base + 108, hp)      # HP
        struct.pack_into('<H', data, base + 84, hp)       # MaxHP
    if mp is not None:
        struct.pack_into('<H', data, base + 120, mp)      # MP
        struct.pack_into('<H', data, base + 96, mp)       # MaxMP
    if attack is not None:
        struct.pack_into('<H', data, base + 204, attack)  # 武术
    if magic is not None:
        struct.pack_into('<H', data, base + 216, magic)   # 灵力
    if defense is not None:
        struct.pack_into('<H', data, base + 228, defense) # 防御
    if dexterity is not None:
        struct.pack_into('<H', data, base + 240, dexterity) # 身法
    if flee is not None:
        struct.pack_into('<H', data, base + 252, flee)    # 吉运

    with open(save_file, 'wb') as f:
        f.write(data)

# 使用示例
modify_lixiaoyao('../unix/1.rpg', hp=999, mp=999, attack=500, magic=500, defense=300, dexterity=300, flee=100)
```

---

## 📚 PLAYERROLES 完整结构

基于源代码 `global.h` 中的定义：

```c
typedef struct tagPLAYERROLES
{
   PLAYERS            rgwAvatar;             // +0   (6*2=12 bytes)
   PLAYERS            rgwSpriteNumInBattle;  // +12  (6*2=12 bytes)
   PLAYERS            rgwSpriteNum;          // +24  (6*2=12 bytes)
   PLAYERS            rgwName;               // +36  (6*2=12 bytes)
   PLAYERS            rgwAttackAll;          // +48  (6*2=12 bytes)
   PLAYERS            rgwUnknown1;           // +60  (6*2=12 bytes)
   PLAYERS            rgwLevel;              // +72  (6*2=12 bytes)
   PLAYERS            rgwMaxHP;              // +84  (6*2=12 bytes) ✅
   PLAYERS            rgwMaxMP;              // +96  (6*2=12 bytes) ✅
   PLAYERS            rgwHP;                 // +108 (6*2=12 bytes) ✅
   PLAYERS            rgwMP;                 // +120 (6*2=12 bytes) ✅
   WORD               rgwEquipment[6][6];    // +132 (72 bytes)
   PLAYERS            rgwAttackStrength;     // +204 (6*2=12 bytes) ✅
   PLAYERS            rgwMagicStrength;      // +216 (6*2=12 bytes) ✅
   PLAYERS            rgwDefense;            // +228 (6*2=12 bytes) ✅
   PLAYERS            rgwDexterity;          // +240 (6*2=12 bytes) ✅
   PLAYERS            rgwFleeRate;           // +252 (6*2=12 bytes) ✅
   PLAYERS            rgwPoisonResistance;   // +264 (6*2=12 bytes)
   WORD               rgwElementalResistance[5][6]; // +276 (60 bytes)
   // ... 更多字段
} PLAYERROLES;
```

其中 `PLAYERS` 定义为 `WORD[6]`，即 6 个角色的数组。

---

## 🎯 其他角色

理论上，其他角色的数据也在 PLAYERROLES 结构中：

- **李逍遥**: 第 0 个 (偏移+0)
- **赵灵儿**: 第 1 个 (偏移+2)
- **林月如**: 第 2 个 (偏移+4)
- **阿奴**: 第 3 个 (偏移+6)
- **刘晋元**: 第 4 个 (偏移+8)
- **盖罗娇**: 第 5 个 (偏移+10)

例如，赵灵儿的 HP 偏移应该是: `0x01FC + 108 + 2 = 0x026A`

---

## ⚠️ 免责声明

1. 本文档仅供学习和研究使用
2. 修改存档可能影响游戏体验
3. 请在修改前备份存档
4. 不同版本的游戏存档格式可能不同
5. 使用修改器的风险由用户自行承担

---

## 🤝 贡献

如果你发现了新的偏移地址或有任何改进建议，欢迎补充！

---

**最后更新**: 2026-02-16  
**测试版本**: SDLPAL (WIN95 格式存档)  
**测试平台**: macOS
