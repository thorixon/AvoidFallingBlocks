import random, os, time, threading


class Map:
    def __init__(self, height = 8, width = 7):
        self.height = height
        self.width = width
        self.player_position = int(self.width/2)
        self.empty_sign = " "
        self.block_sign = "O"
        self.player_sign = "P"
        self.map = [[self.empty_sign for i in range(self.width)] for j in range(self.height)]
        self.map[self.height-1][self.player_position] = self.player_sign
        random.seed()

    def falling_of_blocks(self):
        for i in range(len(self.map)-2, 0, -1):
            self.map[i] = self.map[i-1]

    def will_block_fall_on_player(self):
        for pos in range(self.width):
            if self.map[-2][pos] == self.block_sign and self.map[-1][pos] == self.player_sign:
                return True
        return False

    def generate_falling_blocks(self, least=0, most=3):
        self.map[0] = [self.empty_sign for i in range(self.width)]
        amount = random.randint(least, most)
        while amount > 0:
            pos = random.randint(0, self.width-1)
            if self.map[0][pos] == self.empty_sign:
                self.map[0][pos] = self.block_sign
                amount -= 1

    def change_player_position(self, direction):
        for pos in range(self.width):
            if self.map[-1][pos] == self.player_sign:
                self.map[-1][pos] = self.empty_sign
                if direction == "left":
                    self.map[-1][max(0, pos-1)] = self.player_sign
                elif direction == "right":
                    self.map[-1][min(pos+1, self.width-1)] = self.player_sign
                break

    def print_map(self):
        for row in self.map:
            row_string = "|"
            for el in row:
                row_string += "{:^3}".format(el)
            row_string += "|"
            print(row_string.center(100))


class Game:
    def __init__(self):
        self.game_map = Map()
        self.score = 0
        self.stop_event = threading.Event()

    def print_game(self):
        self.game_map.print_map()
        print((str(self.score).center(100)))

    @staticmethod
    def clear_screen():
        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    def player_controls(self):
        while not self.stop_event.is_set():
            direction = input()
            if direction == "a":
                self.game_map.change_player_position("left")
            if direction == "d":
                self.game_map.change_player_position("right")
            self.clear_screen()
            self.print_game()
            self.stop_event.wait(0.1)

    def next_turn(self, falling_time, least_blocks, most_blocks):
        self.print_game()
        time.sleep(falling_time)
        if self.game_map.will_block_fall_on_player():
            return False
        self.game_map.falling_of_blocks()
        self.game_map.generate_falling_blocks(least_blocks, most_blocks)
        self.score += 1
        self.clear_screen()
        return True

    def start_game(self):
        cond = True
        print("Avoid the falling blocks!\n"
              "Type 'a' to go left, type 'd' to go right.\n"
              "The game works best when played in terminal.\n"
              "Type anything to start!".center(100))
        input()
        player_thread = threading.Thread(target=self.player_controls)
        player_thread.start()
        while cond:
            if self.score > 175:
                cond = self.next_turn(0.3, 3, 5)
            elif self.score > 150:
                cond = self.next_turn(0.4, 2, 5)
            elif self.score > 125:
                cond = self.next_turn(0.5, 2, 4)
            elif self.score > 100:
                cond = self.next_turn(0.6, 1, 4)
            elif self.score > 75:
                cond = self.next_turn(0.7, 1, 3)
            elif self.score > 50:
                cond = self.next_turn(0.7, 0, 3)
            elif self.score > 25:
                cond = self.next_turn(0.7, 0, 2)
            else:
                cond = self.next_turn(0.7, 0, 1)

        print(f"Your result is {self.score}".center(100))
        self.stop_event.set()
        player_thread.join()
