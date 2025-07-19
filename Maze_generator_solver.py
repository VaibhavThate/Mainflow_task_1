import random
from collections import deque

def generate_maze(width, height):
    # Ensure dimensions are odd
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    maze = [[1 for _ in range(width)] for _ in range(height)]

    def is_valid(nx, ny):
        if nx <= 0 or ny <= 0 or nx >= width - 1 or ny >= height - 1:
            return False
        if maze[ny][nx] == 0:
            return False
        count = 0
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x, y = nx + dx, ny + dy
            if 0 <= x < width and 0 <= y < height:
                if maze[y][x] == 0:
                    count += 1
        return count <= 1

    def dfs(x, y):
        maze[y][x] = 0
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                dfs(nx, ny)

    dfs(1, 1)
    maze[1][1] = 'S'
    maze[height - 2][width - 2] = 'E'
    return maze

def solve_maze(maze):
    height = len(maze)
    width = len(maze[0])
    start = end = None

    for y in range(height):
        for x in range(width):
            if maze[y][x] == 'S':
                start = (x, y)
            elif maze[y][x] == 'E':
                end = (x, y)

    visited = [[False for _ in range(width)] for _ in range(height)]
    prev = [[None for _ in range(width)] for _ in range(height)]
    queue = deque([start])
    visited[start[1]][start[0]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            break
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if not visited[ny][nx] and (maze[ny][nx] == 0 or maze[ny][nx] == 'E'):
                    visited[ny][nx] = True
                    prev[ny][nx] = (x, y)
                    queue.append((nx, ny))

    # Reconstruct path
    path = []
    x, y = end
    while (x, y) != start:
        path.append((x, y))
        x, y = prev[y][x]
    path.append(start)
    path.reverse()

    for x, y in path:
        if maze[y][x] == 0:
            maze[y][x] = '.'

    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(str(cell) for cell in row))

# Main Execution
if __name__ == "__main__":
    try:
        width = int(input("Enter maze width (odd number): "))
        height = int(input("Enter maze height (odd number): "))
    except ValueError:
        print("Invalid input! Using default size 21x21.")
        width, height = 21, 21

    maze = generate_maze(width, height)
    print("\nGenerated Maze:")
    print_maze(maze)

    maze = solve_maze(maze)
    print("\nSolved Maze:")
    print_maze(maze)
