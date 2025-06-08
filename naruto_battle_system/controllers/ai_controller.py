from typing import List, Dict, Optional
import random
from ..models.character import Character
from ..models.battle_state import BattleState
from ..models.action import Action
from ..models.enums import ActionType, SkillType


class AIController:
    """AI控制器，用于控制AI角色的战斗决策"""
    
    def __init__(self, battle_state: BattleState):
        """初始化AI控制器
        
        Args:
            battle_state: 战斗状态
        """
        self.battle_state = battle_state
    
    def get_action(self, character: Character) -> Action:
        """获取AI角色的动作
        
        Args:
            character: AI控制的角色
            
        Returns:
            生成的动作
        """
        # 判断角色所在队伍
        own_team = self.battle_state.team_a if character in self.battle_state.team_a.characters else self.battle_state.team_b
        enemy_team = self.battle_state.team_b if own_team == self.battle_state.team_a else self.battle_state.team_a
        
        # 获取敌方存活角色
        alive_enemies = [c for c in enemy_team.characters if c.is_alive]
        # 获取友方存活角色
        alive_allies = [c for c in own_team.characters if c.is_alive and c != character]
        
        # 如果没有存活的敌人，角色只能跳过回合
        if not alive_enemies:
            return Action(character, ActionType.PASS, None, None)
        
        # 判断当前状态
        team_health_percentage = sum(c.hp for c in own_team.characters if c.is_alive) / sum(c.max_hp for c in own_team.characters if c.is_alive)
        
        # 紧急治疗逻辑：如果有队友HP低于20%且自己有治疗技能
        critical_allies = [c for c in alive_allies if c.hp / c.max_hp < 0.2]
        healing_skills = [s for s in character.skills if s.skill_type == SkillType.HEALING and s.cost <= character.chakra]
        
        if critical_allies and healing_skills:
            # 选择HP最低的队友进行治疗
            target = min(critical_allies, key=lambda c: c.hp / c.max_hp)
            # 选择最强的治疗技能
            skill = max(healing_skills, key=lambda s: s.get_power_rating())
            return Action(character, ActionType.SKILL, target, skill)
        
        # 群体技能逻辑：如果敌人至少有2个，且有群体攻击技能，则有一定几率使用
        aoe_skills = [s for s in character.skills if s.target_type.value.startswith("ALL_") and s.cost <= character.chakra]
        if len(alive_enemies) >= 2 and aoe_skills and random.random() < 0.7:
            skill = random.choice(aoe_skills)
            # 群体技能通常不需要选择特定目标
            return Action(character, ActionType.SKILL, alive_enemies[0], skill)
        
        # 增益技能逻辑：当队伍健康状况良好时，有一定几率使用增益技能
        if team_health_percentage > 0.6:
            buff_skills = [s for s in character.skills if s.skill_type == SkillType.BUFF and s.cost <= character.chakra]
            if buff_skills and random.random() < 0.4:
                skill = random.choice(buff_skills)
                if skill.target_type.name == "SELF":
                    return Action(character, ActionType.SKILL, character, skill)
                else:
                    # 为友方选择一个随机目标
                    targets = alive_allies if alive_allies else [character]
                    target = random.choice(targets)
                    return Action(character, ActionType.SKILL, target, skill)
        
        # 攻击技能逻辑
        attack_skills = [s for s in character.skills if s.skill_type in [SkillType.DAMAGE, SkillType.DEBUFF] and s.cost <= character.chakra]
        
        # 有50%的概率使用攻击技能，如果有的话
        if attack_skills and random.random() < 0.5:
            skill = self._select_best_attack_skill(character, attack_skills, alive_enemies)
            # 选择最佳目标
            target = self._select_best_target(character, skill, alive_enemies)
            return Action(character, ActionType.SKILL, target, skill)
        
        # 默认使用普通攻击
        # 选择最佳目标
        target = self._select_attack_target(character, alive_enemies)
        return Action(character, ActionType.ATTACK, target, None)
    
    def _select_best_attack_skill(self, character: Character, skills: List, enemies: List[Character]) -> Optional:
        """选择最佳攻击技能
        
        Args:
            character: AI角色
            skills: 可用的攻击技能列表
            enemies: 敌人列表
            
        Returns:
            选择的技能
        """
        # 简单策略：如果敌人很多且有群体技能，优先使用群体技能
        if len(enemies) >= 3:
            aoe_skills = [s for s in skills if s.target_type.name in ["ALL_ENEMIES", "RANDOM_ENEMIES"]]
            if aoe_skills:
                return max(aoe_skills, key=lambda s: s.get_power_rating())
        
        # 否则优先选择单体伤害最高的技能
        single_target_skills = [s for s in skills if s.target_type.name == "SINGLE"]
        if single_target_skills:
            return max(single_target_skills, key=lambda s: s.get_power_rating())
        
        # 如果上述都没有，随机选择一个技能
        return random.choice(skills)
    
    def _select_best_target(self, character: Character, skill, enemies: List[Character]) -> Character:
        """为技能选择最佳目标
        
        Args:
            character: AI角色
            skill: 要使用的技能
            enemies: 敌人列表
            
        Returns:
            选择的目标
        """
        from ..models.skill import DamageEffect, DebuffEffect
        
        # 如果是群体技能，目标不重要
        if skill.target_type.name in ["ALL_ENEMIES", "RANDOM_ENEMIES"]:
            return enemies[0]
        
        # 根据技能类型选择不同的目标
        has_damage = any(isinstance(e, DamageEffect) for e in skill.effects)
        has_debuff = any(isinstance(e, DebuffEffect) for e in skill.effects)
        
        if has_damage and not has_debuff:
            # 纯伤害技能，优先选择血量最低的敌人
            return min(enemies, key=lambda e: e.hp)
        elif has_debuff and not has_damage:
            # 纯减益技能，优先选择血量最高的敌人
            return max(enemies, key=lambda e: e.hp)
        else:
            # 混合技能，随机选择一个敌人
            return random.choice(enemies)
    
    def _select_attack_target(self, character: Character, enemies: List[Character]) -> Character:
        """为普通攻击选择最佳目标
        
        Args:
            character: AI角色
            enemies: 敌人列表
            
        Returns:
            选择的目标
        """
        # 简单策略：80%的几率选择血量最低的敌人，20%的几率随机选择
        if random.random() < 0.8:
            return min(enemies, key=lambda e: e.hp)
        else:
            return random.choice(enemies) 