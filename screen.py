from tkinter import *
import time

from game import Game
from files import Files

game = Game()
files = Files()



class Screen:

    def __init__(self, screen):
        self.screen = screen
        self.screen.title("Menu Principal - Démineur")
        self.main_menu()
        self.grid = []
        self.timer_label = None

    def main_menu(self):
        self.clear_window()
        self.menubar()
        title_label = Label(self.screen, text="Bienvenue dans le Démineur !", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)

        start_button = Button(self.screen, text="Démarrer une partie", font=("Helvetica", 14), command=self.game_menu)
        start_button.pack(pady=10)

        start_button1 = Button(self.screen, text="Scores", font=("Helvetica", 14), command=self.score_menu)
        start_button1.pack(pady=10)

        exit_button = Button(self.screen, text="Quitter le jeu", font=("Arial", 16), command=quit)
        exit_button.pack(pady=10)

        start_button2 = Button(self.screen, text="Hall of Fame", font=("Helvetica", 14), command=self.Hall_of_Fame_menu)
        start_button2.pack(pady=10)

    def game_menu(self):
        self.clear_window()
        self.menubar()
        self.difficult_list()
        game_label = Label(self.screen, text="Écran de jeu", font=("Helvetica", 16))
        game_label.pack(pady=20)
        back_button = Button(self.screen, text="Retour au menu", font=("Helvetica", 14), command=self.main_menu)
        back_button.pack(pady=10)

    def menubar(self):
        menubar = Menu(screen)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Import", command = lambda : self.score_menu())
        menu1.add_command(label="Home", command = lambda : self.main_menu())
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=screen.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)
        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="A propos", command="")
        menubar.add_cascade(label="Aide", menu=menu2)
        screen.config(menu=menubar)

    def difficult_list(self):
        self.value = StringVar()
        self.value.set("1")
        bouton1 = Radiobutton(screen, text="Facile", variable=self.value, value=1)
        bouton2 = Radiobutton(screen, text="Moyen", variable=self.value, value=2)
        bouton3 = Radiobutton(screen, text="Difficile", variable=self.value, value=3)
        bouton1.pack()
        bouton2.pack()
        bouton3.pack()

        difficulty_label = Label(self.screen, text="Sélectionnez une difficulté", font=("Helvetica", 12))
        difficulty_labels = Label(self.screen, textvariable=self.value, font=("Helvetica", 12))
        difficulty_label.pack()
        difficulty_labels.pack()
        self.screen.update()

        button = Button(self.screen, text="Lancer", font=("Helvetica", 14), command=lambda: self.start_game(self.value.get()))
        button.pack(pady=10)

    def clear_window(self):
        for widget in self.screen.winfo_children():
            if widget != self.timer_label:
                widget.destroy()

    def start_game(self, difficult):
        game.reset()
        self.start_time = time.time()

        if difficult == "1":
            game.set(4, 4)
            game.mines(10)
        if difficult == "2":
            game.set(16, 16)
            game.mines(40)
        if difficult == "3":
            game.set(30, 16)
            game.mines(99)

        game.init_tab = [[cell if cell == "X" else 0 for cell in row] for row in game.tab]

        game.init_tab = [row[:] for row in game.tab]  # Sauvegarde de l'état initial
        self.grid = self.create_empty_grid()  # Grille vide pour le suivi des découvertes
        game.cases()  # Calcul des nombres autour des mines
        game.grid_to_push = self.grid  # Mise à jour de la grille à afficher
        self.refresh()
        print(game.tab)

    def score_menu(self):
        tab = files.read_game_data()
        self.clear_window()
        self.menubar()
        self.selected_game = None

        frame = LabelFrame(self.screen, text='Votre score :', font=("Arial", 16))
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        # Bouton rejouer désactivé au départ
        self.reload_button = Button(self.screen, text="Rejouer", borderwidth=1, state="disabled",command=self.replay_game)
        self.reload_button.grid(row=10, column=10, pady=20)

        # Ajouter des boutons pour chaque sauvegarde
        for ligne, game in enumerate(tab):
            Button(
                self.screen, text=f"{game['nom']} - {game['score']} - {game['difficulte']}", borderwidth=1, command=lambda g=game: self.select_savegame(g)).grid(row=ligne + 1, column=0, padx=5, pady=5)

        screen.geometry("400x300")

    def cell_clicked(self, row, col):
        print(f"Cell clicked: ({row}, {col})")
        print(game.first)
        game.recursiveDiscover(row, col)
        self.refresh()
        if game.check_victory():
            game.win = True
            self.end_game()

    def create_empty_grid(self):
        tab = [[0 for _ in range(game.width)] for _ in range(game.height)]
        return tab

    def refresh(self):
        self.screen.update()
        self.clear_window()
        self.menubar()





        for x in range(game.height):
            for y in range(game.width):
                button = Button(self.screen, text=str(game.grid_to_push[x][y]), width=2, height=1, command=lambda r=x, c=y: self.cell_clicked(r, c))
                button.grid(row=x, column=y)

        button_width = button.winfo_reqwidth()
        button_height = button.winfo_reqheight()

        window_width = button_width * game.width + 1
        window_height = button_height * game.height + 21

        self.screen.geometry(f"{window_width}x{window_height}")

        if not game.playing:
            self.end_game()

    def select_savegame(self, game):
        self.selected_game = game
        self.reload_button.config(state="normal")

    def replay_game(self):
        if self.selected_game:
            # Charger les dimensions et le tableau sauvegardé
            game.tab = [row[:] for row in
                        self.selected_game["tableau"]]  # Copie profonde pour éviter les problèmes de référence
            game.height = len(game.tab)
            game.width = len(game.tab[0])

            # Créer une nouvelle grille vide pour `grid_to_push`
            self.grid = [[0 for _ in range(game.width)] for _ in range(game.height)]
            game.grid_to_push = self.grid  # Associe la grille vide

            # Restaurer l'état initial si nécessaire (par exemple, init_tab)
            game.init_tab = [row[:] for row in self.selected_game["tableau"]]

            # Mettre à jour l'affichage et réinitialiser l'état de jeu
            game.playing = True  # Réactiver l'état de jeu
            self.refresh()
            self.screen.update()
            game.win = False

    def end_game(self):
        self.clear_window()
        self.menubar()
        game.first = True
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time


        title = StringVar()
        if game.win:
            title.set("Gagné")
        else :
            title.set("Perdu")
        title_label = Label(self.screen, textvariable=title, font=("Helvetica", 16))
        title_label.pack(pady=20)

        game.score = int(self.elapsed_time)
        score = StringVar()
        score.set(str(self.elapsed_time))
        score.set("Score :  " + str(game.score))
        game_label = Label(self.screen, textvariable=score, font=("Helvetica", 16))
        game_label.pack(pady=20)


        valueInput = StringVar()
        valueInput.set("Inconnu")
        entree = Entry(screen, textvariable=valueInput, width=30)
        entree.pack()
        self.screen.update()

        difficult = StringVar()
        if game.height == 9:
            difficult.set("Facile")
        elif game.height == 16 and game.width == 16:
            difficult.set("Moyen")
        elif game.width == 30 and game.height == 16:
            difficult.set("Difficile")

        reload = Button(self.screen, text="Sauvegarder", borderwidth=1, command=lambda: (files.save_game(valueInput.get(), game.score, difficult.get(), game.init_tab), self.main_menu()) )
        reload.pack(pady=20)

        screen.geometry("400x300")

        #print("Grid to push : " ,game.grid_to_push)
        #print("Tab : " ,game.tab)
        #print("Init Tab : ", game.init_tab)

    def Hall_of_Fame_menu(self):
        self.clear_window()
        self.menubar()
        all_data = files.read_game_data()
        difficulties = {"Facile": [], "Moyen": [], "Difficile": []}
        for game in all_data:
            difficulties[game["difficulte"]].append(game)
        frame_facile = LabelFrame(self.screen, text="Facile", font=("Arial", 12))
        frame_facile.grid(row=0, column=0, padx=10, pady=10)
        frame_moyen = LabelFrame(self.screen, text="Moyen", font=("Arial", 12))
        frame_moyen.grid(row=0, column=1, padx=10, pady=10)
        frame_difficile = LabelFrame(self.screen, text="Difficile", font=("Arial", 12))
        frame_difficile.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.display_entries(frame_facile, difficulties["Facile"])
        self.display_entries(frame_moyen, difficulties["Moyen"])
        self.display_entries(frame_difficile, difficulties["Difficile"])
        self.screen.update()

    def display_entries(self, frame, data):
        data.sort(key=lambda x: x['score'])
        for i, game in enumerate(data):
            label = Label(frame, text=f"{i + 1}. {game['nom']} - {game['score']}", font=("Arial", 10))
            label.grid(row=i, column=0, sticky=W)











if __name__ == "__main__":
    screen = Tk()
    app = Screen(screen)
    screen.geometry("400x300")
    screen.mainloop()
