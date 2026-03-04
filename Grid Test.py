
import pygame
import heapq

pygame.init()

if __name__ == "__main__":

    ROWS = 5
    COLS = 5
    CELL_SIZE = 100

    HEIGHT = ROWS * CELL_SIZE
    WIDTH = COLS * CELL_SIZE

    #This creates the screen. pygame.draw uses this as a canvas - Jason S
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Color codes - Jason S
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    #Text font - Jason S
    font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    running = True

    while running:
        #screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLS):
                #pygame rect needs (x, y, width, height) - Jason S
                rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1) #remove 1 to fill square -Jason S

        #Init start position with color/text - Jason S
        row = 0
        col = 0
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect)
        text = font.render("START", True, BLACK)
        screen.blit(text, (col * CELL_SIZE, row * CELL_SIZE))

        # Init end position with color/text - Jason S
        row = 4
        col = 0
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        text = font.render("END", True, BLACK)
        screen.blit(text, (col * CELL_SIZE, row * CELL_SIZE))

        # Init block position - Jason S
        row = 2
        col = 0
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLACK, rect)

        pygame.display.flip()
        clock.tick(60) #Indentation IMPORTANT. Clock tick inside for loop causing many updates per frame -Jason S

pygame.quit()