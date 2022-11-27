import copy


class Tetris:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.current_figure = None
        self.current_figure_rotate_count = 0
        self.O = [[4, 14, 15, 5]]
        self.I = [[4, 14, 24, 34], [3, 4, 5, 6]]
        self.S = [[5, 4, 14, 13], [4, 14, 15, 25]]
        self.Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
        self.L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        self.J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
        self.T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        self.table = ['-' for _ in range(self.columns * self.rows)]
        self.table_tmp = None
        self.table_size = self.columns * self.rows
        self.left_border = [i for i in range(0, self.table_size, self.columns)]
        self.right_border = [i for i in range(self.columns - 1, self.table_size, self.columns)]
        self.bottom_border = [i for i in range(self.table_size - self.columns, self.table_size)]
        self.figures = {'O': [[4, 14, 15, 5]],
                        'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
                        'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
                        'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
                        'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                        'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                        'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}

    def convert_1d_to_2d(self, cols):
        return [self.table[i: i + cols] for i in range(0, len(self.table), cols)]

    def check_left_side(self):
        for index in self.current_figure[self.current_figure_rotate_count % len(self.current_figure)]:
            if index in self.left_border:
                return False
        return True

    def check_right_side(self):
        for index in self.current_figure[self.current_figure_rotate_count % len(self.current_figure)]:
            if index in self.right_border:
                return False
        return True

    def check_bottom_side(self):
        for index in self.current_figure[self.current_figure_rotate_count % len(self.current_figure)]:
            if index in self.bottom_border:
                self.table_tmp = self.table.copy()
                temp_list = []
                temp_left_list = []
                temp_right_list = []
                for temp_index in self.current_figure[self.current_figure_rotate_count % len(self.current_figure)]:
                    temp_list.append(temp_index - self.columns)
                    temp_left_list.append(temp_index + 1)
                    temp_right_list.append(temp_index - 1)
                self.bottom_border = list(set(self.bottom_border + temp_list))
                self.left_border = list(set(self.left_border + temp_left_list))
                self.right_border = list(set(self.right_border + temp_right_list))
                return False
        return True

    def move_current_figure(self, command):
        if command == "rotate":
            if self.check_bottom_side():
                self.current_figure_rotate_count += 1
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns) % self.table_size
        elif command == "down":
            if self.check_bottom_side():
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns) % self.table_size
        elif command == "right":
            if self.check_right_side() and self.check_bottom_side():
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns + 1) % self.table_size
            elif self.check_bottom_side():
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns) % self.table_size
        elif command == "left":
            if self.check_left_side() and self.check_bottom_side():
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns - 1) % self.table_size
            elif self.check_bottom_side():
                for figure_state_id, state in enumerate(self.current_figure):
                    for index_id, index in enumerate(state):
                        self.current_figure[figure_state_id][index_id] = (index + self.columns) % self.table_size

    def clear_filled_rows(self):
        for key in range(0, self.table_size, self.columns):
            if self.table[key: key + self.columns].count('0') == self.columns:
                self.table[key: key + self.columns] = []
                self.table[:0] = ['-' for _ in range(self.columns)]
                self.update_borders(key)

    def update_borders(self, key_):
        for val in range(key_, key_ + self.columns):
            self.left_border.remove(val)
            self.right_border.remove(val)
            self.bottom_border.remove(val - self.columns)

    def draw_figure_on_grid(self, figure_name, command=None):
        # removed this row in stage 4 because the empty line disappeared after stage 3
        # print()
        if command is not None:
            self.move_current_figure(command)
        for index in self.current_figure[self.current_figure_rotate_count % len(self.current_figure)]:
            self.table[index] = '0'
        self.draw_grid()
        self.check_bottom_side()
        self.reset_grid()
        if self.table_tmp:
            self.table = self.table_tmp.copy()

    def reset_grid(self):
        self.table = ['-' for _ in range(self.table_size)]

    def check_game_over(self):
        for key in range(0, self.rows):
            if self.table[key] == '0':
                return True
        return False

    def draw_grid(self, figure=None, command=None):
        if not figure:
            print('\n'.join(' '.join(*zip(*row)) for row in self.convert_1d_to_2d(self.columns)), end="\n\n")
        elif figure == 'O':
            self.draw_figure_on_grid('O', command)
        elif figure == 'I':
            self.draw_figure_on_grid('I', command)
        elif figure == 'S':
            self.draw_figure_on_grid('S', command)
        elif figure == 'Z':
            self.draw_figure_on_grid('Z', command)
        elif figure == 'L':
            self.draw_figure_on_grid('L', command)
        elif figure == 'J':
            self.draw_figure_on_grid('J', command)
        elif figure == 'T':
            self.draw_figure_on_grid('T', command)


def main():
    state = False
    columns, rows = map(int, input().split())
    my_game = Tetris(columns, rows)
    my_game.draw_grid()
    command = input()

    while command != "exit" and state is False:
        if command == 'piece':
            figure = input()
            my_game.current_figure = copy.deepcopy(my_game.figures[figure])
            my_game.current_figure_rotate_count = 0
            if my_game.table_tmp:
                my_game.table = my_game.table_tmp.copy()
        elif command == "break":
            my_game.clear_filled_rows()
            my_game.table_tmp = my_game.table.copy()
            figure = None
        state = my_game.check_game_over()
        my_game.draw_grid(figure, command)
        if state is True:
            print("Game Over!")
            break
        command = input().lower()


if __name__ == "__main__":
    main()
