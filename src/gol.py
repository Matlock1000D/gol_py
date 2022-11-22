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
        while self.generation < self.rounds:
            self.generation += 1
            yield self.update_state()
            if self.steady_state == 1:
                break

    def run_game(self, maxrounds):
        """Pelin pääsilmukka"""
        self.rounds = maxrounds
        anim = FuncAnimation(self.fig, self.printfield, frames=self.frames, interval=100)
        plt.show()
        anim.save('gol_anim.gif')
        if self.steady_state == 1:
            return -1
        return 1
    
    def read_data(self, initstate):
        """Luetaan data tiedostosta"""
        with open(initstate) as stagefile:
            data = stagefile.read()
        data_rows = data.split()
        if len(data_rows) != len(data_rows[0]):
            raise Exception("Pelialue ei ole neliömäinen!")
        if not all(cell == '0' or cell == '1' for cell in (cell for row in data_rows for cell in row)):
            raise Exception("Kiellettyjä merkkejä kenttätiedostossa")
        self.maxx = len(data_rows)
        self.field = [[0] * self.maxx for i in range(0,self.maxx)]
        for y, row in enumerate(data_rows):
            for x, cell in enumerate(row):
                self.field[y][x] = int(cell)
        self.field.reverse()    #y-akseli oikein päin
   
    def init_field(self, size, initstate, init_method='array'):
        """Kentän alkutilanteen asetus"""
        if init_method == 'array':
            self.field = [[0] * size for i in range(0,size)]    #pelikentän alustus kuolleiksi soluiksi
            for x,y in initstate:
                if x >= size or y >= size or x < 0 or y < 0:
                    raise Exception("Solun indeksit yli pelialueen rajojen!")
                self.field[y][x] = 1
        elif init_method == 'file':
            self.read_data(initstate)
        else:
            raise Exception("Tällaista alustusmetodia emme tue!")

    def __init__(self, size, initstate, init_method='array'):
        self.rounds = -1    #kierrosmäärä
        self.maxx = size    #pelikentän sivun koko soluina. Tällä hetkellä tukee vain neliön muotoisia kenttiä.
        self.testvar = 1
        self.generation = 0
        self.init_field(size, initstate, init_method)
        self.screensize = self.maxx
        self.steady_state = 0

        #kuvien alustaminen
        self.fig = plt.figure(frameon=False)
        self.axis = plt.axes(frame_on=False)
