# imports
import pygame
import random
import math

# colors
BACKGROUND_COLOR = pygame.Color("#faf8ef")
DARK_TEXT_COLOR = pygame.Color("#776e65")
LIGHT_TEXT_COLOR = pygame.Color("#f9f6f2")
GRID_COLOR = pygame.Color("#bbada0")
BUTTON_COLOR = pygame.Color("#8f7a66")
BUTTON_COLOR_HLGHT = pygame.Color("#aa9888")
EMPTY_TILE_COLOR = pygame.Color("#cdc1b4")
EXTRA_TILE_COLOR = pygame.Color("#3e3933")

# may add colors if wanted
TILE_COLORS = {
    0: EMPTY_TILE_COLOR,
    2: pygame.Color("#eee4da"),
    4: pygame.Color("#eee1c9"),
    8: pygame.Color("#f3b27a"),
    16: pygame.Color("#f69664"),
    32: pygame.Color("#f77c5f"),
    64: pygame.Color("#f75f3b"),
    128: pygame.Color("#edd073"),
    256: pygame.Color("#edcc62"),
    512: pygame.Color("#edc850"),
    1024: pygame.Color("#edc53f"),
    2048: pygame.Color("#edc22e")
}

class Layout:
    button_hlght: bool
    screen: pygame.Surface
    board: list[list[int]]

    # locations + dimensions, stored as pygame rects
    board_rect: pygame.rect
    button_box_rect: pygame.rect
    score_box_rect: pygame.rect
    high_score_box_rect: pygame.rect

    # sizes and offsets, stored as floats
    height: float
    width: float
    tile_size: float
    edge_border_size: float
    border_size: float

    # locations for text, stored as size 2 tuples of floats
    title_text_pos: tuple[float, float]
    button_text_pos: tuple[float, float]
    score_title_text_pos: tuple[float, float]
    high_score_title_text_pos: tuple[float, float]
    score_text_pos: tuple[float, float]
    high_score_text_pos: tuple[float, float] # todo

    # rendered text, stored as pygame images
    title_text: pygame.image
    button_text: pygame.image
    score_title_text: pygame.image
    high_score_title_text: pygame.image
    score_text: pygame.image
    high_score_text: pygame.image # todo

    # font for the score and high score
    score_font: pygame.font

    tile_text: dict[int, pygame.Surface] = {}

    def __init__(self, screen: pygame.Surface, board: list[list[int]]):
        self.button_hlght = False
        self.screen = screen
        self.board = board
        self.resize()

    def change_board(self, board: list[list[int]]):
        self.board = board
        self.resize()

    def resize(self):
        # clear cached tile text
        self.tile_text.clear()

        # get number of tiles in row/column of board
        num_tiles = len(self.board)

        # get new screen dimensions
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()

        # find the smaller dimension
        min_dim = min(self.height, self.width)

        # calculate border size
        self.edge_border_size = min_dim / 40

        # calculate top padding
        top_pad = 5 * self.edge_border_size

        # calculate border_size, the spacing between tiles
        self.border_size = min_dim / (15 * num_tiles)

        # calculate board size and location
        board_size_height_limited = self.height - top_pad - self.edge_border_size
        board_size_width_limited = self.width - 2 * self.edge_border_size
        board_size = min(board_size_width_limited, board_size_height_limited)

        board_off_x = (self.width - board_size) / 2
        self.board_rect = pygame.Rect(board_off_x, top_pad, board_size, board_size)

        # calculate tile size
        self.tile_size = (board_size - (num_tiles + 1) * self.border_size) / num_tiles

        # calculate title position
        title_off_y = top_pad - top_pad + self.edge_border_size
        self.title_text_pos = (board_off_x, title_off_y)

        # create title text surface
        title_font = pygame.font.Font(pygame.font.get_default_font(), int(3 * self.edge_border_size))
        self.title_text = title_font.render(pygame.display.get_caption()[0], True, DARK_TEXT_COLOR)

        # create new game button text surface
        button_font = pygame.font.Font(pygame.font.get_default_font(), int(1.1 * self.edge_border_size))
        self.button_text = button_font.render("New Game", True, LIGHT_TEXT_COLOR)

        # create score and high score text surfaces
        font = pygame.font.Font(pygame.font.get_default_font(), int(self.edge_border_size))
        self.score_title_text = font.render("Score", True, LIGHT_TEXT_COLOR)
        self.high_score_title_text = font.render("High Score", True, LIGHT_TEXT_COLOR)

        # calculate new game button box dimensions
        # score and high score boxs share the same dimensions
        button_width = (board_size - self.title_text.get_width()) / 3 - self.edge_border_size
        button_height = 3 * self.edge_border_size

        # calculate x positions of button, score box, and high score box
        button_box_x_pos = board_off_x + self.title_text.get_width() + self.edge_border_size
        score_box_x_pos = button_box_x_pos + (self.edge_border_size + button_width)
        high_score_box_x_pos = score_box_x_pos + (self.edge_border_size + button_width)

        # create new game button, score, and high score box rects
        self.button_box_rect = pygame.Rect(button_box_x_pos, self.edge_border_size, button_width, button_height)
        self.score_box_rect = pygame.Rect(score_box_x_pos, self.edge_border_size, button_width, button_height)
        self.high_score_box_rect = pygame.Rect(high_score_box_x_pos, self.edge_border_size, button_width, button_height)

        # create new game button, score title, and high score title text position tuples
        button_text_pos_x = button_box_x_pos + (button_width - self.button_text.get_width()) / 2
        button_text_pos_y = self.edge_border_size + (button_height - self.button_text.get_height()) / 2
        self.button_text_pos = (button_text_pos_x, button_text_pos_y)

        score_title_text_pos_x = score_box_x_pos + (button_width - self.score_title_text.get_width()) / 2
        score_title_text_pos_y = 1.25 * self.edge_border_size
        self.score_title_text_pos = (score_title_text_pos_x, score_title_text_pos_y)

        high_score_title_text_pos_x = high_score_box_x_pos + (button_width - self.high_score_title_text.get_width()) / 2
        high_score_title_text_pos_y = 1.25 * self.edge_border_size
        self.high_score_title_text_pos = (high_score_title_text_pos_x, high_score_title_text_pos_y)

        # create score and high score font and score text surface
        self.score_font = pygame.font.Font(pygame.font.get_default_font(), int(1.25 * self.edge_border_size))
        
        self.score_text = self.score_font.render(str(score), True, LIGHT_TEXT_COLOR)
        self.high_score_text = self.score_font.render(str(high_score.get(num_tiles)), True, LIGHT_TEXT_COLOR)

        # create score and high score text position tuple
        score_text_pos_x = score_box_x_pos + (button_width - self.score_text.get_width()) / 2
        score_text_pos_y = 2.5 * self.edge_border_size
        self.score_text_pos = (score_text_pos_x, score_text_pos_y)

        high_score_text_pos_x = high_score_box_x_pos + (button_width - self.high_score_text.get_width()) / 2
        self.high_score_text_pos = (high_score_text_pos_x, score_text_pos_y)

    # draws a complete game frame
    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        self.draw_title()
        self.draw_board()

    # updates score_text and score_text_pos
    def update_score_text(self):
        self.score_text = self.score_font.render(str(score), True, LIGHT_TEXT_COLOR)
        pos_x = self.score_box_rect[0] + (self.score_box_rect[2] - self.score_text.get_width()) / 2
        pos_y = 2.5 * self.edge_border_size
        self.score_text_pos = (pos_x, pos_y)

        # update high score if necessary - todo: move this logic elsewhere
        if (score > high_score.get(len(self.board))):
            high_score.update({len(self.board): score})
            self.high_score_text = self.score_font.render(str(score), True, LIGHT_TEXT_COLOR)
            high_pos_x = self.high_score_box_rect[0] + (self.high_score_box_rect[2] - self.high_score_text.get_width()) / 2
            self.high_score_text_pos = (high_pos_x, pos_y)

    # calculates the rect for a tile at the passed coordinates
    def get_tile_rect(self, i: int, j: int) -> pygame.Rect:
        x_pos = self.board_rect[0] + self.border_size + i * (self.border_size + self.tile_size)
        y_pos = self.board_rect[1] + self.border_size + j * (self.border_size + self.tile_size)
        return pygame.Rect(x_pos, y_pos, self.tile_size, self.tile_size)
    
    # calculates the position to center text on a tile
    def get_tile_text_pos(self, tile_rect: pygame.rect, text: pygame.Surface) -> tuple[float, float]:
        x_pos = tile_rect[0] + (tile_rect[2] - text.get_width()) / 2
        y_pos = tile_rect[1] + (tile_rect[3] - text.get_height()) / 2
        return (x_pos, y_pos)

    # draw board and tiles based on game state
    def draw_board(self):
        # get size of board
        size = len(self.board)

        # draw board backdrop which becomes the grid around the tiles
        pygame.draw.rect(self.screen, GRID_COLOR, self.board_rect)

        # draw tiles
        for i in range(size):
            for j in range(size):
                # draw square
                tile_rect = self.get_tile_rect(i, j)
                tile_color = TILE_COLORS.get(board[j][i], EXTRA_TILE_COLOR)
                pygame.draw.rect(self.screen, tile_color, tile_rect)
                
                # if tile in this location, draw number
                if board[j][i] != 0:
                    # get text image
                    text = self.tile_text.get(board[j][i])
                    # generate text image if needed
                    if text == None:
                        text = self.create_text(board[j][i])
                        self.tile_text.update({board[j][i]: text})
                    # draw number
                    self.screen.blit(text, self.get_tile_text_pos(tile_rect, text))
    
    # draw title, new game button, score, and high score
    def draw_title(self):
        screen.blit(self.title_text, self.title_text_pos)
        button_color = BUTTON_COLOR_HLGHT if self.button_hlght else BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, self.button_box_rect)
        pygame.draw.rect(self.screen, TILE_COLORS.get(0), self.score_box_rect)
        pygame.draw.rect(self.screen, TILE_COLORS.get(0), self.high_score_box_rect)
        screen.blit(self.button_text, self.button_text_pos)
        screen.blit(self.score_title_text, self.score_title_text_pos)
        screen.blit(self.high_score_title_text, self.high_score_title_text_pos)
        screen.blit(self.score_text, self.score_text_pos)
        screen.blit(self.high_score_text, self.high_score_text_pos)

    def create_text(self, num: int) -> pygame.Surface:
        tile_color = TILE_COLORS.get(num, EXTRA_TILE_COLOR)
        if tile_color[0] * 0.299 + tile_color[1] * 0.587 + tile_color[2] * 0.114 > 210:
            color = DARK_TEXT_COLOR
        else:
            color = LIGHT_TEXT_COLOR
        
        if int(math.log10(num)) >= 3:
            font_scaling_factor = 0.35 * int(math.log10(num))
        else:
            font_scaling_factor = 0

        font = pygame.font.Font(None, int(self.tile_size / (2.5 + font_scaling_factor)))
        return font.render(str(num), True, color)


