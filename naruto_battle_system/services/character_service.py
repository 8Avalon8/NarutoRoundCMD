from typing import List, Dict, Any, Optional
from ..models.character import Character
from ..models.skill import Skill, DamageEffect, HealingEffect
from ..models.status_effect import StatusEffect
from ..models.enums import SkillType, TargetType, StatusEffectType
from ..data.repositories import CharacterRepository


class CharacterService:
    """角色服务，处理角色相关的业务逻辑"""
    
    def __init__(self, character_repository: CharacterRepository):
        """初始化角色服务
        
        Args:
            character_repository: 角色仓库实例
        """
        self.character_repository = character_repository
    
    def create_character(self, character_data: Dict[str, Any]) -> Character:
        """创建新角色
        
        Args:
            character_data: 角色数据字典
            
        Returns:
            创建的角色
            
        Raises:
            ValueError: 如果角色数据无效
        """
        # 验证必填字段
        required_fields = ["name", "hp", "chakra", "attack", "defense", "speed"]
        for field in required_fields:
            if field not in character_data:
                raise ValueError(f"缺少必填字段: {field}")
        
        # 创建基础角色
        character = Character(
            name=character_data["name"],
            hp=character_data["hp"],
            max_hp=character_data.get("max_hp", character_data["hp"]),
            chakra=character_data["chakra"],
            max_chakra=character_data.get("max_chakra", character_data["chakra"]),
            attack=character_data["attack"],
            defense=character_data["defense"],
            speed=character_data["speed"],
            is_player_controlled=character_data.get("is_player_controlled", False)
        )
        
        # 添加技能
        if "skills" in character_data and isinstance(character_data["skills"], list):
            for skill_data in character_data["skills"]:
                skill = self._create_skill(skill_data)
                if skill:
                    character.skills.append(skill)
        
        # 添加角色特性
        if "traits" in character_data and isinstance(character_data["traits"], list):
            for trait_data in character_data["traits"]:
                trait = self._create_trait(trait_data)
                if trait:
                    character.traits.append(trait)
        
        # 保存角色
        self.character_repository.add(character)
        return character
    
    def _create_skill(self, skill_data: Dict[str, Any]) -> Optional[Skill]:
        """从数据创建技能
        
        Args:
            skill_data: 技能数据字典
            
        Returns:
            创建的技能，如果数据无效返回None
        """
        # 验证必填字段
        required_fields = ["name", "description", "cost", "skill_type", "target_type"]
        for field in required_fields:
            if field not in skill_data:
                return None
        
        try:
            # 解析枚举值
            skill_type = SkillType[skill_data["skill_type"]]
            target_type = TargetType[skill_data["target_type"]]
            
            skill = Skill(
                name=skill_data["name"],
                description=skill_data["description"],
                cost=skill_data["cost"],
                skill_type=skill_type,
                target_type=target_type
            )
            
            # 添加技能效果
            if "effects" in skill_data and isinstance(skill_data["effects"], list):
                for effect_data in skill_data["effects"]:
                    effect = self._create_skill_effect(effect_data)
                    if effect:
                        skill.effects.append(effect)
            
            return skill
        except (KeyError, ValueError):
            return None
    
    def _create_skill_effect(self, effect_data: Dict[str, Any]) -> Optional[Any]:
        """从数据创建技能效果
        
        Args:
            effect_data: 效果数据字典
            
        Returns:
            创建的效果对象，如果数据无效返回None
        """
        if "effect_type" not in effect_data:
            return None
            
        effect_type = effect_data["effect_type"]
        
        try:
            if effect_type == "DAMAGE":
                return DamageEffect(
                    base_value=effect_data.get("base_value", 0),
                    scaling=effect_data.get("scaling", 0)
                )
            elif effect_type == "HEALING":
                return HealingEffect(
                    base_value=effect_data.get("base_value", 0),
                    scaling=effect_data.get("scaling", 0)
                )
            elif effect_type == "STATUS":
                if "status_type" not in effect_data:
                    return None
                    
                status_type = StatusEffectType[effect_data["status_type"]]
                return StatusEffect(
                    effect_type=status_type,
                    value=effect_data.get("value", 0),
                    duration=effect_data.get("duration", 1)
                )
        except (KeyError, ValueError):
            return None
            
        return None
    
    def _create_trait(self, trait_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """从数据创建角色特性
        
        Args:
            trait_data: 特性数据字典
            
        Returns:
            创建的特性对象，如果数据无效返回None
        """
        # 简单实现，只是返回原始字典
        if isinstance(trait_data, dict) and "name" in trait_data:
            return trait_data
        return None
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """根据ID获取角色
        
        Args:
            character_id: 角色ID
            
        Returns:
            找到的角色，如果不存在返回None
        """
        return self.character_repository.get_character(character_id)
    
    def get_all(self) -> List[Character]:
        """获取所有角色
        
        Returns:
            所有角色的列表
        """
        return self.character_repository.get_all()
    
    def update_character(self, character: Character) -> bool:
        """更新角色信息
        
        Args:
            character: 要更新的角色实例
            
        Returns:
            更新是否成功
        """
        return self.character_repository.update_character(character)
    
    def delete_character(self, character_id: str) -> bool:
        """删除角色
        
        Args:
            character_id: 要删除的角色ID
            
        Returns:
            删除是否成功
        """
        return self.character_repository.delete_character(character_id)
    
    def create_default_characters(self) -> List[Character]:
        """创建默认角色
        
        Returns:
            创建的默认角色列表
        """
        default_characters = []
        
        # 创建鸣人
        naruto_data = {
            "name": "漩涡鸣人",
            "hp": 1000,
            "chakra": 1000,
            "attack": 85,
            "defense": 60,
            "speed": 75,
            "is_player_controlled": True,
            "skills": [
                {
                    "name": "螺旋丸",
                    "description": "对单个目标造成大量伤害",
                    "cost": 30,
                    "skill_type": "DAMAGE",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 100,
                            "scaling": 50
                        }
                    ]
                },
                {
                    "name": "影分身之术",
                    "description": "增加自身攻击力",
                    "cost": 20,
                    "skill_type": "BUFF",
                    "target_type": "SELF",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "ATTACK_UP",
                            "value": 30,
                            "duration": 3
                        }
                    ]
                },
                {
                    "name": "九尾模式",
                    "description": "大幅增加自身攻击力和速度",
                    "cost": 50,
                    "skill_type": "BUFF",
                    "target_type": "SELF",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "ATTACK_UP",
                            "value": 50,
                            "duration": 3
                        },
                        {
                            "effect_type": "STATUS",
                            "status_type": "SPEED_UP",
                            "value": 30,
                            "duration": 3
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "不屈意志",
                    "description": "HP低于20%时，攻击力增加20%"
                },
                {
                    "name": "九尾之力",
                    "description": "每回合恢复5%的最大生命值"
                }
            ]
        }
        default_characters.append(self.create_character(naruto_data))
        
        # 创建佐助
        sasuke_data = {
            "name": "宇智波佐助",
            "hp": 850,
            "chakra": 900,
            "attack": 95,
            "defense": 65,
            "speed": 85,
            "is_player_controlled": True,
            "skills": [
                {
                    "name": "千鸟",
                    "description": "对单个目标造成大量伤害",
                    "cost": 30,
                    "skill_type": "DAMAGE",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 120,
                            "scaling": 60
                        }
                    ]
                },
                {
                    "name": "天照",
                    "description": "对敌人造成持续伤害",
                    "cost": 45,
                    "skill_type": "DEBUFF",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "DOT",
                            "value": 40,
                            "duration": 3
                        }
                    ]
                },
                {
                    "name": "须佐能乎",
                    "description": "大幅增加自身防御力",
                    "cost": 50,
                    "skill_type": "BUFF",
                    "target_type": "SELF",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "DEFENSE_UP",
                            "value": 70,
                            "duration": 3
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "写轮眼",
                    "description": "提高暴击率15%"
                },
                {
                    "name": "雷遁查克拉",
                    "description": "雷属性技能伤害提高20%"
                }
            ]
        }
        default_characters.append(self.create_character(sasuke_data))
        
        # 创建小樱
        sakura_data = {
            "name": "春野樱",
            "hp": 750,
            "chakra": 800,
            "attack": 65,
            "defense": 60,
            "speed": 70,
            "is_player_controlled": True,
            "skills": [
                {
                    "name": "怪力",
                    "description": "对单个目标造成伤害",
                    "cost": 20,
                    "skill_type": "DAMAGE",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 90,
                            "scaling": 40
                        }
                    ]
                },
                {
                    "name": "医疗忍术",
                    "description": "治疗单个目标",
                    "cost": 30,
                    "skill_type": "HEALING",
                    "target_type": "ALLY",
                    "effects": [
                        {
                            "effect_type": "HEALING",
                            "base_value": 100,
                            "scaling": 50
                        }
                    ]
                },
                {
                    "name": "百豪之术",
                    "description": "治疗所有友方角色",
                    "cost": 50,
                    "skill_type": "HEALING",
                    "target_type": "ALL_ALLIES",
                    "effects": [
                        {
                            "effect_type": "HEALING",
                            "base_value": 80,
                            "scaling": 40
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "精准查克拉控制",
                    "description": "治疗效果提高20%"
                },
                {
                    "name": "医疗忍者",
                    "description": "每回合恢复额外5%的查克拉"
                }
            ]
        }
        default_characters.append(self.create_character(sakura_data))
        
        # 创建卡卡西
        kakashi_data = {
            "name": "旗木卡卡西",
            "hp": 900,
            "chakra": 850,
            "attack": 90,
            "defense": 80,
            "speed": 90,
            "is_player_controlled": False,
            "skills": [
                {
                    "name": "雷切",
                    "description": "对单个目标造成大量伤害",
                    "cost": 35,
                    "skill_type": "DAMAGE",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 130,
                            "scaling": 60
                        }
                    ]
                },
                {
                    "name": "水龙弹之术",
                    "description": "对所有敌人造成伤害",
                    "cost": 40,
                    "skill_type": "DAMAGE",
                    "target_type": "ALL_ENEMIES",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 70,
                            "scaling": 30
                        }
                    ]
                },
                {
                    "name": "写轮眼洞察",
                    "description": "降低敌人闪避率",
                    "cost": 25,
                    "skill_type": "DEBUFF",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "EVASION_DOWN",
                            "value": 50,
                            "duration": 2
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "复制忍者",
                    "description": "有10%几率复制敌人的技能"
                },
                {
                    "name": "写轮眼",
                    "description": "提高暴击率15%"
                }
            ]
        }
        default_characters.append(self.create_character(kakashi_data))
        
        # 创建宁次
        neji_data = {
            "name": "日向宁次",
            "hp": 800,
            "chakra": 750,
            "attack": 85,
            "defense": 75,
            "speed": 80,
            "is_player_controlled": False,
            "skills": [
                {
                    "name": "八卦六十四掌",
                    "description": "对单个目标造成多段伤害",
                    "cost": 35,
                    "skill_type": "DAMAGE",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 110,
                            "scaling": 50
                        }
                    ]
                },
                {
                    "name": "回天",
                    "description": "提高自身防御和闪避",
                    "cost": 30,
                    "skill_type": "BUFF",
                    "target_type": "SELF",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "DEFENSE_UP",
                            "value": 40,
                            "duration": 2
                        },
                        {
                            "effect_type": "STATUS",
                            "status_type": "EVASION_UP",
                            "value": 30,
                            "duration": 2
                        }
                    ]
                },
                {
                    "name": "白眼",
                    "description": "降低敌人防御",
                    "cost": 25,
                    "skill_type": "DEBUFF",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "DEFENSE_DOWN",
                            "value": 40,
                            "duration": 2
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "白眼",
                    "description": "攻击有15%几率无视敌人30%防御"
                },
                {
                    "name": "柔拳",
                    "description": "攻击有20%几率封印敌人查克拉，减少10点"
                }
            ]
        }
        default_characters.append(self.create_character(neji_data))
        
        # 创建我爱罗
        gaara_data = {
            "name": "我爱罗",
            "hp": 950,
            "chakra": 900,
            "attack": 80,
            "defense": 100,
            "speed": 65,
            "is_player_controlled": False,
            "skills": [
                {
                    "name": "沙暴",
                    "description": "对所有敌人造成伤害",
                    "cost": 35,
                    "skill_type": "DAMAGE",
                    "target_type": "ALL_ENEMIES",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 70,
                            "scaling": 30
                        }
                    ]
                },
                {
                    "name": "砂缚柩",
                    "description": "束缚敌人，造成伤害并降低速度",
                    "cost": 40,
                    "skill_type": "DEBUFF",
                    "target_type": "SINGLE",
                    "effects": [
                        {
                            "effect_type": "DAMAGE",
                            "base_value": 80,
                            "scaling": 40
                        },
                        {
                            "effect_type": "STATUS",
                            "status_type": "SPEED_DOWN",
                            "value": 40,
                            "duration": 2
                        }
                    ]
                },
                {
                    "name": "砂之铠",
                    "description": "大幅提高自身防御",
                    "cost": 30,
                    "skill_type": "BUFF",
                    "target_type": "SELF",
                    "effects": [
                        {
                            "effect_type": "STATUS",
                            "status_type": "DEFENSE_UP",
                            "value": 80,
                            "duration": 3
                        }
                    ]
                }
            ],
            "traits": [
                {
                    "name": "砂之守护",
                    "description": "受到攻击时有30%几率减少30%伤害"
                },
                {
                    "name": "一尾守鹤",
                    "description": "HP低于30%时，攻击力增加40%"
                }
            ]
        }
        default_characters.append(self.create_character(gaara_data))
        
        return default_characters 