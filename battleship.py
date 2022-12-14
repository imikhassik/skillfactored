from random import randint, choice


def instructions():
    print("-------------------------------------------------")
    print("                  МОРСКОЙ БОЙ                    ")
    print("-------------------------------------------------")
    print("   Введите координаты, чтобы расположить корабли:")
    print("   1 корабль на 3 клетки, 2 на две, 4 на одну.   ")
    print("   Достаточно указать первую клетку и направление")
    print("   Например: 1 1 v расположит корабль от левой   ")
    print("   верхней клетки по вертикали.                  ")
    print("   Направления:                                  ")
    print("   h - по горизонтали, v - по вертикали          ")
    print("-------------------------------------------------")


class Board:
    def __init__(self):
        self.board = [['O'] * 6 for _ in range(6)]

    def get_board(self):
        return self.board

    def place_ship(self, ship, board):
        # Черновое расположение корабля
        try:
            while ship.size:
                if ship.radar(board):
                    self.board[ship.x][ship.y] = '*'
                    if ship.direction in ('v', 'V') and ship.size > 1:
                        ship.x += 1
                    elif ship.direction in ('h', 'H') and ship.size > 1:
                        ship.y += 1
                    ship.size -= 1
                else:
                    return False
            return True
        except IndexError:
            if board == user_board:
                print("Координаты за пределами поля")
            return False

    def confirm_placement(self, flag):
        # Если корабль можно расположить, то подтверждает расположение, если нет - откатывает
        if flag:
            for row in range(6):
                for column in range(6):
                    if self.get_board()[row][column] == '*':
                        self.get_board()[row][column] = '■'
        else:
            for row in range(6):
                for column in range(6):
                    if self.get_board()[row][column] == '*':
                        self.get_board()[row][column] = 'O'

    def print_boards(self, other=None):
        # Печатает одно или два поля
        if other:
            print()
            print('  | 1 | 2 | 3 | 4 | 5 | 6 |       | 1 | 2 | 3 | 4 | 5 | 6 |\n')
            for i in range(6):
                print(i + 1, end=' | ')
                for j in range(6):
                    print(f"{self.board[i][j]}", end=' | ')
                print(f'\t{i + 1}', end=' | ')
                for j in range(6):
                    print(f"{other.get_board()[i][j]}", end=' | ')
                print('\n')
        else:
            print()
            print('  | 1 | 2 | 3 | 4 | 5 | 6 |\n')
            for i in range(6):
                print(i + 1, end=' | ')
                for j in range(6):
                    print(f"{self.board[i][j]}", end=' | ')
                print('\n')

    def reload(self):
        # Перезагружает поле. Нужна, когда некуда больше поставить корабль.
        self.__init__()
        Ship.setup_fleet(self, 1)

    def scan(self):
        # Проверяет, остались ли еще корабли
        for i in self.get_board():
            for j in i:
                if j == '■':
                    return True
        return False

    def shoot(self, other):
        # Получает координаты выстрела и применяет выстрелы на полях
        x, y = None, None
        if other == ai_board:
            while Board.scan(other):
                try:
                    x, y = input("Введите координаты выстрела: ").split()
                    x, y = map(int, (x, y))
                    if x in range(1, 7) and y in range(1, 7):
                        x -= 1
                        y -= 1
                    if self.board[x][y] != 'O' and self.board[x][y] != '■':
                        print("Сюда уже стреляли!")
                        continue
                    break
                except (ValueError, IndexError):
                    print("Некорректные координаты. Пример корректного ввода: 2 1")
                    continue
        else:
            while Board.scan(other):
                x, y = randint(0, 5), randint(0, 5)
                if self.board[x][y] != 'O' and self.board[x][y] != '■':
                    continue
                break

        while Board.scan(other):
            self.board[x][y] = f'\033[1;91mX\033[0m' if other.board[x][y] == '■' else '\033[1;34;1mT\033[0m'
            other.board[x][y] = f'\033[1;91mX\033[0m' if other.board[x][y] == '■' else '\033[1;34;1mT\033[0m'
            user_board.print_boards(user_battlefield)
            break

    @staticmethod
    def set_turn(t=0):
        # Меняет очередь
        if t:
            t = 0
        else:
            t = 1
        return t


