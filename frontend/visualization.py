
import pygame
from typing import List
from models.node import Node

# 颜色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# 网格参数
GRID_SIZE = 40
MARGIN = 1

class Visualizer:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.width = cols * (GRID_SIZE + MARGIN) + MARGIN
        self.height = rows * (GRID_SIZE + MARGIN) + MARGIN
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A*算法可视化演示")
    
    def draw_grid(self, grid: List[List[Node]], start: Node, end: Node, path: List[Node], current_node: Node = None) -> None:
        """
        绘制网格和路径

        Args:
            grid (List[List[Node]]): 网格，由Node对象的二维列表组成
            start (Node): 起点节点
            end (Node): 终点节点
            path (List[Node]): 路径，由Node对象的列表组成
            current_node (Node, optional): 当前算法正在考虑的节点，默认为None

        Returns:
            None

        绘制网格和路径到屏幕上。
        首先绘制基础网格节点，根据节点类型使用不同颜色表示：
        - 白色表示普通节点
        - 绿色表示起点
        - 红色表示终点
        - 深蓝色表示路径上的节点
        - 黑色表示墙壁节点

        如果提供了current_node参数，则绘制当前路径（浅蓝色）和当前节点（黄色），并确保当前节点位于最上层显示。

        使用pygame库进行图形绘制，并在每次绘制后刷新屏幕并稍作延迟。
        """
        
        self.screen.fill(WHITE)
        
        # 1. 先绘制基础网格节点
        for row in grid:
            for node in row:
                color = WHITE
                if node == start:
                    color = GREEN
                elif node == end:
                    color = RED
                elif node in path:
                    color = BLUE  # 最终路径保持深蓝色
                elif node.is_wall:
                    color = BLACK
                
                pygame.draw.rect(self.screen, color, [
                    node.col * (GRID_SIZE + MARGIN),
                    node.row * (GRID_SIZE + MARGIN),
                    GRID_SIZE,
                    GRID_SIZE
                ])
        
        # 2. 然后绘制当前路径（浅蓝色）
        if current_node:
            current_path = []
            temp = current_node
            while temp:
                current_path.append(temp)
                temp = temp.parent
            for node in current_path:
                if node != start and node != end and node not in path:  # 避免覆盖关键节点
                    pygame.draw.rect(self.screen, (173, 216, 230), [  # 浅蓝色
                        node.col * (GRID_SIZE + MARGIN),
                        node.row * (GRID_SIZE + MARGIN),
                        GRID_SIZE,
                        GRID_SIZE
                    ])
        
        # 3. 最后绘制当前节点（黄色）确保最上层显示
        if current_node:
            pygame.draw.rect(self.screen, YELLOW, [
                current_node.col * (GRID_SIZE + MARGIN),
                current_node.row * (GRID_SIZE + MARGIN),
                GRID_SIZE,
                GRID_SIZE
            ])
        
        pygame.display.flip()
        pygame.time.delay(50)  # 增加短暂延迟
