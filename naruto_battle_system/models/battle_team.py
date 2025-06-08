"""
战斗小队数据模型
定义了游戏中队伍的属性和行为
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .character import Character

@dataclass
class BattleTeam:
    """战斗小队数据模型"""
    name: str
    player_id: str                      # 玩家/AI的ID
    characters: List[Character] = field(default_factory=list)  # 队伍中的角色列表（测试用）
    character_ids: List[str] = field(default_factory=list)     # 队伍中的角色ID列表 (按手位1-4排序)
    shared_chakra: int = 0              # 小队当前共享查克拉总量
    max_chakra: int = 100               # 小队查克拉上限 (通常为100)
    chakra_per_turn: int = 20           # 每回合自动回复的查克拉 (通常为20)
    team_buffs: List[str] = field(default_factory=list)  # 队伍级别的Buff ID列表 (如结界)
    
    def __post_init__(self):
        """初始化后的处理，确保兼容测试"""
        # 如果提供了characters列表但没有character_ids，则生成character_ids
        if self.characters and not self.character_ids:
            self.character_ids = [c.id for c in self.characters if hasattr(c, 'id')]
    
    def add_chakra(self, amount: int) -> int:
        """
        增加队伍查克拉
        
        Args:
            amount: 增加的查克拉量
            
        Returns:
            增加后的查克拉总量
        """
        self.shared_chakra = min(self.max_chakra, self.shared_chakra + amount)
        return self.shared_chakra
        
    def use_chakra(self, amount: int) -> bool:
        """
        使用队伍查克拉
        
        Args:
            amount: 使用的查克拉量
            
        Returns:
            如果查克拉足够使用则为True，否则为False
        """
        if self.shared_chakra >= amount:
            self.shared_chakra -= amount
            return True
        return False
        
    def process_turn_start(self) -> None:
        """处理回合开始时的查克拉恢复"""
        self.shared_chakra = min(self.max_chakra, self.shared_chakra + self.chakra_per_turn)
        
    def is_defeated(self, all_characters: Dict[str, 'Character'] = None) -> bool:
        """
        检查队伍是否已被击败
        
        Args:
            all_characters: 所有角色的字典，键为角色ID，值为角色对象
            
        Returns:
            如果队伍所有角色都已被击败则为True，否则为False
        """
        # 测试兼容：如果提供了characters列表，直接使用它
        if self.characters:
            return all(not c.is_alive for c in self.characters)
            
        # 原始实现
        if all_characters:
            for char_id in self.character_ids:
                character = all_characters.get(char_id)
                if character and character.is_alive:
                    return False
            return True
        return False
        
    def get_alive_characters(self, all_characters: Dict[str, 'Character'] = None) -> List[str]:
        """
        获取队伍中存活的角色ID列表
        
        Args:
            all_characters: 所有角色的字典，键为角色ID，值为角色对象
            
        Returns:
            存活角色ID列表
        """
        # 测试兼容：如果提供了characters列表，直接使用它
        if self.characters:
            return [c.id for c in self.characters if c.is_alive and hasattr(c, 'id')]
            
        # 原始实现
        if all_characters:
            return [char_id for char_id in self.character_ids 
                    if char_id in all_characters and all_characters[char_id].is_alive]
        return []
    
    def add_team_buff(self, buff_id: str) -> None:
        """
        添加队伍Buff
        
        Args:
            buff_id: 要添加的BuffID
        """
        if buff_id not in self.team_buffs:
            self.team_buffs.append(buff_id)
            
    def remove_team_buff(self, buff_id: str) -> bool:
        """
        移除队伍Buff
        
        Args:
            buff_id: 要移除的BuffID
            
        Returns:
            是否成功移除
        """
        if buff_id in self.team_buffs:
            self.team_buffs.remove(buff_id)
            return True
        return False
        
    def has_team_buff(self, buff_id: str) -> bool:
        """
        检查队伍是否有指定的Buff
        
        Args:
            buff_id: 要检查的BuffID
            
        Returns:
            如果有则为True，否则为False
        """
        return buff_id in self.team_buffs
        
    def to_dict(self) -> Dict[str, Any]:
        """将队伍转换为字典形式"""
        return {
            "player_id": self.player_id,
            "character_ids": self.character_ids,
            "chakra": f"{self.shared_chakra}/{self.max_chakra}",
            "chakra_per_turn": self.chakra_per_turn,
            "team_buffs": self.team_buffs
        } 