class Ship:
    def __init__(self, x=0, y=0, direction='h', size=3):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size

    def get_coordinates(self, board):
        # Получает координаты для расположения кораблей
        if board == user_board:
            while True:
                try:
                    if self.size > 1:
                        self.x, self.y, self.direction = input("Введите координаты и направление корабля: ").split()
                    else:
                        self.x, self.y = input("Введите координаты корабля: ").split()
                    self.x, self.y = map(int, (self.x, self.y))
                    if self.x in range(1, 7) and self.y in range(1, 7) and self.direction in ('h', 'H', 'v', 'V'):
                        self.x -= 1
                        self.y -= 1
                        break
                    elif self.direction not in ('h', 'H', 'v', 'V'):
                        print("Направление: h - по горизонтали, v - по вертикали")
                    else:
                        print("Координаты за пределами поля")
                except ValueError:
                    if self.size > 1:
                        print("Некорректные координаты. Пример корректного ввода: 2 1 h")
                    else:
                        print("Некорректные координаты. Пример корректного ввода для корабля на одну клетку: 2 1")
                    continue
        elif board == ai_board:
            if self.size > 1:
                self.x, self.y, self.direction = randint(0, 5), randint(0, 5), choice(['h', 'v'])
            else:
                self.x, self.y = randint(0, 5), randint(0, 5)

    def radar(self, board):
        # Проверяет все клетки вокруг потенциальных координат для расположения корабля
        search_area = board.get_board().copy()
        try:
            if self.x < 0 or self.x > 5 or self.y < 0 or self.y > 5:
                raise ValueError("Координаты за пределами поля")
            elif 0 < self.x < 5 and 0 < self.y < 5:
                search_area = [row[self.y-1:self.y+2] for row in search_area[self.x-1:self.x+2]]
            elif self.x == 0 and self.y == 0:
                search_area = [row[self.y:self.y+2] for row in search_area[self.x:self.x+2]]
            elif self.x == 5 and self.y == 0:
                search_area = [row[self.y:self.y+2] for row in search_area[self.x-1:self.x+1]]
            elif self.x == 0 and self.y == 5:
                search_area = [row[self.y-1:self.y+1] for row in search_area[self.x:self.x+2]]
            elif self.x == 5 and self.y == 5:
                search_area = [row[self.y-1:self.y+1] for row in search_area[self.x-1:self.x+1]]
            elif self.x == 0:
                search_area = [row[self.y-1:self.y+2] for row in search_area[self.x:self.x+2]]
            elif self.x == 5:
                search_area = [row[self.y-1:self.y+2] for row in search_area[self.x-1:self.x+1]]
            elif self.y == 0:
                search_area = [row[self.y:self.y+2] for row in search_area[self.x-1:self.x+2]]
            elif self.y == 5:
                search_area = [row[self.y-1:self.y+1] for row in search_area[self.x-1:self.x+2]]
        except ValueError:
            if board == user_board:
                print("Координаты за пределами поля")
                return False
            else:
                return False

        for row in search_area:
            if '■' in row and board == user_board:
                print("Другой корабль слишком близко")
                cleanup = input("Очистить поле? (y/n): ").lower()
                if cleanup == 'y':
                    board.reload()
                else:
                    return False
            elif '■' in row and board == ai_board:
                return False

        else:
            return True

    @staticmethod
    def setup_fleet(board, reload=0):
        # Расставляет корабли по координатам
        ships = {}
        sizes = [3, 2, 2, 1, 1, 1, 1]
        i = 0
        failed_attempts = 0
        while i <= 6:
            if reload:
                i = 0
                reload = 0
                if board == user_board:
                    board.print_boards()
            ships[i] = Ship()
            ships[i].size = sizes[i]
            ships[i].get_coordinates(board)
            if board.place_ship(ships[i], board):
                board.confirm_placement(1)
                if board == user_board:
                    board.print_boards()
                i += 1
            else:
                failed_attempts += 1
                if failed_attempts == 100:
                    board.reload()
                    break
                board.confirm_placement(0)
                continue


instructions()
user_board = Board()
ai_board = Board()
user_board.print_boards()
Ship.setup_fleet(user_board)
Ship.setup_fleet(ai_board)
user_battlefield = Board()
ai_battlefield = Board()
user_board.print_boards(user_battlefield)
turn = Board.set_turn()
print("Теперь стреляйте!")
while True:
    if turn:
        user_battlefield.shoot(ai_board)
        if not ai_board.scan():
            print("Победа! Все вражеские корабли взорваны!")
            break
        turn = Board.set_turn(turn)
    else:
        ai_battlefield.shoot(user_board)
        print("Противник стрелял!")
        if not user_board.scan():
            print("Все ваши корабли взорваны. Искусственный интеллект победил!")
            break
        turn = Board.set_turn(turn)
