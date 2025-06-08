"""
战斗行动数据模型
定义了游戏中行动和行动结果的属性和行为
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

from .character import Character
from .enums import ActionType as EnumActionType

# 测试用的Action类，简化版
@dataclass
class Action:
    """战斗行动数据模型 - 测试用简化版"""
    character: Character                # 执行角色
    action_type: EnumActionType         # 行动类型
    target: Optional[Character] = None  # 目标角色
    skill: Optional[Any] = None         # 使用的技能
    
    def to_dict(self) -> Dict[str, Any]:
        """将行动转换为字典形式"""
        return {
            "character": self.character.name if self.character else None,
            "action_type": self.action_type.name if self.action_type else None,
            "target": self.target.name if self.target else None,
            "skill": self.skill.name if self.skill and hasattr(self.skill, 'name') else None
        }

# 测试用的ActionResult类，简化版
@dataclass
class ActionResult:
    """战斗行动结果数据模型 - 测试用简化版"""
    action: Action                      # 执行的行动
    success: bool = True                # 行动是否成功
    messages: List[str] = field(default_factory=list)  # 结果消息列表
    
    def add_message(self, message: str) -> None:
        """添加结果消息"""
        self.messages.append(message)

# 原始的ActionType枚举
class OriginalActionType(Enum):
    """行动类型枚举"""
    NORMAL_ATTACK = "NORMAL_ATTACK"  # 普通攻击
    MYSTERY_ART = "MYSTERY_ART"      # 奥义技能
    CHASE = "CHASE"                  # 追打
    PASS = "PASS"                    # 跳过行动

# 原始的Action类
@dataclass
class OriginalAction:
    """战斗行动数据模型 - 原始版本"""
    type: OriginalActionType             # 行动类型
    character_id: str                    # 执行角色ID
    skill_id: Optional[str] = None       # 使用的技能ID
    target_ids: List[str] = field(default_factory=list)  # 目标ID列表
    
    def to_dict(self) -> Dict[str, Any]:
        """将行动转换为字典形式"""
        return {
            "type": self.type.value,
            "character_id": self.character_id,
            "skill_id": self.skill_id,
            "target_ids": self.target_ids
        }

@dataclass
class DamageDetail:
    """伤害细节"""
    target_id: str           # 目标ID
    damage_amount: int       # 伤害数值
    is_critical: bool = False  # 是否暴击
    
    def to_dict(self) -> Dict[str, Any]:
        """将伤害细节转换为字典形式"""
        return {
            "target_id": self.target_id,
            "damage_amount": self.damage_amount,
            "is_critical": self.is_critical
        }

@dataclass
class HealingDetail:
    """治疗细节"""
    target_id: str           # 目标ID
    heal_amount: int         # 治疗数值
    
    def to_dict(self) -> Dict[str, Any]:
        """将治疗细节转换为字典形式"""
        return {
            "target_id": self.target_id,
            "heal_amount": self.heal_amount
        }

@dataclass
class StatusChangeDetail:
    """状态变化细节"""
    status_id: str               # 状态ID
    target_id: str               # 目标ID
    source_id: str               # 来源ID
    is_applied: bool = True      # 是否添加状态（False表示移除）
    stacks: int = 1              # 层数
    
    def to_dict(self) -> Dict[str, Any]:
        """将状态变化细节转换为字典形式"""
        return {
            "status_id": self.status_id,
            "target_id": self.target_id,
            "source_id": self.source_id,
            "is_applied": self.is_applied,
            "stacks": self.stacks
        }

@dataclass
class ChakraChangeDetail:
    """查克拉变化细节"""
    team_id: str             # 队伍ID
    change_amount: int       # 变化数值
    
    def to_dict(self) -> Dict[str, Any]:
        """将查克拉变化细节转换为字典形式"""
        return {
            "team_id": self.team_id,
            "change_amount": self.change_amount
        }

@dataclass
class ChaseDetail:
    """追打细节"""
    character_id: str          # 追打角色ID
    skill_id: str              # 追打技能ID
    target_id: str             # 目标ID
    chase_state: str           # 响应的状态
    combo_count: int           # 当前连击数
    
    def to_dict(self) -> Dict[str, Any]:
        """将追打细节转换为字典形式"""
        return {
            "character_id": self.character_id,
            "skill_id": self.skill_id,
            "target_id": self.target_id,
            "chase_state": self.chase_state,
            "combo_count": self.combo_count
        }

@dataclass
class OriginalActionResult:
    """战斗行动结果数据模型 - 原始版本"""
    action: OriginalAction                                # 执行的行动
    success: bool = True                                # 行动是否成功
    damage_details: List[DamageDetail] = field(default_factory=list)  # 伤害细节列表
    healing_details: List[HealingDetail] = field(default_factory=list)  # 治疗细节列表
    status_changes: List[StatusChangeDetail] = field(default_factory=list)  # 状态变化列表
    chakra_changes: List[ChakraChangeDetail] = field(default_factory=list)  # 查克拉变化列表
    chase_details: List[ChaseDetail] = field(default_factory=list)  # 追打细节列表
    messages: List[str] = field(default_factory=list)   # 结果消息列表
    
    def to_dict(self) -> Dict[str, Any]:
        """将行动结果转换为字典形式"""
        return {
            "action": self.action.to_dict(),
            "success": self.success,
            "damage_details": [d.to_dict() for d in self.damage_details],
            "healing_details": [h.to_dict() for h in self.healing_details],
            "status_changes": [s.to_dict() for s in self.status_changes],
            "chakra_changes": [c.to_dict() for c in self.chakra_changes],
            "chase_details": [c.to_dict() for c in self.chase_details],
            "messages": self.messages
        }
        
    def add_message(self, message: str) -> None:
        """
        添加结果消息
        
        Args:
            message: 要添加的消息
        """
        self.messages.append(message)
        
    def add_damage(self, target_id: str, damage: int, is_critical: bool = False) -> None:
        """
        添加伤害细节
        
        Args:
            target_id: 目标ID
            damage: 伤害数值
            is_critical: 是否暴击
        """
        self.damage_details.append(DamageDetail(
            target_id=target_id,
            damage_amount=damage,
            is_critical=is_critical
        ))
        
    def add_healing(self, target_id: str, heal_amount: int) -> None:
        """
        添加治疗细节
        
        Args:
            target_id: 目标ID
            heal_amount: 治疗数值
        """
        self.healing_details.append(HealingDetail(
            target_id=target_id,
            heal_amount=heal_amount
        ))
        
    def add_status_change(self, status_id: str, target_id: str, 
                         source_id: str, is_applied: bool = True, stacks: int = 1) -> None:
        """
        添加状态变化细节
        
        Args:
            status_id: 状态ID
            target_id: 目标ID
            source_id: 来源ID
            is_applied: 是否添加状态
            stacks: 层数
        """
        self.status_changes.append(StatusChangeDetail(
            status_id=status_id,
            target_id=target_id,
            source_id=source_id,
            is_applied=is_applied,
            stacks=stacks
        ))
        
    def add_chakra_change(self, team_id: str, change_amount: int) -> None:
        """
        添加查克拉变化细节
        
        Args:
            team_id: 队伍ID
            change_amount: 变化数值
        """
        self.chakra_changes.append(ChakraChangeDetail(
            team_id=team_id,
            change_amount=change_amount
        ))
        
    def add_chase(self, character_id: str, skill_id: str, 
                target_id: str, chase_state: str, combo_count: int) -> None:
        """
        添加追打细节
        
        Args:
            character_id: 追打角色ID
            skill_id: 追打技能ID
            target_id: 目标ID
            chase_state: 响应的状态
            combo_count: 当前连击数
        """
        self.chase_details.append(ChaseDetail(
            character_id=character_id,
            skill_id=skill_id,
            target_id=target_id,
            chase_state=chase_state,
            combo_count=combo_count
        )) 