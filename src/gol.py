"""Conwayn Game of Life"""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

class GolMain:
    """Game of Life -peliä kuvaava luokka"""

    testvar = 0
    #Laita ykköseksi, jos systeemi on löytänyt kiintopisteen

    def update_state(self):
        """Iteroi pelikenttää yksi kierros eteenpäin."""
        newfield = [[0] * self.maxx for i in range(self.maxx)]
        for x in range(self.maxx):
            for y in range(self.maxx):
                lifeval = 0
                for i in range (x-1,x+2):
                    for j in range (y-1,y+2):
                        if ((i < 0 or i >= self.maxx or j < 0 or j >= self.maxx) 
                        or (i == x and j == y)):
                            value = 0
                        else:
                            value = self.field[j][i]
                        lifeval = lifeval + value
                if lifeval == 2 and self.field[y][x] == 1:
                    newfield[y][x] = 1
                elif lifeval == 3:
                    newfield[y][x] = 1
                else:
                    newfield[y][x] = 0
        if self.field == newfield:
            self.steady_state = 1
        self.field = newfield
        return newfield

    def printfield(self, fieldmap):
        """Tulosta kentän tila"""
        self.axis.clear()
        self.axis = plt.axes(xlim =(0,self.screensize),
                ylim =(0,self.screensize))
        plt.grid()
        self.axis.get_xaxis().set_ticks([])
        self.axis.get_yaxis().set_ticks([])
        self.axis.grid(True)
        block = self.screensize/self.maxx
        for x in range (self.maxx):
            for y in range (self.maxx):
                if fieldmap[y][x] == 1:
                    self.axis.add_patch(Rectangle((x,y),block,block))
    
    def frames(self):
        """Apufunktio animaation piirtoon... Mutta hoitaa tosiasiassa myös varsinaisen pelin pyörittämisen!"""
        self.steady_state = 1
        yield self.field
        for i in range(self.rounds):
            print(i)
            yield self.update_state()
            if self.steady_state == 1:
                break

    def run_game(self, maxrounds):
        self.rounds = maxrounds
        anim = FuncAnimation(self.fig, self.printfield, frames=self.frames, interval=500)
        plt.show()
        if self.steady_state == 1:
            return -1
        return 1
   
    def __init__(self, size, initstate):
        self.rounds = -1
        self.field = [[0] * size for i in range(0,size)]
        self.maxx = size
        self.testvar = 1
        for x,y in initstate:
            if x >= size or y >= size or x < 0 or y < 0:
                raise Exception("Solun indeksit yli pelialueen rajojen!")
            self.field[y][x] = 1
        self.screensize = size
        self.steady_state = 0

        #kuvien alustaminen
        self.fig = plt.figure(frameon=False)
        self.axis = plt.axes(frame_on=False)
        #self.axis.get_xaxis().set_ticks([])
        #self.axis.get_yaxis().set_ticks([])
        