# spawns a tile in a random position on the passed board
# 90% chance for a 2 tile, 10% for a 4
# do not call on a full board, will result in an infinite loop
def spawn_tile(board: list[list[int]]):
    sz = len(board) - 1
    x = random.randint(0, sz)
    y = random.randint(0, sz)
    while board[x][y] != 0:
        x = random.randint(0, sz)
        y = random.randint(0, sz)
    board[x][y] = 2 if random.random() < 0.9 else 4
        
# slides all tiles to the left
def move(board: list[list[int]]) -> bool:
    size = len(board)
    changed = False
    for i in range(size):
        pos = -1
        for j in range(size):
            if board[i][j] == 0 and pos == -1:
                pos = j
            elif board[i][j] != 0 and pos >= 0:
                board[i][pos] = board[i][j]
                board[i][j] = 0
                pos += 1
                changed = True
    return changed

# merges tiles to the left
def merge(board: list[list[int]]) -> bool:
    global score
    size = len(board)
    changed = False
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                board[i][j] *= 2
                board[i][j + 1] = 0
                score += board[i][j]
                changed = True
    return changed

# reverses the board along the horizontal axis
def reverse(board: list[list[int]]):
    size = len(board)
    for i in range(size):
        for j in range(size // 2):
            temp = board[i][j]
            board[i][j] = board[i][size - 1 - j]
            board[i][size - 1 - j] = temp

# takes the transpose of the board in place
def transpose(board: list[list[int]]):
    size = len(board)
    for i in range(size):
        for j in range(i):
            temp = board[i][j]
            board[i][j] = board[j][i]
            board[j][i] = temp

# checks if the game is over
# if board is full and no merges are possible
def is_game_over(board: list[list[int]]) -> bool:
    size = len(board)
    # check if board is full
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return False
    # checks if merges are possible
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] == board[i][j + 1]:
                return False
            if board[j][i] == board[j + 1][i]:
                return False

    return True

