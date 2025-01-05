import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'
os.environ['KIVY_WINDOW'] = 'sdl2'

from multiprocessing import Process
from score_app import ScoreApp  # Importer l'application KivyMD
from snake import main as pygame_game  # Importer la fonction du jeu Pygame

def start_kivy():
    score_app = ScoreApp()
    score_app.run()

def start_pygame():
    pygame_game()

if __name__ == "__main__":
    # Lancer les deux processus séparés
    kivy_process = Process(target=start_kivy)
    pygame_process = Process(target=start_pygame)

    kivy_process.start()
    pygame_process.start()

    kivy_process.join()
    pygame_process.join()
