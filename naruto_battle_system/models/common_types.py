from typing import List, Dict, Optional, Callable, Any, Protocol, TypeVar, TYPE_CHECKING

# 定义类型变量
T = TypeVar('T')

# 使用协议定义接口
class ActionProtocol(Protocol):
    """动作接口协议"""
    pass

class CharacterProtocol(Protocol):
    """角色接口协议"""
    id: str
    name: str
    is_player_controlled: bool

class BattleTeamProtocol(Protocol):
    """队伍接口协议"""
    name: str
    characters: List[CharacterProtocol]

# 如果需要在类型检查时使用完整类
if TYPE_CHECKING:
    from ..models.battle_state import BattleState, BattleSession
    from ..controllers.input_controller import InputController
    from ..controllers.battle_controller import BattleController
    from ..models.action import Action
    from ..views.battle_view import BattleView 