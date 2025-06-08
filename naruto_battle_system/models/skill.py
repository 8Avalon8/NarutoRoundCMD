"""
技能数据模型
定义了游戏中技能和技能效果的所有属性
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .enums import SkillType, TargetType, EffectType, ChaseState, RemoveStatusType, StatusType

@dataclass
class SkillEffect:
    """技能效果数据模型"""
    effect_type: EffectType                 # 效果类型
    value_formula: str                      # 效果值计算公式
    status_id_to_apply: Optional[str] = None  # 要施加的状态ID
    apply_chance: float = 1.0               # 施加概率
    remove_status_type: Optional[RemoveStatusType] = None  # 要移除的状态类型
    specific_status_id: Optional[str] = None  # 指定要移除的状态ID
    chakra_change_amount: int = 0           # 查克拉变化量
    summon_character_id: Optional[str] = None  # 召唤的角色ID
    
    def to_dict(self) -> Dict[str, Any]:
        """将效果转换为字典形式"""
        return {
            "effect_type": self.effect_type.name,
            "value_formula": self.value_formula,
            "status_id_to_apply": self.status_id_to_apply,
            "apply_chance": self.apply_chance,
            "remove_status_type": self.remove_status_type.name if self.remove_status_type else None,
            "specific_status_id": self.specific_status_id,
            "chakra_change_amount": self.chakra_change_amount,
            "summon_character_id": self.summon_character_id
        }

@dataclass
class DamageEffect:
    """伤害效果类，用于表示技能造成的伤害"""
    base_value: int                         # 基础伤害值
    scaling: int                            # 攻击力加成百分比
    
    def calculate_damage(self, attacker_attack: int) -> int:
        """根据攻击者攻击力计算最终伤害"""
        return self.base_value + (attacker_attack * self.scaling // 100)

@dataclass
class HealingEffect:
    """治疗效果类，用于表示技能的治疗"""
    base_value: int                         # 基础治疗值
    scaling: int                            # 属性加成百分比
    
    def calculate_healing(self, caster_stat: int) -> int:
        """根据施法者属性计算最终治疗量"""
        return self.base_value + (caster_stat * self.scaling // 100)

@dataclass
class Skill:
    """技能数据模型"""
    name: str                         # 技能名称
    description: str                  # 技能描述
    skill_type: SkillType = SkillType.NORMAL  # 技能类型
    target_type: TargetType = TargetType.SINGLE_ENEMY_FRONT  # 目标选取类型
    id: str = ""                      # 技能唯一ID
    cost: int = 0                     # 查克拉消耗，兼容测试
    chakra_cost: int = 0              # 查克拉消耗
    cooldown_turns: int = 0           # 冷却回合数
    current_cooldown: int = 0         # 当前剩余冷却回合
    target_count: int = 1             # 目标数量
    effects: List[any] = field(default_factory=list)  # 技能效果列表
    
    # 追打相关参数
    causes_chase_state: ChaseState = ChaseState.NONE  # 此技能命中后造成的追打状态
    requires_chase_state: ChaseState = ChaseState.NONE  # 此追打技响应的敌方状态
    chase_priority: int = 0           # 追打优先级
    is_interruptible: bool = True     # 是否可被打断
    is_instant: bool = False          # 是否瞬发
    
    def __post_init__(self):
        """初始化后的处理"""
        # 兼容测试，如果设置了cost但没有设置chakra_cost
        if self.cost > 0 and self.chakra_cost == 0:
            self.chakra_cost = self.cost
    
    def can_be_used(self, team_chakra: int) -> bool:
        """
        检查技能是否可以使用
        
        Args:
            team_chakra: 队伍当前查克拉
            
        Returns:
            如果可以使用则为True，否则为False
        """
        # 检查冷却
        if self.current_cooldown > 0:
            return False
            
        # 检查查克拉（仅对奥义）
        if self.skill_type == SkillType.MYSTERY and self.chakra_cost > team_chakra:
            return False
            
        return True
        
    def can_chase(self, target_state: ChaseState) -> bool:
        """
        检查是否可以对指定状态进行追打
        
        Args:
            target_state: 目标的追打状态
            
        Returns:
            如果可以追打则为True，否则为False
        """
        return self.skill_type == SkillType.CHASE and self.requires_chase_state == target_state
        
    def reduce_cooldown(self, amount: int = 1) -> None:
        """
        减少技能冷却
        
        Args:
            amount: 减少的回合数
        """
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - amount)
            
    def reset_cooldown(self) -> None:
        """重置技能冷却"""
        self.current_cooldown = self.cooldown_turns
        
    def to_dict(self) -> Dict[str, Any]:
        """将技能转换为字典形式"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.skill_type.name,
            "description": self.description,
            "chakra_cost": self.chakra_cost,
            "cooldown": f"{self.current_cooldown}/{self.cooldown_turns}",
            "target_type": self.target_type.name,
            "target_count": self.target_count,
            "causes_chase_state": self.causes_chase_state.name,
            "requires_chase_state": self.requires_chase_state.name,
            "is_interruptible": self.is_interruptible,
            "is_instant": self.is_instant,
            "effects": [effect.to_dict() for effect in self.effects if hasattr(effect, 'to_dict')]
        } 