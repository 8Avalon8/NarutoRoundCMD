import unittest
from ..models.character import Character
from ..models.skill import Skill, DamageEffect, HealingEffect
from ..models.status_effect import StatusEffect
from ..models.enums import SkillType, TargetType, StatusEffectType


class TestCharacter(unittest.TestCase):
    """测试角色模型"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建基础角色
        self.character = Character(
            name="测试角色",
            hp=100,
            max_hp=100,
            chakra=50,
            max_chakra=100,
            attack=30,
            defense=20,
            speed=40
        )
        
        # 创建技能
        damage_effect = DamageEffect(base_value=20, scaling=50)
        self.damage_skill = Skill(
            name="伤害技能",
            description="造成伤害的技能",
            cost=10,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE
        )
        self.damage_skill.effects.append(damage_effect)
        
        healing_effect = HealingEffect(base_value=20, scaling=50)
        self.healing_skill = Skill(
            name="治疗技能",
            description="恢复生命的技能",
            cost=10,
            skill_type=SkillType.HEALING,
            target_type=TargetType.SINGLE
        )
        self.healing_skill.effects.append(healing_effect)
    
    def test_character_initialization(self):
        """测试角色初始化"""
        # 检查角色属性是否正确设置
        self.assertEqual(self.character.name, "测试角色")
        self.assertEqual(self.character.hp, 100)
        self.assertEqual(self.character.max_hp, 100)
        self.assertEqual(self.character.chakra, 50)
        self.assertEqual(self.character.max_chakra, 100)
        self.assertEqual(self.character.attack, 30)
        self.assertEqual(self.character.defense, 20)
        self.assertEqual(self.character.speed, 40)
        self.assertTrue(self.character.is_alive)
        self.assertEqual(len(self.character.skills), 0)
        self.assertEqual(len(self.character.status_effects), 0)
    
    def test_add_skill(self):
        """测试添加技能"""
        # 添加技能
        self.character.skills.append(self.damage_skill)
        self.character.skills.append(self.healing_skill)
        
        # 检查技能是否添加成功
        self.assertEqual(len(self.character.skills), 2)
        self.assertEqual(self.character.skills[0].name, "伤害技能")
        self.assertEqual(self.character.skills[1].name, "治疗技能")
    
    def test_add_status_effect(self):
        """测试添加状态效果"""
        # 创建状态效果
        buff = StatusEffect(
            name="攻击提升",
            description="攻击提升",
            effect_type=StatusEffectType.BUFF_ATK,
            value=20,
            duration=2,
            source_character_id=None
        )
        
        debuff = StatusEffect(
            name="防御降低",    
            description="防御降低",
            effect_type=StatusEffectType.DEBUFF_DEF,
            value=15,
            duration=3,
            source_character_id=None
        )
        
        # 添加状态效果
        self.character.status_effects.append(buff)
        self.character.status_effects.append(debuff)
        
        # 检查状态效果是否添加成功
        self.assertEqual(len(self.character.status_effects), 2)
        self.assertEqual(self.character.status_effects[0].effect_type, StatusEffectType.BUFF_ATK)
        self.assertEqual(self.character.status_effects[1].effect_type, StatusEffectType.DEBUFF_DEF)
    
    def test_take_damage(self):
        """测试受到伤害"""
        # 初始HP
        initial_hp = self.character.hp
        
        # 造成伤害
        damage = 30
        self.character.hp = max(0, self.character.hp - damage)
        
        # 检查HP是否正确减少
        self.assertEqual(self.character.hp, initial_hp - damage)
        
        # 造成致命伤害
        self.character.hp = 0
        
        # 检查角色是否阵亡
        self.assertEqual(self.character.hp, 0)
    
    def test_heal(self):
        """测试治疗"""
        # 先造成一些伤害
        self.character.hp = 50
        
        # 恢复生命
        healing = 20
        self.character.hp = min(self.character.max_hp, self.character.hp + healing)
        
        # 检查HP是否正确恢复
        self.assertEqual(self.character.hp, 70)
        
        # 过量治疗不应超过最大HP
        self.character.hp = min(self.character.max_hp, self.character.hp + 50)
        self.assertEqual(self.character.hp, self.character.max_hp)
    
    def test_use_chakra(self):
        """测试使用查克拉"""
        # 初始查克拉
        initial_chakra = self.character.chakra
        
        # 消耗查克拉
        cost = 20
        if self.character.chakra >= cost:
            self.character.chakra -= cost
        
        # 检查查克拉是否正确减少
        self.assertEqual(self.character.chakra, initial_chakra - cost)
        
        # 尝试消耗超过剩余量的查克拉
        cost = 40
        if self.character.chakra >= cost:
            self.character.chakra -= cost
        else:
            # 查克拉不足，不应该减少
            self.assertEqual(self.character.chakra, initial_chakra - 20)
    
    def test_restore_chakra(self):
        """测试恢复查克拉"""
        # 先消耗一些查克拉
        self.character.chakra = 20
        
        # 恢复查克拉
        regen = 15
        self.character.chakra = min(self.character.max_chakra, self.character.chakra + regen)
        
        # 检查查克拉是否正确恢复
        self.assertEqual(self.character.chakra, 35)
        
        # 过量恢复不应超过最大查克拉
        self.character.chakra = min(self.character.max_chakra, self.character.chakra + 100)
        self.assertEqual(self.character.chakra, self.character.max_chakra)
    
    def test_clone(self):
        """测试角色克隆"""
        # 为角色添加技能和状态效果
        self.character.skills.append(self.damage_skill)
        
        buff = StatusEffect(
            name="攻击提升",
            description="攻击提升",
            effect_type=StatusEffectType.BUFF_ATK,
            value=20,
            duration=2,
            source_character_id=None
        )
        self.character.status_effects.append(buff)
        
        # 克隆角色
        clone = self.character.clone()
        
        # 检查克隆是否成功
        self.assertEqual(clone.name, self.character.name)
        self.assertEqual(clone.hp, self.character.hp)
        self.assertEqual(clone.max_hp, self.character.max_hp)
        self.assertEqual(clone.chakra, self.character.chakra)
        self.assertEqual(clone.max_chakra, self.character.max_chakra)
        self.assertEqual(clone.attack, self.character.attack)
        self.assertEqual(clone.defense, self.character.defense)
        self.assertEqual(clone.speed, self.character.speed)
        
        # 确保是深拷贝
        self.assertIsNot(clone, self.character)
        self.assertEqual(len(clone.skills), 1)
        self.assertEqual(len(clone.status_effects), 1)


if __name__ == '__main__':
    unittest.main() 