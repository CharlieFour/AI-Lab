import pygame
import math
import random
from astar import a_star_animated
from grid import create_grid
from utils import clear_path
from ui import Button, Slider

# ==================== CONSTANTS ====================
# Colors
BG_COLOR = (30, 30, 30)
PANEL_COLOR = (45, 45, 45)
GRID_LINE = (60, 60, 60)
START_COLOR = (76, 175, 80)
GOAL_COLOR = (244, 67, 54)
OBSTACLE_COLOR = (50, 50, 50)
VISITED_COLOR = (0, 150, 136)
PATH_COLOR = (255, 235, 59)
HOVER_COLOR = (255, 255, 255, 30)

# UI
FONT_NAME = "Arial"
FONT_SIZE = 16
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 35
PANEL_WIDTH = 300
MARGIN = 20

# ==================== FIXED GRID SIZE ====================
ROWS = 20
COLS = 30
CELL_SIZE = 30  # will be recalculated based on screen size

# ==================== INITIAL SETUP ====================
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = min(1400, info.current_w - 100)
SCREEN_HEIGHT = min(800, info.current_h - 100)
GRID_WIDTH = SCREEN_WIDTH - PANEL_WIDTH - 3 * MARGIN
# Recalculate cell size to fit grid area
max_cell_w = GRID_WIDTH // COLS
max_cell_h = (SCREEN_HEIGHT - 2 * MARGIN) // ROWS
CELL_SIZE = min(max_cell_w, max_cell_h, 40)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
small_font = pygame.font.SysFont(FONT_NAME, 12)

# Grid surface
grid_surface = pygame.Surface((GRID_WIDTH, SCREEN_HEIGHT - 2 * MARGIN))
grid_rect = grid_surface.get_rect(topleft=(MARGIN, MARGIN))

# ==================== GLOBALS ====================
grid = create_grid(ROWS, COLS)
start = None
goal = None
mode = "obstacle"          # start, goal, obstacle, erase
animating = False
animation_gen = None
step_mode = False
heuristic = "manhattan"    # or "euclidean"
hover_cell = None
error_message = ""

stats = {
    'nodes_visited': 0,
    'path_length': 0
}

# ==================== UI ELEMENTS ====================
panel_x = SCREEN_WIDTH - PANEL_WIDTH - MARGIN
panel_y = MARGIN

# Mode buttons
mode_buttons = [
    Button(panel_x, panel_y + i * (BUTTON_HEIGHT + 5), BUTTON_WIDTH, BUTTON_HEIGHT, text)
    for i, text in enumerate(["Start", "Goal", "Obstacle", "Erase"])
]

