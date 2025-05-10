
import heapq
from typing import List, Tuple, Optional
from models.node import Node
import pygame  # 添加pygame导入

def heuristic(node: Node, end_node: Node) -> float:
    """计算启发式距离(曼哈顿距离)"""
    return abs(node.row - end_node.row) + abs(node.col - end_node.col)

def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
    """获取相邻节点"""
    neighbors = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4方向移动
        r, c = node.row + dr, node.col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            neighbors.append(grid[r][c])
    return neighbors

def reconstruct_path(current: Node) -> List[Node]:
    """重建路径"""
    path = []
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]

def initialize_grid(rows: int, cols: int) -> List[List[Node]]:
    """初始化网格"""
    return [[Node(r, c) for c in range(cols)] for r in range(rows)]

def a_star(grid: List[List[Node]], start: Node, end: Node, visualizer=None) -> List[Node]:
    """
    使用A*算法寻找从起点到终点的最短路径。

    Args:
        grid (List[List[Node]]): 网格地图，由Node对象组成的二维列表。
        start (Node): 起点Node对象。
        end (Node): 终点Node对象。
        visualizer (Visualizer, optional): 可视化器对象，用于在算法执行过程中显示网格地图和路径。默认为None，不使用可视化。

    Returns:
        List[Node]: 从起点到终点的最短路径，由Node对象组成的列表。如果找不到路径，则返回空列表。

    """
    
    open_set = []
    heapq.heappush(open_set, (start.f, start))
    
    start.g = 0
    start.h = heuristic(start, end)
    start.f = start.g + start.h
    
    # 初始可视化
    if visualizer:
        visualizer.draw_grid(grid, start, end, [], start)
        pygame.time.delay(200)  # 初始延迟稍长
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if visualizer:
            visualizer.draw_grid(grid, start, end, [], current)
            pygame.time.delay(100)  # 添加延迟使可视化更清晰
        
        if current == end:
            path = reconstruct_path(current)
            if visualizer:
                visualizer.draw_grid(grid, start, end, path)
            return path
        
        for neighbor in get_neighbors(grid, current):
            if neighbor.is_wall:
                continue
                
            tentative_g = current.g + 1
            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(open_set, (neighbor.f, neighbor))
                if visualizer:
                    visualizer.draw_grid(grid, start, end, [], current)
                    pygame.time.delay(50)
    
    return []  # 无路径
