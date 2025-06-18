import pygame


class Player:
    def __init__(self, pos):
        self.pos = pos

    def move(self, dx, dy, grid):
        x, y = self.pos
        new_x = x + dx
        new_y = y + dy

        if not (0 <= new_y < len(grid) and 0 <= new_x < len(grid[0])):
            return

        target_cell = grid[new_y][new_x]

        if target_cell == "#":
            return  # mur = stop

        if target_cell == ".":
            grid[new_y][new_x] == "+"

        if target_cell in ("$", "*"):
            box_new_x = new_x + dx
            box_new_y = new_y + dy
            if not (0 <= box_new_y < len(grid) and 0 <= box_new_x < len(grid[0])):
                return

            box_target_cell = grid[box_new_y][box_new_x]
            if box_target_cell not in (" ", "."):
                return  # boîte bloquée

            # Pousser la boîte
            grid[box_new_y][box_new_x] = "*" if box_target_cell == "." else "$"
            grid[new_y][new_x] = "." if target_cell == "*" else " "
        if target_cell == "*":
            return

        # Mettre à jour la position du joueur

        current_cell = grid[y][x]
        if current_cell == "+":
            grid[y][x] = "."
        else:
            grid[y][x] = " "

        self.pos = (new_x, new_y)

        if target_cell == ".":
            grid[new_y][new_x] = "+"  # joueur sur une cible
        else:
            grid[new_y][new_x] = "@"  # joueur sur une case normale
