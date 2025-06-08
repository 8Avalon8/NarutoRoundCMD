from typing import Dict, List, Callable, Any


class EventSystem:
    """事件系统，用于处理游戏中的各种事件"""
    
    def __init__(self):
        """初始化事件系统"""
        self._listeners: Dict[str, List[Callable[..., Any]]] = {}
    
    def add_listener(self, event_name: str, callback: Callable[..., Any]) -> None:
        """添加事件监听器
        
        Args:
            event_name: 事件名称
            callback: 事件回调函数
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        
        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)
    
    def remove_listener(self, event_name: str, callback: Callable[..., Any]) -> bool:
        """移除事件监听器
        
        Args:
            event_name: 事件名称
            callback: 要移除的事件回调函数
            
        Returns:
            是否成功移除
        """
        if event_name in self._listeners and callback in self._listeners[event_name]:
            self._listeners[event_name].remove(callback)
            return True
        return False
    
    def clear_listeners(self, event_name: str = None) -> None:
        """清除指定事件或所有事件的监听器
        
        Args:
            event_name: 要清除的事件名称，如果为None则清除所有事件监听器
        """
        if event_name is None:
            self._listeners.clear()
        elif event_name in self._listeners:
            del self._listeners[event_name]
    
    def dispatch(self, event_name: str, *args, **kwargs) -> None:
        """触发指定事件，调用所有监听该事件的回调函数
        
        Args:
            event_name: 要触发的事件名称
            *args: 传递给回调函数的位置参数
            **kwargs: 传递给回调函数的关键字参数
        """
        if event_name in self._listeners:
            # 复制一份监听器列表，以防在回调过程中列表被修改
            listeners = list(self._listeners[event_name])
            for callback in listeners:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in event listener: {e}")
    
    def has_listeners(self, event_name: str) -> bool:
        """判断指定事件是否有监听器
        
        Args:
            event_name: 事件名称
            
        Returns:
            如果有至少一个监听器返回True，否则返回False
        """
        return event_name in self._listeners and len(self._listeners[event_name]) > 0
    
    def get_listener_count(self, event_name: str) -> int:
        """获取指定事件的监听器数量
        
        Args:
            event_name: 事件名称
            
        Returns:
            监听器数量
        """
        if event_name in self._listeners:
            return len(self._listeners[event_name])
        return 0


# 全局事件系统实例
global_event_system = EventSystem() 