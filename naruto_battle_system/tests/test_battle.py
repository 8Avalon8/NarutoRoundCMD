import unittest
from unittest.mock import MagicMock, patch
import random

from ..models.character import Character
from ..models.battle_state import BattleState
from ..models.battle_team import BattleTeam
from ..models.action import Action, ActionResult
from ..models.skill import Skill, DamageEffect
from ..models.enums import ActionType, SkillType, TargetType
from ..controllers.battle_controller import BattleController


class TestBattleController(unittest.TestCase):
    """测试战斗控制器"""
    
    def setUp(self):
        """设置测试环境"""
        # 设置随机种子以使测试可重复
        random.seed(42)
        
        # 创建模拟角色
        self.character1 = Character(
            name="测试角色1",
            hp=100,
            max_hp=100,
            chakra=100,
            max_chakra=100,
            attack=50,
            defense=30,
            speed=50
        )
        
        self.character2 = Character(
            name="测试角色2",
            hp=100,
            max_hp=100,
            chakra=100,
            max_chakra=100,
            attack=40,
            defense=40,
            speed=40
        )
        
        # 创建技能
        damage_effect = DamageEffect(base_value=20, scaling=50)
        self.test_skill = Skill(
            name="测试技能",
            description="用于测试的技能",
            cost=20,
            skill_type=SkillType.DAMAGE,
            target_type=TargetType.SINGLE
        )
        self.test_skill.effects.append(damage_effect)
        
        # 为角色添加技能
        self.character1.skills.append(self.test_skill)
        
        # 创建队伍
        self.team_a = BattleTeam(name="队伍A", player_id="player1", characters=[self.character1])
        self.team_b = BattleTeam(name="队伍B", player_id="player2", characters=[self.character2])
        
        # 创建战斗状态
        self.battle_state = BattleState(self.team_a, self.team_b)
        
        # 创建模拟事件监听器
        self.mock_events = MagicMock()
        
        # 创建战斗控制器
        self.battle_controller = BattleController(self.battle_state, self.mock_events)
    
    def test_start_battle(self):
        """测试开始战斗"""
        self.battle_controller.start_battle()
        
        # 验证事件回调被正确调用
        self.mock_events.on_battle_start.assert_called_once_with(self.battle_state)
        self.mock_events.on_round_start.assert_called_once_with(self.battle_state)
        
        # 验证回合数已增加
        self.assertEqual(self.battle_state.current_round, 1)
        
        # 验证行动顺序已计算
        self.assertGreater(len(self.battle_state.turn_order), 0)
    
    def test_execute_attack_action(self):
        """测试执行攻击动作"""
        # 创建攻击动作
        action = Action(
            character=self.character1,
            action_type=ActionType.ATTACK,
            target=self.character2,
            skill=None
        )
        
        # 执行动作
        self.battle_controller.execute_action(action)
        
        # 验证动作执行事件被调用
        self.mock_events.on_action_executed.assert_called_once()
        
        # 验证伤害已造成
        self.assertLess(self.character2.hp, self.character2.max_hp)
    
    def test_execute_skill_action(self):
        """测试执行技能动作"""
        # 开始战斗以初始化回合顺序等
        self.battle_controller.start_battle()

        # 设置初始查克拉
        self.character1.chakra = 100
        
        # 创建技能动作
        action = Action(
            character=self.character1,
            action_type=ActionType.SKILL,
            target=self.character2,
            skill=self.test_skill
        )
        
        # 记录初始查克拉值
        initial_chakra = self.character1.chakra
        print(f"初始查克拉: {initial_chakra}")
        print(f"技能消耗: {self.test_skill.cost}")
        
        # 执行动作
        self.battle_controller.execute_action(action)
        
        # 验证查克拉已消耗
        print(f"执行后查克拉: {self.character1.chakra}")
        
        # 断言查克拉减少了20
        self.assertEqual(self.character1.chakra, 80, "查克拉应该减少20点")
        
        # 验证动作执行事件被调用
        self.mock_events.on_action_executed.assert_called_once()
        
        # 验证伤害已造成
        self.assertLess(self.character2.hp, self.character2.max_hp)
    
    def test_is_battle_over(self):
        """测试战斗结束判定"""
        # 初始状态下战斗不应该结束
        self.assertFalse(self.battle_controller.is_battle_over())
        
        # 使其中一个角色阵亡
        self.character2.hp = 0
        self.character2.is_alive = False
        
        # 现在战斗应该结束
        self.assertTrue(self.battle_controller.is_battle_over())
        
        # 验证获胜队伍
        winning_team = self.battle_controller.get_winning_team()
        self.assertEqual(winning_team, self.team_a)
    
    def test_next_turn(self):
        """测试下一个回合"""
        # 设置初始回合
        self.battle_controller.start_battle()
        initial_index = self.battle_state.current_character_index
        
        # 进入下一个角色的回合
        self.battle_controller.next_turn()
        
        # 验证角色索引已经改变
        self.assertNotEqual(self.battle_state.current_character_index, initial_index)
    
    def test_process_turn(self):
        """测试处理回合"""
        # 设置初始回合
        self.battle_controller.start_battle()
        
        # 模拟处理回合
        with patch.object(self.battle_controller, '_generate_ai_action') as mock_ai:
            # 设置AI动作为跳过回合
            mock_action = Action(self.character1, ActionType.PASS, None, None)
            mock_ai.return_value = mock_action
            
            # 处理回合
            self.battle_controller.process_turn()
            
            # 验证回合处理后事件被调用
            self.mock_events.on_action_executed.assert_called()


if __name__ == '__main__':
    unittest.main() 