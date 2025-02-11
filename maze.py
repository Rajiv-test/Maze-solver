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
        self._solve()
        
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
            
            
    def _solve(self):
        return self._solve_r(0,0)
    

    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j].visited = True
        if i == len(self._cells)-1 and j == len(self._cells[0])-1:
            return True
        neighbors = []
        if not (i == len(self._cells) -1 and j ==len(self._cells[0])-1) and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
            neighbors.append((i,j+1))
        if not (i ==0 and j == 0 ) and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
            neighbors.append((i,j-1))
        if not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
            neighbors.append((i+1,j))
        if not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
            neighbors.append((i-1,j))

        if neighbors == []:
            return False
        for cell in neighbors:
            to_cell_x ,to_cell_y = cell
            self._cells[i][j].draw_move(self._cells[to_cell_x][to_cell_y])
            if self._solve_r(*cell):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[to_cell_x][to_cell_y],undo= True)
        return False
    
    def _solve_bfs(self):
        
        to_visit = [(0,0)]
        while to_visit:
            self._animate()
            neighbors = []
            i,j = to_visit.pop(0)
            self._cells[i][j].visited = True
            
            
            if not (i == len(self._cells) -1 and j ==len(self._cells[0])-1) and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
                to_visit.append((i,j+1))
                neighbors.append((i,j+1))
            if not (i ==0 and j == 0 ) and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
                to_visit.append((i,j-1))
                neighbors.append((i,j-1))
            if not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
                to_visit.append((i+1,j))
                neighbors.append((i+1,j))
            if not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
                to_visit.append((i-1,j)) 
                neighbors.append((i-1,j)) 
            for neighbor in neighbors:
                to_i,to_j = neighbor
                self._cells[i][j].draw_move(self._cells[to_i][to_j])
                if to_i == len(self._cells)-1 and to_j == len(self._cells[0])-1:
                    return True
        return False
