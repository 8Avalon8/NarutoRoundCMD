from typing import List, Dict, Optional, Callable, Any, TYPE_CHECKING
from ..models.character import Character
from ..models.action import Action
from ..models.enums import ActionType
from ..models.skill import Skill
from ..models.common_types import CharacterProtocol

# 使用TYPE_CHECKING进行条件导入
if TYPE_CHECKING:
    from ..models.battle_state import BattleState


class InputController:
    """输入控制器，处理玩家输入"""
    
    def __init__(self, battle_state: Any):
        """初始化输入控制器
        
        Args:
            battle_state: 战斗状态
        """
        self.battle_state = battle_state
        self.on_action_selected_callback: Optional[Callable[[Action], None]] = None
        
    def register_action_callback(self, callback: Callable[[Action], None]) -> None:
        """注册动作选择回调函数
        
        Args:
            callback: 当玩家选择动作时调用的函数
        """
        self.on_action_selected_callback = callback
        
    def process_command(self, command: str, character: Character) -> bool:
        """处理玩家输入的命令
        
        Args:
            command: 玩家输入的命令字符串
            character: 当前行动的角色
            
        Returns:
            如果命令有效并已处理返回True，否则返回False
        """
        # 分割命令和参数
        parts = command.strip().split()
        if not parts:
            return False
            
        command_type = parts[0].lower()
        
        # 处理不同类型的命令
        if command_type == "attack" or command_type == "a":
            return self._handle_attack_command(parts, character)
        elif command_type == "skill" or command_type == "s":
            return self._handle_skill_command(parts, character)
        elif command_type == "item" or command_type == "i":
            return self._handle_item_command(parts, character)
        elif command_type == "pass" or command_type == "p":
            return self._handle_pass_command(character)
        elif command_type == "help" or command_type == "h":
            self._show_help()
            return False
        elif command_type == "status" or command_type == "st":
            self._show_battle_status()
            return False
        else:
            print(f"未知命令: {command_type}。输入 'help' 查看可用命令。")
            return False
    
    def _handle_attack_command(self, parts: List[str], character: Character) -> bool:
        """处理攻击命令
        
        Args:
            parts: 命令拆分后的部分
            character: 当前行动的角色
            
        Returns:
            如果命令处理成功返回True
        """
        # 判断角色所在队伍
        own_team = self.battle_state.team_a if character in self.battle_state.team_a.characters else self.battle_state.team_b
        enemy_team = self.battle_state.team_b if own_team == self.battle_state.team_a else self.battle_state.team_a
        
        # 获取敌方存活角色
        alive_enemies = [c for c in enemy_team.characters if c.is_alive]
        
        if not alive_enemies:
            print("没有可攻击的目标！")
            return False
        
        target_idx = 0
        # 如果指定了目标索引
        if len(parts) > 1:
            try:
                target_idx = int(parts[1]) - 1  # 转为0-based索引
                if target_idx < 0 or target_idx >= len(alive_enemies):
                    print(f"无效的目标索引: {target_idx + 1}")
                    self._show_enemy_targets(alive_enemies)
                    return False
            except ValueError:
                print(f"无效的目标索引: {parts[1]}")
                self._show_enemy_targets(alive_enemies)
                return False
        else:
            # 如果没有指定目标，显示可用目标
            if len(alive_enemies) > 1:
                self._show_enemy_targets(alive_enemies)
                return False
        
        target = alive_enemies[target_idx]
        
        # 创建攻击动作
        action = Action(character, ActionType.ATTACK, target, None)
        
        # 通知回调
        if self.on_action_selected_callback:
            self.on_action_selected_callback(action)
        
        return True
    
    def _handle_skill_command(self, parts: List[str], character: Character) -> bool:
        """处理技能命令
        
        Args:
            parts: 命令拆分后的部分
            character: 当前行动的角色
            
        Returns:
            如果命令处理成功返回True
        """
        # 显示角色的技能
        skills = character.skills
        
        if not skills:
            print(f"{character.name}没有可用的技能！")
            return False
        
        # 如果只是输入了"skill"，显示技能列表
        if len(parts) == 1:
            self._show_character_skills(character)
            return False
        
        # 解析技能索引
        try:
            skill_idx = int(parts[1]) - 1  # 转为0-based索引
            if skill_idx < 0 or skill_idx >= len(skills):
                print(f"无效的技能索引: {skill_idx + 1}")
                self._show_character_skills(character)
                return False
        except ValueError:
            print(f"无效的技能索引: {parts[1]}")
            self._show_character_skills(character)
            return False
        
        skill = skills[skill_idx]
        
        # 检查查克拉是否足够
        if character.chakra < skill.cost:
            print(f"查克拉不足！{skill.name}需要{skill.cost}点查克拉，但{character.name}只有{character.chakra}点。")
            return False
        
        # 判断目标类型
        target_type = skill.target_type
        
        # 判断角色所在队伍
        own_team = self.battle_state.team_a if character in self.battle_state.team_a.characters else self.battle_state.team_b
        enemy_team = self.battle_state.team_b if own_team == self.battle_state.team_a else self.battle_state.team_a
        
        # 根据技能目标类型确定可选目标
        if target_type.name == "SELF":
            target = character
        elif target_type.name == "SINGLE":
            # 获取敌方存活角色
            alive_enemies = [c for c in enemy_team.characters if c.is_alive]
            
            if not alive_enemies:
                print("没有可攻击的目标！")
                return False
            
            # 如果没有指定目标或目标无效
            if len(parts) <= 2:
                self._show_enemy_targets(alive_enemies)
                print(f"请为{skill.name}技能选择一个目标: skill {skill_idx + 1} <目标ID>")
                return False
            
            try:
                target_idx = int(parts[2]) - 1  # 转为0-based索引
                if target_idx < 0 or target_idx >= len(alive_enemies):
                    print(f"无效的目标索引: {target_idx + 1}")
                    self._show_enemy_targets(alive_enemies)
                    return False
                
                target = alive_enemies[target_idx]
            except ValueError:
                print(f"无效的目标索引: {parts[2]}")
                self._show_enemy_targets(alive_enemies)
                return False
        elif target_type.name == "ALLY":
            # 获取友方存活角色
            alive_allies = [c for c in own_team.characters if c.is_alive]
            
            if not alive_allies:
                print("没有可选择的友方目标！")
                return False
            
            # 如果没有指定目标或目标无效
            if len(parts) <= 2:
                self._show_ally_targets(alive_allies)
                print(f"请为{skill.name}技能选择一个友方目标: skill {skill_idx + 1} <目标ID>")
                return False
            
            try:
                target_idx = int(parts[2]) - 1  # 转为0-based索引
                if target_idx < 0 or target_idx >= len(alive_allies):
                    print(f"无效的目标索引: {target_idx + 1}")
                    self._show_ally_targets(alive_allies)
                    return False
                
                target = alive_allies[target_idx]
            except ValueError:
                print(f"无效的目标索引: {parts[2]}")
                self._show_ally_targets(alive_allies)
                return False
        elif target_type.name in ["ALL_ALLIES", "ALL_ENEMIES", "RANDOM_ENEMY"]:
            # 群体技能或随机目标技能不需要指定目标
            if target_type.name == "ALL_ALLIES":
                # 随便选一个友方角色作为名义上的目标
                target = character
            else:
                # 随便选一个敌人作为名义上的目标
                alive_enemies = [c for c in enemy_team.characters if c.is_alive]
                if not alive_enemies:
                    print("没有可攻击的目标！")
                    return False
                target = alive_enemies[0]
        else:
            print(f"未知的技能目标类型: {target_type}")
            return False
        
        # 创建技能动作
        action = Action(character, ActionType.SKILL, target, skill)
        
        # 通知回调
        if self.on_action_selected_callback:
            self.on_action_selected_callback(action)
        
        return True
    
    def _handle_item_command(self, parts: List[str], character: Character) -> bool:
        """处理道具命令
        
        Args:
            parts: 命令拆分后的部分
            character: 当前行动的角色
            
        Returns:
            如果命令处理成功返回True
        """
        # 道具系统尚未实现
        print("道具系统尚未实现。")
        return False
    
    def _handle_pass_command(self, character: Character) -> bool:
        """处理跳过回合命令
        
        Args:
            character: 当前行动的角色
            
        Returns:
            如果命令处理成功返回True
        """
        # 创建跳过动作
        action = Action(character, ActionType.PASS, None, None)
        
        # 通知回调
        if self.on_action_selected_callback:
            self.on_action_selected_callback(action)
        
        return True
    
    def _show_help(self) -> None:
        """显示帮助信息"""
        print("可用命令:")
        print("  attack/a [目标ID] - 对指定目标进行普通攻击")
        print("  skill/s [技能ID] [目标ID] - 使用指定技能攻击指定目标")
        print("  item/i [道具ID] [目标ID] - 使用指定道具（尚未实现）")
        print("  pass/p - 跳过当前回合")
        print("  status/st - 显示战斗状态")
        print("  help/h - 显示此帮助信息")
    
    def _show_battle_status(self) -> None:
        """显示战斗状态"""
        print("\n===== 战斗状态 =====")
        print(f"当前回合: {self.battle_state.current_round}")
        
        # 显示队伍A的状态
        print(f"\n队伍 {self.battle_state.team_a.name}:")
        for i, character in enumerate(self.battle_state.team_a.characters):
            status = "存活" if character.is_alive else "阵亡"
            print(f"  {i+1}. {character.name} - HP: {character.hp}/{character.max_hp} CP: {character.chakra}/{character.max_chakra} ({status})")
            if character.status_effects:
                effect_texts = [f"{effect.effect_type.name}({effect.duration}回合)" for effect in character.status_effects]
                print(f"     状态: {', '.join(effect_texts)}")
        
        # 显示队伍B的状态
        print(f"\n队伍 {self.battle_state.team_b.name}:")
        for i, character in enumerate(self.battle_state.team_b.characters):
            status = "存活" if character.is_alive else "阵亡"
            print(f"  {i+1}. {character.name} - HP: {character.hp}/{character.max_hp} CP: {character.chakra}/{character.max_chakra} ({status})")
            if character.status_effects:
                effect_texts = [f"{effect.effect_type.name}({effect.duration}回合)" for effect in character.status_effects]
                print(f"     状态: {', '.join(effect_texts)}")
        
        print("\n===================")
    
    def _show_character_skills(self, character: Character) -> None:
        """显示角色的技能列表
        
        Args:
            character: 要显示技能的角色
        """
        print(f"\n{character.name}的技能列表:")
        for i, skill in enumerate(character.skills):
            cost_str = f"CP: {skill.cost}"
            print(f"  {i+1}. {skill.name} [{cost_str}] - {skill.description} (目标: {skill.target_type.name})")
        print("\n使用方式: skill <技能ID> [目标ID]")
    
    def _show_enemy_targets(self, enemies: List[Character]) -> None:
        """显示敌方目标列表
        
        Args:
            enemies: 敌方角色列表
        """
        print("\n可选的敌方目标:")
        for i, enemy in enumerate(enemies):
            print(f"  {i+1}. {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}")
    
    def _show_ally_targets(self, allies: List[Character]) -> None:
        """显示友方目标列表
        
        Args:
            allies: 友方角色列表
        """
        print("\n可选的友方目标:")
        for i, ally in enumerate(allies):
            print(f"  {i+1}. {ally.name} - HP: {ally.hp}/{ally.max_hp}") 