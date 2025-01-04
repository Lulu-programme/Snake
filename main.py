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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Taille du bloc (le serpent est composé de blocs)
BLOCK_SIZE = 20

# Position initiale du serpent (x, y)
snake = [(WIDTH // 2, HEIGHT // 2)] # Liste des segments du serpent
snake_dx = 0 # Direction en X
snake_dy = 0 # Direction en Y

# Position de la nourriture
food_x = random.randint(0, (WIDTH // BLOCK_SIZE) -1) * BLOCK_SIZE
food_y = random.randint(0, (HEIGHT // BLOCK_SIZE) -1) * BLOCK_SIZE

# Framerate
FPS = 10
clock = pygame.time.Clock()

# Police pour le text
font = pygame.font.SysFont('Hack', 40)

# Variable de score
score = 0

# Fonction pour afficher le score à l'écran
def display_score():
    score_text = font.render(f'Score : {score}', True, WHITE)
    WINDOW.blit(score_text, (10, 10)) # on affiche le score en haut à gauche

# Fonction pour afficher le texte
def display_message(text, color):
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(message, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000) # Pause de 2 second avant de fermer
    
# Fonction pour générer de nouvelles coordonnées pour la nourriture
def generate_food():
    return (
        random.randint(0, (WIDTH // BLOCK_SIZE) -1) * BLOCK_SIZE,
        random.randint(0, (HEIGHT // BLOCK_SIZE) -1) * BLOCK_SIZE
    )

# Boucle principale
def main():
    global snake_dx, snake_dy, food_x, food_y, score
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = BLOCK_SIZE
                elif event.key == pygame.K_LEFT and snake_dx == 0:
                    snake_dy = 0
                    snake_dx = -BLOCK_SIZE
                elif event.key == pygame.K_RIGHT and snake_dx == 0:
                    snake_dy = 0
                    snake_dx = BLOCK_SIZE
    
        # Mettre à jour la position du serpent
        new_head = (snake[0][0] + snake_dx, snake[0][1] + snake_dy) # Nouvelle tête
        snake.insert(0, new_head) # Ajouter la nouvelle tête au début
        
        # Vérifier les collisions avec les bords et lui-même
        if (
            snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT
        ) or len(snake) > 2 and snake[0] in snake[1:]: # Ajouter la vérification avec lui-même
            WINDOW.fill(BLACK)
            display_message(f'GAME OVER - Score : {score}', RED)
            running = False
            return # Sortir directement pour éviter d'autres erreurs
            
        # Vérifier les collisions avec la nourriture
        if snake[0] == (food_x, food_y):
            food_x, food_y = generate_food() # Générer la nouvelle position de la nourriture
            score += 10 # On augmente le score par 10
        else:
            snake.pop() # Retirer le dernier segment si pas de nourriture mangée

        # Remplir l'écran de noir
        WINDOW.fill(BLACK)
        
        # On affiche le score
        display_score()
        
        # Dessiner la nourriture
        pygame.draw.rect(WINDOW, RED, (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))

        # Dessiner le serpent
        for segment in snake:
            pygame.draw.rect(WINDOW, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôle de la vitesse du jeu
        clock.tick(FPS)

    # Quitter Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
