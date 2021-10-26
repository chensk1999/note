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

装备
soldiers should always have armor vests and advanced helmets
Go to the Assign tab then you can change the outfit worn by colonists under 'Current outfit'
Choosing 'Clear forced' in the Apparel tab clears the forced status on apparel allowing colonists to replace them if needed. 

武器
按照射击技能从高到低，应该装备狙击步枪, bolt-action rifles > charge rifles > 冲锋步枪 > 轻机枪 > 霰弹枪(非战斗用) > minigun(完全不需射击技能)
chain shotgun不推荐使用
长剑杀伤力最强，锤最适合用来击晕人

炮塔

```
O#O
###
O#O
#=墙，O=炮塔
```

# PSI

Minecraft的PSI模组的咒语

收支平衡的魔力消耗
护腿：25
循环：75

```
// 构筑一个方块拦截弹射物
{spellName:"ProjectileDeviate",uuidMost:9210403355473365057L,validSpell:1b,spellList:[{data:{params:{_number:4},key:"operatorSquareRoot"},x:2,y:2},{data:{params:{_target:1},key:"trickEvaluate"},x:2,y:3},{data:{params:{_target:4},key:"connector"},x:3,y:1},{data:{params:{_vector2:2,_vector1:1},key:"operatorVectorDotProduct"},x:3,y:2},{data:{params:{_target:4},key:"operatorEntityMotion"},x:3,y:3},{data:{key:"errorSuppressor"},x:3,y:4},{data:{params:{_vector3:0,_vector2:2,_vector1:4},key:"operatorVectorSubtract"},x:4,y:1},{data:{params:{_target:2},key:"operatorEntityPosition"},x:4,y:2},{data:{params:{_target:4},key:"operatorRandomEntity"},x:4,y:3},{data:{params:{_target:1},key:"operatorEntityPosition"},x:4,y:4},{data:{params:{_target:2},key:"connector"},x:5,y:1},{data:{params:{_target:4},key:"operatorEntityPosition"},x:5,y:2},{data:{params:{_position:1,_radius:4},key:"selectorNearbyProjectiles"},x:5,y:3},{data:{params:{_time:4,_position:3},key:"trickConjureBlock"},x:5,y:4},{data:{key:"selectorCaster"},x:6,y:2},{data:{key:"constantNumber",constantValue:"8"},x:6,y:3},{data:{key:"constantNumber",constantValue:"5"},x:6,y:4}],uuidLeast:-5494237698469689705L}

// 标准魔法。先施法标记挖掘区域的一个角落（标记目视方块，并且会放出光球提示），然后潜行施法标记对角方向的角落
// 然后切换到挖掘魔法，就能自动向下挖。使用内存#1和#2，#1是第一个角落，#2的x、z坐标绝对值是x、z方向区域长宽（正负号取决于方向）
{spellName:"挖掘范围标记",uuidMost:3669774797398556918L,validSpell:1b,spellList:[{data:{key:"selectorSneakStatus"},x:0,y:6},{data:{params:{_number2:1,_number3:0,_number1:2},key:"operatorSubtract"},x:0,y:7},{data:{key:"constantNumber",constantValue:"2"},x:0,y:8},{data:{key:"constantNumber",constantValue:"1"},x:1,y:2},{data:{params:{_x:1,_y:0,_z:0},key:"operatorVectorConstruct"},x:1,y:3},{data:{key:"constantNumber",constantValue:"1"},x:1,y:5},{data:{params:{_number2:1,_number3:0,_number1:3},key:"operatorSubtract"},x:1,y:6},{data:{params:{_target:3,_constant:2},key:"constantWrapper"},x:1,y:7},{data:{key:"constantNumber",constantValue:"2"},x:1,y:8},{data:{params:{_number:3},key:"selectorSavedVector"},x:2,y:2},{data:{params:{_vector2:3,_vector1:4},key:"operatorVectorProject"},x:2,y:3},{data:{params:{_target:1},key:"operatorVectorNormalize"},x:2,y:4},{data:{params:{_target:2},key:"trickEvaluate"},x:2,y:5},{data:{params:{_target:3},key:"connector"},x:2,y:6},{data:{params:{_number:3,_target:4},key:"trickSaveVector"},x:2,y:7},{data:{key:"selectorSneakStatus"},x:2,y:8},{data:{params:{_vector3:0,_vector2:3,_vector1:4},key:"operatorVectorSubtract"},x:3,y:2},{data:{params:{_target:1},key:"connector"},x:3,y:3},{data:{params:{_vector3:1,_vector2:4,_vector1:3},key:"operatorVectorSum"},x:3,y:4},{data:{params:{_target:1},key:"connector"},x:3,y:5},{data:{params:{_number2:3,_vector1:1},key:"operatorVectorMultiply"},x:3,y:6},{data:{comment:"潜行状态为s，则储存;v[2-s] = s*v[1] - (s-1)*v[2]，其中s=0, 1;v1为目视方块，v2为目视方块与v1之差",params:{_vector3:0,_vector2:1,_vector1:2},key:"operatorVectorSubtract"},x:3,y:7},{data:{comment:"未潜行时施法，将视线指向方块储存为向量1",params:{_number2:3,_vector1:4},key:"operatorVectorMultiply"},x:3,y:8},{data:{params:{_target:4},key:"connector"},x:4,y:2},{data:{params:{_vector2:4,_vector1:3},key:"operatorVectorProject"},x:4,y:3},{data:{params:{_target:1},key:"operatorVectorNormalize"},x:4,y:4},{data:{params:{_target:4},key:"connector"},x:4,y:8},{data:{params:{_target:4},key:"connector"},x:5,y:2},{data:{params:{_x:0,_y:0,_z:2},key:"operatorVectorConstruct"},x:5,y:3},{data:{key:"constantNumber",constantValue:"1"},x:5,y:4},{data:{params:{_target:4},key:"connector"},x:5,y:8},{data:{params:{_target:2},key:"connector"},x:6,y:2},{data:{params:{_target:2},key:"connector"},x:6,y:3},{data:{params:{_target:4},key:"connector"},x:6,y:4},{data:{params:{_target:1},key:"connector"},x:6,y:5},{data:{params:{_target:1},key:"connector"},x:6,y:6},{data:{params:{_target:1},key:"connector"},x:6,y:7},{data:{params:{_target:1},key:"connector"},x:6,y:8},{data:{params:{_ray:4,_max:0,_position:2},key:"operatorVectorRaycast"},x:7,y:4},{data:{params:{_target:4},key:"operatorEntityPosition"},x:7,y:5},{data:{params:{_target:4},key:"operatorEntityPosition"},x:7,y:6},{data:{params:{_ray:4,_max:0,_position:1},key:"operatorVectorRaycastAxis"},x:7,y:7},{data:{params:{_vector3:0,_vector2:3,_vector1:1},key:"operatorVectorSum"},x:7,y:8},{data:{params:{_target:2},key:"operatorEntityLook"},x:8,y:4},{data:{key:"selectorCaster"},x:8,y:5},{data:{params:{_target:1},key:"connector"},x:8,y:6},{data:{params:{_target:1},key:"operatorEntityLook"},x:8,y:7},{data:{params:{_time:0,_position:3},key:"trickConjureLight"},x:8,y:8}],uuidLeast:-7642207706111360756L}

// 循环魔法，从内存#1开始、以#2的x和z坐标作为长宽（可正可负）向下挖掘
{spellName:"挖掘",uuidMost:-1367599413568385145L,validSpell:1b,spellList:[{data:{key:"constantNumber",constantValue:"2"},x:0,y:3},{data:{params:{_target:2},key:"operatorVectorExtractX"},x:1,y:0},{data:{params:{_target:2},key:"connector"},x:1,y:1},{data:{params:{_target:2},key:"connector"},x:1,y:2},{data:{params:{_number:3},key:"selectorSavedVector"},x:1,y:3},{data:{params:{_target:1},key:"connector"},x:1,y:4},{data:{params:{_target:1},key:"connector"},x:1,y:5},{data:{params:{_number2:2,_number3:0,_number1:3},key:"operatorMultiply"},x:2,y:0},{data:{params:{_target:2},key:"connector"},x:2,y:1},{data:{params:{_target:2},key:"connector"},x:2,y:2},{data:{params:{_target:3},key:"operatorVectorExtractZ"},x:2,y:3},{data:{params:{_target:3},key:"operatorVectorExtractX"},x:2,y:5},{data:{params:{_target:1},key:"connector"},x:2,y:6},{data:{params:{_target:3},key:"operatorAbsolute"},x:3,y:0},{data:{key:"constantNumber",constantValue:"1"},x:3,y:1},{data:{params:{_number2:3,_number3:1,_number1:2},key:"operatorSum"},x:3,y:2},{data:{params:{_number2:3,_number1:2},key:"operatorModulus"},x:3,y:3},{data:{params:{_number2:2,_number1:4},key:"operatorIntegerDivide"},x:3,y:4},{data:{params:{_target:3},key:"operatorAbsolute"},x:3,y:5},{data:{params:{_target:3},key:"connector"},x:3,y:6},{data:{params:{_number2:3,_number1:2},key:"operatorIntegerDivide"},x:4,y:0},{data:{key:"selectorLoopcastIndex"},x:4,y:1},{data:{params:{_target:3},key:"connector"},x:4,y:2},{data:{params:{_number2:1,_number3:0,_number1:3},key:"operatorMin"},x:4,y:3},{data:{key:"selectorLoopcastIndex"},x:4,y:4},{data:{params:{_number2:3,_number1:1},key:"operatorModulus"},x:4,y:5},{data:{params:{_number2:1,_number3:2,_number1:3},key:"operatorSum"},x:4,y:6},{data:{key:"constantNumber",constantValue:"1"},x:4,y:7},{data:{params:{_number2:4,_number3:0,_number1:3},key:"operatorMultiply"},x:5,y:0},{data:{params:{_target:1},key:"connector"},x:5,y:1},{data:{params:{_target:1},key:"connector"},x:5,y:2},{data:{params:{_x:2,_y:1,_z:3},key:"operatorVectorConstruct"},x:5,y:3},{data:{params:{_target:2},key:"connector"},x:5,y:4},{data:{params:{_number2:2,_number3:0,_number1:3},key:"operatorMin"},x:5,y:5},{data:{params:{_target:3},key:"connector"},x:5,y:6},{data:{key:"constantNumber",constantValue:"-3"},x:6,y:0},{data:{key:"constantNumber",constantValue:"1"},x:6,y:1},{data:{params:{_number:1},key:"selectorSavedVector"},x:6,y:2},{data:{params:{_vector3:0,_vector2:1,_vector1:3},key:"operatorVectorSum"},x:6,y:3},{data:{params:{_max:4,_target:2,_position:1},key:"trickBreakInSequence"},x:6,y:4},{data:{params:{_x:0,_y:4,_z:0},key:"operatorVectorConstruct"},x:6,y:5},{data:{key:"constantNumber",constantValue:"3"},x:7,y:4},{data:{key:"constantNumber",constantValue:"-3"},x:7,y:5}],uuidLeast:-7019747334406200440L}

// 护腿魔法。潜行时在脚下以及运动方向前一格构筑方块
{spellName:"空中步行",uuidMost:4353741199554135646L,validSpell:1b,spellList:[{data:{params:{_target:2},key:"trickDie"},x:0,y:0},{data:{params:{_number2:2,_number3:0,_number1:4},key:"operatorSubtract"},x:0,y:1},{data:{key:"constantNumber",constantValue:"1"},x:0,y:2},{data:{key:"selectorCaster"},x:0,y:4},{data:{key:"selectorSneakStatus"},x:1,y:1},{data:{params:{_time:2,_position:4},key:"trickConjureBlock"},x:1,y:2},{data:{key:"constantNumber",constantValue:"1200"},x:1,y:3},{data:{params:{_target:3},key:"operatorEntityMotion"},x:1,y:4},{data:{params:{_target:1},key:"operatorVectorExtractY"},x:1,y:5},{data:{key:"constantNumber",constantValue:"2"},x:2,y:0},{data:{params:{_target:4},key:"connector"},x:2,y:1},{data:{params:{_vector3:0,_vector2:2,_vector1:1},key:"operatorVectorSum"},x:2,y:2},{data:{params:{_target:4},key:"connector"},x:2,y:3},{data:{params:{_vector3:0,_vector2:2,_vector1:3},key:"operatorVectorSubtract"},x:2,y:4},{data:{params:{_x:0,_y:3,_z:0},key:"operatorVectorConstruct"},x:2,y:5},{data:{params:{_x:0,_y:3,_z:0},key:"operatorVectorConstruct"},x:3,y:0},{data:{params:{_vector3:0,_vector2:1,_vector1:4},key:"operatorVectorSubtract"},x:3,y:1},{data:{params:{_position:1},key:"selectorBlockPresence"},x:3,y:2},{data:{params:{_number2:4,_vector1:2},key:"operatorVectorMultiply"},x:3,y:3},{data:{params:{_target:3},key:"operatorVectorNormalize"},x:3,y:4},{data:{key:"selectorCaster"},x:4,y:0},{data:{params:{_target:1},key:"operatorEntityPosition"},x:4,y:1},{data:{params:{_number2:4,_number3:0,_number1:3},key:"operatorSubtract"},x:4,y:2},{data:{params:{_number2:4,_number3:0,_number1:1},key:"operatorMax"},x:4,y:3},{data:{key:"constantNumber",constantValue:"1"},x:5,y:2},{data:{key:"constantNumber",constantValue:"0"},x:5,y:3}],uuidLeast:-7317583663487969378L}

{spellName:"实体收容",uuidMost:-8347084623467098407L,validSpell:1b,spellList:[{data:{key:"constantNumber",constantValue:"600"},x:0,y:0},{data:{params:{_time:1,_position:2},key:"trickConjureBlock"},x:0,y:1},{data:{params:{_vector3:0,_vector2:2,_vector1:4},key:"operatorVectorSum"},x:0,y:2},{data:{params:{_x:0,_y:2,_z:0},key:"operatorVectorConstruct"},x:0,y:3},{data:{key:"constantNumber",constantValue:"2"},x:0,y:4},{data:{key:"constantNumber",constantValue:"600"},x:0,y:5},{data:{params:{_target:4},key:"connector"},x:1,y:2},{data:{params:{_vector3:0,_vector2:4,_vector1:1},key:"operatorVectorSum"},x:1,y:3},{data:{params:{_target:1},key:"connector"},x:1,y:4},{data:{params:{_max:4,_time:3,_target:2,_position:1},key:"trickConjureBlockSequence"},x:1,y:5},{data:{params:{_target:4},key:"connector"},x:1,y:6},{data:{params:{_position:4},key:"trickBlaze"},x:2,y:1},{data:{params:{_target:4},key:"connector"},x:2,y:2},{data:{params:{_x:2,_y:0,_z:0},key:"operatorVectorConstruct"},x:2,y:3},{data:{key:"constantNumber",constantValue:"1"},x:2,y:4},{data:{key:"constantNumber",constantValue:"3"},x:2,y:5},{data:{params:{_x:0,_y:1,_z:0},key:"operatorVectorConstruct"},x:2,y:6},{data:{key:"selectorFocalPoint"},x:3,y:0},{data:{params:{_target:4},key:"operatorEntityPosition"},x:3,y:1},{data:{params:{_target:1},key:"connector"},x:3,y:2},{data:{params:{_vector3:0,_vector2:3,_vector1:1},key:"operatorVectorSubtract"},x:3,y:3},{data:{params:{_target:1},key:"connector"},x:3,y:4},{data:{params:{_max:3,_time:4,_target:2,_position:1},key:"trickConjureBlockSequence"},x:3,y:5},{data:{params:{_target:3},key:"connector"},x:3,y:6},{data:{params:{_target:3},key:"operatorEntityPosition"},x:4,y:0},{data:{params:{_target:4,_position:1},key:"operatorClosestToPoint"},x:4,y:1},{data:{params:{_target:3},key:"connector"},x:4,y:2},{data:{key:"constantNumber",constantValue:"600"},x:4,y:5},{data:{params:{_target:3},key:"connector"},x:4,y:6},{data:{params:{_target:3},key:"connector"},x:5,y:0},{data:{params:{_position:1,_radius:4},key:"selectorNearbyLiving"},x:5,y:1},{data:{params:{_target:3},key:"connector"},x:5,y:2},{data:{params:{_vector3:0,_vector2:4,_vector1:1},key:"operatorVectorSum"},x:5,y:3},{data:{params:{_target:1},key:"connector"},x:5,y:4},{data:{params:{_max:4,_time:3,_target:2,_position:1},key:"trickConjureBlockSequence"},x:5,y:5},{data:{params:{_target:3},key:"connector"},x:5,y:6},{data:{key:"constantNumber",constantValue:"8"},x:6,y:1},{data:{params:{_target:3},key:"connector"},x:6,y:2},{data:{params:{_x:0,_y:0,_z:2},key:"operatorVectorConstruct"},x:6,y:3},{data:{key:"constantNumber",constantValue:"1"},x:6,y:4},{data:{key:"constantNumber",constantValue:"3"},x:6,y:5},{data:{params:{_max:1,_time:2,_target:3,_position:4},key:"trickConjureBlockSequence"},x:6,y:6},{data:{key:"constantNumber",constantValue:"600"},x:6,y:7},{data:{key:"errorSuppressor"},x:7,y:0},{data:{params:{_target:3},key:"connector"},x:7,y:2},{data:{params:{_vector3:0,_vector2:3,_vector1:1},key:"operatorVectorSubtract"},x:7,y:3},{data:{params:{_target:1},key:"connector"},x:7,y:4},{data:{params:{_target:1},key:"connector"},x:7,y:5},{data:{params:{_target:1},key:"connector"},x:7,y:6}],uuidLeast:-7686361113585539424L}

{spellName:"barrier",uuidMost:5019302112127173582L,validSpell:1b,spellList:[{data:{params:{_target:4},key:"connector"},x:1,y:1},{data:{params:{_max:4,_time:0,_target:1,_position:2},key:"trickConjureBlockSequence"},x:1,y:2},{data:{params:{_vector3:0,_vector2:2,_vector1:4},key:"operatorVectorSum"},x:1,y:3},{data:{params:{_target:2},key:"connector"},x:1,y:4},{data:{params:{_target:2},key:"connector"},x:1,y:5},{data:{params:{_target:2},key:"connector"},x:1,y:6},{data:{params:{_target:2},key:"connector"},x:1,y:7},{data:{params:{_target:4},key:"connector"},x:1,y:8},{data:{params:{_target:4},key:"connector"},x:2,y:1},{data:{key:"constantNumber",constantValue:"5"},x:2,y:2},{data:{params:{_target:4},key:"connector"},x:2,y:3},{data:{key:"constantNumber",constantValue:"5"},x:2,y:4},{data:{params:{_number2:1,_vector1:2},key:"operatorVectorMultiply"},x:2,y:5},{data:{params:{_target:2},key:"operatorEntityLook"},x:2,y:6},{data:{params:{_target:4},key:"connector"},x:2,y:7},{data:{params:{_target:4},key:"connector"},x:2,y:8},{data:{params:{_target:4},key:"connector"},x:3,y:1},{data:{params:{_max:3,_time:0,_target:1,_position:2},key:"trickConjureBlockSequence"},x:3,y:2},{data:{params:{_target:2},key:"connector"},x:3,y:3},{data:{params:{_target:2},key:"connector"},x:3,y:4},{data:{params:{_vector3:0,_vector2:2,_vector1:3},key:"operatorVectorSum"},x:3,y:5},{data:{params:{_target:2},key:"operatorEntityPosition"},x:3,y:6},{data:{key:"selectorCaster"},x:3,y:7},{data:{params:{_target:4},key:"connector"},x:3,y:8},{data:{key:"constantNumber",constantValue:"9"},x:4,y:0},{data:{params:{_number2:1,_vector1:4},key:"operatorVectorMultiply"},x:4,y:1},{data:{params:{_max:4,_time:0,_target:1,_position:2},key:"trickConjureBlockSequence"},x:4,y:2},{data:{params:{_vector3:0,_vector2:4,_vector1:2},key:"operatorVectorSubtract"},x:4,y:3},{data:{params:{_target:3},key:"connector"},x:4,y:4},{data:{params:{_target:4},key:"connector"},x:4,y:8},{data:{key:"constantNumber",constantValue:"1"},x:5,y:0},{data:{params:{_target:4},key:"operatorVectorNormalize"},x:5,y:1},{data:{key:"constantNumber",constantValue:"5"},x:5,y:2},{data:{params:{_target:4},key:"connector"},x:5,y:3},{data:{params:{_target:4},key:"connector"},x:5,y:8},{data:{params:{_x:0,_y:3,_z:0},key:"operatorVectorConstruct"},x:6,y:0},{data:{params:{_vector2:1,_vector1:4},key:"operatorVectorCrossProduct"},x:6,y:1},{data:{params:{_vector2:4,_vector1:1},key:"operatorVectorCrossProduct"},x:6,y:2},{data:{params:{_target:1},key:"operatorVectorNormalize"},x:6,y:3},{data:{params:{_target:1},key:"connector"},x:6,y:4},{data:{params:{_target:1},key:"connector"},x:6,y:5},{data:{params:{_target:1},key:"connector"},x:6,y:6},{data:{params:{_target:1},key:"connector"},x:6,y:7},{data:{params:{_target:1},key:"connector"},x:6,y:8},{data:{key:"selectorCaster"},x:7,y:0},{data:{params:{_target:1},key:"operatorEntityLook"},x:7,y:1},{data:{params:{_target:1},key:"connector"},x:7,y:2}],uuidLeast:-7711147611344218784L}
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