import os
import sys
from typing import Dict, List, Any, Optional

from .views.menu_view import MenuView
from .services.battle_service import BattleService
from .services.character_service import CharacterService
from .data.repositories import CharacterRepository
from .config.game_config import game_config
from .utils.logger import game_logger


class Game:
    """游戏主类，控制游戏流程"""
    
    def __init__(self):
        """初始化游戏"""
        self.menu_view = MenuView()
        self.character_repository = CharacterRepository()
        self.character_service = CharacterService(self.character_repository)
        self.battle_service = BattleService(self.character_repository)
        self.running = False
    
    def initialize(self) -> None:
        """初始化游戏数据"""
        # 如果没有角色数据，创建默认角色
        if not self.character_repository.get_all():
            game_logger.info("创建默认角色数据")
            self.character_service.create_default_characters()
    
    def run(self) -> None:
        """运行游戏主循环"""
        self.running = True
        self.initialize()
        
        while self.running:
            choice = self.menu_view.show_main_menu()
            
            if choice == 1:  # 开始新战斗
                self._start_new_battle()
            elif choice == 2:  # 角色列表
                self._show_characters()
            elif choice == 3:  # 帮助信息
                self._show_help()
            elif choice == 4:  # 退出游戏
                self._exit_game()
    
    def _start_new_battle(self) -> None:
        """开始新的战斗"""
        # 获取可用角色
        available_characters = self.battle_service.get_available_characters()
        
        # 显示战斗设置菜单
        (team_a_indices, team_b_indices) = self.menu_view.show_battle_setup_menu(available_characters)
        
        # 创建角色实例
        team_a_characters = self.battle_service.create_characters_from_indices(team_a_indices, True)
        team_b_characters = self.battle_service.create_characters_from_indices(team_b_indices, False)
        
        # 创建战斗
        battle_session = self.battle_service.create_battle(
            team_a_characters, 
            team_b_characters, 
            "第七班", 
            "敌方忍者"
        )
        
        # 战斗日志
        game_logger.log_battle_event("BATTLE_START", 
                                     f"队伍A: {', '.join([c.name for c in team_a_characters])} VS "
                                     f"队伍B: {', '.join([c.name for c in team_b_characters])}")
        
        # 开始战斗
        self.battle_service.start_battle(battle_session.battle_id)
        
        # 获取战斗结果
        winning_team = self.battle_service.end_battle(battle_session.battle_id)
        
        if winning_team:
            # 显示战斗结果
            self.menu_view.show_battle_result(
                winning_team.name,
                battle_session.battle_state.current_round
            )
            
            # 战斗日志
            game_logger.log_battle_event(
                "BATTLE_END", 
                f"胜利队伍: {winning_team.name}, 回合数: {battle_session.battle_state.current_round}"
            )
    
    def _show_characters(self) -> None:
        """显示角色列表"""
        characters_data = self.battle_service.get_available_characters()
        self.menu_view.show_character_list(characters_data)
    
    def _show_help(self) -> None:
        """显示帮助信息"""
        self.menu_view.show_help()
    
    def _exit_game(self) -> None:
        """退出游戏"""
        if self.menu_view.show_exit_confirmation():
            game_logger.info("游戏结束")
            self.running = False


def main():
    """游戏入口函数"""
    try:
        # 初始化日志
        debug_mode = game_config.get("game", {}).get("debug_mode", False)
        log_level = "DEBUG" if debug_mode else game_config.get("data", {}).get("log_level", "INFO")
        game_logger.info(f"游戏启动，日志级别: {log_level}")
        
        # 创建并运行游戏
        game = Game()
        game.run()
        
    except Exception as e:
        game_logger.critical(f"游戏发生严重错误: {str(e)}")
        print(f"发生错误: {str(e)}")
    finally:
        print("游戏已退出。")


if __name__ == "__main__":
    main() 