# makes a move: dir='u' for up, 'd' for down 'r' for right, 'l' for left
def make_move(board: list[list[int]], dir: str):
    global score_text, score_text_pos
    changed = False
    if dir == 'u' or dir == 'd':
        transpose(board)
    if dir == 'd' or dir =='r':
        reverse(board)

    changed = changed or move(board)
    changed_im = merge(board)
    changed = changed or changed_im

    if changed_im == True:
        move(board)
    
    if dir == 'd' or dir =='r':
        reverse(board)
    if dir == 'u' or dir == 'd':
        transpose(board)

    if changed:
        spawn_tile(board)
        layout.update_score_text()

# create a board of passed size with 2 initial tiles
def create_board(size: int) -> list[list[int]]:
    new_board = [[0] * size for i in range(size)]
    spawn_tile(new_board)
    spawn_tile(new_board)
    return new_board

# pygame setup
pygame.init()
screen = pygame.display.set_mode((660, 720), pygame.RESIZABLE)
pygame.display.set_caption('2048')
clock = pygame.time.Clock()
running = True

# setup
size = 4
score = 0
board = create_board(size)

# best score for each size
high_score: dict[int, int] = {}
high_score.update({size: 0})

layout = Layout(screen, board)

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            layout.resize()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    make_move(board, 'u')
                case pygame.K_s | pygame.K_DOWN:
                    make_move(board, 'd')
                case pygame.K_a | pygame.K_LEFT:
                    make_move(board, 'l')
                case pygame.K_d | pygame.K_RIGHT:
                    make_move(board, 'r')
        elif event.type == pygame.MOUSEMOTION:
            if layout.button_box_rect.collidepoint(event.pos):
                layout.button_hlght = True
            else:
                layout.button_hlght = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if layout.button_box_rect.collidepoint(event.pos):
                board = create_board(size)
                score = 0
                layout.update_score_text()
            
            if is_game_over(board):
                print("game over!")

    layout.draw()

    pygame.display.flip()

    # limit framerate
    clock.tick(60)

pygame.quit()