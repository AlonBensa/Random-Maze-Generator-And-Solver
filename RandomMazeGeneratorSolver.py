import random
from enum import Enum
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

LENGTH_X = LENGTH_Y = 30
MAZE_WIDTH = 900
MAZE_HEIGHT = 900

class Directions(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def createMaze(links, board, indexes):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :type board: Dictionary{Tuple(int, int): bool}
    :type indexes: Tuple(int, int)
    :rtype: Dictionary{Tuple(int, int): List[int]}
    """

    board[indexes] = True
    possibleDirections = getPossibleDirections(indexes)
    next_indexes = []

    while len(next_indexes) < possibleDirections:
        possible_directions = list(Directions)
        direction = random.choice(possible_directions)
        nxt_idx = modifyIndexes(direction, indexes)

        if nxt_idx not in next_indexes and isValidIndex(nxt_idx):
            next_indexes.append(nxt_idx)

            if board[nxt_idx] == False:
                if indexes not in links:
                    links[indexes] = [nxt_idx]
                else:
                    links[indexes].append(nxt_idx)

                links = createMaze(links, board, nxt_idx)

    return links

def modifyIndexes(direction, indexes):
    """
    :type direction: Directions(Enum)
    :type indexes: Tuple(int, int)
    :rtype: Tuple(int, int)
    """

    x, y = indexes

    if direction == Directions.UP: y -= 1
    elif direction == Directions.RIGHT: x += 1
    elif direction == Directions.DOWN: y += 1
    elif direction == Directions.LEFT: x -= 1

    return x, y

def getPossibleDirections(indexes):
    """
    :type indexes: Tuple(int, int)
    :rtype: int
    """

    x, y = indexes
    if x == 0 and y == 0 or x == LENGTH_X-1 and y == 0 or x == 0 and y == LENGTH_Y-1 or x == LENGTH_X-1 and y == LENGTH_Y-1: return 2
    elif x == 0 and 0 < y < LENGTH_Y-1 or y == 0 and 0 < x < LENGTH_X-1 or x == LENGTH_X-1 and 0 < y < LENGTH_Y-1 or y == LENGTH_Y-1 and 0 < x < LENGTH_X-1: return 3
    else: return 4

def isValidIndex(indexes):
    """
    :type indexes: Tuple(int, int)
    :rtype: bool
    """

    x, y = indexes
    return 0 <= x < LENGTH_X and 0 <= y < LENGTH_Y

def drawMaze(links):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :rtype: void
    """

    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((MAZE_WIDTH + BLOCK_SIZE_X, MAZE_HEIGHT + BLOCK_SIZE_Y))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    linkLinks(links)
    drawGrid(links)

def drawGrid(links):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :rtype: void
    """

    for y in range(0, MAZE_WIDTH - BLOCK_SIZE_Y, BLOCK_SIZE_Y):
        for x in range(0, MAZE_HEIGHT - BLOCK_SIZE_X, BLOCK_SIZE_X):
            rect = pygame.Rect(x * 2 + BLOCK_SIZE_X, y * 2 + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y)
            if (x / BLOCK_SIZE_X, y / BLOCK_SIZE_Y) in links.keys() or any((x / BLOCK_SIZE_X, y / BLOCK_SIZE_Y) in sublist for sublist in links.values()):
                pygame.draw.rect(SCREEN, WHITE, rect)

    pygame.draw.rect(SCREEN, BLUE, pygame.Rect(BLOCK_SIZE_X, BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
    pygame.draw.rect(SCREEN, RED, pygame.Rect(MAZE_WIDTH - BLOCK_SIZE_X, MAZE_HEIGHT - BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
    
def linkLinks(links):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :rtype: void
    """

    for key, values in links.items():
        key_x, key_y = key
        for val in values:
            val_x, val_y = val
            rect = pygame.Rect(val_x * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, val_y * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y)
            pygame.draw.rect(SCREEN, WHITE, rect)
            rect = pygame.Rect(((val_x + key_x) / 2) * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, ((val_y + key_y) / 2) * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y)
            pygame.draw.rect(SCREEN, WHITE, rect)

def createLinksGraph(links):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :rtype: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    """

    graph = {}
    for key, values in links.items():
        if key not in graph:
            graph[key] = []
        for val in values:
            graph[key].append(val)
            if val not in graph:
                graph[val] = [key]
            else:
                graph[val].append(key)

    return graph

def solveMaze(links):
    """
    :type links: Dictionary{Tuple(int, int): List[Tuple(int, int)]}
    :rtype: List[Tuple(int, int)]
    """

    visited = {}
    prev = {}
    queue = []
    for key, values in links.items():
        visited[key] = False
        for value in values:
            visited[value] = False

    first_key = next(iter(links))
    queue.append(first_key)
    visited[first_key] = True

    while queue:
        node = queue.pop(0)

        for val in links[node]:
            if visited[val] == False:
                queue.append(val)
                visited[val] = True
                prev[val] = node

    return reconstructPath(prev)

def reconstructPath(prevs):
    """
    :type prevs: Dictionary{Tuple(int, int): Tuple(int, int)}
    :rtype: List[Tuple(int, int)]
    """

    path = []
    startNode=(0, 0)
    endNode=(LENGTH_X-1, LENGTH_Y-1)
    node = endNode

    while node != startNode:
        path.insert(0, node)
        node = prevs[node]
    
    return path

def drawSolution(solution):
    """
    :type solution: List[Tuple(int, int)]
    :rtype: void
    """

    prev_x, prev_y = (0, 0)
    countColor = 0
    for val in solution:
        val_x, val_y = val
        if countColor < 255:
            pygame.draw.rect(SCREEN, (0+countColor, 0, 255-countColor), pygame.Rect(val_x * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, val_y * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
            pygame.draw.rect(SCREEN, (0+countColor, 0, 255-countColor), pygame.Rect(((val_x + prev_x) / 2) * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, ((val_y + prev_y) / 2) * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
        else:
            pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(val_x * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, val_y * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
            pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(((val_x + prev_x) / 2) * 2 * BLOCK_SIZE_X + BLOCK_SIZE_X, ((val_y + prev_y) / 2) * 2 * BLOCK_SIZE_Y + BLOCK_SIZE_Y, BLOCK_SIZE_X, BLOCK_SIZE_Y))
        countColor += 1
        prev_x, prev_y = val 

if "__main__" == __name__:
    global BLOCK_SIZE_X, BLOCK_SIZE_Y
    BLOCK_SIZE_X = int(MAZE_WIDTH / LENGTH_X / 2)
    BLOCK_SIZE_Y = int(MAZE_HEIGHT / LENGTH_Y / 2)

    #Create board as a dictionary of indexes and the values are, is the indexes are visited or not
    board = {}
    for x in range(LENGTH_X):
        for y in range(LENGTH_Y):
            board[(x, y)] = False

    links = createMaze({}, board, (0, 0)) #Get the links between the indexes to draw the board
    solution = solveMaze(createLinksGraph(links)) #Create from the links between the indexes a graph of the links and use bfs to solve the maze
    drawMaze(links) #Draw the maze with the links given by createMaze function with pygame library
    drawSolution(solution) #Draw the solution on the board with purple color to see it

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()