
import pygame
from typing import List
from models.node import Node
from algorithm.a_star import a_star, initialize_grid
from frontend.visualization import Visualizer, GRID_SIZE, MARGIN

def generate_random_obstacles(grid: List[List[Node]], start: Node, end: Node, density: float = 0.25) -> None:
    """随机生成障碍物
    Args:
        density: 障碍物密度(0-1)
    """
    import random
    for row in grid:
        for node in row:
            if node != start and node != end and random.random() < density:
                node.is_wall = True

def main():
    """主程序"""
    pygame.init()
    
    # 网格尺寸
    ROWS, COLS = 15, 20
    
    # 初始化界面
    visualizer = Visualizer(ROWS, COLS)
    
    # 初始化网格
    grid = initialize_grid(ROWS, COLS)
    start = grid[0][0]
    end = grid[ROWS-1][COLS-1]
    
    # 生成随机障碍物
    generate_random_obstacles(grid, start, end)
    
    running = True
    path = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = a_star(grid, start, end, visualizer)
                elif event.key == pygame.K_r:  # 按R键重新生成障碍物
                    # 保存当前起点和终点
                    start_pos = (start.row, start.col)
                    end_pos = (end.row, end.col)
                    # 重置网格
                    grid = initialize_grid(ROWS, COLS)
                    # 恢复起点和终点
                    start = grid[start_pos[0]][start_pos[1]]
                    end = grid[end_pos[0]][end_pos[1]]
                    # 生成随机障碍物(会自动避开起点和终点)
                    generate_random_obstacles(grid, start, end)
                    path = []  # 清除路径
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (GRID_SIZE + MARGIN)
                row = pos[1] // (GRID_SIZE + MARGIN)
                
                if 0 <= row < ROWS and 0 <= col < COLS:
                    node = grid[row][col]
                    if event.button == 1:  # 左键设置障碍
                        node.is_wall = not node.is_wall
                    elif event.button == 3:  # 右键设置起点/终点
                        if node != start and node != end:
                            if start == grid[0][0]:
                                start = node
                            else:
                                end = node
        
        visualizer.draw_grid(grid, start, end, path)
    
    pygame.quit()

if __name__ == "__main__":
    main()
