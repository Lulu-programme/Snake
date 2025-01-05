from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton


class ScoreApp(MDApp):
    def build(self):
        # Créer une disposition verticale
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        # Label pour afficher le score
        self.score_label = MDLabel(
            text="Score : 0",
            halign="center",
            font_style="H4"
        )
        layout.add_widget(self.score_label)

        # Boutons pour interagir (exemple : pause et quitter)
        pause_button = MDRaisedButton(
            text="Pause",
            pos_hint={"center_x": 0.5},
            on_release=self.pause_game
        )
        quit_button = MDRaisedButton(
            text="Quitter",
            pos_hint={"center_x": 0.5},
            on_release=self.quit_game
        )
        layout.add_widget(pause_button)
        layout.add_widget(quit_button)

        return layout

    def pause_game(self, *args):
        # Exemple : Afficher un message pour montrer l'interaction
        print("Pause demandée")

    def quit_game(self, *args):
        # Fermer l'application
        print("Quitter le jeu")
        self.stop()

    def update_score(self, score):
        # Mettre à jour le score
        self.score_label.text = f"Score : {score}"


if __name__ == "__main__":
    ScoreApp().run()
