"""
角色数据模型
定义了游戏中角色的所有属性和状态
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Union
from .enums import ChaseState

@dataclass
class Character:
    """角色数据模型"""
    name: str                    # 角色名称
    
    # 基本属性
    hp: int = 0                  # 当前生命值，兼容测试用例
    max_hp: int = 100            # 最大生命值
    chakra: int = 0              # 当前查克拉
    max_chakra: int = 100        # 最大查克拉
    attack: int = 10             # 攻击力
    defense: int = 10            # 防御力
    speed: int = 10              # 速度/先攻值
    
    # 高级属性
    id: str = ""                 # 角色唯一ID
    ninja_tech: int = 0          # 忍术攻击
    resistance: int = 0          # 忍术防御
    crit_rate: float = 0.05      # 暴击率
    crit_damage_bonus: float = 0.5  # 暴击伤害加成
    position: int = 1            # 战场位置/手位 (1-4)
    
    # 技能相关
    skills: List[any] = field(default_factory=list)  # 所有技能列表，用于测试
    normal_attack_id: str = ""   # 普攻技能ID
    mystery_art_id: str = ""     # 奥义技能ID
    chase_skill_ids: List[str] = field(default_factory=list)  # 追打技能ID列表
    passive_skill_ids: List[str] = field(default_factory=list)  # 被动技能ID列表
    traits: List[any] = field(default_factory=list)  # 角色特性列表
    
    # 状态效果
    status_effects: List[any] = field(default_factory=list)  # 用于测试的状态效果列表
    current_buffs: List[str] = field(default_factory=list)   # 当前生效的Buff ID列表
    current_debuffs: List[str] = field(default_factory=list) # 当前生效的Debuff ID列表
    current_states: Set[ChaseState] = field(default_factory=set)  # 当前角色处于的追打状态
    
    # 角色标签和状态
    tags: List[str] = field(default_factory=list)  # 角色标签
    is_alive: bool = True                          # 是否存活
    can_act: bool = True                           # 是否能行动
    summoner_id: Optional[str] = None              # 召唤者ID
    is_summon: bool = False                        # 是否为召唤物
    chakra_regen: int = 10                         # 每回合恢复查克拉
    is_player_controlled: bool = False             # 是否由玩家控制
    
    # 内部属性
    current_hp: int = 0                           # 内部使用的当前生命值
    
    def __post_init__(self):
        """初始化后的处理，确保当前生命值不超过最大生命值"""
        # 如果测试设置了hp，则把它作为current_hp
        if self.hp > 0:
            self.current_hp = self.hp
        else:
            self.current_hp = self.max_hp
            self.hp = self.max_hp
            
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
            self.hp = self.max_hp
            
    def is_affected_by_chase_state(self, state: ChaseState) -> bool:
        """
        检查角色是否受到特定追打状态的影响
        
        Args:
            state: 要检查的追打状态
            
        Returns:
            如果角色受到该状态影响则为True，否则为False
        """
        return state in self.current_states
        
    def add_chase_state(self, state: ChaseState) -> None:
        """
        添加追打状态
        
        Args:
            state: 要添加的追打状态
        """
        if state != ChaseState.NONE:
            self.current_states.add(state)
            
    def remove_chase_state(self, state: ChaseState) -> None:
        """
        移除追打状态
        
        Args:
            state: 要移除的追打状态
        """
        if state in self.current_states:
            self.current_states.remove(state)
            
    def clear_chase_states(self) -> None:
        """清除所有追打状态"""
        self.current_states.clear()
        
    def take_damage(self, amount: int) -> int:
        """
        受到伤害
        
        Args:
            amount: 伤害数值
            
        Returns:
            实际受到的伤害值
        """
        if not self.is_alive:
            return 0
            
        actual_damage = min(self.current_hp, amount)
        self.current_hp -= actual_damage
        self.hp = self.current_hp  # 同步更新hp属性
        
        if self.current_hp <= 0:
            self.is_alive = False
            self.current_hp = 0
            self.hp = 0
            
        return actual_damage
        
    def heal(self, amount: int) -> int:
        """
        接受治疗
        
        Args:
            amount: 治疗数值
            
        Returns:
            实际恢复的生命值
        """
        if not self.is_alive:
            return 0
            
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        self.hp = self.current_hp  # 同步更新hp属性
        return self.current_hp - old_hp
        
    def can_use_skill(self, skill_id: str, team_chakra: int) -> bool:
        """
        检查是否能使用指定技能
        
        Args:
            skill_id: 技能ID
            team_chakra: 队伍当前查克拉
            
        Returns:
            如果能使用则为True，否则为False
        """
        # 此方法需要在控制器中实现，因为需要访问技能数据
        pass
        
    def get_effective_stat(self, stat_name: str) -> float:
        """
        获取经过Buff/Debuff修正后的属性值
        
        Args:
            stat_name: 属性名称
            
        Returns:
            修正后的属性值
        """
        # 此方法需要在控制器中实现，因为需要计算状态效果的影响
        pass 

    def clone(self) -> "Character":
        """
        克隆角色
        """
        return Character(
            name=self.name,
            hp=self.hp,
            max_hp=self.max_hp,
            chakra=self.chakra,
            max_chakra=self.max_chakra,
            attack=self.attack,
            defense=self.defense,
            speed=self.speed,
            ninja_tech=self.ninja_tech,
            resistance=self.resistance,
            crit_rate=self.crit_rate,
            crit_damage_bonus=self.crit_damage_bonus,
            position=self.position,
            skills=self.skills,
            normal_attack_id=self.normal_attack_id,
            mystery_art_id=self.mystery_art_id,
            chase_skill_ids=self.chase_skill_ids,
            passive_skill_ids=self.passive_skill_ids,
            status_effects=self.status_effects,
            current_buffs=self.current_buffs,
            current_debuffs=self.current_debuffs,
            current_states=self.current_states,
            tags=self.tags,
            is_alive=self.is_alive,
            can_act=self.can_act,
            summoner_id=self.summoner_id,
            is_summon=self.is_summon,
            chakra_regen=self.chakra_regen,
            is_player_controlled=self.is_player_controlled,
            current_hp=self.current_hp
        )