import os
from typing import List, Dict, Callable, Any, Optional


class MenuView:
    """菜单视图，用于显示游戏菜单和处理菜单选择"""
    
    def __init__(self):
        """初始化菜单视图"""
        pass
    
    def clear_screen(self) -> None:
        """清空控制台屏幕"""
        #os.system('cls' if os.name == 'nt' else 'clear')
        pass
    
    def show_title(self) -> None:
        """显示游戏标题"""
        self.clear_screen()
        print("""
██████╗ ██╗   ██╗████████╗ ██████╗     ██████╗  █████╗ ████████╗████████╗██╗     ███████╗
██╔═══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝
██║   ██║██║   ██║   ██║   ██║   ██║    ██████╔╝███████║   ██║      ██║   ██║     █████╗  
██║   ██║██║   ██║   ██║   ██║   ██║    ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  
██████╔╝╚██████╔╝   ██║   ╚██████╔╝    ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗
╚═════╝  ╚═════╝    ╚═╝    ╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝
                                                                                         
███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗                                    
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║                                    
███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║                                    
╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║                                    
███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║                                    
╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝                                    
""")
        print("\n" + "=" * 80)
        print("                        火影忍者OL - 回合制战斗系统演示")
        print("=" * 80 + "\n")
    
    def show_main_menu(self) -> int:
        """显示主菜单并获取选择
        
        Returns:
            用户选择的菜单项索引
        """
        self.show_title()
        
        print("主菜单:")
        print("1. 开始新战斗")
        print("2. 角色列表")
        print("3. 帮助信息")
        print("4. 退出游戏")
        print("\n" + "-" * 80)
        
        while True:
            try:
                choice = int(input("\n请输入选项 (1-4): "))
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("无效选项，请输入 1-4 之间的数字。")
            except ValueError:
                print("无效输入，请输入数字。")
    
    def show_battle_setup_menu(self, available_characters: List[Dict[str, Any]]) -> tuple:
        """显示战斗设置菜单并获取选择
        
        Args:
            available_characters: 可选角色列表
            
        Returns:
            包含队伍A角色索引列表和队伍B角色索引列表的元组
        """
        self.clear_screen()
        print("\n===== 战斗设置 =====\n")
        
        print("可选角色:")
        for i, character in enumerate(available_characters):
            print(f"{i+1}. {character['name']} (HP: {character['hp']}, 攻击: {character['attack']}, 速度: {character['speed']})")
        
        print("\n" + "-" * 80)
        
        # 选择队伍A的角色
        team_a_indices = []
        print("\n为队伍A选择角色 (输入角色编号，以空格分隔，如 '1 3 5'):")
        while not team_a_indices:
            try:
                indices_input = input("> ").strip().split()
                team_a_indices = [int(idx) - 1 for idx in indices_input]
                
                # 验证输入
                if any(idx < 0 or idx >= len(available_characters) for idx in team_a_indices):
                    print("无效的角色编号，请重新输入。")
                    team_a_indices = []
                elif len(team_a_indices) < 1:
                    print("至少需要选择一个角色。")
                    team_a_indices = []
                elif len(team_a_indices) > 3:
                    print("最多只能选择三个角色。")
                    team_a_indices = []
            except ValueError:
                print("输入格式错误，请输入角色编号，以空格分隔。")
                team_a_indices = []
        
        # 选择队伍B的角色
        team_b_indices = []
        print("\n为队伍B选择角色 (输入角色编号，以空格分隔，如 '2 4 6'):")
        while not team_b_indices:
            try:
                indices_input = input("> ").strip().split()
                team_b_indices = [int(idx) - 1 for idx in indices_input]
                
                # 验证输入
                if any(idx < 0 or idx >= len(available_characters) for idx in team_b_indices):
                    print("无效的角色编号，请重新输入。")
                    team_b_indices = []
                elif len(team_b_indices) < 1:
                    print("至少需要选择一个角色。")
                    team_b_indices = []
                elif len(team_b_indices) > 3:
                    print("最多只能选择三个角色。")
                    team_b_indices = []
            except ValueError:
                print("输入格式错误，请输入角色编号，以空格分隔。")
                team_b_indices = []
        
        # 确认选择
        self.clear_screen()
        print("\n===== 战斗确认 =====\n")
        
        print("队伍A角色:")
        for idx in team_a_indices:
            print(f"- {available_characters[idx]['name']}")
        
        print("\n队伍B角色:")
        for idx in team_b_indices:
            print(f"- {available_characters[idx]['name']}")
        
        print("\n确认开始战斗? (y/n)")
        while True:
            confirm = input("> ").strip().lower()
            if confirm == 'y':
                return (team_a_indices, team_b_indices)
            elif confirm == 'n':
                return self.show_battle_setup_menu(available_characters)
            else:
                print("请输入 'y' 确认或 'n' 重新选择。")
    
    def show_character_list(self, characters: List[Dict[str, Any]]) -> None:
        """显示角色列表
        
        Args:
            characters: 角色列表
        """
        self.clear_screen()
        print("\n===== 角色列表 =====\n")
        
        for i, character in enumerate(characters):
            print(f"\n{i+1}. {character['name']}")
            print(f"   HP: {character['hp']}/{character['max_hp']}")
            print(f"   查克拉: {character['chakra']}/{character['max_chakra']}")
            print(f"   攻击力: {character['attack']}")
            print(f"   防御力: {character['defense']}")
            print(f"   速度: {character['speed']}")
            
            if character.get('skills'):
                print("   技能:")
                for skill in character['skills']:
                    print(f"   - {skill['name']}: {skill['description']}")
        
        print("\n按Enter键返回主菜单...")
        input()
    
    def show_help(self) -> None:
        """显示帮助信息"""
        self.clear_screen()
        print("\n===== 帮助信息 =====\n")
        
        print("战斗系统说明:")
        print("1. 回合制战斗 - 每个角色按照速度顺序依次行动")
        print("2. 技能系统 - 使用查克拉施放忍术，每回合开始会恢复部分查克拉")
        print("3. 状态效果 - 角色可以受到各种状态效果的影响，如中毒、灼烧等")
        print("4. 连击系统 - 有一定几率触发连击，进行额外的攻击")
        
        print("\n战斗指令:")
        print("- attack/a [目标ID] - 对指定目标进行普通攻击")
        print("- skill/s [技能ID] [目标ID] - 使用指定技能攻击指定目标")
        print("- item/i [道具ID] [目标ID] - 使用指定道具（尚未实现）")
        print("- pass/p - 跳过当前回合")
        print("- status/st - 显示战斗状态")
        print("- help/h - 显示帮助信息")
        
        print("\n按Enter键返回主菜单...")
        input()
    
    def show_exit_confirmation(self) -> bool:
        """显示退出确认对话框
        
        Returns:
            如果用户确认退出返回True，否则返回False
        """
        self.clear_screen()
        print("\n确定要退出游戏吗? (y/n)")
        
        while True:
            choice = input("> ").strip().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("请输入 'y' 确认退出或 'n' 取消。")
    
    def show_battle_result(self, winner_name: str, rounds: int) -> None:
        """显示战斗结果
        
        Args:
            winner_name: 获胜队伍名称
            rounds: 战斗回合数
        """
        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"战斗结束！{winner_name} 在第 {rounds} 回合获胜！")
        print("=" * 60)
        
        print("\n按Enter键继续...")
        input() 