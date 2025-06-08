import logging
import os
import sys
from datetime import datetime
from typing import Optional


class GameLogger:
    """游戏日志工具类"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, log_file: Optional[str] = None, log_level: int = logging.INFO):
        """初始化日志工具
        
        Args:
            log_file: 日志文件路径，如果为None则使用默认路径
            log_level: 日志级别
        """
        # 避免重复初始化
        if self._initialized:
            return
            
        # 设置默认日志文件
        if log_file is None:
            log_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = os.path.join(log_dir, f'game_{timestamp}.log')
        
        # 配置日志记录器
        self.logger = logging.getLogger('naruto_battle')
        self.logger.setLevel(log_level)
        
        # 清除现有处理器
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        
        # 添加文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # 添加控制台处理器（仅在调试模式下）
        if log_level <= logging.DEBUG:
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(console_handler)
        
        self.log_file = log_file
        self._initialized = True
    
    def debug(self, message: str) -> None:
        """记录调试级别日志
        
        Args:
            message: 日志消息
        """
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录信息级别日志
        
        Args:
            message: 日志消息
        """
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告级别日志
        
        Args:
            message: 日志消息
        """
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录错误级别日志
        
        Args:
            message: 日志消息
        """
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录严重错误级别日志
        
        Args:
            message: 日志消息
        """
        self.logger.critical(message)
    
    def log_battle_action(self, character_name: str, action_type: str, target_name: str = None, details: str = None) -> None:
        """记录战斗动作
        
        Args:
            character_name: 执行动作的角色名称
            action_type: 动作类型
            target_name: 动作目标的名称
            details: 额外的详细信息
        """
        message = f"战斗动作: {character_name} 执行了 {action_type}"
        if target_name:
            message += f" 目标: {target_name}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_battle_event(self, event_type: str, details: str = None) -> None:
        """记录战斗事件
        
        Args:
            event_type: 事件类型
            details: 事件详细信息
        """
        message = f"战斗事件: {event_type}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_error_event(self, event_type: str, error: Exception) -> None:
        """记录错误事件
        
        Args:
            event_type: 事件类型
            error: 错误对象
        """
        message = f"错误事件: {event_type} - {str(error)}"
        self.error(message)


# 全局日志工具实例
game_logger = GameLogger() 