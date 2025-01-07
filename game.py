from random import randint


from files import Files

class Game:

    def __init__(self):
        self.tab= []
        self.init_tab = []
        self.width = 0
        self.height = 0
        self.grid_to_push = []
        self.playing = True
        self.score = 0
        self.win = False
        self.first = True


    def set(self, width, height):
        self.tab = [[0 for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def mines(self, nb):
        """nb: int > 0 nombre de minestab: tableau de tableau"""
        for i in range(len(self.tab)):
            cpt = 0
            left = 0
            while cpt < nb / len(self.tab):
                j = randint(0, len(self.tab[i]) - 1)
                if self.tab[i][j] == 0:
                    self.tab[i][j] = "X"
                    cpt += 1
            if left != 0:
                j = randint(0, len(self.tab[i]) - 1)
                if self.tab[i][j] == 0:
                    self.tab[i][j] = "X"
                    left -= 1

    def cases(self):
        for i in range(len(self.tab)):
            for j in range(len(self.tab[i])):
                if self.tab[i][j] == 0:
                    cpt = 0
                    for e in range(-1, 2):
                        for f in range(-1, 2):
                            new_i = i + e
                            new_j = j + f
                            if 0 <= new_i < len(self.tab) and 0 <= new_j < len(self.tab[i]) and self.tab[new_i][new_j] == "X":
                                cpt += 1

                            self.tab[i][j] = str(cpt)

    def clicked(self, x, y):
        if self.tab[x][y] == 1:
            return True
        elif self.tab[x][y] == 0:
            self.tab[x][y] = 2
            return False
        return False

    def recursiveDiscover(self, x, y):
        if self.tab[x][y] == 0:
            self.tab[x][y] = " "
            for e in range(-1, 2):
                for f in range(-1, 2):
                    new_x = x + e
                    new_y = y + f
                    if 0 <= new_x < len(self.tab) and 0 <= new_y < len(self.tab[x]):
                        if self.tab[x + e][y + f] == 0:
                            self.grid_to_push[x][y] = self.tab[x][y]
                            self.first = False
                            self.recursiveDiscover(new_x, new_y)
                        elif self.tab[x + e][y + f] != 1:
                            self.first = False
                            self.grid_to_push[x][y] = self.tab[x][y]
        elif self.tab[x][y] != "X":
            self.first = False
            self.grid_to_push[x][y] = self.tab[x][y]

        elif self.tab[x][y] == "X" and self.first == False:
            self.first = False
            self.playing = False

        return self.grid_to_push[x][y]

    def reset(self):
        """Réinitialise toutes les variables du jeu pour une nouvelle partie."""
        self.tab = []
        self.init_tab = []
        self.width = 0
        self.height = 0
        self.grid_to_push = []
        self.playing = True
        self.win = False

    def check_victory(self):
        for i in range(self.height):
            for j in range(self.width):

                if self.tab[i][j] != "X" and self.grid_to_push[i][j] == 0:
                    return False
        return True



game = Game()
files = Files()
