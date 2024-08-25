import random

class Ship:
    def __init__(se, x, y, s):
        se.x = x
        se.y = y
        se.s = s
        se.h = 0

    def is_sunk(se):
        return se.h == se.s

class Board:
    def __init__(se, s=6):
        se.s = s
        se.sh = []
        se.h = set()
        se.m = set()

    def add_ship(se, sh):
        for x in range(sh.x, sh.x + sh.s):
            if se.is_occupied(x, sh.y):
                raise ValueError("Корабль не может быть размещен на этой позиции.")
        se.sh.append(sh)

    def is_occupied(se, x, y):
        for sh in se.sh:
            if x >= sh.x and x < sh.x + sh.s and y == sh.y:
                return True
        return False

    def shoot(se, x, y):
        if (x, y) in se.h or (x, y) in se.m:
            return False

        for sh in se.sh:
            if x >= sh.x and x < sh.x + sh.s and y == sh.y:
                sh.h += 1
                se.h.add((x, y))
                return True

        se.m.add((x, y))
        return False

    def all_ships_sunk(se):
        return all(sh.is_sunk() for sh in se.sh)

    def display_board(se, show_opponent_sh=False):
        print("  ", end="")
        for x in range(se.s):
            print(f"{x+1} ", end="")
        print()

        for y in range(se.s):
            print(f"{y+1} ", end="")
            for x in range(se.s):
                if (x, y) in se.h:
                    print("X ", end="")
                elif (x, y) in se.m:
                    print("T ", end="")
                elif show_opponent_sh and se.is_occupied(x, y):
                    print("■  ", end="")
                else:
                    print("O ", end="")
            print()

class Game:
    def __init__(se, board_s=6):
        se.player_board = Board(board_s)
        se.ai_board = Board(board_s)
        se.setup_game()

    def setup_game(se):
        se.place_ships(se.player_board)
        se.place_ships(se.ai_board)

    def place_ships(se, board):
        sh_s = [3,2,2,1,1,1,1]
        for s in sh_s:
            while True:
                x = random.randint(0, board.s - 1)
                y = random.randint(0, board.s - 1)
                try:
                    board.add_ship(Ship(x, y, s))
                    break
                except ValueError:
                    continue

    def player_turn(se):
        while True:
            try:
                x = int(input("Введите координату X: ")) - 1
                y = int(input("Введите координату Y: ")) - 1
                if se.ai_board.shoot(x, y):
                    print("Попадание!")
                else:
                    print("Промах.")
                break
            except (ValueError, IndexError):
                print("Неверные координаты, попробуйте еще раз.")

    def ai_turn(se):
        while True:
            x = random.randint(0, se.player_board.s - 1)
            y = random.randint(0, se.player_board.s - 1)
            if se.player_board.shoot(x, y):
                print("Компьютер попал в ваш корабль.")
                break
            else:
                print("Компьютер промахнулся.")
                break

    def play(se):
        while True:
            print("Ваше игровое поле:")
            se.player_board.display_board(show_opponent_sh=True)
            print("\nПоле противника:")
            se.ai_board.display_board()
            se.player_turn()
            if se.ai_board.all_ships_sunk():
                print("Вы победили!")
                break
            se.ai_turn()
            if se.player_board.all_ships_sunk():
                print("Компьютер победил.")
                break

if __name__ == "__main__":
    game = Game()
    game.play()
