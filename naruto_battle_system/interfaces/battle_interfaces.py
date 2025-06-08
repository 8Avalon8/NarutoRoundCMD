"""
战斗系统接口定义
定义了战斗控制器、状态查询和事件系统的所有接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Tuple, Optional, TypeVar, Generic, TYPE_CHECKING

from ..models.character import Character
from ..models.battle_team import BattleTeam
from ..models.action import ActionResult
from ..models.common_types import CharacterProtocol

# 条件导入，避免循环引用
if TYPE_CHECKING:
    from ..models.battle_state import BattleState
    from ..models.battle_state import BattleSession

# 使用泛型定义
T = TypeVar('T')
CharacterId = str
TeamId = str
SkillId = str
StatusEffectId = str

class IAction:
    """战斗行动接口"""
    pass

class IActionResult:
    """行动结果接口"""
    pass

class IBattleState:
    """战斗状态接口"""
    pass

class Target:
    """目标信息"""
    pass

class CharacterStatus:
    """角色状态信息"""
    pass

class TeamStatus:
    """队伍状态信息"""
    pass

class SkillInfo:
    """技能信息"""
    pass

class IBattleController(ABC):
    """战斗控制器接口"""
    
    @abstractmethod
    def start_battle(self, team1: Optional['BattleTeam'] = None, team2: Optional['BattleTeam'] = None) -> Optional[Any]:
        """
        开始一场战斗
        
        Args:
            team1: 第一支队伍
            team2: 第二支队伍
            
        Returns:
            战斗会话对象
        """
        pass
    
    @abstractmethod
    def get_available_actions(self, character_id: CharacterId) -> List[IAction]:
        """
        获取指定角色可用的行动
        
        Args:
            character_id: 角色ID
            
        Returns:
            可用行动列表
        """
        pass
        
    @abstractmethod
    def execute_action(self, action: Any) -> Any:
        """
        执行一个行动并返回结果
        
        Args:
            action: 要执行的行动
            
        Returns:
            行动结果
        """
        pass
        
    @abstractmethod
    def get_battle_state(self) -> IBattleState:
        """
        获取当前战斗状态
        
        Returns:
            战斗状态对象
        """
        pass
        
    @abstractmethod
    def is_battle_ended(self) -> bool:
        """
        检查战斗是否结束
        
        Returns:
            如果战斗已结束则为True，否则为False
        """
        pass

class IBattleQuery(ABC):
    """战斗查询接口"""
    
    @abstractmethod
    def get_character_status(self, character_id: CharacterId) -> CharacterStatus:
        """
        获取角色状态
        
        Args:
            character_id: 角色ID
            
        Returns:
            角色状态对象
        """
        pass
        
    @abstractmethod
    def get_team_status(self, team_id: TeamId) -> TeamStatus:
        """
        获取队伍状态
        
        Args:
            team_id: 队伍ID
            
        Returns:
            队伍状态对象
        """
        pass
        
    @abstractmethod
    def get_skill_info(self, skill_id: SkillId) -> SkillInfo:
        """
        获取技能信息
        
        Args:
            skill_id: 技能ID
            
        Returns:
            技能信息对象
        """
        pass
        
    @abstractmethod
    def get_available_targets(self, skill_id: SkillId, caster_id: CharacterId) -> List[Target]:
        """
        获取技能可用目标列表
        
        Args:
            skill_id: 技能ID
            caster_id: 施法者ID
            
        Returns:
            可用目标列表
        """
        pass

class IBattleEvents(ABC):
    """战斗事件接口"""
    
    # 测试用事件方法
    def on_battle_start(self, battle_state: Any) -> None:
        """战斗开始事件"""
        pass
        
    def on_round_start(self, battle_state: Any) -> None:
        """回合开始事件"""
        pass
        
    def on_turn_start(self, character: Character) -> None:
        """角色回合开始事件"""
        pass
        
    def on_turn_end(self, character: Character) -> None:
        """角色回合结束事件"""
        pass
        
    def on_turn_skipped(self, character: Character) -> None:
        """角色回合被跳过事件"""
        pass
        
    def on_action_executed(self, result: ActionResult) -> None:
        """动作执行完成事件"""
        pass
        
    def on_battle_end(self, battle_state: Any) -> None:
        """战斗结束事件"""
        pass
        
    def on_effect_triggered(self, character: Character, effect: Any, value: int) -> None:
        """效果触发事件"""
        pass
        
    def on_status_effect_removed(self, character: Character, effect: Any) -> None:
        """状态效果移除事件"""
        pass
    
    @abstractmethod
    def subscribe_damage_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        订阅伤害事件
        
        Args:
            callback: 事件回调函数，接收事件数据字典
        """
        pass
        
    @abstractmethod
    def subscribe_status_change_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        订阅状态变化事件
        
        Args:
            callback: 事件回调函数，接收事件数据字典
        """
        pass
        
    @abstractmethod
    def subscribe_turn_change_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        订阅回合变化事件
        
        Args:
            callback: 事件回调函数，接收事件数据字典
        """
        pass
        
    @abstractmethod
    def subscribe_chase_trigger_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        订阅追打触发事件
        
        Args:
            callback: 事件回调函数，接收事件数据字典
        """
        pass

class IRepository(Generic[T]):
    """仓库接口"""
    
    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        """
        获取实体
        
        Args:
            id: 实体ID
            
        Returns:
            指定ID的实体，如果不存在则返回None
        """
        pass
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """
        添加实体
        
        Args:
            entity: 要添加的实体
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """
        更新实体
        
        Args:
            entity: 要更新的实体
        """
        pass
    
    @abstractmethod
    def remove(self, id: str) -> bool:
        """
        删除实体
        
        Args:
            id: 实体ID
            
        Returns:
            是否删除成功
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        获取所有实体
        
        Returns:
            所有实体的列表
        """
        pass 