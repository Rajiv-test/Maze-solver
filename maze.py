from cell import Cell
from time import sleep

class Maze:
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        
        self._create_cells()
    
    def _create_cells(self):
        self._cells = [[]for row in range(self._num_rows)]
        for row in range(len(self._cells)):
            for col in range(self._num_cols):
                self._cells[row].append(Cell(self._win))
        
        for row in range(len(self._cells)):
            for col in range(self._num_cols):
                self._draw_cell(self._cells[row][col],row,col)
        
    def _draw_cell(self,cell,i,j):
        x1 = self._x1+(self._cell_size_x * i)
        y1 = self._y1+(self._cell_size_y * j)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell.draw(x1,y1,x2,y2)
        self._animate()
       
       
    def _animate(self):
        if self._win is None:
            return None
        self._win.redraw()
        sleep(0.005)
       
       
       
       
       
       

       
       
       
       
                 
                




        
    