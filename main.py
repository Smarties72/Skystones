import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# Constantes
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 3
CELL_SIZE = 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 50, 50)
BLUE  = (50, 50, 200)
CARD_COLOR = (100, 200, 100)  # Couleur par défaut pour les cartes

tuto_page = 0

BRIGHTNESS_ADJUST = 60
menu_bg_paths = ["img/gui/menu1.jpg", "img/gui/menu2.jpg", "img/gui/menu3.jpg", "img/gui/menu4.jpg", "img/gui/menu5.jpg", "img/gui/menu6.jpg" ,"img/gui/menu7.jpg", "img/gui/menu8.jpg", "img/gui/menu9.jpg", "img/gui/menu10.jpg", "img/gui/menu11.jpg", "img/gui/menu12.jpg", "img/gui/menu13.jpg", "img/gui/menu14.jpg", "img/gui/menu15.jpg"] 
menu_bg_images = []
for path in menu_bg_paths:
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        bright = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        bright.fill((BRIGHTNESS_ADJUST, BRIGHTNESS_ADJUST, BRIGHTNESS_ADJUST, 0))
        img.blit(bright, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        menu_bg_images.append(img)
    except Exception as e:
        print(f"Erreur chargement background {path}: {e}")
menu_bg_index = 0
menu_bg_last_switch = pygame.time.get_ticks()
MENU_BG_DELAY = 3000  # 3 secondes

def load_music(state):
    global selected_music
    pygame.mixer.music.stop()
    if selected_music and state not in ("game", "game_ai"):
        try:
            pygame.mixer.music.load(f"img/gui/{selected_music}")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[load_music] Erreur chargement «{selected_music}» : {e}")
        return
    music_map = {
        "menu":        "img/gui/musique de menu.mp3",
        "game":        "img/gui/musique de jeu.mp3",
        "game_ai":     "img/gui/musique de jeu.mp3",
        "cards_view":  "img/gui/musique carte.mp3",
        "game_over":   "img/gui/musique fin de partie.mp3",
    }

    musique = music_map.get(state)
    if not musique:
        print(f"[load_music] État inconnu «{state}», pas de musique.")
        return
    try:
        pygame.mixer.music.load(musique)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[load_music] Erreur chargement «{musique}» : {e}")

  


PLAYER_CELL_COLOR = (173, 216, 230)   
OPPONENT_CELL_COLOR = (255, 182, 193)  


ai_difficulty = "easy"


card_values = {f"Carte{i}": (1, 1, 1, 1) for i in range(1, 34)}
card_values["Carte1"] = (3, 2, 0, 2)
card_values["Carte2"] = (0, 0, 0, 4)
card_values["Carte3"] = (2, 2, 0, 2)
card_values["Carte4"] = (0, 0, 2, 0)
card_values["Carte5"] = (2, 0, 0, 0)
card_values["Carte6"] = (1, 0, 1, 1)
card_values["Carte7"] = (1, 1, 3, 1)
card_values["Carte8"] = (1, 2, 2, 2)
card_values["Carte9"] = (2, 3, 2, 1)
card_values["Carte10"] = (0, 1, 3, 3)
card_values["Carte11"] = (2, 2, 2, 2)
card_values["Carte12"] = (1, 3, 3, 1)
card_values["Carte13"] = (2, 1, 2, 1)
card_values["Carte14"] = (2, 2, 2, 2)
card_values["Carte15"] = (2, 1, 2, 1)
card_values["Carte16"] = (2, 3, 2, 1)
card_values["Carte17"] = (3, 1, 2, 2)
card_values["Carte18"] = (1, 1, 1, 1)
card_values["Carte19"] = (1, 1, 3, 3)
card_values["Carte20"] = (2, 2, 2, 3)
card_values["Carte21"] = (0, 3, 2, 1)
card_values["Carte22"] = (3, 3, 1, 1)
card_values["Carte23"] = (3, 3, 3, 3)
card_values["Carte24"] = (4, 4, 4, 4)
card_values["Carte25"] = (0, 0, 4, 0)
card_values["Carte26"] = (4, 0, 0, 0)
card_values["Carte27"] = (0, 4, 0, 0)
card_values["Carte28"] = (2, 2, 3, 2)
card_values["Carte29"] = (0, 0, 1, 1)
card_values["Carte30"] = (4, 1, 0, 1)
card_values["Carte31"] = (0, 1, 0, 1)
card_values["Carte32"] = (1, 0, 0, 1)
card_values["Carte33"] = (3, 0, 0, 3)


def draw_background():
    top_color = (180, 220, 255)
    bottom_color = (255, 255, 255)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
            int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
            int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))


