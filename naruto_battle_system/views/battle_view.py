from typing import Any, Callable, List, Dict, Optional
import os
import time
from ..models.character import Character
from ..models.battle_state import BattleState
from ..models.action import ActionResult
from ..models.enums import ActionType, StatusEffectType
from ..interfaces.battle_interfaces import IBattleEvents
from ..utils.logger import game_logger


class ConsoleColors:
    """控制台颜色常量"""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class BattleView(IBattleEvents):
    """战斗视图，实现IBattleEvents接口，用于显示战斗过程"""
    
    def __init__(self, battle_state: BattleState, animation_speed: float = 0.5):
        """初始化战斗视图
        
        Args:
            battle_state: 战斗状态
            animation_speed: 动画显示速度，单位为秒
        """
        self.battle_state = battle_state
        self.animation_speed = animation_speed
    
    def clear_screen(self) -> None:
        """清空控制台屏幕"""
        #os.system('cls' if os.name == 'nt' else 'clear')
        pass
    
    def _wait(self, duration: float = None) -> None:
        """等待一段时间
        
        Args:
            duration: 等待时间，如果为None则使用默认动画速度
        """
        time.sleep(duration if duration is not None else self.animation_speed)
    
    def show_battle_field(self) -> None:
        """显示战场"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"{ConsoleColors.YELLOW}战斗回合: {self.battle_state.current_round}{ConsoleColors.RESET}")
        
        # 显示队伍A
        print(f"\n{ConsoleColors.BLUE}【{self.battle_state.team_a.name}】{ConsoleColors.RESET}")
        for character in self.battle_state.team_a.characters:
            self._display_character(character)
            
        print("\n" + "-" * 60)
        
        # 显示队伍B
        print(f"\n{ConsoleColors.RED}【{self.battle_state.team_b.name}】{ConsoleColors.RESET}")
        for character in self.battle_state.team_b.characters:
            self._display_character(character)
            
        print("\n" + "=" * 60)
    
    def _display_character(self, character: Character) -> None:
        """显示角色状态
        
        Args:
            character: 要显示的角色
        """
        # 计算HP和CP百分比，用于显示进度条
        hp_percent = int((character.hp / character.max_hp) * 20)
        cp_percent = int((character.chakra / character.max_chakra) * 10)
        
        # 根据血量决定颜色
        hp_color = ConsoleColors.GREEN
        if character.hp < character.max_hp * 0.3:
            hp_color = ConsoleColors.RED
        elif character.hp < character.max_hp * 0.7:
            hp_color = ConsoleColors.YELLOW
            
        # 状态颜色
        status_color = ConsoleColors.GREEN if character.is_alive else ConsoleColors.RED
        status_text = "存活" if character.is_alive else "阵亡"
        
        # 当前行动角色标记
        current_marker = ""
        current_character = self.battle_state.get_current_character()
        if current_character and current_character.id == character.id:
            current_marker = f"{ConsoleColors.YELLOW}*{ConsoleColors.RESET} "
        
        # 角色名和状态
        print(f"{current_marker}{character.name} [{status_color}{status_text}{ConsoleColors.RESET}]")
        
        # 仅当角色存活时显示详细信息
        if character.is_alive:
            # HP进度条
            hp_bar = f"[{hp_color}{'■' * hp_percent}{ConsoleColors.RESET}{'□' * (20 - hp_percent)}]"
            print(f"  HP: {hp_bar} {character.hp}/{character.max_hp}")
            
            # CP进度条
            cp_bar = f"[{ConsoleColors.BLUE}{'■' * cp_percent}{ConsoleColors.RESET}{'□' * (10 - cp_percent)}]"
            print(f"  CP: {cp_bar} {character.chakra}/{character.max_chakra}")
            
            # 状态效果
            if character.status_effects:
                effect_texts = []
                for effect in character.status_effects:
                    effect_color = ConsoleColors.RED if effect.is_debuff() else ConsoleColors.GREEN
                    effect_texts.append(f"{effect_color}{effect.effect_type.name}{ConsoleColors.RESET}({effect.duration})")
                print(f"  状态: {', '.join(effect_texts)}")
    
    def on_battle_start(self, battle_state: BattleState) -> None:
        """战斗开始事件
        
        Args:
            battle_state: 战斗状态
        """
        self.clear_screen()
        print(f"\n{ConsoleColors.YELLOW}战斗开始！{ConsoleColors.RESET}")
        print(f"{ConsoleColors.BLUE}{battle_state.team_a.name}{ConsoleColors.RESET} VS {ConsoleColors.RED}{battle_state.team_b.name}{ConsoleColors.RESET}")
        self._wait(1.0)
        self.show_battle_field()
    
    def on_battle_end(self, battle_state: BattleState) -> None:
        """战斗结束事件
        
        Args:
            battle_state: 战斗状态
        """
        # 判断获胜队伍
        team_a_alive = any(c.is_alive for c in battle_state.team_a.characters)
        team_b_alive = any(c.is_alive for c in battle_state.team_b.characters)
        
        winner = None
        if team_a_alive and not team_b_alive:
            winner = battle_state.team_a
        elif team_b_alive and not team_a_alive:
            winner = battle_state.team_b
        
        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"{ConsoleColors.YELLOW}战斗结束！{ConsoleColors.RESET}")
        
        if winner:
            print(f"\n{ConsoleColors.GREEN}获胜队伍: {winner.name}{ConsoleColors.RESET}")
        else:
            print(f"\n{ConsoleColors.YELLOW}战斗以平局结束{ConsoleColors.RESET}")
        
        # 显示双方剩余角色
        print(f"\n{ConsoleColors.BLUE}【{battle_state.team_a.name}】{ConsoleColors.RESET} 剩余角色:")
        for character in battle_state.team_a.characters:
            if character.is_alive:
                print(f"  {character.name} - HP: {character.hp}/{character.max_hp}")
        
        print(f"\n{ConsoleColors.RED}【{battle_state.team_b.name}】{ConsoleColors.RESET} 剩余角色:")
        for character in battle_state.team_b.characters:
            if character.is_alive:
                print(f"  {character.name} - HP: {character.hp}/{character.max_hp}")
        
        print("\n" + "=" * 60)
    
    def on_round_start(self, battle_state: BattleState) -> None:
        """回合开始事件
        
        Args:
            battle_state: 战斗状态
        """
        print(f"\n{ConsoleColors.YELLOW}===== 第 {battle_state.current_round} 回合开始 ====={ConsoleColors.RESET}")
        self._wait(0.5)
    
    def on_round_end(self, battle_state: BattleState) -> None:
        """回合结束事件
        
        Args:
            battle_state: 战斗状态
        """
        print(f"\n{ConsoleColors.YELLOW}===== 第 {battle_state.current_round} 回合结束 ====={ConsoleColors.RESET}")
        self._wait(0.5)
    
    def on_turn_start(self, character: Character) -> None:
        """角色回合开始事件
        
        Args:
            character: 行动的角色
        """
        game_logger.debug(f"BattleView.on_turn_start called for character: {character.name} (ID: {character.id})")
        self.show_battle_field()
        print(f"\n{ConsoleColors.CYAN}{character.name} 的回合{ConsoleColors.RESET}")
        self._wait(0.3)
    
    def on_turn_end(self, character: Character) -> None:
        """角色回合结束事件
        
        Args:
            character: 行动结束的角色
        """
        print(f"\n{ConsoleColors.CYAN}{character.name} 的回合结束{ConsoleColors.RESET}")
        self._wait(0.3)
    
    def on_turn_skipped(self, character: Character) -> None:
        """角色跳过回合事件
        
        Args:
            character: 跳过回合的角色
        """
        print(f"\n{ConsoleColors.PURPLE}{character.name} 无法行动，跳过回合{ConsoleColors.RESET}")
        self._wait(0.5)
    
    def on_action_executed(self, result: ActionResult) -> None:
        """动作执行事件
        
        Args:
            result: 动作结果
        """
        action = result.action
        character = action.character
        
        if not result.success:
            print(f"\n{ConsoleColors.RED}{result.message}{ConsoleColors.RESET}")
            self._wait()
            return
        
        # 根据动作类型显示不同信息
        if action.action_type == ActionType.ATTACK:
            if result.damage > 0:
                print(f"\n{ConsoleColors.YELLOW}{character.name} 攻击了 {action.target.name}，造成了 {result.damage} 点伤害！{ConsoleColors.RESET}")
            else:
                print(f"\n{ConsoleColors.YELLOW}{character.name} 攻击了 {action.target.name}，但未造成伤害！{ConsoleColors.RESET}")
                
        elif action.action_type == ActionType.SKILL:
            skill_color = ConsoleColors.PURPLE
            print(f"\n{skill_color}{character.name} 使用了 {action.skill.name}！{ConsoleColors.RESET}")
            
            if result.damage > 0:
                print(f"{ConsoleColors.RED}造成了 {result.damage} 点伤害！{ConsoleColors.RESET}")
                
            if result.healing > 0:
                print(f"{ConsoleColors.GREEN}恢复了 {result.healing} 点生命值！{ConsoleColors.RESET}")
                
        elif action.action_type == ActionType.PASS:
            print(f"\n{ConsoleColors.CYAN}{character.name} 跳过了回合{ConsoleColors.RESET}")
        
        self._wait()
    
    def on_character_defeated(self, character: Character) -> None:
        """角色阵亡事件
        
        Args:
            character: 阵亡的角色
        """
        print(f"\n{ConsoleColors.RED}{character.name} 已被击败！{ConsoleColors.RESET}")
        self._wait()
    
    def on_combo_triggered(self, character: Character) -> None:
        """连击触发事件
        
        Args:
            character: 触发连击的角色
        """
        print(f"\n{ConsoleColors.YELLOW}连击！{character.name} 获得了额外的攻击机会！{ConsoleColors.RESET}")
        self._wait(0.5)
    
    def on_status_effect_applied(self, character: Character, effect) -> None:
        """状态效果应用事件
        
        Args:
            character: 受到效果的角色
            effect: 应用的状态效果
        """
        effect_color = ConsoleColors.RED if effect.is_debuff() else ConsoleColors.GREEN
        print(f"\n{effect_color}{character.name} 受到了 {effect.effect_type.name} 效果，持续 {effect.duration} 回合{ConsoleColors.RESET}")
        self._wait(0.3)
    
    def on_status_effect_removed(self, character: Character, effect) -> None:
        """状态效果移除事件
        
        Args:
            character: 效果被移除的角色
            effect: 移除的状态效果
        """
        print(f"\n{ConsoleColors.CYAN}{character.name} 的 {effect.effect_type.name} 效果已结束{ConsoleColors.RESET}")
        self._wait(0.2)
    
    def on_effect_triggered(self, character: Character, effect, value: int) -> None:
        """状态效果触发事件
        
        Args:
            character: 效果触发的角色
            effect: 触发的状态效果
            value: 效果值（如伤害或恢复量）
        """
        if effect.effect_type == StatusEffectType.DOT:
            print(f"\n{ConsoleColors.RED}{character.name} 受到了 {effect.effect_type.name} 效果，损失了 {value} 点生命值{ConsoleColors.RESET}")
        elif effect.effect_type == StatusEffectType.HOT:
            print(f"\n{ConsoleColors.GREEN}{character.name} 受到了 {effect.effect_type.name} 效果，恢复了 {value} 点生命值{ConsoleColors.RESET}")
        self._wait(0.2)
    
    def prompt_for_action(self, character: Character) -> None:
        """提示玩家输入动作
        
        Args:
            character: 当前行动的角色
        """
        print(f"\n{ConsoleColors.CYAN}请为 {character.name} 选择动作 (输入 'help' 查看命令){ConsoleColors.RESET}")
        print("> ", end="", flush=True) 
        
    def subscribe_damage_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """订阅伤害事件
        
        Args:
            callback: 事件回调函数
        """
        
        pass
    
    def subscribe_status_change_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """订阅状态变化事件
        
        Args:
            callback: 事件回调函数
        """
        pass
    
    def subscribe_turn_change_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """订阅回合变化事件
        
        Args:
            callback: 事件回调函数
        """
        pass
    
    def subscribe_chase_trigger_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """订阅追打触发事件
        
        Args:
            callback: 事件回调函数
        """
        pass