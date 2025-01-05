import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Ludovic")

# Couleurs (RGB)
BLACK = (0, 0, 0)
SCREEN = (119, 147, 108)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Variables divers
BLOCK_SIZE = 20
score = 0
speed = 1
fps = 5 + speed
clock = pygame.time.Clock()
num_obstacles = 5
obstacles = [
    (
        random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
        random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE,
    )
    for _ in range(num_obstacles)
]
paused = False

 # Charger la police depuis les assets
font = pygame.font.Font('assets/hack.ttf', 40)
lcd_font = pygame.font.Font('assets/nokia.ttf', 30)

# Charger et adapter les images
apple_img = pygame.image.load('assets/apple.png')
apple_img = pygame.transform.scale(apple_img, (BLOCK_SIZE, BLOCK_SIZE))
rock_img = pygame.image.load('assets/boulder.png')
rock_img = pygame.transform.scale(rock_img, (BLOCK_SIZE, BLOCK_SIZE))
head_img = pygame.image.load('assets/head_snake.png')
head_img = pygame.transform.scale(head_img, (BLOCK_SIZE, BLOCK_SIZE))
body_img = pygame.image.load('assets/body_snake.png')
body_img = pygame.transform.scale(body_img, (BLOCK_SIZE, BLOCK_SIZE))

# Charger la musique
bite_sound = pygame.mixer.Sound('assets/apple_bite.ogg')
game_over_sound = pygame.mixer.Sound('assets/game_over.wav')

# charger la musique de fond
pygame.mixer.music.load('assets/background.mp3')
pygame.mixer.music.play(-1) # -1 permet de jouer le son en boucle

# Réglage du volume
bite_sound.set_volume(1.0)
pygame.mixer.music.set_volume(0.5)

