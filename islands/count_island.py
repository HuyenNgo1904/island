from django.db import transaction
from .models import Island

def count_and_create_islands(grid):
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    island_count = 0

    with transaction.atomic():
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == "1":
                    island_count += 1
                    dfs(grid, i, j)

    return island_count

def dfs(grid, i, j):
    if (
        0 <= i < len(grid) and
        0 <= j < len(grid[0]) and
        grid[i][j] == "1"
    ):
        # Mark the current cell as visited
        grid[i][j] = "0"

        # Create a record in the database for the island
        Island.objects.create(latitude=i, longitude=j, island_area=1.0, detected_time="2024-01-23T12:00:00Z")

        # Perform DFS on adjacent cells
        dfs(grid, i + 1, j)
        dfs(grid, i - 1, j)
        dfs(grid, i, j + 1)
        dfs(grid, i, j - 1)
