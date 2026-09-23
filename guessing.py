import random
import time
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.attempts = 0
        self.games = 0
        self.wins = 0
        self.total_time = 0
class Game:
    def __init__(self):
        self.players = []
        self.leaderboard = []
    def save_leaderboard(self):
        with open("leaderboard.txt", "w") as file:
            for p in self.leaderboard:
                file.write(f"{p.name},{p.score},{p.games},"
                           f"{p.wins},{p.total_time}\n")
    def load_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    p = Player(data[0])
                    p.score = int(data[1])
                    p.games = int(data[2])
                    p.wins = int(data[3])
                    p.total_time = float(data[4])
                    self.leaderboard.append(p)
        except FileNotFoundError:
            pass
    def add_players(self):
        self.players = []
        while True:
            try:
                n = int(input("Number of players (2-5): "))
                if 2 <= n <= 5:
                    break
                print("Enter between 2 and 5.")
            except ValueError:
                print("Enter a valid number.")
        for i in range(n):
            while True:
                name = input("Player name: ").strip()

                if name == "":
                    print("Name cannot be empty.")
                    continue
                duplicate = False
                for p in self.players:
                    if p.name.lower() == name.lower():
                        duplicate = True
                if duplicate:
                    print("Duplicate name.")
                else:
                    self.players.append(Player(name))
                    break
    def choose_level(self):
        print("1. Easy (1-50)")
        print("2. Medium (1-100)")
        print("3. Hard (1-500)")
        choice = input("Choose level: ")
        if choice == "1":
            return 50, 5
        elif choice == "2":
            return 100, 7
        elif choice == "3":
            return 500, 10
        else:
            print("Invalid level.")
            return None, None
    def update_leaderboard(self, p):
        for old in self.leaderboard:
            if old.name.lower() == p.name.lower():
                old.score += p.score
                old.games += p.games
                old.wins += p.wins
                old.total_time += p.total_time
                return
        self.leaderboard.append(p)
    def start_game(self):
        self.add_players()
        maximum, limit = self.choose_level()
        if maximum is None:
            return
        secret = random.randint(1, maximum)
        random.shuffle(self.players)
        for p in self.players:
            p.attempts = 0
            p.games += 1
            won = False
            print("\n", p.name, "'s turn")
            start = time.time()
            while p.attempts < limit:
                try:
                    guess = int(input("Guess the number: "))
                except ValueError:
                    print("Enter a number.")
                    continue
                if guess < 1 or guess > maximum:
                    print("Guess must be within the range.")
                    continue
                p.attempts += 1
                if guess == secret:
                    taken = time.time() - start
                    p.wins += 1
                    points = max(0, 100 - (p.attempts - 1) * 10)
                    bonus = 50 if taken <= 10 else 25 if taken <= 20 else 0
                    p.score += points + bonus
                    p.total_time += taken
                    print("Correct!")
                    print("Time:", round(taken, 2), "seconds")
                    print("Points:", points, "Bonus:", bonus)
                    won = True
                    break
                elif guess > secret:
                    print("Too High")
                else:
                    print("Too Low")
                if abs(secret - guess) <= 5:
                    print("Very Close!")
                p.score = max(0, p.score - 5)
                print("5 points deducted.")
            if not won:
                print("No attempts left. Zero points for this round.")
                print("Secret number:", secret)
            self.update_leaderboard(p)
        self.save_leaderboard()
        print("\nGame completed!")
        self.show_leaderboard()
    def show_rules(self):
        print("\nRULES")
        print("1. 2 to 5 players.")
        print("2. Names must be unique.")
        print("3. Choose Easy, Medium, or Hard.")
        print("4. Players have limited attempts.")
        print("5. Hints: Too High, Too Low, Very Close.")
        print("6. Incorrect guesses reduce points.")
        print("7. Quick correct guesses get time bonuses.")
        print("8. No points when attempts finish.")
        print("9. Leaderboard is saved after each game.")
    def show_leaderboard(self):
        if not self.leaderboard:
            print("No scores available.")
            return
        self.leaderboard.sort(key=lambda p: p.score, reverse=True)
        print("\nLEADERBOARD")
        for i, p in enumerate(self.leaderboard, 1):
            print(i, p.name, "Score:", p.score,
                  "Games:", p.games, "Wins:", p.wins)
    def search_player(self):
        name = input("Player name: ")
        for p in self.leaderboard:
            if p.name.lower() == name.lower():
                print("Name:", p.name)
                print("Score:", p.score)
                print("Games:", p.games)
                print("Wins:", p.wins)
                print("Total time:", round(p.total_time, 2))
                return
        print("Player not found.")
    def menu(self):
        self.load_leaderboard()
        while True:
            print("\n1. New Game")
            print("2. Rules")
            print("3. Leaderboard")
            print("4. Search Player")
            print("5. Exit")
            choice = input("Choice: ")
            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.show_rules()
            elif choice == "3":
                self.show_leaderboard()
            elif choice == "4":
                self.search_player()
            elif choice == "5":
                self.save_leaderboard()
                print("Thank you!")
                break
            else:
                print("Invalid choice.")
game = Game()
game.menu()
