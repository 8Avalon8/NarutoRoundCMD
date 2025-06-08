"""
数据存储库
提供对游戏数据的访问接口和实现
"""
import json
import os
from typing import Dict, List, Optional, TypeVar, Generic, Type
from ..interfaces.battle_interfaces import IRepository
from ..models.character import Character
from ..models.skill import Skill, SkillEffect
from ..models.status_effect import InstantEffect, PeriodicEffect, StatModifier, StatusEffectDefinition
from ..models.enums import *

T = TypeVar('T')

class JsonRepository(Generic[T]):
    """JSON数据存储库基类"""
    
    def __init__(self, data_file: str, model_class: Type[T]):
        """
        初始化存储库
        
        Args:
            data_file: 数据文件路径
            model_class: 模型类
        """
        self.data_file = data_file
        self.model_class = model_class
        self.entities: Dict[str, T] = {}
        self.load_data()
        
    def load_data(self) -> None:
        """从文件加载数据"""
        if not os.path.exists(self.data_file):
            self.entities = {}
            return
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    entity = self._create_entity_from_dict(item)
                    if entity:
                        self.entities[getattr(entity, 'id')] = entity
        except Exception as e:
            print(f"加载数据时出错: {str(e)}")
            self.entities = {}
            
    def save_data(self) -> None:
        """保存数据到文件"""
        data = []
        for entity in self.entities.values():
            data.append(self._convert_entity_to_dict(entity))
            
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def _create_entity_from_dict(self, data: Dict) -> Optional[T]:
        """
        从字典创建实体对象，子类需要重写此方法
        
        Args:
            data: 实体数据字典
            
        Returns:
            创建的实体对象，如果创建失败则为None
        """
        raise NotImplementedError("子类必须实现此方法")
        
    def _convert_entity_to_dict(self, entity: T) -> Dict:
        """
        将实体对象转换为字典，子类需要重写此方法
        
        Args:
            entity: 实体对象
            
        Returns:
            转换后的字典
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def get(self, id: str) -> Optional[T]:
        """
        获取指定ID的实体
        
        Args:
            id: 实体ID
            
        Returns:
            实体对象，如果不存在则为None
        """
        return self.entities.get(id)
        
    def add(self, entity: T) -> None:
        """
        添加实体
        
        Args:
            entity: 要添加的实体
        """
        self.entities[getattr(entity, 'id')] = entity
        self.save_data()
        
    def update(self, entity: T) -> None:
        """
        更新实体
        
        Args:
            entity: 要更新的实体
        """
        if getattr(entity, 'id') in self.entities:
            self.entities[getattr(entity, 'id')] = entity
            self.save_data()
        
    def remove(self, id: str) -> bool:
        """
        移除实体
        
        Args:
            id: 要移除的实体ID
            
        Returns:
            是否成功移除
        """
        if id in self.entities:
            del self.entities[id]
            self.save_data()
            return True
        return False
        
    def get_all(self) -> List[T]:
        """
        获取所有实体
        
        Returns:
            所有实体的列表
        """
        return list(self.entities.values())

class CharacterRepository(JsonRepository[Character], IRepository[Character]):
    """角色数据存储库"""
    
    def __init__(self, data_file: str = 'data/characters.json'):
        """
        初始化角色存储库
        
        Args:
            data_file: 数据文件路径
        """
        super().__init__(data_file, Character)
        
    def _create_entity_from_dict(self, data: Dict) -> Optional[Character]:
        """
        从字典创建角色对象
        
        Args:
            data: 角色数据字典
            
        Returns:
            创建的角色对象，如果创建失败则为None
        """
        try:
            return Character(
                id=data['id'],
                name=data['name'],
                max_hp=data['max_hp'],
                current_hp=data['current_hp'],
                attack=data['attack'],
                defense=data['defense'],
                ninja_tech=data['ninja_tech'],
                resistance=data['resistance'],
                speed=data['speed'],
                crit_rate=data['crit_rate'],
                crit_damage_bonus=data['crit_damage_bonus'],
                position=data['position'],
                normal_attack_id=data['normal_attack_id'],
                mystery_art_id=data['mystery_art_id'],
                chase_skill_ids=data.get('chase_skill_ids', []),
                passive_skill_ids=data.get('passive_skill_ids', []),
                tags=data.get('tags', []),
                is_alive=data.get('is_alive', True),
                can_act=data.get('can_act', True),
                is_summon=data.get('is_summon', False),
                summoner_id=data.get('summoner_id')
            )
        except Exception as e:
            print(f"创建角色时出错: {str(e)}")
            return None
            
    def _convert_entity_to_dict(self, entity: Character) -> Dict:
        """
        将角色对象转换为字典
        
        Args:
            entity: 角色对象
            
        Returns:
            转换后的字典
        """
        return {
            'id': entity.id,
            'name': entity.name,
            'max_hp': entity.max_hp,
            'current_hp': entity.current_hp,
            'attack': entity.attack,
            'defense': entity.defense,
            'ninja_tech': entity.ninja_tech,
            'resistance': entity.resistance,
            'speed': entity.speed,
            'crit_rate': entity.crit_rate,
            'crit_damage_bonus': entity.crit_damage_bonus,
            'position': entity.position,
            'normal_attack_id': entity.normal_attack_id,
            'mystery_art_id': entity.mystery_art_id,
            'chase_skill_ids': entity.chase_skill_ids,
            'passive_skill_ids': entity.passive_skill_ids,
            'tags': entity.tags,
            'is_alive': entity.is_alive,
            'can_act': entity.can_act,
            'is_summon': entity.is_summon,
            'summoner_id': entity.summoner_id
        }

class SkillRepository(JsonRepository[Skill], IRepository[Skill]):
    """技能数据存储库"""
    
    def __init__(self, data_file: str = 'data/skills.json'):
        """
        初始化技能存储库
        
        Args:
            data_file: 数据文件路径
        """
        super().__init__(data_file, Skill)
        
    def _create_entity_from_dict(self, data: Dict) -> Optional[Skill]:
        """
        从字典创建技能对象
        
        Args:
            data: 技能数据字典
            
        Returns:
            创建的技能对象，如果创建失败则为None
        """
        try:
            effects = []
            for effect_data in data.get('effects', []):
                effect = SkillEffect(
                    effect_type=EffectType[effect_data['effect_type']],
                    value_formula=effect_data['value_formula'],
                    status_id_to_apply=effect_data.get('status_id_to_apply'),
                    apply_chance=effect_data.get('apply_chance', 1.0),
                    remove_status_type=RemoveStatusType[effect_data['remove_status_type']] if effect_data.get('remove_status_type') else None,
                    specific_status_id=effect_data.get('specific_status_id'),
                    chakra_change_amount=effect_data.get('chakra_change_amount', 0),
                    summon_character_id=effect_data.get('summon_character_id')
                )
                effects.append(effect)
                
            return Skill(
                id=data['id'],
                name=data['name'],
                type=SkillType[data['type']],
                description=data['description'],
                chakra_cost=data.get('chakra_cost', 0),
                cooldown_turns=data.get('cooldown_turns', 0),
                current_cooldown=data.get('current_cooldown', 0),
                target_type=TargetType[data['target_type']],
                target_count=data.get('target_count', 1),
                effects=effects,
                causes_chase_state=ChaseState[data.get('causes_chase_state', 'NONE')],
                requires_chase_state=ChaseState[data.get('requires_chase_state', 'NONE')],
                chase_priority=data.get('chase_priority', 0),
                is_interruptible=data.get('is_interruptible', True),
                is_instant=data.get('is_instant', False)
            )
        except Exception as e:
            print(f"创建技能时出错: {str(e)}")
            return None
            
    def _convert_entity_to_dict(self, entity: Skill) -> Dict:
        """
        将技能对象转换为字典
        
        Args:
            entity: 技能对象
            
        Returns:
            转换后的字典
        """
        effects = []
        for effect in entity.effects:
            effect_dict = {
                'effect_type': effect.effect_type.name,
                'value_formula': effect.value_formula
            }
            
            if effect.status_id_to_apply:
                effect_dict['status_id_to_apply'] = effect.status_id_to_apply
                
            if effect.apply_chance != 1.0:
                effect_dict['apply_chance'] = effect.apply_chance
                
            if effect.remove_status_type:
                effect_dict['remove_status_type'] = effect.remove_status_type.name
                
            if effect.specific_status_id:
                effect_dict['specific_status_id'] = effect.specific_status_id
                
            if effect.chakra_change_amount != 0:
                effect_dict['chakra_change_amount'] = effect.chakra_change_amount
                
            if effect.summon_character_id:
                effect_dict['summon_character_id'] = effect.summon_character_id
                
            effects.append(effect_dict)
            
        return {
            'id': entity.id,
            'name': entity.name,
            'type': entity.type.name,
            'description': entity.description,
            'chakra_cost': entity.chakra_cost,
            'cooldown_turns': entity.cooldown_turns,
            'current_cooldown': entity.current_cooldown,
            'target_type': entity.target_type.name,
            'target_count': entity.target_count,
            'effects': effects,
            'causes_chase_state': entity.causes_chase_state.name,
            'requires_chase_state': entity.requires_chase_state.name,
            'chase_priority': entity.chase_priority,
            'is_interruptible': entity.is_interruptible,
            'is_instant': entity.is_instant
        }

class StatusEffectRepository(JsonRepository[StatusEffectDefinition], IRepository[StatusEffectDefinition]):
    """状态效果数据存储库"""
    
    def __init__(self, data_file: str = 'data/status_effects.json'):
        """
        初始化状态效果存储库
        
        Args:
            data_file: 数据文件路径
        """
        super().__init__(data_file, StatusEffectDefinition)
        
    def _create_entity_from_dict(self, data: Dict) -> Optional[StatusEffectDefinition]:
        """
        从字典创建状态效果对象
        
        Args:
            data: 状态效果数据字典
            
        Returns:
            创建的状态效果对象，如果创建失败则为None
        """
        try:
            # 创建即时效果列表
            on_apply_effects = []
            for effect_data in data.get('on_apply_effects', []):
                effect = self._create_instant_effect_from_dict(effect_data)
                on_apply_effects.append(effect)
                
            on_remove_effects = []
            for effect_data in data.get('on_remove_effects', []):
                effect = self._create_instant_effect_from_dict(effect_data)
                on_remove_effects.append(effect)
                
            # 创建周期性效果列表
            on_turn_start_effects = []
            for effect_data in data.get('on_turn_start_effects', []):
                effect = self._create_periodic_effect_from_dict(effect_data)
                on_turn_start_effects.append(effect)
                
            on_turn_end_effects = []
            for effect_data in data.get('on_turn_end_effects', []):
                effect = self._create_periodic_effect_from_dict(effect_data)
                on_turn_end_effects.append(effect)
                
            # 创建属性修改器列表
            modifiers = []
            for modifier_data in data.get('modifiers', []):
                modifier = self._create_stat_modifier_from_dict(modifier_data)
                modifiers.append(modifier)
                
            return StatusEffectDefinition(
                id=data['id'],
                name=data['name'],
                type=StatusType[data['type']],
                icon=data['icon'],
                description=data['description'],
                max_stacks=data['max_stacks'],
                duration_turns=data['duration_turns'],
                is_permanent=data.get('is_permanent', False),
                on_apply_effects=on_apply_effects,
                on_turn_start_effects=on_turn_start_effects,
                on_turn_end_effects=on_turn_end_effects,
                on_remove_effects=on_remove_effects,
                modifiers=modifiers,
                prevents_action=data.get('prevents_action', False),
                prevents_chase=data.get('prevents_chase', False),
                prevents_mystery=data.get('prevents_mystery', False),
                is_dispellable=data.get('is_dispellable', True),
                is_dispelled_by=data.get('is_dispelled_by', []),
                is_immunity_bypassed_by=data.get('is_immunity_bypassed_by', [])
            )
        except Exception as e:
            print(f"创建状态效果时出错: {str(e)}")
            return None
            
    def _convert_entity_to_dict(self, entity: StatusEffectDefinition) -> Dict:
        """
        将状态效果对象转换为字典
        
        Args:
            entity: 状态效果对象
            
        Returns:
            转换后的字典
        """
        # 转换即时效果列表
        on_apply_effects = []
        for effect in entity.on_apply_effects:
            on_apply_effects.append(self._convert_instant_effect_to_dict(effect))
            
        on_remove_effects = []
        for effect in entity.on_remove_effects:
            on_remove_effects.append(self._convert_instant_effect_to_dict(effect))
            
        # 转换周期性效果列表
        on_turn_start_effects = []
        for effect in entity.on_turn_start_effects:
            on_turn_start_effects.append(self._convert_periodic_effect_to_dict(effect))
            
        on_turn_end_effects = []
        for effect in entity.on_turn_end_effects:
            on_turn_end_effects.append(self._convert_periodic_effect_to_dict(effect))
            
        # 转换属性修改器列表
        modifiers = []
        for modifier in entity.modifiers:
            modifiers.append(self._convert_stat_modifier_to_dict(modifier))
            
        return {
            'id': entity.id,
            'name': entity.name,
            'type': entity.type.name,
            'icon': entity.icon,
            'description': entity.description,
            'max_stacks': entity.max_stacks,
            'duration_turns': entity.duration_turns,
            'is_permanent': entity.is_permanent,
            'on_apply_effects': on_apply_effects,
            'on_turn_start_effects': on_turn_start_effects,
            'on_turn_end_effects': on_turn_end_effects,
            'on_remove_effects': on_remove_effects,
            'modifiers': modifiers,
            'prevents_action': entity.prevents_action,
            'prevents_chase': entity.prevents_chase,
            'prevents_mystery': entity.prevents_mystery,
            'is_dispellable': entity.is_dispellable,
            'is_dispelled_by': entity.is_dispelled_by,
            'is_immunity_bypassed_by': entity.is_immunity_bypassed_by
        }
        
    def _create_instant_effect_from_dict(self, data: Dict) -> 'InstantEffect':
        """从字典创建即时效果"""
        from ..models.status_effect import InstantEffect
        return InstantEffect(
            effect_type=EffectType[data['effect_type']],
            value_formula=data['value_formula']
        )
        
    def _create_periodic_effect_from_dict(self, data: Dict) -> 'PeriodicEffect':
        """从字典创建周期性效果"""
        from ..models.status_effect import PeriodicEffect
        return PeriodicEffect(
            effect_type=EffectType[data['effect_type']],
            value_formula=data['value_formula']
        )
        
    def _create_stat_modifier_from_dict(self, data: Dict) -> 'StatModifier':
        """从字典创建属性修改器"""
        from ..models.status_effect import StatModifier
        return StatModifier(
            stat_name=data['stat_name'],
            value=data['value'],
            is_percentage=data['is_percentage']
        )
        
    def _convert_instant_effect_to_dict(self, effect: 'InstantEffect') -> Dict:
        """将即时效果转换为字典"""
        return {
            'effect_type': effect.effect_type.name,
            'value_formula': effect.value_formula
        }
        
    def _convert_periodic_effect_to_dict(self, effect: 'PeriodicEffect') -> Dict:
        """将周期性效果转换为字典"""
        return {
            'effect_type': effect.effect_type.name,
            'value_formula': effect.value_formula
        }
        
    def _convert_stat_modifier_to_dict(self, modifier: 'StatModifier') -> Dict:
        """将属性修改器转换为字典"""
        return {
            'stat_name': modifier.stat_name,
            'value': modifier.value,
            'is_percentage': modifier.is_percentage
        } 