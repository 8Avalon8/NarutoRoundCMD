"""
枚举类型定义
包含战斗系统中使用的所有枚举类型
"""
from enum import Enum, auto

class ActionType(Enum):
    """动作类型枚举"""
    ATTACK = auto()   # 普通攻击
    SKILL = auto()    # 技能
    ITEM = auto()     # 使用道具
    PASS = auto()     # 跳过回合
    DEFEND = auto()   # 防御

class SkillType(Enum):
    """技能类型枚举"""
    NORMAL = auto()    # 普通攻击
    MYSTERY = auto()   # 奥义技能
    CHASE = auto()     # 追打技能
    PASSIVE = auto()   # 被动技能
    DAMAGE = auto()    # 伤害技能（测试用）
    HEALING = auto()   # 治疗技能（测试用）

class TargetType(Enum):
    """目标选择类型枚举"""
    SINGLE = auto()                  # 单个目标（测试用）
    SINGLE_ENEMY_FRONT = auto()      # 正面敌人
    SINGLE_ENEMY_LOWEST_HP = auto()  # 生命最低敌人
    SINGLE_ENEMY_MANUAL = auto()     # 手动选择敌人
    ALL_ENEMIES = auto()             # 敌方全体
    RANDOM_N_ENEMIES = auto()        # 随机N个敌人
    ENEMY_ROW_MOST = auto()          # 敌人最多的一横行
    SELF = auto()                    # 自身
    SINGLE_ALLY = auto()             # 单个友方
    ALL_ALLIES = auto()              # 友方全体

class StatusEffectType(Enum):
    """状态效果类型枚举"""
    BUFF_ATK = auto()    # 攻击力提升
    BUFF_DEF = auto()    # 防御力提升
    BUFF_SPD = auto()    # 速度提升
    DEBUFF_ATK = auto()  # 攻击力降低
    DEBUFF_DEF = auto()  # 防御力降低
    DEBUFF_SPD = auto()  # 速度降低
    STUN = auto()        # 眩晕
    FREEZE = auto()      # 冰冻
    DOT = auto()         # 持续伤害
    HOT = auto()         # 持续治疗
    SHIELD = auto()      # 护盾
    REFLECT = auto()     # 伤害反弹
    IMMUNITY = auto()    # 状态免疫

class EffectType(Enum):
    """效果类型枚举"""
    DAMAGE = auto()        # 造成伤害
    HEAL = auto()          # 治疗
    APPLY_STATUS = auto()  # 施加状态
    REMOVE_STATUS = auto() # 移除状态
    MODIFY_CHAKRA = auto() # 修改查克拉
    SUMMON = auto()        # 召唤单位

class StatusType(Enum):
    """状态类型枚举"""
    BUFF = auto()   # 增益效果
    DEBUFF = auto() # 减益效果

class ChaseState(Enum):
    """追打状态枚举"""
    NONE = auto()       # 无特殊状态
    SMALL_FLOAT = auto()# 小浮空
    BIG_FLOAT = auto()  # 大浮空
    KNOCKDOWN = auto()  # 倒地
    REPEL = auto()      # 击退

class RemoveStatusType(Enum):
    """状态移除类型枚举"""
    BUFF = auto()           # 移除增益效果
    DEBUFF = auto()         # 移除减益效果
    SPECIFIC_STATUS = auto() # 移除特定状态 