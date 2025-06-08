import time
import os
import random
from typing import List, Dict, Any
from ..models.enums import ActionType, SkillType


class AnimationManager:
    """动画管理器，用于控制战斗中的动画效果"""
    
    def __init__(self, animation_speed: float = 0.05, enable_animations: bool = True):
        """初始化动画管理器
        
        Args:
            animation_speed: 基础动画速度，数值越小动画越快
            enable_animations: 是否启用动画效果
        """
        self.animation_speed = animation_speed
        self.enable_animations = enable_animations
    
    def wait(self, duration: float = None) -> None:
        """等待指定时间
        
        Args:
            duration: 等待时间，如果为None则使用基础动画速度
        """
        if self.enable_animations:
            time.sleep(duration if duration is not None else self.animation_speed)
    
    def clear_screen(self) -> None:
        """清空控制台屏幕"""
        #os.system('cls' if os.name == 'nt' else 'clear')
        pass
    
    def play_attack_animation(self, attacker_name: str, target_name: str, damage: int) -> None:
        """播放普通攻击动画
        
        Args:
            attacker_name: 攻击者名称
            target_name: 目标名称
            damage: 造成的伤害
        """
        if not self.enable_animations:
            return
            
        print(f"\n{attacker_name} 对 {target_name} 发起攻击...")
        self.wait(0.5)
        
        # 简单的ASCII动画
        frames = [
            "  >>--->  ",
            "   >>---> ",
            "    >>--->",
            "     >>---",
            "      >>--",
            "       >>-",
            "        >>",
            "         >",
            "          ",
            "    *     ",
            "   *#*    ",
            "  *###*   ",
            " *#####*  ",
            "*#######* ",
            " *#####*  ",
            "  *###*   ",
            "   *#*    ",
            "    *     "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait()
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
        print(f"\r造成 {damage} 点伤害！")
        self.wait(0.5)
    
    def play_skill_animation(self, caster_name: str, skill_name: str, skill_type: SkillType) -> None:
        """播放技能施放动画
        
        Args:
            caster_name: 施法者名称
            skill_name: 技能名称
            skill_type: 技能类型
        """
        if not self.enable_animations:
            return
            
        print(f"\n{caster_name} 正在准备忍术 {skill_name}...")
        self.wait(0.5)
        
        # 根据技能类型显示不同的动画
        if skill_type == SkillType.DAMAGE:
            self._play_damage_skill_animation()
        elif skill_type == SkillType.HEALING:
            self._play_healing_skill_animation()
        elif skill_type == SkillType.BUFF:
            self._play_buff_skill_animation()
        elif skill_type == SkillType.DEBUFF:
            self._play_debuff_skill_animation()
        else:
            self._play_generic_skill_animation()
            
        print(f"\n{skill_name} 施放完成！")
        self.wait(0.5)
    
    def _play_damage_skill_animation(self) -> None:
        """播放伤害型技能动画"""
        frames = [
            "      (   )  ",
            "     (    )  ",
            "    (     )  ",
            "   (      )  ",
            "  (  火遁  )  ",
            " (        )  ",
            "(         )  ",
            " (        )  ",
            "  (      )  ",
            "   (    )  ",
            "    (  )   ",
            "   炎炎炎炎   ",
            "  炎炎炎炎炎  ",
            " 炎炎炎炎炎炎 ",
            "炎炎炎炎炎炎炎",
            " 炎炎炎炎炎炎 ",
            "  炎炎炎炎炎  ",
            "   炎炎炎炎   ",
            "    炎炎炎    ",
            "     炎炎     ",
            "      炎      "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait()
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def _play_healing_skill_animation(self) -> None:
        """播放治疗型技能动画"""
        frames = [
            "      +      ",
            "     +++     ",
            "    +++++    ",
            "   +++++++   ",
            "  +++++++++  ",
            " +++++++++++  ",
            "+++++++++++++ ",
            " ++++医疗忍术++++",
            "  +++++++++  ",
            "   +++++++   ",
            "    +++++    ",
            "     +++     ",
            "      +      "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def _play_buff_skill_animation(self) -> None:
        """播放增益型技能动画"""
        frames = [
            "     ↑     ",
            "    ↑↑↑    ",
            "   ↑↑↑↑↑   ",
            "  ↑↑↑↑↑↑↑  ",
            " ↑↑↑强化↑↑↑ ",
            "↑↑↑↑↑↑↑↑↑↑↑",
            " ↑↑↑↑↑↑↑↑↑ ",
            "  ↑↑↑↑↑↑↑  ",
            "   ↑↑↑↑↑   ",
            "    ↑↑↑    ",
            "     ↑     "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def _play_debuff_skill_animation(self) -> None:
        """播放减益型技能动画"""
        frames = [
            "     ↓     ",
            "    ↓↓↓    ",
            "   ↓↓↓↓↓   ",
            "  ↓↓↓↓↓↓↓  ",
            " ↓↓↓弱化↓↓↓ ",
            "↓↓↓↓↓↓↓↓↓↓↓",
            " ↓↓↓↓↓↓↓↓↓ ",
            "  ↓↓↓↓↓↓↓  ",
            "   ↓↓↓↓↓   ",
            "    ↓↓↓    ",
            "     ↓     "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def _play_generic_skill_animation(self) -> None:
        """播放通用技能动画"""
        frames = [
            "    *    ",
            "   ***   ",
            "  *****  ",
            " ******* ",
            "*********",
            " ******* ",
            "  *****  ",
            "   ***   ",
            "    *    "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def play_combo_animation(self) -> None:
        """播放连击动画"""
        if not self.enable_animations:
            return
            
        print("\n连击触发！")
        
        frames = [
            "C      ",
            "CO     ",
            "COM    ",
            "COMB   ",
            "COMBO  ",
            "COMBO! ",
            "COMBO!!",
            " OMBO!!",
            "  MBO!!",
            "   BO!!",
            "    O!!",
            "     !!",
            "      !"
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.05)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
    
    def play_status_effect_animation(self, effect_name: str, is_debuff: bool) -> None:
        """播放状态效果动画
        
        Args:
            effect_name: 效果名称
            is_debuff: 是否为减益效果
        """
        if not self.enable_animations:
            return
            
        symbol = "↓" if is_debuff else "↑"
        
        for _ in range(5):
            print(f"\r{symbol} {effect_name} {symbol}", end="", flush=True)
            self.wait(0.1)
            print(f"\r  {effect_name}  ", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * (len(effect_name) + 4)}", end="", flush=True)  # 清除动画
    
    def play_character_defeated_animation(self, character_name: str) -> None:
        """播放角色阵亡动画
        
        Args:
            character_name: 阵亡角色的名称
        """
        if not self.enable_animations:
            return
            
        print(f"\n{character_name} 已被击败！")
        
        frames = [
            "  \\o/  ",
            "   o   ",
            "   o\\  ",
            "  /o   ",
            "   o   ",
            "  _o_  ",
            "   o   ",
            "   o/  ",
            "  \\o_  ",
            "   o   ",
            "  /o\\  ",
            "   o   ",
            "   o_  ",
            "  _o/  ",
            "   o   ",
            "   O   ",
            "  /X\\  ",
            "  / \\  "
        ]
        
        for frame in frames:
            print(f"\r{frame}", end="", flush=True)
            self.wait(0.1)
            
        print(f"\r{' ' * 20}", end="", flush=True)  # 清除动画
        self.wait(0.5)
    
    def play_battle_start_animation(self) -> None:
        """播放战斗开始动画"""
        if not self.enable_animations:
            return
            
        self.clear_screen()
        
        text = "战斗开始！"
        padding = 40
        
        for i in range(padding, -1, -1):
            self.clear_screen()
            print("\n" * 10)
            print(" " * i + text + " " * (padding - i))
            self.wait(0.05)
            
        self.wait(1.0)
    
    def play_battle_end_animation(self, winner_name: str) -> None:
        """播放战斗结束动画
        
        Args:
            winner_name: 获胜方名称
        """
        if not self.enable_animations:
            return
            
        self.clear_screen()
        
        frames = [
            "====================",
            "=====战斗结束!=====",
            "====================",
            "                    ",
            "====================",
            "=====战斗结束!=====",
            "====================",
        ]
        
        for _ in range(3):
            for frame in frames:
                self.clear_screen()
                print("\n" * 10)
                print(frame)
                self.wait(0.2)
                
        self.clear_screen()
        print("\n" * 10)
        print(f"获胜方: {winner_name}")
        self.wait(1.0) 