# Action buttons (two columns)
action_buttons = [
    Button(panel_x, panel_y + 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Run"),
    Button(panel_x + BUTTON_WIDTH + 10, panel_y + 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Step"),
    Button(panel_x, panel_y + 200 + BUTTON_HEIGHT + 5, BUTTON_WIDTH, BUTTON_HEIGHT, "Clear Path"),
    Button(panel_x + BUTTON_WIDTH + 10, panel_y + 200 + BUTTON_HEIGHT + 5, BUTTON_WIDTH, BUTTON_HEIGHT, "Reset"),
]

# Heuristic buttons
heuristic_buttons = [
    Button(panel_x, panel_y + 350, 80, 30, "Manhattan"),
    Button(panel_x + 90, panel_y + 350, 80, 30, "Euclidean"),
]

# Sliders
# Speed slider: 0 (left) = slow (200ms), 200 (right) = fast (0ms)
speed_slider = Slider(panel_x, panel_y + 400, 200, 20, 0, 200, 50, "Speed (ms)")
random_slider = Slider(panel_x, panel_y + 500, 200, 20, 0, 100, 20, "Random %")

# Random generate button
random_btn = Button(panel_x + 210, panel_y + 495, 60, 30, "Generate")

# Stats font
stats_font = pygame.font.SysFont(FONT_NAME, 18)

# ==================== HELPER FUNCTIONS ====================
def heuristic_func(a, b):
    if heuristic == "manhattan":
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    else:  # euclidean
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def clear_obstacles():
    """Remove all obstacles but keep start and goal."""
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == '#':
                grid[i][j] = '-'

def draw_grid():
    grid_surface.fill(BG_COLOR)
    cell_w = CELL_SIZE
    cell_h = CELL_SIZE
    for i in range(ROWS):
        for j in range(COLS):
            rect = (j * cell_w, i * cell_h, cell_w, cell_h)
            color = BG_COLOR
            if grid[i][j] == '#':
                color = OBSTACLE_COLOR
            elif grid[i][j] == 'S':
                color = START_COLOR
            elif grid[i][j] == 'G':
                color = GOAL_COLOR
            elif grid[i][j] == 'o':
                color = PATH_COLOR
            elif grid[i][j] == '.':
                color = VISITED_COLOR
            pygame.draw.rect(grid_surface, color, rect)
            pygame.draw.rect(grid_surface, GRID_LINE, rect, 1)
    # Hover effect
    if hover_cell and not animating:
        i, j = hover_cell
        if 0 <= i < ROWS and 0 <= j < COLS:
            s = pygame.Surface((cell_w, cell_h), pygame.SRCALPHA)
            s.fill(HOVER_COLOR)
            grid_surface.blit(s, (j * cell_w, i * cell_h))
    screen.blit(grid_surface, grid_rect.topleft)

def draw_panel():
    # Panel background
    pygame.draw.rect(screen, PANEL_COLOR,
                     (panel_x - 10, panel_y - 10, PANEL_WIDTH, SCREEN_HEIGHT - 2 * MARGIN + 20),
                     border_radius=10)

    # Mode buttons with active highlight
    for btn in mode_buttons:
        btn.draw(screen, font)
        if btn.text.lower() == mode:
            pygame.draw.rect(screen, (100, 100, 255), btn.rect, 3, border_radius=6)

    for btn in action_buttons:
        btn.draw(screen, font)

    # Heuristic buttons
    for btn in heuristic_buttons:
        btn.draw(screen, small_font)
        if btn.text.lower() == heuristic:
            pygame.draw.rect(screen, (100, 100, 255), btn.rect, 2, border_radius=6)

    speed_slider.draw(screen, small_font)
    random_slider.draw(screen, small_font)

    # Random generate button
    random_btn.draw(screen, small_font)

    # Stats (two lines, third for error)
    stats_y = panel_y + 550
    stats_text = [
        f"Nodes visited: {stats['nodes_visited']}",
        f"Path length: {stats['path_length']}"
    ]
    for i, line in enumerate(stats_text):
        surf = stats_font.render(line, True, (200, 200, 200))
        screen.blit(surf, (panel_x, stats_y + i * 25))

    # Error message (replaces time)
    if error_message:
        err_surf = stats_font.render(error_message, True, (255, 100, 100))
        screen.blit(err_surf, (panel_x, stats_y + 2 * 25))

def reset(keep_obstacles=False):
    global start, goal, animating, animation_gen, stats, error_message
    if not keep_obstacles:
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j] = '-'
        start = None
        goal = None
    else:
        # just clear path and visited
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] in ('.', 'o'):
                    grid[i][j] = '-'
    animating = False
    animation_gen = None
    stats = {'nodes_visited': 0, 'path_length': 0}
    error_message = ""

def run_astar():
    global animation_gen, animating, stats, step_mode, error_message
    if not start or not goal:
        error_message = "Set start and goal first!"
        return
    clear_path(grid)   # remove old path/visited from grid
    stats['nodes_visited'] = 0
    stats['path_length'] = 0
    error_message = ""
    animation_gen = a_star_animated(grid, start, goal, ROWS, COLS)
    animating = True
    step_mode = False   # continuous by default

