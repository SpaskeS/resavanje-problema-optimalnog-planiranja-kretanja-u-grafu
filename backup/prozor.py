from tkinter import *
import tkinter.messagebox

class Prozor:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)

        self.napravi_elemente()
        self.konfigurisi_elemente()

        self.canvas_mode = None
        self.grana_pocetak = 0
        self.x_grana= None
        self.y_grana= None
        self.prvi_cvor = None
        self.grane = {}
        self.cvorovi = {}
        self.prepreke = []
        self.pocetak = None
        self.postoji_pocetak = False
        self.kraj = None
        self.postoji_kraj=False
        self.p = {}
        self.algoritam = None

    def napravi_elemente(self):
        self.button_alg_1 = Button(self.root, text='Algoritam grube sile', command=self.start_alg_1, width=30)
        self.button_alg_2 = Button(self.root, text='Pohlepni algoritam', command=self.start_alg_2, width=30)
        self.button_alg_3 = Button(self.root, text='Genetski algoritam', command=self.start_alg_3, width=30)
        self.button_pocetak = Button(self.root, text='Početak', command=self.pocetak, width=30)
        self.button_kraj = Button(self.root, text='Kraj', command=self.kraj, width=30)
        self.button_dodaj_cvor = Button(self.root, text='Dodaj čvor', command=self.dodaj_cvor, width=30)
        self.button_dodaj_granu = Button(self.root, text='Dodaj granu', command=self.dodaj_granu, width=30)
        self.button_izbrisi_cvor = Button(self.root, text='Izbriši čvor', command=self.izbrisi_cvor, width=30)
        self.button_izbrisi_granu = Button(self.root, text='Izbriši granu', command=self.izbrisi_granu, width=30)
        self.button_reset = Button(self.root, text='Reset', command=self.reset, width=30)
        self.button_exit = Button(self.root, text='Exit', command= self.quit, width=30)
        self.button_dodaj_prepreku = Button(self.root, text='Dodaj prepreku', command = self.dodaj_prepreku, width=30)
        self.canvas = Canvas(self.root, width = 800, height = 700, bg='white')


    def konfigurisi_elemente(self):
        self.button_alg_1.grid(column=0, row = 0)
        self.button_alg_2.grid(column=1, row = 0)
        self.button_alg_3.grid(column=2, row = 0)
        self.button_pocetak.grid(column=3, row=1)
        self.button_kraj.grid(column=4, row=1)
        self.button_dodaj_cvor.grid(column = 3, row = 2)
        self.button_dodaj_granu.grid(column=4, row = 2)
        self.button_izbrisi_cvor.grid(column=3, row=3)
        self.button_izbrisi_granu.grid(column=4, row=3)
        self.button_exit.grid(column=4, row=0)
        self.button_reset.grid(column = 4, row=4)
        self.button_dodaj_prepreku.grid(column = 3, row=4)
        self.canvas.grid(row=1, column=0, columnspan=3, rowspan=4)

        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        self.root.grid_columnconfigure(2,weight=1)
        self.root.grid_columnconfigure(3,weight=1)
        self.root.grid_columnconfigure(4,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_rowconfigure(2,weight=1)
        self.root.grid_rowconfigure(3,weight=1)
        self.root.grid_rowconfigure(4,weight=1)
        self.canvas.bind('<Button-1>', self.canvas_klik)

    def start_alg_1(self):
        if tkinter.messagebox.askquestion('Algoritam grube sile', 'Pokreni algoritam grube sile?') == 'yes':
            print('Pokrecem algoritam grube sile')
            self.generate_p()
            self.algoritam = 'b'

    def start_alg_2(self):
        if tkinter.messagebox.askquestion('Pohlepni algoritam', 'Pokreni Pohlepni algoritam?') == 'yes':
            print('Pokrecem Pohlepni algoritam')
            self.generate_p()
            self.algoritam = 'h'

    def start_alg_3(self):
        if tkinter.messagebox.askquestion('Genetski algoritam', 'Pokreni genetski algoritam?') == 'yes':
            print('Pokrecem genetski algoritam')
            self.generate_p()
            self.algoritam = 'g'

    def pocetak(self):
        self.canvas_mode = 'pocetak'

    def kraj(self):
        self.canvas_mode='kraj'

    def dodaj_cvor(self):
        self.canvas_mode = 'dodaj_cvor'

    def dodaj_granu(self):
        self.canvas_mode = 'dodaj_granu'

    def izbrisi_cvor(self):
        self.canvas_mode = 'izbrisi_cvor'

    def izbrisi_granu(self):
        self.canvas_mode = 'izbrisi_granu'

    def dodaj_prepreku(self):
        self.canvas_mode = 'dodaj_prepreku'

    def reset(self):
        if tkinter.messagebox.askquestion('Reset', 'Da li hocete da restartuje graf?') == 'yes':
            print('Restartujem graf')
            self.canvas.delete(ALL)
            self.grane = {}
            self.cvorovi = {}
            self.prepreke = []
            self.canvas_mode = None

    def grana_klik(self, event):
        if self.canvas_mode == 'izbrisi_granu':
            self.canvas.delete(event)
            self.grane.pop(event)

    def canvas_klik(self,event):
        x = event.x
        y = event.y

        if self.canvas_mode == 'dodaj_cvor':
            for (id, koordinate) in self.cvorovi.items():
                if abs(x-koordinate[0]) < 50 and abs(y-koordinate[1]) < 50:
                    print('Drugi cvor je previse blizu')
                    return
            cvor = self.canvas.create_oval(x-15, y-15, x+15, y+15, outline='red', fill='gray')
            self.cvorovi[cvor] = (x, y)

        if self.canvas_mode == 'dodaj_granu':
            for (id, koordinate) in self.cvorovi.items():
                if abs(koordinate[0]-x) <= 15 and abs(koordinate[1]-y) <= 15:
                    if self.grana_pocetak==0:
                        self.x_grana = x
                        self.y_grana = y
                        self.prvi_cvor = id
                        self.grana_pocetak=1
                    else:
                        if id == self.prvi_cvor:
                            print('Cvor ne moze imati povratnih grana')
                            return
                        self.grana_pocetak=0
                        grana = self.canvas.create_line(self.cvorovi[self.prvi_cvor][0], self.cvorovi[self.prvi_cvor][1], koordinate[0], koordinate[1], width=4, fill='blue')
                        self.grane[grana] = (self.prvi_cvor, id)
                        self.canvas.tag_lower(grana)
                        self.canvas.tag_bind(grana, '<Button-1>', lambda g: self.grana_klik(grana))
                        self.prvi_cvor = None

        if self.canvas_mode == 'izbrisi_cvor':
            for (id, koordinate) in self.cvorovi.items():
                if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                    self.canvas.delete(id)
                    self.cvorovi.pop(id)
                    grane_za_brisanje = []
                    for(gid, cvorovi_grane) in self.grane.items():
                        if id == cvorovi_grane[0] or id == cvorovi_grane[1]:
                            self.canvas.delete(gid)
                            grane_za_brisanje.append(gid)
                    for gid in grane_za_brisanje:
                        self.grane.pop(gid)
                    return

        if self.canvas_mode == 'pocetak':
            for (id, koordinate) in self.cvorovi.items():
                if abs(x-koordinate[0]) < 15 and abs(y-koordinate[1]) < 15:
                    if self.postoji_pocetak == False:
                        self.canvas.itemconfig(id, fill='green')
                        self.pocetak=id
                        self.postoji_pocetak=True
                    else:
                        if tkinter.messagebox.askquestion('Promeni start', 'Da li hocete da promenite pocetni cvor?') == 'yes':
                            self.canvas.itemconfig(self.pocetak, fill='gray')
                            self.canvas.itemconfig(id, fill='green')
                            self.pocetak=id

        if self.canvas_mode == 'kraj':
            for (id, koordinate) in self.cvorovi.items():
                if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                        if self.postoji_kraj == False:
                            self.canvas.itemconfig(id, fill='red')
                            self.kraj=id
                            self.postoji_kraj=True
                        else:
                            if tkinter.messagebox.askquestion('Promeni kraj', 'Da li hocete da promenite ciljni cvor?') == 'yes':
                                    self.canvas.itemconfig(self.kraj, fill='gray')
                                    self.canvas.itemconfig(id, fill='red')
                                    self.kraj=id

        if self.canvas_mode == 'dodaj_prepreku':
            for (id, koordinate) in self.cvorovi.items():
                if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                    self.prepreke.append(id)
                    self.canvas.itemconfig(id, fill='black')

    def quit(self):
        self.root.destroy()

    def generate_p(self):

        cvorovi = []

        for (id, koord) in self.cvorovi.items():
            cvorovi.append(chr(id+64))

        self.pocetak = chr(self.pocetak + 64)
        self.kraj = chr(self.kraj + 64)

        for i in range(len(self.prepreke)):
            self.prepreke[i] = chr(64 + self.prepreke[i])

        grane = []

        for (id, nodes) in self.grane.items():
            grane.append((chr(nodes[0] + 64), chr(nodes[1] + 64)))

        self.p = {
            'nodes': cvorovi,

            'edges' : grane,

            'obstacles' : self.prepreke,

            'start' : self.pocetak,

            'target' : self.kraj
        }

    def get_p(self):
        return self.p

    def get_algoritam(self):
        return self.algoritam
