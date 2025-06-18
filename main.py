import pygame
import os
from player import Player
import copy

# --- Constantes ---
SQUARE_SIZE = 80
FPS = 60


# --- Chargement des images ---
def load_images():
    images = {}
    names = ["wall", "floor", "box", "target", "box_on_target", "player"]
    for name in names:
        try:
            img = pygame.image.load(f"assets/{name}.png")
            images[name] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        except:
            print(f"Erreur : image '{name}.png' introuvable dans /assets/")
            raise
    return images


# --- Lecture du niveau texte ---
def load_level(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        grid = [list(line.strip()) for line in lines]
        return grid
    except FileNotFoundError:
        print(f"Erreur : niveau '{path}' introuvable.")
        raise


# --- Dessin du niveau ---
def draw_level(win, grid, images):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            cell = grid[row][col]

            win.blit(images["floor"], (x, y))

            if cell == "#":
                win.blit(images["wall"], (x, y))
            elif cell == "$":
                win.blit(images["box"], (x, y))
            elif cell == ".":
                win.blit(images["target"], (x, y))
            elif cell == "*":
                win.blit(images["box_on_target"], (x, y))
            elif cell == "@":
                win.blit(images["player"], (x, y))
            elif cell == "+":
                win.blit(images["target"], (x, y))
                win.blit(images["player"], (x, y))


def show_victory_menu(win):
    font = pygame.font.SysFont(None, 50)

    title = font.render("Tu as gagné !", True, (255, 255, 255))
    option1 = font.render(
        "Appuie sur [N] pour jouer un autre niveau", True, (200, 200, 200)
    )
    option2 = font.render("Appuie sur [Q] pour quitter", True, (200, 200, 200))

    title_rect = title.get_rect(
        center=(win.get_width() // 2, win.get_height() // 2 - 60)
    )
    opt1_rect = option1.get_rect(center=(win.get_width() // 2, win.get_height() // 2))
    opt2_rect = option2.get_rect(
        center=(win.get_width() // 2, win.get_height() // 2 + 60)
    )

    while True:
        win.fill((0, 0, 0))
        win.blit(title, title_rect)
        win.blit(option1, opt1_rect)
        win.blit(option2, opt2_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return "next"
                elif event.key == pygame.K_q:
                    return "quit"


def is_victory(grid):
    for row in grid:
        for cell in row:
            if cell == "$":  # une boîte n'est pas sur une cible
                return False
    return True


# --- Fonction principale ---
def main(level_path):
    pygame.init()

    # Charger niveau et images
    grid = load_level(level_path)
    original_grid = copy.deepcopy(grid)
    images = load_images()

    rows = len(grid)
    cols = len(grid[0])

    WIDTH, HEIGHT = cols * SQUARE_SIZE, rows * SQUARE_SIZE

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sokoban")
    clock = pygame.time.Clock()

    # Afficher la position du joueur
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                player = Player((x, y))
                original_player_pos = (x, y)
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, grid)

                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, grid)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, grid)

                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, grid)
                elif event.key == pygame.K_r:

                    grid = copy.deepcopy(original_grid)
                    player = Player(original_player_pos)

        if is_victory(grid):
            result = show_victory_menu(win)
            pygame.quit()
            return result

        draw_level(win, grid, images)
        pygame.display.flip()
    pygame.quit()
    return "quit"


if __name__ == "__main__":
    try:
        continuer = True
        while continuer:

            a = int(input("choisisez quel niveau vous voulez jouer : "))
            match a:
                case 1:
                    result = main("levels1/level1.txt")
                case 2:
                    result = main("levels/level2.txt")
                case 3:
                    result = main("levels/level3.txt")
                case 4:
                    result = main("levels/level4.txt")
                case 5:
                    result = main("levels/level5.txt")
                case 6:
                    result = main("levels/level6.txt")
                case 7:
                    result = main("levels/level7.txt")
                case 8:
                    result = main("levels/level8.txt")
                case 9:
                    result = main("levels/level9.txt")
                case 10:
                    result = main("levels/level10.txt")
                case 11:
                    result = main("levels/level11.txt")
                case _:
                    print("Option invalide.")
                    continue
            if result == "quit":
                continuer = False
                pygame.quit()
    except Exception as e:
        print("Erreur lors de l'exécution :", e)
        input("Appuie sur Entrée pour quitter...")