# -----   Fonction du serpent   -----
# Position initiale du serpent (x, y)
snake = [(WIDTH // 2, HEIGHT // 2)] # Liste des segments du serpent
snake_dx = 0 # Direction en X
snake_dy = 0 # Direction en Y

# Fonction pour envoyer le corps dans le sens de marche
def update_body_direction(prev_segment, curr_segment, next_segment, body_img):
    # Vérifier si le segment est aligné horizontalement
    if prev_segment[1] == curr_segment[1] == next_segment[1]:
        return body_img  # Aligné horizontalement
    # Vérifier si le segment est aligné verticalement
    elif prev_segment[0] == curr_segment[0] == next_segment[0]:
        return pygame.transform.rotate(body_img, 90)  # Aligné verticalement
    # Autres cas pour gérer les courbes
    elif prev_segment[0] < curr_segment[0] and next_segment[1] < curr_segment[1]:
        return pygame.transform.rotate(body_img, 90)  # Haut-droite
    elif prev_segment[1] < curr_segment[1] and next_segment[0] > curr_segment[0]:
        return pygame.transform.rotate(body_img, -90)  # Bas-droite
    # Ajoute d'autres cas pour les courbes ici...
    return body_img

# Fonction pour envoyer la tête dans le sens de marche
def update_head_direction(dx, dy, image):
    if dx > 0:
        return image
    elif dx < 0:
        return pygame.transform.flip(image, True, False)
    elif dy < 0:
        return pygame.transform.rotate(image, 90)
    elif dy > 0:
        return pygame.transform.rotate(image, -90)

# -----   Fonction des obstacles   -----
# Vérifier les collisions avec les obstacles
def check_obstacle_collision():
    if snake[0] in obstacles:
        return True
    return False

# Fonction pour dessiner les obstacles
def draw_obstacle():
    for obs_x, obs_y in obstacles:
        WINDOW.blit(rock_img, (obs_x, obs_y)) # dessiner chaque obstacle
    
# Fonction pour générer de nouveau obstacle
def generate_obstacle():
    obs = []
    while num_obstacles != len(obs):
        element = (
            random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
            random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE,
        )
        next_position = (snake[0][0] + snake_dx, snake[0][1] + snake_dy)
        if element not in snake and element != next_position:
            obs.append(element)
    return obs   

# -----   Fonction de la nourriture   -----
# Position de la nourriture
food_x = random.randint(0, (WIDTH // BLOCK_SIZE) -1) * BLOCK_SIZE
food_y = random.randint(0, (HEIGHT // BLOCK_SIZE) -1) * BLOCK_SIZE

# Fonction pour dessiner la pomme
def draw_food():
    WINDOW.blit(apple_img, (food_x, food_y))
    
# Fonction pour générer de nouvelles coordonnées pour la nourriture
def generate_food():
    food = (
        random.randint(0, (WIDTH // BLOCK_SIZE) -1) * BLOCK_SIZE,
        random.randint(0, (HEIGHT // BLOCK_SIZE) -1) * BLOCK_SIZE
    )
    if food in obstacles or food in snake:
        return generate_food()
    return food

# ----- Fonction pour les affichages -----
# Fonction pour afficher le score à l'écran
def display_score():
    score_text = lcd_font.render(f'SCORE : {score} - VITESSE : {speed}', True, BLACK)
    WINDOW.blit(score_text, (10, 10)) # on affiche le score en haut à gauche

# Fonction pour afficher le texte
def display_message(text, color):
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(message, text_rect)
    pygame.display.flip()
    if paused:
        pygame.time.delay(100)
    else:
        pygame.time.delay(2000) # Pause de 2 second avant de fermer

# ----- Fonction du jeux -----
# Boucle principale
def main():
    global snake_dx, snake_dy, food_x, food_y, score, speed, obstacles, paused
    head_direction = head_img # Renvoi l'image rectifiée à la création de la tête
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if not paused:
                    if event.key == pygame.K_UP and snake_dy == 0:
                        snake_dx = 0
                        snake_dy = -BLOCK_SIZE
                        head_direction = update_head_direction(snake_dx, snake_dy, head_img)
                    elif event.key == pygame.K_DOWN and snake_dy == 0:
                        snake_dx = 0
                        snake_dy = BLOCK_SIZE
                        head_direction = update_head_direction(snake_dx, snake_dy, head_img)
                    elif event.key == pygame.K_LEFT and snake_dx == 0:
                        snake_dy = 0
                        snake_dx = -BLOCK_SIZE
                        head_direction = update_head_direction(snake_dx, snake_dy, head_img)
                    elif event.key == pygame.K_RIGHT and snake_dx == 0:
                        snake_dy = 0
                        snake_dx = BLOCK_SIZE
                        head_direction = update_head_direction(snake_dx, snake_dy, head_img)
                        
        # Si en pause, afficher un message
        if paused:
            pygame.mixer.music.pause()
            display_message('PAUSE', WHITE)
            continue
    
        # Mettre à jour la position du serpent
        new_head = (snake[0][0] + snake_dx, snake[0][1] + snake_dy) # Nouvelle tête
        snake.insert(0, new_head) # Ajouter la nouvelle tête au début
        
        # Vérifier les collisions avec les bords et lui-même
        if (
            snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT
        ) or len(snake) > 2 and snake[0] in snake[1:] or check_obstacle_collision(): # Ajouter la vérification avec lui-même
            WINDOW.fill(BLACK)
            pygame.mixer.music.stop()
            game_over_sound.play()
            display_message(f'GAME OVER - Score : {score}', RED)
            running = False
            return # Sortir directement pour éviter d'autres erreurs
            
        # Vérifier les collisions avec la nourriture
        if snake[0] == (food_x, food_y):
            bite_sound.play()
            food_x, food_y = generate_food() # Générer la nouvelle position de la nourriture
            score += 10 # On augmente le score par 10
            if (score // 100) == speed:
                speed += 1 # augmenter la vitesse du serpent
                obstacles = generate_obstacle() # On change les obstacles
        else:
            snake.pop() # Retirer le dernier segment si pas de nourriture mangée

        # Remplir l'écran de noir
        WINDOW.fill(SCREEN)
        
        # On affiche le score
        display_score()
        
        # Dessiner les obstacles
        draw_obstacle()
        
        # Dessiner la nourriture
        draw_food()

        # Dessiner le serpent
        for index, segment in enumerate(snake):
            if index == 0:
                WINDOW.blit(head_direction, (segment[0], segment[1]))
            elif index == len(snake) - 1: # pour avoir la queue du serpent
                pygame.draw.rect(WINDOW, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            else:
                prev_segment = snake[index - 1]
                next_segment = snake[index + 1]
                body_direction = update_body_direction(prev_segment, segment, next_segment, body_img)
                WINDOW.blit(body_direction, (segment[0], segment[1]))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôle de la vitesse du jeu
        clock.tick(fps)

    # Quitter Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
