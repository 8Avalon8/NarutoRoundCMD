import json
import os
from typing import Dict, Any, Optional


class GameConfig:
    """游戏配置类，用于管理游戏设置"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_file: Optional[str] = None):
        """初始化游戏配置
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        # 避免重复初始化
        if self._initialized:
            return
            
        # 设置默认配置文件路径
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), 'game_settings.json')
        
        self.config_file = config_file
        self._config_data = {}
        
        # 加载配置
        self.load_config()
        
        # 如果配置为空，设置默认配置
        if not self._config_data:
            self._set_default_config()
            self.save_config()
        
        self._initialized = True
    
    def load_config(self) -> bool:
        """从文件加载配置
        
        Returns:
            加载是否成功
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                return True
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
        return False
    
    def save_config(self) -> bool:
        """保存配置到文件
        
        Returns:
            保存是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键
            default: 如果键不存在时返回的默认值
            
        Returns:
            配置值
        """
        return self._config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._config_data[key] = value
    
    def _set_default_config(self) -> None:
        """设置默认配置"""
        self._config_data = {
            "game": {
                "name": "火影忍者OL战斗系统",
                "version": "1.0.0",
                "debug_mode": False,
                "language": "zh_CN"
            },
            "battle": {
                "animation_speed": 0.5,
                "enable_animations": True,
                "default_team_size": 3,
                "max_rounds": 50,
                "chakra_regen_rate": 10,  # 每回合恢复的查克拉百分比
                "combo_base_chance": 0.05,  # 基础连击几率
                "combo_speed_factor": 0.001  # 速度对连击几率的影响因子
            },
            "display": {
                "show_damage_numbers": True,
                "show_status_effects": True,
                "use_colors": True,
                "clear_screen": True
            },
            "audio": {
                "enable_sound": False,
                "volume": 0.5,
                "music_volume": 0.3,
                "effects_volume": 0.7
            },
            "data": {
                "save_battle_logs": True,
                "auto_save": True,
                "log_level": "INFO"
            }
        }
    
    def get_battle_config(self) -> Dict[str, Any]:
        """获取战斗相关配置
        
        Returns:
            战斗配置字典
        """
        return self._config_data.get("battle", {})
    
    def get_display_config(self) -> Dict[str, Any]:
        """获取显示相关配置
        
        Returns:
            显示配置字典
        """
        return self._config_data.get("display", {})
    
    def get_data_config(self) -> Dict[str, Any]:
        """获取数据相关配置
        
        Returns:
            数据配置字典
        """
        return self._config_data.get("data", {})


# 全局配置实例
game_config = GameConfig() 