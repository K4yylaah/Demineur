import csv


class Files:

    def save_game(self, name, score, difficulty, tab):
        game_data = {
            "nom": name,
            "score": score,
            "difficulte": difficulty,
            "tableau": tab
        }

        with open('game_data.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["nom", "score", "difficulte", "tableau"])

            # Si le fichier est vide, écrire l'en-tête
            if file.tell() == 0:
                writer.writeheader()

            board_str = "\n".join([" ".join(map(str, row)) for row in tab])
            game_data["tableau"] = board_str
            writer.writerow(game_data)

    import csv

    def read_game_data(self, file_path='game_data.csv', filter_name=None, filter_value=None, filter_difficult=None):
        all_games = []

        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if not all(key in row for key in ["nom", "score", "difficulte", "tableau"]):
                        print(f"Ligne invalide dans le fichier CSV : {row}")
                        continue

                    try:
                        player_name = row["nom"]
                        score = int(row["score"])
                        difficulty = row["difficulte"]
                        board_str = row["tableau"].strip('"')  # Supprime les guillemets autour du tableau

                        # Conversion de la chaîne en tableau
                        board = [list(map(lambda x: int(x) if x.isdigit() else x, line.split())) for line in
                                 board_str.split('\n')]

                        all_games.append({
                            "nom": player_name,
                            "score": score,
                            "difficulte": difficulty,
                            "tableau": board
                        })

                    except ValueError as e:
                        print(f"Erreur de conversion dans la ligne : {row} - {e}")
                        continue

            # Application des filtres
            if filter_name:
                all_games = [game for game in all_games if game["nom"] == filter_name]
            if filter_value:
                all_games = [game for game in all_games if game["score"] == filter_value]
            if filter_difficult:
                all_games = [game for game in all_games if game["difficulte"] == filter_difficult]

        except FileNotFoundError:
            print(f"Le fichier {file_path} n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

        return all_games


files = Files()
game_board = [[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0],[0, 1, 0], [1, 0, 1], [0, 0, 0]]

