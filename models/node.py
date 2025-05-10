
from typing import Optional

class Node:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.g = float('inf')  # 从起点到当前节点的实际距离
        self.h = 0  # 启发式距离
        self.f = float('inf')  # 总代价 f = g + h
        self.parent: Optional['Node'] = None  # 路径回溯
        self.is_wall = False  # 是否是障碍物

    def __lt__(self, other):
        return self.f < other.f
