from typing import List, Dict, Optional, Tuple
import random
from ..interfaces.battle_interfaces import IBattleController, IBattleEvents, IAction
from ..models.character import Character
from ..models.battle_state import BattleState, BattleSession
from ..models.battle_team import BattleTeam
from ..models.action import Action, ActionResult
from ..models.enums import ActionType, TargetType, StatusEffectType
from ..models.status_effect import StatusEffect
from ..models.skill import Skill


class BattleController(IBattleController):
    """战斗控制器，实现战斗逻辑"""
    
    def __init__(self, battle_state: BattleState, events: IBattleEvents):
        """初始化战斗控制器
        
        Args:
            battle_state: 战斗状态
            events: 战斗事件接口
        """
        self.battle_state = battle_state
        self.events = events
        self._action_queue = []
    
    # 实现抽象方法，用于测试
    def start_battle(self, team1: Optional[BattleTeam] = None, team2: Optional[BattleTeam] = None) -> Optional[BattleSession]:
        """开始战斗"""
        self.events.on_battle_start(self.battle_state)
        self._prepare_new_round()
        return None
    
    def get_available_actions(self, character_id: str) -> List[IAction]:
        """获取可用动作列表"""
        # 简化实现，仅用于测试
        return []
    
    def get_battle_state(self) -> BattleState:
        """获取当前战斗状态"""
        # 简化实现，仅用于测试
        return self.battle_state
    
    def is_battle_ended(self) -> bool:
        """检查战斗是否结束"""
        # 委托给is_battle_over方法
        return self.is_battle_over()
    
    def _prepare_new_round(self) -> None:
        """准备新回合"""
        self.battle_state.current_round += 1
        self.battle_state.reset_round_data()
        
        # 应用回合开始时的效果
        for team in [self.battle_state.team_a, self.battle_state.team_b]:
            for character in team.characters:
                if not character.is_alive:
                    continue
                    
                # 回复查克拉
                character.chakra = min(character.chakra + character.chakra_regen, character.max_chakra)
                
                # 处理状态效果
                self._process_turn_based_effects(character)
        
        self.events.on_round_start(self.battle_state)
        
        # 计算行动顺序
        self._calculate_turn_order()
        
    def _calculate_turn_order(self) -> None:
        """计算行动顺序"""
        all_characters = []
        
        # 收集所有活着的角色
        for team in [self.battle_state.team_a, self.battle_state.team_b]:
            for character in team.characters:
                if character.is_alive:
                    all_characters.append(character)
        
        # 根据速度和随机因素排序
        random.shuffle(all_characters)  # 先随机打乱以处理速度相同的情况
        all_characters.sort(key=lambda c: c.speed, reverse=True)
        
        self.battle_state.turn_order = all_characters
        self.battle_state.current_character_index = 0
        
        if all_characters:
            self.events.on_turn_start(all_characters[0])
    
    def _process_turn_based_effects(self, character: Character) -> None:
        """处理回合制状态效果
        
        Args:
            character: 需要处理状态效果的角色
        """
        effects_to_remove = []
        
        for effect in character.status_effects:
            # 减少持续时间
            if effect.duration > 0:
                effect.duration -= 1
            
            # 应用效果
            if effect.effect_type == StatusEffectType.DOT:
                damage = effect.value
                character.hp = max(0, character.hp - damage)
                self.events.on_effect_triggered(character, effect, damage)
                
            elif effect.effect_type == StatusEffectType.HOT:
                healing = effect.value
                character.hp = min(character.max_hp, character.hp + healing)
                self.events.on_effect_triggered(character, effect, healing)
            
            # 标记已过期的效果
            if effect.duration == 0:
                effects_to_remove.append(effect)
        
        # 移除过期的效果
        for effect in effects_to_remove:
            character.status_effects.remove(effect)
            self.events.on_status_effect_removed(character, effect)
    
    def process_turn(self) -> bool:
        """处理当前角色的回合，返回战斗是否结束"""
        if self.is_battle_over():
            self.events.on_battle_end(self.battle_state)
            return True
            
        current_character = self.get_current_character()
        if not current_character:
            self._prepare_new_round()
            return self.process_turn()
        
        # 如果角色无法行动（如被眩晕），跳过回合
        if self._is_character_disabled(current_character):
            self.events.on_turn_skipped(current_character)
            return self.next_turn()
            
        # 如果是AI控制的角色，生成AI动作
        if not current_character.is_player_controlled:
            action = self._generate_ai_action(current_character)
            return self.execute_action(action)
            
        # 等待玩家输入，此时不推进回合
        return False
    
    def _is_character_disabled(self, character: Character) -> bool:
        """判断角色是否无法行动
        
        Args:
            character: 要检查的角色
            
        Returns:
            如果角色无法行动返回True
        """
        for effect in character.status_effects:
            if effect.effect_type in [StatusEffectType.STUN, StatusEffectType.FREEZE]:
                return True
        return False
    
    def _generate_ai_action(self, character: Character) -> Action:
        """为AI角色生成动作
        
        Args:
            character: AI控制的角色
            
        Returns:
            生成的动作
        """
        # 简单的AI逻辑：优先使用技能，如果没有可用的技能则普通攻击
        enemy_team = self.battle_state.team_a if character in self.battle_state.team_b.characters else self.battle_state.team_b
        
        # 查找敌人中HP最低的作为目标
        targets = [c for c in enemy_team.characters if c.is_alive]
        if not targets:
            return Action(character, ActionType.PASS, None, None)
            
        target = min(targets, key=lambda c: c.hp)
        
        # 尝试使用技能
        available_skills = [skill for skill in character.skills if skill.cost <= character.chakra]
        if available_skills:
            skill = random.choice(available_skills)
            return Action(character, ActionType.SKILL, target, skill)
        
        # 如果没有可用技能，使用普通攻击
        return Action(character, ActionType.ATTACK, target, None)
    
    def execute_action(self, action: Action) -> bool:
        """执行动作
        
        Args:
            action: 要执行的动作
            
        Returns:
            战斗是否结束
        """
        result = ActionResult(action)
        
        if action.action_type == ActionType.ATTACK:
            self._execute_attack(action, result)
        elif action.action_type == ActionType.SKILL:
            self._execute_skill(action, result)
        elif action.action_type == ActionType.ITEM:
            self._execute_item(action, result)
        elif action.action_type == ActionType.PASS:
            result.success = True
            
        # 触发动作完成事件
        self.events.on_action_executed(result)
        
        # 检查任何一方是否全部阵亡
        if self.is_battle_over():
            self.events.on_battle_end(self.battle_state)
            return True
            
        # 添加可能的连击动作到队列
        self._process_combo_actions(action, result)
        
        # 如果有连击队列，处理连击
        if self._action_queue:
            next_action = self._action_queue.pop(0)
            return self.execute_action(next_action)
            
        # 进入下一个角色的回合
        return self.next_turn()
    
    def _execute_attack(self, action: Action, result: ActionResult) -> None:
        """执行攻击动作
        
        Args:
            action: 攻击动作
            result: 动作结果
        """
        attacker = action.character
        target = action.target
        
        if not target or not target.is_alive:
            result.success = False
            result.add_message(f"{attacker.name}的攻击没有有效目标")
            return
            
        # 计算伤害
        base_damage = attacker.attack - target.defense // 2
        damage = max(1, base_damage)  # 至少造成1点伤害
        
        # 应用伤害
        actual_damage = target.take_damage(damage)
        
        # 记录结果
        result.success = True
        result.add_message(f"{attacker.name}攻击了{target.name}，造成了{actual_damage}点伤害")
        
        # 检查目标是否死亡
        if not target.is_alive:
            result.add_message(f"{target.name}被击败了")
    
    def _execute_skill(self, action: Action, result: ActionResult) -> None:
        """执行技能动作
        
        Args:
            action: 技能动作
            result: 动作结果
        """
        caster = action.character
        skill = action.skill
        target = action.target
        
        if not skill:
            result.success = False
            result.add_message(f"{caster.name}尝试使用技能，但没有指定技能")
            return
            
        if not target or not target.is_alive:
            result.success = False
            result.add_message(f"{caster.name}的{skill.name}没有有效目标")
            return
            
        # 消耗查克拉 (优先使用skill.cost，兼容测试)
        cost = skill.cost if hasattr(skill, 'cost') and skill.cost > 0 else skill.chakra_cost
        if cost > 0:
            caster.chakra = max(0, caster.chakra - cost)
            
        # 应用技能效果
        for effect in skill.effects:
            self._apply_skill_effect(caster, target, effect, result)
            
        # 记录结果
        result.success = True
        result.add_message(f"{caster.name}对{target.name}使用了{skill.name}")
    
    def _execute_item(self, action: Action, result: ActionResult) -> None:
        """执行道具使用
        
        Args:
            action: 道具动作
            result: 动作结果
        """
        # 道具系统尚未实现
        result.success = False
        result.message = "道具系统尚未实现"
    
    def _get_skill_targets(self, action: Action) -> List[Character]:
        """获取技能的目标列表
        
        Args:
            action: 技能动作
            
        Returns:
            技能影响的目标列表
        """
        skill = action.skill
        character = action.character
        
        # 确定角色所在队伍和敌对队伍
        own_team = self.battle_state.team_a if character in self.battle_state.team_a.characters else self.battle_state.team_b
        enemy_team = self.battle_state.team_b if own_team == self.battle_state.team_a else self.battle_state.team_a
        
        targets = []
        
        if skill.target_type == TargetType.SINGLE:
            if action.target and action.target.is_alive:
                targets = [action.target]
                
        elif skill.target_type == TargetType.ALL_ALLIES:
            targets = [c for c in own_team.characters if c.is_alive]
            
        elif skill.target_type == TargetType.ALL_ENEMIES:
            targets = [c for c in enemy_team.characters if c.is_alive]
            
        elif skill.target_type == TargetType.SELF:
            targets = [character]
            
        elif skill.target_type == TargetType.RANDOM_ENEMY:
            alive_enemies = [c for c in enemy_team.characters if c.is_alive]
            if alive_enemies:
                targets = [random.choice(alive_enemies)]
        
        return targets
    
    def _apply_skill_effect(self, caster: Character, target: Character, effect, result: ActionResult) -> None:
        """应用技能效果
        
        Args:
            caster: 施法者
            target: 目标
            effect: 效果
            result: 动作结果
        """
        from ..models.skill import DamageEffect, HealingEffect
        
        if isinstance(effect, DamageEffect):
            # 计算伤害
            damage = effect.calculate_damage(caster.attack)
            
            # 应用伤害
            actual_damage = target.take_damage(damage)
            
            # 记录结果
            result.add_message(f"{caster.name}的技能对{target.name}造成了{actual_damage}点伤害")
            
            # 检查目标是否死亡
            if not target.is_alive:
                result.add_message(f"{target.name}被击败了")
                
        elif isinstance(effect, HealingEffect):
            # 计算治疗量
            healing = effect.calculate_healing(caster.attack)
            
            # 应用治疗
            actual_healing = target.heal(healing)
            
            # 记录结果
            result.add_message(f"{caster.name}的技能为{target.name}恢复了{actual_healing}点生命值")
    
    def _process_combo_actions(self, action: Action, result: ActionResult) -> None:
        """处理连击动作
        
        Args:
            action: 触发连击的动作
            result: 动作结果
        """
        # 简化实现，仅用于测试
        pass
    
    def next_turn(self) -> bool:
        """进入下一个角色的回合，返回战斗是否结束"""
        if self.is_battle_over():
            self.events.on_battle_end(self.battle_state)
            return True
            
        # 结束当前角色的回合
        current_character = self.get_current_character()
        if current_character:
            self.events.on_turn_end(current_character)
        
        # 移动到下一个角色
        self.battle_state.current_character_index += 1
        
        # 如果已经处理完本回合所有角色，开始新回合
        if self.battle_state.current_character_index >= len(self.battle_state.turn_order):
            self._prepare_new_round()
            return False
            
        # 获取下一个行动的角色
        next_character = self.get_current_character()
        if next_character:
            self.events.on_turn_start(next_character)
            
        return False
    
    def get_current_character(self) -> Optional[Character]:
        """获取当前行动的角色"""
        if (self.battle_state.current_character_index < 0 or 
            self.battle_state.current_character_index >= len(self.battle_state.turn_order)):
            return None
            
        return self.battle_state.turn_order[self.battle_state.current_character_index]
    
    def is_battle_over(self) -> bool:
        """判断战斗是否结束"""
        team_a_alive = any(c.is_alive for c in self.battle_state.team_a.characters)
        team_b_alive = any(c.is_alive for c in self.battle_state.team_b.characters)
        
        return not (team_a_alive and team_b_alive)
    
    def get_winning_team(self) -> Optional[BattleTeam]:
        """获取获胜的队伍，如果战斗未结束返回None"""
        if not self.is_battle_over():
            return None
            
        team_a_alive = any(c.is_alive for c in self.battle_state.team_a.characters)
        if team_a_alive:
            return self.battle_state.team_a
        else:
            return self.battle_state.team_b 