# Rimworld

## 基地需要的设施

Power
dining room, kitchen and freezer
recreation room
bedrooms
hospital
workshop
laboratory
prison
backup

农业：in soil, 24 crops sustain 1 person; in hydroponics, 8 crops/person。经济作物是棉花比蘑菇赚钱

1 boomalope = 2.5 chenmuel generator

## 战斗

### 装备

soldiers should always have armor vests and advanced helmets
Go to the Assign tab then you can change the outfit worn by colonists under 'Current outfit'
Choosing 'Clear forced' in the Apparel tab clears the forced status on apparel allowing colonists to replace them if needed. 

### 武器

按照射击技能从高到低，应该装备狙击步枪, bolt-action rifles > charge rifles > 冲锋步枪 > 轻机枪 > 霰弹枪(非战斗用) > minigun(完全不需射击技能)
chain shotgun不推荐使用
长剑杀伤力最强，锤最适合用来击晕人

### 炮塔

```
O#O
###
O#O
#=墙，O=炮塔
```

# Advanced IK

HS2的Advanced IK模组

```
BodyTop
    p_cf_anim/cf_J_Root/cf_N_height/cf_J_Hips
        cf_J_Kosi01 腰部（以及下半身）角度、位置，尺寸
            cf_J_Kosi01_s 腰上部位置、角度、尺寸。其子类效果不明
            cf_J_Kosi02   腰下部（以及下半身）位置、角度、尺寸
                cf_J_Kosi02_s  不动下半身
                cf_J_LegUp00_L 左腿髋关节位置、角度，以及右腿尺寸
                cf_J_SiriDam_L 左侧臀部的位置、尺寸
            cf_J_LegUpDam_L 大腿和腰连接部分外侧
        cf_J_Spine01 背部（以及上半身）角度、位置，尺寸
            cf_J_Spine01_s 背下部位置、角度、尺寸。其子类效果不明
            cf_J_Spine02   背上部（以及上半身）角度、位置，尺寸
                cf_J_Spine02_s 不动上半身
                cf_J_Spine03   位置比02要载高一点，其余相同
                    cf_J_Mune00 胸部整体。子类有点高深
                    cf_J_Neck   脖子（以及头）
                    cf_J_ShoulderIK_L 肩膀以及手臂
                        cf_J_ArmUp00_L 左臂
                            cf_J_ArmElbo_dam_01_L 肘关节
                            cf_J_ArmLow01_R 小臂
                            ArmUp01~03_dam 大臂的不同部位
                        cf_J_Shoulder02_s_R 肩关节
```

"隐藏"肢体：从远端到进端的重要节点分别是

- 小臂：ArmLow01
- 肘关节：ArmElbo_dam_01
- 大臂：ArmUp03 ~ 01

假设想要实现大臂中段以下被截断的效果，首先要将ArmLow01、ArmElbo_dam_01、ArmUp03的scale设置为0，然后调节ArmUp02的y_scale，达到想要的剩余长度。最后，调节ArmLow01、ArmElbo_dam_01、ArmUp03的位置到断面处（否则就会凸出来一块尖尖的东西）

如果不想做那么细致，可以调ArmUp00，直接去掉整条手臂
双腿的做法是一样的，只需要把Arm全部换成Leg，ArmElbo换成LegKnee

# Emuera

## 宏（マクロ）

保存与使用方法：shift+F1~F12保存宏，F1~F12使用宏。另外，ctrl+0~9可以切换不同的宏组（マクログループ），因此一共能保存12×10=120个宏。游戏退出后，宏保存在macro.txt

语法：`\e`相当于esc，`\n`相当于回车，`()*n`表重复。使用例：`(0\e)*3`实现重复三次选择0选项

## 调试（デバッグ）

在命令行加上`-Debug`参数启动Emuera，就能在调试窗口看各种信息

调试模式下，可以输入`@command`直接执行，比如`@PRINTV FLAG:200`（不过，作为防作弊机制，执行命令之后玩家名会倍更改为イカサマ）

特殊调试指令：`REBOOT`重启，`OUTPUT`将文本输出到log，`EXIT`退出，`CONFIG`打开设置窗口，`DEBUG`打开调试窗口

[语法](https://ja.osdn.net/projects/emuera/wiki/FrontPage)

# SMT & Persona技能

## 魔法

| 词根      | 中文   | 日文   | 推测出处                                                |
| --------- | ------ | ------ | ------------------------------------------------------- |
| 火        | 亚基   | アギ   | 吠陀教及印度教的火神阿耆尼（Agni）                      |
| 冰        | 布芙   | ブフ   | 梵文“冰块”（稍显牵强，存疑）                            |
| 电        | 吉欧   | ジオ   | 北欧神话中的战神提尔（Tyr）的古德语名（稍显牵强，存疑） |
| 风        | 加尔   | ガル   | 印度神话中的金翅鸟迦楼罗（Garuda）                      |
| 冲击      | 赞     | ザン   |                                                         |
| 光 / 破魔 | 哈玛   | ハマ   | 神道教术语“破魔”                                        |
| 暗 / 咒杀 | 姆多   | ムド   | 日语“無道”                                              |
| 万能      | 米吉多 | メギド | 《启示录》中世界末日善恶决战的战场                      |

| 前后缀   | 中文                 | 日文                     | 推测出处         |
| -------- | -------------------- | ------------------------ | ---------------- |
| 范围效果 | 玛哈-                | マハ-                    | 摩诃，即梵文“大” |
| 中等魔法 | -拉，-拉欧，-加，-翁 | -ラ、-ラオ、-ンガ、-オン | 印度教、佛教“唵“ |
| 强力魔法 | -达因                | -ダイン                  | 力的单位         |

## 辅助&回复

| 词根         | 中文   | 日文     | 推测出处            |
| ------------ | ------ | -------- | ------------------- |
| 攻击力       | 塔尔   | タル     |                     |
| 防御力       | 拉库   | ラク     | 梵文“保护”（raksh） |
| 命中&闪避    | 斯库   | スク     |                     |
| 消除负面效果 | 帕特拉 | パトラ   |                     |
| 回复         | 迪亚   | ディア   | 希腊神话；希腊语    |
| 复活         | 利卡姆 | リカーム | 梵文“转世”          |

| 前后缀   | 中文       | 日文       | 推测出处             |
| -------- | ---------- | ---------- | -------------------- |
| 范围效果 | 玛哈-，梅- | マハ-、メ- | 摩诃，即梵文“大”     |
| 消除     | 迪-        | デ-        |                      |
| 增益     | -卡加      | -カジャ    |                      |
| 减益     | -达        | -ンダ      |                      |
| 中等回复 | -拉玛      | -ラマ      | 印度传说中的英雄罗摩 |
| 完全回复 | -拉翰      | -ラハン    |                      |

系列早期，拉玛也用作攻击魔法的后缀