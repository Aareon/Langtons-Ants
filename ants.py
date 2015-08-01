import pygame, random
from pygame.locals import *

class AntGrid(object):
    
    def __init__(self, screen, width, height):
        
        self.screen = screen
        self.width = width
        self.height = height        
        self.clear()
    
    def clear(self):
        
        self.rows = []
        for col_no in xrange(self.height):
            new_row = []
            self.rows.append(new_row)
            for row_no in xrange(self.width):
                new_row.append((0, 0, 0))
        self.screen.fill((0, 0, 0))
    
    # Swaps grid pixels from black to color or color to black
    def colorswap(self, x, y, color):  
        if self.rows[y][x] == (0, 0, 0):
            self.rows[y][x] = color
            self.screen.set_at((x, y), color)
        else:
            self.rows[y][x] = (0, 0, 0)
            self.screen.set_at((x, y), (0, 0, 0))
    
    def get(self, x, y):
        return self.rows[y][x]
  
class Ant(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, x, y, color, direction):
        
        self.grid = grid
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        
        
    def move(self):
                
        self.grid.colorswap(self.x, self.y, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height        
                        
        if self.grid.get(self.x, self.y) == (0, 0, 0):
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4                
        
        
    def render(self, surface, grid_size):
        
        grid_w, grid_h = grid_size        
        
def run():

    pygame.init()

    GRID_SIZE = (600, 600)
    GRID_SQUARE_SIZE = (1, 1)
    ITERATIONS = 1

    w = GRID_SIZE[0] * GRID_SQUARE_SIZE[0]
    h = GRID_SIZE[1] * GRID_SQUARE_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)    
    
    ants = []
    grid = AntGrid(screen, *GRID_SIZE)
    running = False
    
    total_iterations = 0
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                return
            
            if event.type == MOUSEBUTTONDOWN:
                
                x, y = event.pos
                x /= GRID_SQUARE_SIZE[0]
                y /= GRID_SQUARE_SIZE[1]                
                
                NewColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                ant = Ant(grid, int(x), int(y), NewColor , random.randint(0,3))
                grid.colorswap(x, y, ant.color)
                ants.append(ant)
                    
            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:                
                    running = not running
                    
                if event.key == K_c:
                    grid.clear()
                    total_iterations = 0
                    del ants[:]

                if event.key == K_KP_MINUS and ITERATIONS>1:
                    ITERATIONS = ITERATIONS / 10

                if event.key == K_KP_PLUS and ITERATIONS<10000:
                    ITERATIONS = ITERATIONS * 10
                
        #grid.render(screen, GRID_SQUARE_SIZE)
    
        if running:
            for iteration_no in xrange(ITERATIONS):        
                for ant in ants:
                    ant.move()
            total_iterations += ITERATIONS
            
        #txt = "%i iterations"%total_iterations
        #txt_surface = font.render("Running: %i iterations"%total_iterations, True, (255, 255, 255))
        #screen.blit(txt_surface, (0, 0))

        for ant in ants:
            ant.render(screen, GRID_SQUARE_SIZE)
            
    
        pygame.display.update()
    
if __name__ == "__main__":
    run()
            