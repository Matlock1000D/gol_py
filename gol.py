from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

class gol_main:

    testvar = 0

    def update_state(self):
        newfield = [[0] * self.maxx for i in range(self.maxx)]
        for x in range(self.maxx):
            for y in range(self.maxx):
                lifeval = 0
                for i in range (x-1,x+2):
                    for j in range (y-1,y+2):
                        if ((i < 0 or i >= self.maxx or j < 0 or j >= self.maxx) or (i == x and j == y)):
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
        if newfield == self.field:
            return -1
        self.field = newfield

    def printfield(self):
        self.axes.clear()
        block = self.screensize/self.maxx
        for x in range (self.maxx):
            for y in range (self.maxx):
                self.axes.add_patch(Rectangle((x,y),block,block))
        plt.show()
    
    def run_game(self, rounds):
        self.printfield()
        for i in range(rounds):
            if self.update_state() == -1:
                return -1
            self.printfield()
        return 1

    def __init__(self, size, initstate, screensize=1000):
        self.field = [[0] * size for i in range(0,size)]
        self.maxx = size
        self.testvar = 1
        for x,y in initstate:
            if x >= size or y >= size or x < 0 or y < 0:
                raise Exception("Solun indeksit yli pelialueen rajojen!")
            self.field[y][x] = 1
        self.screensize = screensize

        #kuvien alustaminen
        self.fig = plt.figure()
        self.axis = plt.axes(xlim =(0, 0,self.screensize),
                ylim =(0, 0,self.screensize))


def frames():
    while True:
        yield Regr_magic()


fig = plt.figure()

x = []
y = []
def animate(args):
    x.append(args[0])
    y.append(args[1])
    return plt.plot(x, y, color='g')


anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000)
plt.show()