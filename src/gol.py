"""Conwayn Game of Life"""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import pygame

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
        disp_x = 1920   #ikkunan x-resoluutio
        disp_y = 1080   #ikkunan y-resoluutio
        block_x = disp_x/self.maxx  #tiilen koko x-suunnassa
        block_y = disp_y/self.maxx  #tiilen koko y-suunnassa
        block_color = (0,200,0) #tiilen väri
        if self.renderer == 'pygame':
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode((disp_x,disp_y))   #arvataan HD-näyttö
            running = True
            while running:
                # katsotaan, onko prosessointi yritetty lopettaa
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        running = False
                # piirretään
                ## haetaan elävät solut
                live_cells = []
                for y, row in enumerate(self.field):
                    if 1 in row:
                        for x, value in enumerate(row):
                            if value == 1:
                                live_cells.append((x,y))
                screen.fill("white")
                rects = []
                for x,y in live_cells:
                    rects.append(pygame.Rect(x*block_x,disp_y-(y*block_y),block_x,block_y))
                for rect in rects:
                    pygame.draw.rect(screen, block_color, rect)
                pygame.display.flip()   #päivitetään ruutu

                # päivitetään pelitila
                self.update_state()

                clock.tick(self.fps)    #odotetaan seuraavaan frameen
            return 1
        else:
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

    def __init__(self, size, initstate, init_method='array', renderer='matplotlib'):
        if renderer == 'pygame':
            pygame.init()
        self.rounds = -1    #kierrosmäärä
        self.maxx = size    #pelikentän sivun koko soluina. Tällä hetkellä tukee vain neliön muotoisia kenttiä.
        self.testvar = 1
        self.generation = 0
        self.fps = 30       #fps pygame-animaatiolle
        self.init_field(size, initstate, init_method)
        self.screensize = self.maxx
        self.steady_state = 0
        self.renderer = renderer

        #kuvien alustaminen
        self.fig = plt.figure(frameon=False)
        self.axis = plt.axes(frame_on=False)
