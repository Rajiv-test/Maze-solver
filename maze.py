from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,seed = None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_cells_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
        
    def _break_cells_r(self,i,j):
        self._cells[i][j].visited = True
        while True:
            neighbors = []
            if i-1 >= 0 and self._cells[i-1][j].visited == False:
                neighbors.append((i-1,j))
            if i + 1 <= len(self._cells)-1 and self._cells[i+1][j].visited == False:
                neighbors.append((i+1,j))
            if j - 1 >= 0 and self._cells[i][j-1].visited == False:
                neighbors.append((i,j-1))
            if j +1 <= len(self._cells[0])-1 and self._cells[i][j+1].visited == False:
                neighbors.append((i,j+1))
            if neighbors == []:
                self._draw_cell(i,j)
                return  
            choice = random.choice(neighbors)
            self.break_cell(i,j,*choice)
            self._break_cells_r(*choice)
            
            
    def break_cell(self,i1,j1,i2,j2):
        if i1==i2:
            if j2-j1 == 1:
                self._cells[i1][j1].has_bottom_wall = False
                self._cells[i2][j2].has_top_wall = False
            elif j2 - j1 == -1:
                self._cells[i1][j1].has_top_wall = False
                self._cells[i2][j2].has_bottom_wall = False
        elif j2 == j1:
            if i2-i1 == 1:
                self._cells[i1][j1].has_right_wall = False
                self._cells[i2][j2].has_left_wall = False
            elif i2-i1 == -1:
                self._cells[i1][j1].has_left_wall = False
                self._cells[i2][j2].has_right_wall = False
                
    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False