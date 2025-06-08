"""
状态效果数据模型
定义了游戏中状态效果(Buff/Debuff)的所有属性和行为
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .enums import StatusType, EffectType, StatusEffectType

@dataclass
class StatusEffect:
    """状态效果数据模型 - 简化版，用于测试和战斗控制器"""
    name: str                        # 状态名称
    description: str                 # 状态描述
    effect_type: StatusEffectType    # 效果类型
    value: int                       # 效果值
    duration: int                    # 持续回合数
    source_character_id: Optional[str] = None  # 来源角色ID
    is_buff: bool = False            # 是否为增益效果
    
    def to_dict(self) -> Dict[str, Any]:
        """将状态效果转换为字典形式"""
        return {
            "name": self.name,
            "description": self.description,
            "effect_type": self.effect_type.name,
            "value": self.value,
            "duration": self.duration,
            "source_character_id": self.source_character_id,
            "is_buff": self.is_buff
        }

@dataclass
class PeriodicEffect:
    """周期性效果"""
    effect_type: EffectType  # 效果类型
    value_formula: str       # 效果值计算公式
    
    def to_dict(self) -> Dict[str, Any]:
        """将效果转换为字典形式"""
        return {
            "effect_type": self.effect_type.name,
            "value_formula": self.value_formula
        }

@dataclass
class InstantEffect:
    """即时效果"""
    effect_type: EffectType  # 效果类型
    value_formula: str       # 效果值计算公式
    
    def to_dict(self) -> Dict[str, Any]:
        """将效果转换为字典形式"""
        return {
            "effect_type": self.effect_type.name,
            "value_formula": self.value_formula
        }

@dataclass
class StatModifier:
    """属性修改器"""
    stat_name: str       # 修改的属性名
    value: float         # 修改值
    is_percentage: bool  # 是百分比还是固定值
    
    def to_dict(self) -> Dict[str, Any]:
        """将修改器转换为字典形式"""
        return {
            "stat_name": self.stat_name,
            "value": self.value,
            "is_percentage": self.is_percentage
        }
    
    def apply(self, base_value: float) -> float:
        """
        应用修改器到基础属性值
        
        Args:
            base_value: 基础属性值
            
        Returns:
            修改后的属性值
        """
        if self.is_percentage:
            return base_value * (1 + self.value / 100)
        else:
            return base_value + self.value

@dataclass
class StatusEffectDefinition:
    """状态效果定义数据模型"""
    id: str                          # 状态唯一ID
    name: str                        # 状态名称
    type: StatusType                 # 增益或减益
    icon: str                        # 显示图标
    description: str                 # 状态描述
    max_stacks: int                  # 最大叠加层数
    duration_turns: int              # 基础持续回合数
    is_permanent: bool = False       # 是否永久
    
    # 各种效果
    on_apply_effects: List[InstantEffect] = field(default_factory=list)     # 施加时触发
    on_turn_start_effects: List[PeriodicEffect] = field(default_factory=list)  # 回合开始触发
    on_turn_end_effects: List[PeriodicEffect] = field(default_factory=list)    # 回合结束触发
    on_remove_effects: List[InstantEffect] = field(default_factory=list)    # 移除时触发
    
    # 属性修改
    modifiers: List[StatModifier] = field(default_factory=list)  # 属性修改器列表
    
    # 控制效果
    prevents_action: bool = False    # 是否阻止行动
    prevents_chase: bool = False     # 是否阻止追打
    prevents_mystery: bool = False   # 是否阻止奥义
    
    # 驱散和免疫
    is_dispellable: bool = True     # 是否可被驱散
    is_dispelled_by: List[str] = field(default_factory=list)     # 可被哪些特定效果驱散
    is_immunity_bypassed_by: List[str] = field(default_factory=list)  # 可绕过哪些免疫效果
    
    def to_dict(self) -> Dict[str, Any]:
        """将状态效果定义转换为字典形式"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.name,
            "icon": self.icon,
            "description": self.description,
            "max_stacks": self.max_stacks,
            "duration_turns": self.duration_turns,
            "is_permanent": self.is_permanent,
            "prevents_action": self.prevents_action,
            "prevents_chase": self.prevents_chase,
            "prevents_mystery": self.prevents_mystery,
            "is_dispellable": self.is_dispellable
        }

@dataclass
class ActiveStatusEffect:
    """激活的状态效果数据模型"""
    definition_id: str        # 对应StatusEffectDefinition的ID
    source_character_id: str  # 施加者ID
    target_character_id: str  # 承受者ID
    remaining_turns: int      # 剩余回合数
    current_stacks: int = 1   # 当前叠加层数
    applied_turn: int = 0     # 被施加的回合数
    unique_id: str = ""       # 此状态实例的唯一ID（用于区分同一状态的多个实例）
    
    def reduce_duration(self, turns: int = 1) -> bool:
        """
        减少剩余回合数
        
        Args:
            turns: 减少的回合数
            
        Returns:
            状态是否已过期
        """
        if self.remaining_turns <= 0:  # 永久状态
            return False
            
        self.remaining_turns -= turns
        return self.remaining_turns <= 0
        
    def add_stacks(self, stacks: int) -> int:
        """
        增加叠加层数
        
        Args:
            stacks: 要增加的层数
            
        Returns:
            增加后的总层数
        """
        # 获取状态效果定义（实际实现时需要通过控制器或存储库获取）
        max_stacks = 1  # 默认值，应从definition获取
        
        self.current_stacks = min(max_stacks, self.current_stacks + stacks)
        return self.current_stacks
        
    def is_expired(self) -> bool:
        """
        检查状态是否已过期
        
        Returns:
            如果状态已过期则为True，否则为False
        """
        return self.remaining_turns <= 0
        
    def refresh_duration(self, duration: Optional[int] = None) -> None:
        """
        刷新状态持续时间
        
        Args:
            duration: 新的持续时间，如果为None则使用状态定义的默认持续时间
        """
        if duration is not None:
            self.remaining_turns = duration
            
    def to_dict(self) -> Dict[str, Any]:
        """将激活的状态效果转换为字典形式"""
        return {
            "definition_id": self.definition_id,
            "source_character_id": self.source_character_id,
            "target_character_id": self.target_character_id,
            "remaining_turns": self.remaining_turns,
            "current_stacks": self.current_stacks,
            "applied_turn": self.applied_turn,
            "unique_id": self.unique_id
        } 