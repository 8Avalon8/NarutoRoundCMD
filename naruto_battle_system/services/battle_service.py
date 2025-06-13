import uuid
import threading
import time
from typing import List, Dict, Optional, Callable, Any, TYPE_CHECKING
from ..models.character import Character
from ..models.battle_state import BattleState, BattleSession
from ..models.battle_team import BattleTeam
from ..models.action import Action
from ..controllers.battle_controller import BattleController
from ..controllers.input_controller import InputController
from ..views.battle_view import BattleView
from ..data.repositories import CharacterRepository
from ..models.common_types import CharacterProtocol
from ..utils.logger import game_logger


class BattleService:
    """战斗服务，处理战斗流程和管理"""
    
    def __init__(self, character_repository: CharacterRepository):
        """初始化战斗服务
        
        Args:
            character_repository: 角色仓库实例
        """
        self.character_repository = character_repository
        self.active_battles: Dict[str, BattleSession] = {}
    
    def create_battle(self, team_a_characters: List[Character], team_b_characters: List[Character], 
                     team_a_name: str = "玩家队伍", team_b_name: str = "敌方队伍") -> BattleSession:
        """创建新的战斗
        
        Args:
            team_a_characters: 队伍A的角色列表
            team_b_characters: 队伍B的角色列表
            team_a_name: 队伍A的名称
            team_b_name: 队伍B的名称
            
        Returns:
            创建的战斗会话
        """
        # 创建队伍
        team_a = BattleTeam(team_a_name, team_a_characters)
        team_b = BattleTeam(team_b_name, team_b_characters)
        
        # 创建战斗状态
        battle_state = BattleState(team_a, team_b)
        
        # 创建视图
        battle_view = BattleView(battle_state)
        
        # 创建控制器
        battle_controller = BattleController(battle_state, battle_view)
        input_controller = InputController(battle_state)
        
        # 将动作选择回调链接到战斗控制器
        input_controller.register_action_callback(
            lambda action: self._execute_player_action(battle_controller, action)
        )
        
        # 创建并保存战斗会话
        battle_id = str(uuid.uuid4())
        battle_session = BattleSession(
            battle_id=battle_id,
            battle_state=battle_state,
            battle_controller=battle_controller,
            input_controller=input_controller,
            battle_view=battle_view
        )
        
        self.active_battles[battle_id] = battle_session
        return battle_session
    
    def start_battle(self, battle_id: str) -> None:
        """开始指定的战斗
        
        Args:
            battle_id: 要开始的战斗ID
            
        Raises:
            ValueError: 如果找不到指定ID的战斗
        """
        if battle_id not in self.active_battles:
            raise ValueError(f"找不到ID为 {battle_id} 的战斗")
            
        session = self.active_battles[battle_id]
        session.battle_controller.start_battle()
        
        # 开始战斗循环
        self._battle_loop(session)
    
    def _battle_loop(self, session: BattleSession) -> None:
        """战斗主循环
        
        Args:
            session: 战斗会话
        """
        game_logger.debug(f"_battle_loop: Initial check of is_battle_over() for session {session.battle_id}. Result: {session.battle_controller.is_battle_over()}")
        while not session.battle_controller.is_battle_over():
            current_round = session.battle_state.current_round
            game_logger.debug(f"_battle_loop: Round {current_round} - About to call process_turn for session {session.battle_id}.")
            # 处理当前角色的回合
            is_battle_over_flag = session.battle_controller.process_turn()
            game_logger.debug(f"_battle_loop: Round {current_round} - process_turn returned: {is_battle_over_flag}. Current is_battle_over(): {session.battle_controller.is_battle_over()}")
            if is_battle_over_flag:
                break
                
            # 获取当前角色
            current_character = session.battle_controller.get_current_character()
            if not current_character:
                continue
                
            # 如果是玩家控制的角色，等待玩家输入
            if current_character.is_player_controlled:
                self._handle_player_input(session, current_character)
    
    def _handle_player_input(self, session: BattleSession, character: Character) -> None:
        """处理玩家输入
        
        Args:
            session: 战斗会话
            character: 当前行动的角色
        """
        # 提示玩家输入
        session.battle_view.prompt_for_action(character)
        
        # 读取输入并处理
        while True:
            try:
                command = input().strip()
                if session.input_controller.process_command(command, character):
                    break  # 指令处理成功，跳出循环
            except Exception as e:
                print(f"错误: {str(e)}")
    
    def _execute_player_action(self, battle_controller: BattleController, action: Action) -> None:
        """执行玩家选择的动作
        
        Args:
            battle_controller: 战斗控制器
            action: 玩家选择的动作
        """
        battle_controller.execute_action(action)
    
    def end_battle(self, battle_id: str) -> Optional[BattleTeam]:
        """结束指定的战斗，返回获胜队伍
        
        Args:
            battle_id: 要结束的战斗ID
            
        Returns:
            获胜的队伍，如果战斗尚未结束返回None
            
        Raises:
            ValueError: 如果找不到指定ID的战斗
        """
        if battle_id not in self.active_battles:
            raise ValueError(f"找不到ID为 {battle_id} 的战斗")
            
        session = self.active_battles[battle_id]
        winning_team = session.battle_controller.get_winning_team()
        
        if winning_team:
            # 清理战斗资源
            del self.active_battles[battle_id]
            
        return winning_team
    
    def get_available_characters(self) -> List[Dict[str, Any]]:
        """获取可用于战斗的角色列表
        
        Returns:
            可用角色的简化信息列表
        """
        characters = self.character_repository.get_all()
        
        # 转换为简化的字典形式
        result = []
        for character in characters:
            result.append({
                "id": character.id,
                "name": character.name,
                "hp": character.hp,
                "max_hp": character.max_hp,
                "chakra": character.chakra,
                "max_chakra": character.max_chakra,
                "attack": character.attack,
                "defense": character.defense,
                "speed": character.speed,
                "is_player_controlled": character.is_player_controlled,
                "skills": [{"name": skill.name, "description": skill.description} for skill in character.skills]
            })
            
        return result
    
    def create_characters_from_indices(self, character_indices: List[int], make_player_controlled: bool = False) -> List[Character]:
        """根据角色索引创建角色实例列表
        
        Args:
            character_indices: 角色索引列表
            make_player_controlled: 是否将角色设置为玩家控制
            
        Returns:
            创建的角色实例列表
        """
        all_characters = self.character_repository.get_all()
        result = []
        
        for idx in character_indices:
            if 0 <= idx < len(all_characters):
                # 创建角色的深拷贝
                character = all_characters[idx].clone()
                if make_player_controlled:
                    character.is_player_controlled = True
                result.append(character)
                
        return result 