import pygame
import time
from Queue import queue

def bfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    position_queue = queue()
    path_queue = queue()

    position_queue.enqueue(start)
    path_queue.enqueue([start])
    visited = [start]

    while not position_queue.isEmpty():
        current = position_queue.dequeue()
        path = path_queue.dequeue()

        if current == goal:
            return path

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx = x + dx
            ny = y + dy
            nextPostion = (nx, ny)

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and nextPostion not in visited:
                position_queue.enqueue(nextPostion)
                path_queue.enqueue(path + [nextPostion])
                visited.append(nextPostion)
    return None

pygame.init()

grid = [
    [0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 165, 0)

CELL_SIZE = 60
ROWS = len(grid)
COLS = len(grid[0])
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 100

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🤖 Robot BFS Pathfinding 🤖")
font = pygame.font.Font(None, 35)
robot_img = pygame.image.load(r"C:/home/zeyad/Downloads/Ai final project/7masa_ElRobot.jpg")
robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

def draw_buttons():
    start_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 50, 100, 35)
    restart_rect = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 50, 100, 35)

    pygame.draw.rect(win, WHITE, start_rect)
    pygame.draw.rect(win, WHITE, restart_rect)

    pygame.draw.rect(win, GREEN, start_rect, 4)
    pygame.draw.rect(win, YELLOW, restart_rect, 4)

    start_text = font.render("Start", True, BLACK)
    restart_text = font.render("Restart", True, BLACK)

    win.blit(start_text, (start_rect.x + 23, start_rect.y + 5))
    win.blit(restart_text, (restart_rect.x + 10, restart_rect.y + 5))

    return start_rect, restart_rect

def draw_grid(path, robot_pos, start, goal, robot_index):
    win.fill(GREY)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREY if grid[row][col] == 0 else BLACK
            pygame.draw.rect(win, color, rect)
            pygame.draw.rect(win, WHITE, rect, 1)

    if start:
        pygame.draw.rect(win, GREEN, pygame.Rect(start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if goal:
        pygame.draw.rect(win, RED, pygame.Rect(goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if robot_pos:
        win.blit(robot_img, (robot_pos[1] * CELL_SIZE, robot_pos[0] * CELL_SIZE))

    steps_text = font.render(f"Steps: {max(0, robot_index - 1)}", True, BLACK)
    win.blit(steps_text, (10, HEIGHT - 85))
    draw_buttons()
    pygame.display.update()

def main():
    start = None
    goal = None
    robot_pos = None
    robot_index = 0
    start_clicked = False

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < ROWS * CELL_SIZE:
                    col = mouse_pos[0] // CELL_SIZE
                    row = mouse_pos[1] // CELL_SIZE
                    if grid[row][col] == 0:
                        if start is None:
                            start = (row, col)
                        elif goal is None and (row, col) != start:
                            goal = (row, col)
                else:
                    start_rect, restart_rect = draw_buttons()
                    if start_rect.collidepoint(mouse_pos) and start and goal:
                        path = bfs(grid, start, goal)
                        robot_index = 0
                        start_clicked = True

                    elif restart_rect.collidepoint(mouse_pos):
                        start = None
                        goal = None
                        path = []
                        robot_index = 0
                        start_clicked = False
                        robot_pos = None

        if start_clicked and robot_index < len(path):
            robot_pos = path[robot_index]
            draw_grid(path, robot_pos, start, goal, robot_index)
            robot_index += 1
            time.sleep(0.3)
        elif start_clicked and path:
            draw_grid(path, path[-1], start, goal, robot_index)
        else:
            draw_grid([], robot_pos, start, goal, robot_index)

    pygame.quit()


main()