def load_images():
    images = {}
    card_width, card_height = 150, 150
    for i in range(1, 34):
        image_path = f"img/cards/Carte{i}.png"
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (card_width, card_height))
            images[f"Carte{i}"] = image
            print(f"Image {image_path} chargée et redimensionnée avec succès.")
        except pygame.error as e:
            print(f"Erreur de chargement de l'image {image_path}: {e}")
            temp_image = pygame.Surface((card_width, card_height))
            temp_image.fill(CARD_COLOR)
            images[f"Carte{i}"] = temp_image
    return images

def draw_menu() :
    font = pygame.font.Font(None, 50)
    # Boutons centrés
    jouer_button = pygame.Rect(300, 180, 200, 60)
    tuto_button = pygame.Rect(300, 270, 200, 60)
    biblio_button = pygame.Rect(300, 360, 200, 60)
    gear_button = pygame.Rect(WIDTH-80, HEIGHT-80, 60, 60)
    pygame.draw.rect(screen, RED, jouer_button, border_radius=10)
    pygame.draw.rect(screen, BLUE, tuto_button, border_radius=10)
    pygame.draw.rect(screen, RED, biblio_button, border_radius=10)
    pygame.draw.circle(screen, BLACK, gear_button.center, 30)
    for i in range(8):
        angle = i * (360/8)
        x = gear_button.centerx + int(38 * math.cos(math.radians(angle)))
        y = gear_button.centery + int(38 * math.sin(math.radians(angle)))
        pygame.draw.circle(screen, BLACK, (x, y), 7)
    screen.blit(font.render("Jouer", True, WHITE), (jouer_button.x + (jouer_button.width - font.size("Jouer")[0])//2,
                                                    jouer_button.y + (jouer_button.height - font.size("Jouer")[1])//2))
    screen.blit(font.render("Tuto", True, WHITE), (tuto_button.x + (tuto_button.width - font.size("Tuto")[0])//2,
                                                   tuto_button.y + (tuto_button.height - font.size("Tuto")[1])//2))
    screen.blit(font.render("Bibliothèque", True, WHITE), (biblio_button.x + (biblio_button.width - font.size("Bibliothèque")[0])//2,
                                                           biblio_button.y + (biblio_button.height - font.size("Bibliothèque")[1])//2))
    return jouer_button, tuto_button, biblio_button, gear_button


def draw_board():
    board_x = (WIDTH - (CELL_SIZE * GRID_SIZE)) // 2
    board_y = (HEIGHT - (CELL_SIZE * GRID_SIZE)) // 2
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_rect = pygame.Rect(board_x + col * CELL_SIZE, board_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if board_cards[row][col] is not None:
                card, owner = board_cards[row][col]
                fill_color = PLAYER_CELL_COLOR if owner == "player" else OPPONENT_CELL_COLOR
                pygame.draw.rect(screen, fill_color, cell_rect, border_radius=5)
            else:
                pygame.draw.rect(screen, WHITE, cell_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, cell_rect, 2, border_radius=5)
            if board_cards[row][col] is not None:
                card, owner = board_cards[row][col]
                screen.blit(card_images[card], (cell_rect.x, cell_rect.y))


def draw_hand_cards():
    for i, card in enumerate(player_cards):
        x, y = 20, 60 + i * 160
        screen.blit(card_images[card], (x, y))
    for i, card in enumerate(opponent_cards):
        x, y = WIDTH - 170, 60 + i * 160
        screen.blit(card_images[card], (x, y))

def draw_scores():
    player_score = 0
    opponent_score = 0
    for row in board_cards:
        for cell in row:
            if cell is not None:
                card, owner = cell
                if owner == "player":
                    player_score += 1
                else:
                    opponent_score += 1
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Joueur 1: {player_score}", True, BLACK)
    opponent_text = font.render(f"Joueur 2: {opponent_score}", True, BLACK)
    screen.blit(player_text, (WIDTH // 2 - player_text.get_width() - 20, 10))
    screen.blit(opponent_text, (WIDTH // 2 + 20, 10))
    return player_score, opponent_score

def draw_biblio():
    draw_background()
    font = pygame.font.Font(None, 48)
    cartes_button = pygame.Rect(300, 220, 200, 60)
    back_button = pygame.Rect(20, 20, 120, 50)
    pygame.draw.rect(screen, BLUE, cartes_button, border_radius=10)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    screen.blit(font.render("Cartes", True, WHITE), (cartes_button.x + (cartes_button.width - font.size("Cartes")[0])//2,
                                                     cartes_button.y + (cartes_button.height - font.size("Cartes")[1])//2))
    screen.blit(font.render("Retour", True, WHITE), (back_button.x + 10, back_button.y + 10))
    return cartes_button, back_button

def draw_play_modes():
    draw_background()
    font = pygame.font.Font(None, 48)
    mode_1v1_btn = pygame.Rect(300, 140, 200, 60)
    mode_ia_btn = pygame.Rect(300, 230, 200, 60)
    campagne_btn = pygame.Rect(300, 320, 200, 60)
    back_button = pygame.Rect(20, 20, 120, 50)
    pygame.draw.rect(screen, RED, mode_1v1_btn, border_radius=10)
    pygame.draw.rect(screen, BLUE, mode_ia_btn, border_radius=10)
    pygame.draw.rect(screen, RED, campagne_btn, border_radius=10)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    screen.blit(font.render("1V1", True, WHITE), (mode_1v1_btn.x + (mode_1v1_btn.width - font.size("1V1")[0])//2,
                                                  mode_1v1_btn.y + (mode_1v1_btn.height - font.size("1V1")[1])//2))
    screen.blit(font.render("IA versus", True, WHITE), (mode_ia_btn.x + (mode_ia_btn.width - font.size("IA versus")[0])//2,
                                                        mode_ia_btn.y + (mode_ia_btn.height - font.size("IA versus")[1])//2))
    screen.blit(font.render("Campagne", True, WHITE), (campagne_btn.x + (campagne_btn.width - font.size("Campagne")[0])//2,
                                                       campagne_btn.y + (campagne_btn.height - font.size("Campagne")[1])//2))
    screen.blit(font.render("Retour", True, WHITE), (back_button.x + 10, back_button.y + 10))
    return mode_1v1_btn, mode_ia_btn, campagne_btn, back_button

def draw_tuto(tuto_page):
    draw_background()
    font_title = pygame.font.Font(None, 50)
    font = pygame.font.Font(None, 32)

    # Bouton retour
    back_button = pygame.Rect(20, HEIGHT-70, 120, 50)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    back_text = font.render("Retour", True, WHITE)
    screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                            back_button.y + (back_button.height - back_text.get_height()) // 2))

    # Flèches navigation
    arrow_left  = pygame.Rect(40, 30, 60, 60)
    arrow_right = pygame.Rect(WIDTH-100, 30, 60, 60)
    if tuto_page > 0:
        pygame.draw.polygon(screen, BLACK, [(arrow_left.x+50, arrow_left.y), (arrow_left.x+10, arrow_left.y+30), (arrow_left.x+50, arrow_left.y+60)])
    if tuto_page < 5:
        pygame.draw.polygon(screen, BLACK, [(arrow_right.x+10, arrow_right.y), (arrow_right.x+50, arrow_right.y+30), (arrow_right.x+10, arrow_right.y+60)])

    # Contenu des pages
    if tuto_page == 0:
        screen.blit(font_title.render("Bienvenue dans le monde des Skystones !", True, BLACK), (60, 120))
        lines = [
            "Un jeu de cartes tout droit sorti de la célèbre licence Skylanders.",
            "",
            "Utilisez les flèches en haut à droite et"
            "",
            "à gauche pour apprendre les règles du jeu."
        ]
        y = 200
        for line in lines:
            screen.blit(font.render(line, True, BLACK), (60, y))
            y += 40

    elif tuto_page == 1:
        screen.blit(font_title.render("Voici le plateau de jeu :", True, BLACK), (220, 30))
        # Dessin du plateau 3x3 au centre
        grid_x = WIDTH//2 - (CELL_SIZE*GRID_SIZE)//2
        grid_y = HEIGHT//2 - (CELL_SIZE*GRID_SIZE)//2
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(grid_x + col*CELL_SIZE, grid_y + row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 3)

    elif tuto_page == 2:
        screen.blit(font_title.render("Voici une carte", True, BLACK), (270, 60))
        # Affiche Carte1.png au centre
        carte_img = card_images.get("Carte1")
        if carte_img:
            img_rect = carte_img.get_rect(center=(WIDTH//2, HEIGHT//2.5))
            screen.blit(carte_img, img_rect)
        # Texte explicatif
        lines = [
            "Tout autour de cette carte se trouvent des \"épines\"",
            "qui représentent la force du côté de la carte.",
            "Plus il y a d'épines sur un côté, plus ce côté est puissant."
        ]
        y = HEIGHT//2 + 10
        for line in lines:
            screen.blit(font.render(line, True, BLACK), (WIDTH//2 - 250, y))
            y += 35

    elif tuto_page == 3:
        font_title = pygame.font.Font(None, 30)  # Titre moins grand
        font_text = pygame.font.Font(None, 28)   # Texte explicatif plus petit
        # Titre centré
        titre = "Chacun votre tour vous allez poser une carte sur le plateau"
        titre_render = font_title.render(titre, True, BLACK)
        screen.blit(titre_render, ((WIDTH - titre_render.get_width()) // 2, 40))

        # Plateau plus petit (3x3, mais cases de 70px)
        small_cell = 70
        grid_x = WIDTH // 2 - (small_cell * GRID_SIZE) // 2
        grid_y = HEIGHT // 2 - (small_cell * GRID_SIZE) // 2 - 80

        # Dessin du plateau
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(grid_x + col * small_cell, grid_y + row * small_cell, small_cell, small_cell)
                pygame.draw.rect(screen, BLACK, rect, 3)

        # Deux cartes placées (exemple : Carte1 et Carte2)
        carte1 = card_images.get("Carte1")
        carte2 = card_images.get("Carte2")
        if carte1:
            carte1_img = pygame.transform.scale(carte1, (small_cell, small_cell))
            screen.blit(carte1_img, (grid_x + 0 * small_cell, grid_y + 1 * small_cell))  # à gauche au milieu
        if carte2:
            carte2_img = pygame.transform.scale(carte2, (small_cell, small_cell))
            screen.blit(carte2_img, (grid_x + 2 * small_cell, grid_y + 1 * small_cell))  # à droite au milieu

        # Texte explicatif centré sous le plateau
        lines = [
            "A chaque fois que vous posez une carte sur le plateau votre score augmente de 1",
            "et on vérifie si votre carte est en contact avec une carte adverse.",
            "Si la carte que vous venez de poser est plus forte que la carte adverse alors",
            "vous gagnez la carte adverse et votre score augmente de 1.",
            "Si la carte adverse est plus forte, vous perdez la carte que vous venez de poser,",
            "votre score diminue de 1 et celui de l'adversaire augmente de 1."
        ]
        y = grid_y + small_cell * GRID_SIZE + 20
        for line in lines:
            render = font_text.render(line, True, BLACK)
            screen.blit(render, ((WIDTH - render.get_width()) // 2, y))
            y += 32

    elif tuto_page == 4:
        font_title = pygame.font.Font(None, 26)
        font_text = pygame.font.Font(None, 25)
        titre = "La compraison des cartes se fait seulement sur les côtés en contact"
        titre_render = font_title.render(titre, True, BLACK)
        screen.blit(titre_render, ((WIDTH - titre_render.get_width()) // 2, 40))

        # Plateau plus petit (3x3, mais cases de 70px), décalé vers le haut
        small_cell = 70
        grid_x = WIDTH // 2 - (small_cell * GRID_SIZE) // 2
        grid_y = HEIGHT // 2 - (small_cell * GRID_SIZE) // 2 - 80  # Décalage vers le haut

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(grid_x + col * small_cell, grid_y + row * small_cell, small_cell, small_cell)
                pygame.draw.rect(screen, BLACK, rect, 3)

        carte1 = card_images.get("Carte1")
        carte2 = card_images.get("Carte2")
        if carte1:
            carte1_img = pygame.transform.scale(carte1, (small_cell, small_cell))
            screen.blit(carte1_img, (grid_x + 1 * small_cell, grid_y + 1 * small_cell))
        if carte2:
            carte2_img = pygame.transform.scale(carte2, (small_cell, small_cell))
            screen.blit(carte2_img, (grid_x + 2 * small_cell, grid_y + 1 * small_cell))

        lines = [
            "Si la carte que vous venez de poser n'est pas en contact avec une carte adverse,",
            "alors rien ne se passe. Votre score augmente simplement de 1 car vous avez posé une carte.",
            "Si votre carte est en contact avec plusieurs cartes adverses, alors on compare chaque côté.",
            "Si votre carte n'a aucun coté plus fort que les cartes adverses, vous perdez la carte posée.",
            "Mais si au moins un côté est plus fort, alors vous garder votre carte et vous gagnez les cartes", 
            "des côtés que vous avez battu."
        ]
        y = grid_y + small_cell * GRID_SIZE + 20
        for line in lines:
            render = font_text.render(line, True, BLACK)
            screen.blit(render, ((WIDTH - render.get_width()) // 2, y))
            y += 32
    
    elif tuto_page == 5:
        font_title = pygame.font.Font(None, 32)
        font_text = pygame.font.Font(None, 23)
        titre = "A la fin de la partie :"
        titre_render = font_title.render(titre, True, BLACK)
        screen.blit(titre_render, ((WIDTH - titre_render.get_width()) // 2, 40))

        # Plateau rempli (3x3, cases de 70px)
        small_cell = 70
        grid_x = WIDTH // 2 - (small_cell * GRID_SIZE) // 2
        grid_y = HEIGHT // 2 - (small_cell * GRID_SIZE) // 2 - 80

        # Exemple de répartition des cartes et propriétaires
        demo_cards = [
            [("Carte1", "player"),   ("Carte2", "opponent"), ("Carte3", "player")],
            [("Carte4", "opponent"), ("Carte5", "player"),   ("Carte6", "opponent")],
            [("Carte7", "player"),   ("Carte8", "player"),   ("Carte9", "opponent")]
        ]
        player_score = sum(1 for row in demo_cards for card, owner in row if owner == "player")
        opponent_score = sum(1 for row in demo_cards for card, owner in row if owner == "opponent")

        # Dessin du plateau et des cartes + ronds de couleur
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(grid_x + col * small_cell, grid_y + row * small_cell, small_cell, small_cell)
                pygame.draw.rect(screen, BLACK, rect, 3)
                card_name, owner = demo_cards[row][col]
                card_img = card_images.get(card_name)
                if card_img:
                    card_img_scaled = pygame.transform.scale(card_img, (small_cell, small_cell))
                    screen.blit(card_img_scaled, (rect.x, rect.y))
                # Dessine le rond de couleur en bas à droite de la case
                color = BLUE if owner == "player" else RED
                pygame.draw.circle(screen, color, (rect.x + small_cell - 15, rect.y + small_cell - 15), 10)

        # Affichage du score centré au-dessus du plateau
        score_text = font_title.render(f"Score : Joueur Bleu {player_score} - {opponent_score} Joueur Rouge", True, BLACK)
        screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, grid_y - 40))

        # Texte explicatif centré sous le plateau (à compléter)
        lines = [
            "À la fin de la partie, le score est calculé selon le nombre de cartes de chaque joueur.",
            "Comme il y a 9 cases sur le plateau et que le chiffre 9 est impair, il y aura toujours un gagnant.",
            "Le joueur possedant le plus de cartes remporte la partie.",
            "Ici dans cette exemple les ronds indiquent à qui appartient chaque carte pour faciliter la comprehension :",
            "bleu pour Joueur Bleu, rouge pour Joueur Rouge.",
            "Dans une vraie partie les cartes ont un cercle de couleur rouge ou bleu en fonction de qui les possède.",
        ]
        y = grid_y + small_cell * GRID_SIZE + 20
        for line in lines:
            render = font_text.render(line, True, BLACK)
            screen.blit(render, ((WIDTH - render.get_width()) // 2, y))
            y += 28

    return back_button, arrow_left, arrow_right

def draw_music_select(selected_music):
    # Dégradé vertical bleu-violet
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(60 * (1 - ratio) + 120 * ratio),   # du bleu au violet
            int(60 * (1 - ratio) + 40 * ratio),
            int(120 * (1 - ratio) + 180 * ratio)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    font = pygame.font.Font(None, 36)
    back_button = pygame.Rect(20, 20, 120, 50)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    screen.blit(font.render("Retour", True, WHITE), (back_button.x + 10, back_button.y + 10))
    # Liste des musiques
    music_files = [f for f in os.listdir("img/gui") if f.endswith(".mp3") and f not in musics_to_remove]
    y_start = 100 + music_scroll_offset
    select_buttons = []
    for music in music_files:
        music_name = music[:-4]
        text = font.render(music_name, True, WHITE)
        screen.blit(text, (80, y_start))
        
        # Dessine la note de musique à droite du nom
        note_x = 80 + text.get_width() + 30
        note_y = y_start + 15
        pygame.draw.circle(screen, (255, 255, 255), (note_x, note_y), 10)
        pygame.draw.line(screen, (255, 255, 255), (note_x, note_y-10), (note_x, note_y-25), 4)
        pygame.draw.line(screen, (255, 255, 255), (note_x, note_y-25), (note_x+7, note_y-18), 4)

        # Case de sélection tout à droite
        select_rect = pygame.Rect(WIDTH - 80, y_start, 30, 30)
        pygame.draw.rect(screen, BLUE if selected_music == music else (200, 200, 200), select_rect, border_radius=5)
        if selected_music == music:
            pygame.draw.line(screen, WHITE, (select_rect.x+5, select_rect.y+15), (select_rect.x+15, select_rect.y+25), 4)
            pygame.draw.line(screen, WHITE, (select_rect.x+15, select_rect.y+25), (select_rect.x+25, select_rect.y+5), 4)
        select_buttons.append((select_rect, music))
        y_start += 50
    return back_button, select_buttons

def get_grid_position(x, y):
    board_x = (WIDTH - (CELL_SIZE * GRID_SIZE)) // 2
    board_y = (HEIGHT - (CELL_SIZE * GRID_SIZE)) // 2
    col = (x - board_x) // CELL_SIZE
    row = (y - board_y) // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None, None


def place_card(row, col, card, hand):
    if board_cards[row][col] is None:
        board_cards[row][col] = (card, hand)
        if hand == "player":
            player_cards.remove(card)
        else:
            opponent_cards.remove(card)


def check_flips(row, col):
    placed_card, placed_owner = board_cards[row][col]
    placed_vals = card_values[placed_card]
    directions = [(-1, 0, 0, 2), (0, 1, 1, 3), (1, 0, 2, 0), (0, -1, 3, 1)]
    wins = []
    losses = []
  
    for dr, dc, p_idx, n_idx in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board_cards[r][c] is not None:
            neighbor_card, neighbor_owner = board_cards[r][c]
            if neighbor_owner != placed_owner:
                neighbor_vals = card_values[neighbor_card]
                if placed_vals[p_idx] > neighbor_vals[n_idx]:
                    wins.append((r, c))
                elif placed_vals[p_idx] < neighbor_vals[n_idx]:
                    losses.append((r, c))

    
    if wins:
        for r, c in wins:
            card, _ = board_cards[r][c]
            board_cards[r][c] = (card, placed_owner)
    elif losses:
        r, c = losses[0]
        _, neighbor_owner = board_cards[r][c]
        board_cards[row][col] = (placed_card, neighbor_owner)



def draw_gallery(scroll_offset):
    draw_background()
    back_button = pygame.Rect(10, 10, 100, 40)
    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    font = pygame.font.Font(None, 36)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2,
                             back_button.y + (back_button.height - back_text.get_height()) // 2))
    x = 20 + scroll_offset
    y = HEIGHT // 2 - 75
    spacing = 20
    sorted_cards = sorted(card_images.keys(), key=lambda c: int(c.replace("Carte", "")))
    for card in sorted_cards:
        screen.blit(card_images[card], (x, y))
        x += 150 + spacing
    return back_button


def init_game():
    global board_cards, player_cards, opponent_cards, deck, current_turn
    board_cards = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    all_cards = [f"Carte{i}" for i in range(1, 34)]
    random.shuffle(all_cards)
    player_cards = all_cards[:5]
    opponent_cards = all_cards[5:10]
    deck = all_cards[10:]
    current_turn = "player"


def draw_game_over(winner, player_score, opponent_score):
    draw_background()
    font = pygame.font.Font(None, 50)
    if winner == "draw":
        result_text = "Match nul !"
    elif winner == "player":
        result_text = "Joueur 1 a gagné !"
    else:
        result_text = "Joueur 2 a gagné !"
    result_render = font.render(result_text, True, BLACK)
    score_render = font.render(f"{player_score} - {opponent_score}", True, BLACK)
    screen.blit(result_render, (WIDTH//2 - result_render.get_width()//2, HEIGHT//2 - 80))
    screen.blit(score_render, (WIDTH//2 - score_render.get_width()//2, HEIGHT//2))
    menu_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
    pygame.draw.rect(screen, BLUE, menu_button, border_radius=10)
    menu_text = font.render("Menu", True, WHITE)
    screen.blit(menu_text, (menu_button.x + (menu_button.width - menu_text.get_width()) // 2,
                            menu_button.y + (menu_button.height - menu_text.get_height()) // 2))
    return menu_button


def evaluate_move(card, row, col, hand):
    placed_vals = card_values[card]
    gain = 0
    directions = [(-1, 0, 0, 2), (0, 1, 1, 3), (1, 0, 2, 0), (0, -1, 3, 1)]
    for dr, dc, p_idx, n_idx in directions:
        r = row + dr
        c = col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board_cards[r][c] is not None:
            neighbor_card, neighbor_owner = board_cards[r][c]
            neighbor_vals = card_values[neighbor_card]
            if neighbor_owner != hand:
                if placed_vals[p_idx] > neighbor_vals[n_idx]:
                    gain += 1
                elif placed_vals[p_idx] < neighbor_vals[n_idx]:
                    gain -= 1
    return gain


def ai_move():
    moves = []
    for card in opponent_cards:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board_cards[row][col] is None:
                    moves.append((card, row, col))
    if not moves:
        return None
    if ai_difficulty == "easy":
        return random.choice(moves)
    elif ai_difficulty in ("medium", "hard"):
        best_move = None
        best_gain = -999
        for move in moves:
            card, row, col = move
            gain = evaluate_move(card, row, col, "opponent")
            if gain > best_gain:
                best_gain = gain
                best_move = move
        return best_move


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skystones - Prototype")

card_images = load_images()
init_game()


selected_card = None
selected_card_position = None
selected_card_hand = None  
selected_music = None

current_turn = "player"


scroll_offset = 0
music_scroll_offset = 0  # Ajoute cette variable globale


state = "menu"
previous_state = None
running = True

ai_thinking    = False
ai_start_time  = 0
AI_THINK_DELAY = 2000  # en millisecondes
font_think     = pygame.font.Font(None, 50)

tuto_page = 0  # 0 = accueil, 1 = plateau, 2 = carte


musics_to_remove = [
    "musique carte.mp3",
    "musique de jeu.mp3",
    "musique de menu.mp3",
    "musique fin de partie.mp3",
]


dragging_card = None
dragging_hand = None
drag_offset_x = 0
drag_offset_y = 0
dragging_pos = None

while running:
    now = pygame.time.get_ticks()
    if state != previous_state:
        load_music(state)
        previous_state = state

    if state == "menu":
        if menu_bg_images and now - menu_bg_last_switch >= MENU_BG_DELAY:
            menu_bg_index = (menu_bg_index + 1) % len(menu_bg_images)
            menu_bg_last_switch = now
        if menu_bg_images:
            screen.blit(menu_bg_images[menu_bg_index], (0, 0))
        else:
            draw_background()
        jouer_btn, tuto_btn, biblio_btn, gear_btn = draw_menu()
    elif state == "play_modes":
        mode_1v1_btn, mode_ia_btn, campagne_btn, back_btn = draw_play_modes()
    elif state == "biblio":
        cartes_btn, back_btn = draw_biblio()
    elif state == "tuto":
        back_btn, arrow_left, arrow_right = draw_tuto(tuto_page)
    elif state == "music_select":
        back_btn, select_buttons = draw_music_select(selected_music)
    elif state == "cards_view":
        back_btn = draw_gallery(scroll_offset)
    elif state == "game":
        draw_background()
        draw_board()
        draw_hand_cards()
        draw_scores()
        if selected_card is not None and selected_card_position is not None:
            highlight_rect = pygame.Rect(selected_card_position[0]-5, selected_card_position[1]-5, 160, 160)
            border_color = RED if selected_card_hand == "opponent" else BLUE
            pygame.draw.rect(screen, border_color, highlight_rect, 3, border_radius=10)
    elif state == "game_ai":
        draw_background()
        draw_board()
        draw_hand_cards()
        draw_scores()
        # Effet visuel du drag & drop
        if dragging_card and dragging_pos:
            highlight_rect = pygame.Rect(dragging_pos[0] - drag_offset_x - 5, dragging_pos[1] - drag_offset_y - 5, 160, 160)
            pygame.draw.rect(screen, BLUE, highlight_rect, 3, border_radius=10)
        # Effet classique (si sélection sans drag)
        if selected_card is not None and selected_card_position is not None:
            highlight_rect = pygame.Rect(selected_card_position[0]-5, selected_card_position[1]-5, 160, 160)
            border_color = RED if selected_card_hand == "opponent" else BLUE
            pygame.draw.rect(screen, border_color, highlight_rect, 3, border_radius=10)
        # IA réfléchit...
        if current_turn == "opponent":
            now = pygame.time.get_ticks()
            if ai_thinking:
                if now - ai_start_time < AI_THINK_DELAY:
                    text = font_think.render("L'IA réfléchit...", True, BLACK)
                    screen.blit(text, (310, 39))
                else:
                    move = ai_move()
                    if move:
                        card, r, c = move
                        place_card(r, c, card, "opponent")
                        check_flips(r, c)
                    ai_thinking = False
                    current_turn = "player"
                    if all(all(cell for cell in row) for row in board_cards):
                        state = "game_over"
            else:
                ai_thinking = True
                ai_start_time = now
    elif state == "game_over":
        p_s, o_s = draw_scores()
        winner = "player" if p_s > o_s else ("opponent" if o_s > p_s else "draw")
        menu_btn = draw_game_over(winner, p_s, o_s)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                if jouer_btn.collidepoint(event.pos):
                    state = "play_modes"  
                elif tuto_btn.collidepoint(event.pos):
                    state = "tuto"
                elif biblio_btn.collidepoint(event.pos):
                    state = "biblio"
                elif gear_btn.collidepoint(event.pos):
                    state = "music_select"
            elif state == "biblio":
                if cartes_btn.collidepoint(event.pos):
                    state = "cards_view"
                elif back_btn.collidepoint(event.pos):
                    state = "menu"
            elif state == "play_modes":
                if mode_1v1_btn.collidepoint(event.pos):
                    init_game()
                    state = "game"
                elif mode_ia_btn.collidepoint(event.pos):
                    init_game()
                    state = "game_ai"
                elif back_btn.collidepoint(event.pos):
                    state = "menu"
            elif state == "game":
                # Sélection d'une carte dans la main du joueur ou de l'adversaire
                if current_turn == "player":
                    for i, card in enumerate(player_cards):
                        rect = pygame.Rect(20, 60 + i * 160, 150, 150)
                        if rect.collidepoint(event.pos):
                            selected_card = card
                            selected_card_position = (20, 60 + i * 160)
                            selected_card_hand = "player"
                elif current_turn == "opponent":
                    for i, card in enumerate(opponent_cards):
                        rect = pygame.Rect(WIDTH - 170, 60 + i * 160, 150, 150)
                        if rect.collidepoint(event.pos):
                            selected_card = card
                            selected_card_position = (WIDTH - 170, 60 + i * 160)
                            selected_card_hand = "opponent"
            elif state == "game_ai":
                if current_turn == "player":
                    for i, card in enumerate(player_cards):
                        rect = pygame.Rect(20, 60 + i * 160, 150, 150)
                        if rect.collidepoint(event.pos):
                            selected_card = card
                            selected_card_position = (20, 60 + i * 160)
                            selected_card_hand = "player"
            elif state == "cards_view":
                if back_btn.collidepoint(event.pos):
                    state = "biblio"
            elif state == "game_over":
                if menu_btn and menu_btn.collidepoint(event.pos):
                    state = "menu"
            elif state == "tuto":
                if back_btn.collidepoint(event.pos):
                    state = "menu"
                elif arrow_left.collidepoint(event.pos) and tuto_page > 0:
                    tuto_page -= 1
                elif arrow_right.collidepoint(event.pos) and tuto_page < 5:
                    tuto_page += 1
            elif state == "music_select":
                if back_btn.collidepoint(event.pos):
                    state = "menu"
                for rect, music in select_buttons:
                    if rect.collidepoint(event.pos):
                        selected_music = music
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(f"img/gui/{selected_music}")
                        pygame.mixer.music.play(-1)

        elif event.type == pygame.MOUSEMOTION:
            if (state == "game" or state == "game_ai") and selected_card is not None:
                mx, my = event.pos
                selected_card_position = (mx - 75, my - 75)

        elif event.type == pygame.MOUSEBUTTONUP:
            if (state == "game" or state == "game_ai") and selected_card is not None:
                x, y = event.pos
                row, col = get_grid_position(x, y)
                if row is not None and col is not None and board_cards[row][col] is None:
                    place_card(row, col, selected_card, selected_card_hand)
                    check_flips(row, col)
                    # Tour suivant
                    if state == "game_ai":
                        current_turn = "opponent" if current_turn == "player" else "player"
                    else:
                        current_turn = "opponent" if current_turn == "player" else "player"
                    # Fin de partie
                    full = all(all(cell for cell in row) for row in board_cards)
                    if full:
                        state = "game_over"
                selected_card = None
                selected_card_position = None
                selected_card_hand = None

        elif event.type == pygame.KEYDOWN:
            if state == "music_select":
                if event.key == pygame.K_UP:
                    music_scroll_offset += 50
                elif event.key == pygame.K_DOWN:
                    music_scroll_offset -= 50
            elif state == "cards_view":
                if event.key == pygame.K_LEFT:
                    scroll_offset += 50
                elif event.key == pygame.K_RIGHT:
                    scroll_offset -= 50
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state in ("game", "game_ai"):
                # Démarre le drag si on clique sur une carte
                if current_turn == "player":
                    for i, card in enumerate(player_cards):
                        x, y = 20, 60 + i * 160
                        rect = pygame.Rect(x, y, 150, 150)
                        if rect.collidepoint(event.pos):
                            dragging_card = card
                            dragging_hand = "player"
                            drag_offset_x = event.pos[0] - x
                            drag_offset_y = event.pos[1] - y
                            dragging_pos = event.pos
                elif current_turn == "opponent" and state == "game":
                    for i, card in enumerate(opponent_cards):
                        x, y = WIDTH - 170, 60 + i * 160
                        rect = pygame.Rect(x, y, 150, 150)
                        if rect.collidepoint(event.pos):
                            dragging_card = card
                            dragging_hand = "opponent"
                            drag_offset_x = event.pos[0] - x
                            drag_offset_y = event.pos[1] - y
                            dragging_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if dragging_card:
                dragging_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_card and dragging_pos:
                # Vérifie si on relâche sur une case du plateau
                board_x = (WIDTH - (CELL_SIZE * GRID_SIZE)) // 2
                board_y = (HEIGHT - (CELL_SIZE * GRID_SIZE)) // 2
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        cell_rect = pygame.Rect(board_x + col * CELL_SIZE, board_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        if cell_rect.collidepoint(dragging_pos) and board_cards[row][col] is None:
                            place_card(row, col, dragging_card, dragging_hand)
                            check_flips(row, col)
                            dragging_card = None
                            dragging_hand = None
                            dragging_pos = None
                            if state == "game_ai":
                                current_turn = "opponent"
                            else:
                                current_turn = "opponent" if current_turn == "player" else "player"
                            break
                else:
                    # Si pas posé sur le plateau, annule le drag
                    dragging_card = None
                    dragging_hand = None
                    dragging_pos = None
            # Tour de l'IA
            if state == "game_ai" and current_turn == "opponent":
                move = ai_move()
                if move:
                    card, row, col = move
                    place_card(row, col, card, "opponent")
                    check_flips(row, col)
                    current_turn = "player"

    pygame.display.flip()

pygame.quit()
