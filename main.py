from tkinter import Tk, BOTH, Canvas
import time
import random
class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, color):
        line.draw(self.canvas, color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


    def draw(self, canvas, fill_color, width):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=width)

class Cell:
    def __init__(self, x1, x2, y1, y2, win, color = "red", left = True, right = True, top = True, bottom = True):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self.color = color
        self.visited = None

    def draw(self):
        top_wall = Line(self._x1, self._x2, self._y1, self._y1)
        bottom_wall = Line(self._x1, self._x2, self._y2, self._y2)
        left_wall = Line(self._x1, self._x1, self._y1, self._y2)
        right_wall = Line(self._x2, self._x2, self._y1, self._y2)
        if self.has_top_wall:
            top_wall.draw(self._win, self.color, 2)
        if self.has_bottom_wall:
            bottom_wall.draw(self._win, self.color, 2)
        if self.has_left_wall:
            left_wall.draw(self._win, self.color, 2)
        if self.has_right_wall:
            right_wall.draw(self._win, self.color, 2)
        if not self.has_top_wall:
            top_wall.draw(self._win, "#323232", 2)
        if not self.has_bottom_wall:
            bottom_wall.draw(self._win, "#323232", 2)
        if not self.has_left_wall:
            left_wall.draw(self._win, "#323232", 2)
        if not self.has_right_wall:
            right_wall.draw(self._win, "#323232", 2)

    def find_centre(self):
        onex = self._x1 - self._x2
        twox = onex / 2
        finalx = self._x2 + twox
        oney = self._y1 - self._y2
        twoy = oney / 2
        finaly = self._y2 + twoy
        return finalx, finaly
    
    def draw_move(self, to_cell, undo=False):
        print("draw")
        if undo == False:
            colour = "red"
        elif undo == True:
            colour = "gray"
        selfx, selfy = self.find_centre()
        print(to_cell._x1, to_cell._y1)
        print(to_cell._x2, to_cell._y2)
        otherx, othery = to_cell.find_centre()
        print(otherx, othery)

        newline = Line(int(selfx), int(otherx), int(selfy), int(othery))
        newline.draw(self._win, colour, 2)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, color = "Red", seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.counter = 0
        self.color = color
        self._create_cells(self.color)
        if seed != None:
            random.seed(seed)

    def _create_cells(self, color):
        self._cells = []
        for i in range(self.num_rows):
            self.row = []
            for j in range(self.num_cols):
                self._draw_cell(i, j, color)
            self._cells.append(self.row)
        self._break_entrance_and_exit()
            

    def _draw_cell(self, i, j, color):
        x1 = self.x1 + j * self.cell_size_x
        y1 = self.y1 + i * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        cell = Cell(x1, x2, y1, y2, self.win.canvas, color)
        self.row.append(cell)
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()  # Call the redraw method to update the visualization
        

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self._cells[0][0].draw()
        self._cells[self.num_rows - 1][self.num_cols - 1].draw()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            if i < len(self._cells) and j + 1 < len(self._cells[i]) and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if i + 1 < len(self._cells) and j < len(self._cells[i]) and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if i < len(self._cells) and j - 1 >= 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if i - 1 >= 0 and j < len(self._cells[i]) and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))


            if len(to_visit) == 0:
                #breakpoint()
                #self._cells[i][j].draw()
                return
            else:
                direction = random.randrange(0, len(to_visit))
                next_i, next_j = to_visit[direction]

            # Knock down walls based on neighboring cell's position
            if next_i == i + 1:  # Down
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            elif next_i == i - 1:  # Up
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif next_j == j + 1:  # Right
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif next_j == j - 1:  # Left
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            else:
                print(f"Warning: Unexpected cell position. No wall broken between ({i}, {j}) and ({next_i}, {next_j})")

            self._cells[i][j].draw()
            self._cells[next_i][next_j].draw()
            self._animate()
            time.sleep(0.015)
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        
        # Print statement to check if the current cell is the target
        print(self._cells[i][j] == self._cells[self.num_rows - 1][self.num_cols - 1])
        
        # Check if the current cell is the exit
        if self._cells[i][j] == self._cells[self.num_rows - 1][self.num_cols - 1]:
            return True
        
        # Define possible moves in directions: right, down, left, up
        possible_moves = [
            (0, 1, 'right'),   # right
            (1, 0, 'down'),    # down
            (0, -1, 'left'),   # left
            (-1, 0, 'up')      # up
        ]
        
        found_path = False  # Variable to track if any valid path is found

        for di, dj, direction in possible_moves:
            next_i, next_j = i + di, j + dj
            
            # Check if the next cell is within bounds and not visited
            if (0 <= next_i < len(self._cells) and 
                0 <= next_j < len(self._cells[next_i]) and 
                not self._cells[next_i][next_j].visited):
                
                # Check for walls and move accordingly
                if direction == 'right' and not self._cells[i][j].has_right_wall:
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])
                    if self._solve_r(next_i, next_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[next_i][next_j], True)
                
                elif direction == 'down' and not self._cells[i][j].has_bottom_wall:
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])
                    if self._solve_r(next_i, next_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[next_i][next_j], True)

                elif direction == 'left' and not self._cells[i][j].has_left_wall:
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])
                    if self._solve_r(next_i, next_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[next_i][next_j], True)

                elif direction == 'up' and not self._cells[i][j].has_top_wall:
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])
                    if self._solve_r(next_i, next_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[next_i][next_j], True)

        # If none of the moves lead to the exit, it's a dead end
        self._cells[i][j].visited = False  # Unmark the cell as part of backtracking
        return False




def main():
    counter = 0
    win = Window(2050, 2050)
    cells = 10
    # maze_size = 650  # Total size of the maze (e.g., 800x800 pixels)
    # while counter <= 100:
    #     size = maze_size / cells  # Adjust cell size based on number of cells
    #     maze = Maze(5, 5, cells, cells, size, size, win, "White")
    #     maze._break_walls_r(0, 0)
    #     time.sleep(1.5)
    #     win.canvas.delete("all")  # Clear the canvas
    #     #cells += 1  # Increase the number of cells
    #     #counter += 1  # Increment the counter
    maze = Maze(5, 5, 15, 15, 15, 5, win, "White")
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze._solve_r(0, 0)
    win.wait_for_close()
    
    
        

main()
