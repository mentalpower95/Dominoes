import random


class Domino:
    domino_pieces = []
    computer_pieces = []
    player_pieces = []
    snake = []
    status = None

    def main(self):
        self.shuffle()
        while not self.start_game():
            self.shuffle()
        self.print_info()
        self.adding_pieces()

    def shuffle(self):
        self.domino_pieces = [[a, b] for b in range(7) for a in range(7) if a <= b]
        random.shuffle(self.domino_pieces)
        for _ in range(7):
            self.computer_pieces.append(self.domino_pieces.pop())
            self.player_pieces.append(self.domino_pieces.pop())

    def start_game(self):
        starting_pairs = [[6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0]]
        for pair in starting_pairs:
            if pair in self.player_pieces:
                self.snake.append(self.player_pieces.pop(self.player_pieces.index(pair)))
                self.status = "computer"
                return True
            elif pair in self.computer_pieces:
                self.snake.append(self.computer_pieces.pop(self.computer_pieces.index(pair)))
                self.status = "player"
                return True
        return False

    def adding_pieces(self):
        while True:
            if self.status == "player":
                playing_now = self.player_pieces
                while True:
                    chosen_number = input()
                    try:
                        chosen_number = int(chosen_number)
                        if abs(chosen_number) > len(self.player_pieces):
                            print("Invalid input. Please try again.")
                        else:
                            if self.checking_if_legal(chosen_number, playing_now):
                                break
                            else:
                                print("Illegal move. Please try again.")
                    except ValueError:
                        print("Invalid input. Please try again.")
            else:
                pressing = input()
                if pressing == "":
                    pass
                if not self.calculate_and_pick():
                    if len(self.domino_pieces) != 0:
                        take_piece = random.randrange(len(self.domino_pieces))
                        self.computer_pieces.append(self.domino_pieces.pop(take_piece))

            if len(self.computer_pieces) == 0:
                self.print_info()
                print("\nStatus: The game is over. The computer won!")
                break
            elif len(self.player_pieces) == 0:
                self.print_info()
                print("\nStatus: The game is over. You won!")
                break
            elif self.snake[0][0] == self.snake[-1][-1]:
                number = self.snake[0][0]
                counter = 0
                for pair in self.snake:
                    for x in pair:
                        if x == number:
                            counter += 1
                if counter == 8:
                    self.print_info()
                    print("\nStatus: The game is over. It's a draw!")
                    break

            self.status = "player" if self.status == "computer" else "computer"
            self.print_info()

    def print_info(self):
        print(70 * "=")
        print(f"Stock size: {len(self.domino_pieces)}")
        print(f"Computer pieces: {len(self.computer_pieces)}\n")
        if len(self.snake) < 7:
            print(*self.snake, sep="")
        else:
            print(f"{self.snake[0]}{self.snake[1]}{self.snake[2]}...{self.snake[-3]}{self.snake[-2]}{self.snake[-1]}")
        print(f"\nYour pieces:")
        piece_count = 1
        for piece in self.player_pieces:
            print(f"{piece_count}:{piece}")
            piece_count += 1
        if self.status == "computer":
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")

    def checking_if_legal(self, chosen_number, playing_now):
        if chosen_number > 0:
            check = playing_now[chosen_number - 1]
            if self.snake[-1][-1] in check:
                if self.snake[-1][-1] == check[0]:
                    self.snake.insert(len(self.snake), playing_now.pop(chosen_number - 1))
                else:
                    playing_now.remove(check)
                    turned_pair = [check[1], check[0]]
                    self.snake.insert(len(self.snake), turned_pair)
                return True
            else:
                return False
        elif chosen_number < 0:
            check = playing_now[abs(chosen_number) - 1]
            if self.snake[0][0] in check:
                if self.snake[0][0] == check[1]:
                    self.snake.insert(0, playing_now.pop(abs(chosen_number) - 1))
                else:
                    playing_now.remove(check)
                    turned_pair = [check[1], check[0]]
                    self.snake.insert(0, turned_pair)
                return True
            else:
                return False
        else:
            if len(self.domino_pieces) != 0:
                take_piece = random.randrange(len(self.domino_pieces))
                playing_now.append(self.domino_pieces.pop(take_piece))
            return True

    def calculate_and_pick(self):
        number_count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
        all_pieces = self.snake + self.computer_pieces
        counted_pairs = []
        duplicate_pairs = []
        for piece in all_pieces:
            for x in piece:
                number_count[str(x)] += 1
        for part in self.computer_pieces:
            duplicate_pairs.append(part)
            counted_pairs.append(number_count[str(part[0])] + number_count[str(part[1])])
        while len(duplicate_pairs) > 0:
            i = counted_pairs.index(max(counted_pairs))
            chosen_pair = duplicate_pairs[i]
            if self.snake[0][0] in chosen_pair:
                if self.snake[0][0] == chosen_pair[1]:
                    self.snake.insert(0, chosen_pair)
                else:
                    turned_pair = [chosen_pair[1], chosen_pair[0]]
                    self.snake.insert(0, turned_pair)
                self.computer_pieces.remove(chosen_pair)
                return True
            elif self.snake[-1][-1] in chosen_pair:
                if self.snake[-1][-1] == chosen_pair[0]:
                    self.snake.insert(len(self.snake), chosen_pair)
                else:
                    turned_pair = [chosen_pair[1], chosen_pair[0]]
                    self.snake.insert(len(self.snake), turned_pair)
                self.computer_pieces.remove(chosen_pair)
                return True
            del duplicate_pairs[i]
            del counted_pairs[i]
        return False




Domino().main()