# ==================== MAIN LOOP ====================
running = True
while running:
    dt = clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Update hover cell
    if grid_rect.collidepoint(mouse_pos):
        rel_x = mouse_pos[0] - grid_rect.x
        rel_y = mouse_pos[1] - grid_rect.y
        col = rel_x // CELL_SIZE
        row = rel_y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            hover_cell = (row, col)
        else:
            hover_cell = None
    else:
        hover_cell = None

    # Continuous drawing with mouse down
    if mouse_pressed[0] and not animating and grid_rect.collidepoint(mouse_pos):
        rel_x = mouse_pos[0] - grid_rect.x
        rel_y = mouse_pos[1] - grid_rect.y
        col = rel_x // CELL_SIZE
        row = rel_y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            if mode == "start":
                if start:
                    grid[start[0]][start[1]] = '-'
                start = (row, col)
                grid[row][col] = 'S'
            elif mode == "goal":
                if goal:
                    grid[goal[0]][goal[1]] = '-'
                goal = (row, col)
                grid[row][col] = 'G'
            elif mode == "obstacle":
                if grid[row][col] not in ('S', 'G'):
                    grid[row][col] = '#'
            elif mode == "erase":
                if grid[row][col] not in ('S', 'G'):
                    grid[row][col] = '-'

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass all events to sliders
        speed_slider.handle_event(event)
        random_slider.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Mode buttons
            for btn in mode_buttons:
                if btn.clicked(event.pos):
                    mode = btn.text.lower()

            # Action buttons
            for btn in action_buttons:
                if btn.clicked(event.pos):
                    if btn.text == "Run":
                        run_astar()
                    elif btn.text == "Step":
                        if start and goal:
                            run_astar()
                            step_mode = True
                    elif btn.text == "Clear Path":
                        clear_path(grid)
                        stats['nodes_visited'] = 0
                        stats['path_length'] = 0
                    elif btn.text == "Reset":
                        reset(keep_obstacles=False)

            # Heuristic buttons
            for btn in heuristic_buttons:
                if btn.clicked(event.pos):
                    heuristic = btn.text.lower()

            # Random generation
            if random_btn.clicked(event.pos):
                # Remove all existing obstacles first
                clear_obstacles()
                # Place new obstacles
                density = random_slider.val / 100
                for i in range(ROWS):
                    for j in range(COLS):
                        if grid[i][j] not in ('S', 'G') and random.random() < density:
                            grid[i][j] = '#'
                error_message = ""

    # Animation step
    if animating and animation_gen:
        # Invert speed: slider 0 (left) = 200ms delay, 200 (right) = 0ms delay
        delay = 200 - int(speed_slider.val)
        if delay < 0:
            delay = 0

        if step_mode:
            # Advance one step
            try:
                action, data = next(animation_gen)
                if action == "visit":
                    stats['nodes_visited'] += 1
                    x, y = data
                    if grid[x][y] == '-':
                        grid[x][y] = '.'
                elif action == "path":
                    for (x, y) in data:
                        if grid[x][y] not in ('S', 'G'):
                            grid[x][y] = 'o'
                    stats['path_length'] = len(data)
                    animating = False
                elif action == "fail":
                    error_message = "No path found!"
                    animating = False
                step_mode = False   # pause after one step
            except StopIteration:
                animating = False
                step_mode = False
        else:
            # Continuous animation
            try:
                action, data = next(animation_gen)
                if action == "visit":
                    stats['nodes_visited'] += 1
                    x, y = data
                    if grid[x][y] == '-':
                        grid[x][y] = '.'
                elif action == "path":
                    for (x, y) in data:
                        if grid[x][y] not in ('S', 'G'):
                            grid[x][y] = 'o'
                    stats['path_length'] = len(data)
                    animating = False
                elif action == "fail":
                    error_message = "No path found!"
                    animating = False
                pygame.time.wait(delay)
            except StopIteration:
                animating = False

    # Draw everything
    draw_grid()
    draw_panel()
    pygame.display.flip()

pygame.quit()