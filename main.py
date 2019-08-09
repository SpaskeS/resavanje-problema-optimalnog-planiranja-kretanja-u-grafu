from tkinter import *
import tkinter.messagebox

# TODO: Srediti elemente po klasama
# TODO: Izbaciti globalne promenljive ako je moguce
# TODO: staviti da ne mogu da se biraju dva pocetka i dva kraja


canvas_mode = None
grana_pocetak = 0
x_grana= None
y_grana= None
prvi_cvor = None
grane = {}
cvorovi = {}

def start_alg_1():
    if tkinter.messagebox.askquestion('Algoritam 1', 'Pokreni algoritam 1?') == 'yes':
        print('Pokrecem algoritam 1')

def start_alg_2():
    if tkinter.messagebox.askquestion('Algoritam 2', 'Pokreni algoritam 2?') == 'yes':
        print('Pokrecem algoritam 2')

def start_alg_3():
    if tkinter.messagebox.askquestion('Algoritam 3', 'Pokreni algoritam 3?') == 'yes':
        print('Pokrecem algoritam 3')

def pocetak():
    print('Odredi pocetni cvor')
    global canvas_mode
    canvas_mode = 'pocetak'

def kraj():
    print('Odredi krajnji cvor')
    global canvas_mode
    canvas_mode='kraj'

def dodaj_cvor():
    global canvas_mode
    canvas_mode = 'dodaj_cvor'
    print('canvas_mode')

def dodaj_granu():
    global canvas_mode
    canvas_mode = 'dodaj_granu'

def izbrisi_cvor():
    global canvas_mode
    canvas_mode = 'izbrisi_cvor'

def izbrisi_granu():
    global canvas_mode
    canvas_mode = 'izbrisi_granu'

def dodaj_prepreku():
    global canvas_mode
    canvas_mode = 'dodaj_prepreku'


def reset():
    if tkinter.messagebox.askquestion('Reset', 'Da li hocete da restartuje graf?') == 'yes':
        print('Restartujem graf')
        global canvas, grane, cvorovi, canvas_mode
        canvas.delete(ALL)
        grane = {}
        cvorovi= {}
        canvas_mode = None


def grana_klik(event):
    if canvas_mode == 'izbrisi_granu':
        global grane
        canvas.delete(event)
        grane.pop(event)

def canvas_klik(event):
    print(event.x)
    print(event.y)
    print('------------------')
    x = event.x
    y = event.y

    global cvorovi, grane

    if canvas_mode == 'dodaj_cvor':
        global cvorovi
        for (id, koordinate) in cvorovi.items():
            if abs(x-koordinate[0]) < 50 and abs(y-koordinate[1]) < 50:
                print('Drugi cvor je previse blizu')
                return
        cvor = canvas.create_oval(x-15, y-15, x+15, y+15, outline='red', fill='gray')
        cvorovi[cvor] = (x, y)

    if canvas_mode == 'dodaj_granu':
        for (id, koordinate) in cvorovi.items():
            if abs(koordinate[0]-x) <= 15 and abs(koordinate[1]-y) <= 15:
                global grana_pocetak
                if grana_pocetak==0:
                    global x_grana, y_grana, prvi_cvor
                    x_grana = x
                    y_grana = y
                    prvi_cvor = id
                    grana_pocetak=1
                else:
                    if id == prvi_cvor:
                        print('Cvor ne moze imati povratnih grana')
                        return
                    grana_pocetak=0
                    grana = canvas.create_line(cvorovi[prvi_cvor][0], cvorovi[prvi_cvor][1], koordinate[0], koordinate[1], width=4, fill='blue')
                    grane[grana] = (prvi_cvor, id)
                    canvas.tag_lower(grana)
                    print(grana)
                    canvas.tag_bind(grana, '<Button-1>', lambda g: grana_klik(grana))
                    prvi_cvor = None

    if canvas_mode == 'izbrisi_cvor':

        for (id, koordinate) in cvorovi.items():
            if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                canvas.delete(id)
                cvorovi.pop(id)
                grane_za_brisanje = []
                for(gid, cvorovi_grane) in grane.items():
                    if id == cvorovi_grane[0] or id == cvorovi_grane[1]:
                        canvas.delete(gid)
                        grane_za_brisanje.append(gid)
                for gid in grane_za_brisanje:
                    grane.pop(gid)
                return

    if canvas_mode == 'pocetak':
        for (id, koordinate) in cvorovi.items():
            if abs(x-koordinate[0]) < 15 and abs(y-koordinate[1]) < 15:
                canvas.itemconfig(id, fill='green')

    if canvas_mode == 'kraj':
        for (id, koordinate) in cvorovi.items():
            if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                canvas.itemconfig(id, fill='red')

    if canvas_mode == 'dodaj_prepreku':
        for (id, koordinate) in cvorovi.items():
            if abs(koordinate[0]-x) < 15 and abs(koordinate[1]-y) < 15:
                canvas.itemconfig(id, fill='black')

def quit():
    exit(1)

def main():
    root = Tk()
    root.attributes("-fullscreen", True)

    button_alg_1 = Button(root, text='Algoritam 1', command=start_alg_1, width=30)
    button_alg_2 = Button(root, text='Algoritam 2', command=start_alg_2, width=30)
    button_alg_3 = Button(root, text='Algoritam 2', command=start_alg_3, width=30)
    button_pocetak = Button(root, text='Početak', command=pocetak, width=30)
    button_kraj = Button(root, text='Kraj', command=kraj, width=30)
    button_dodaj_cvor = Button(root, text='Dodaj čvor', command=dodaj_cvor, width=30)
    button_dodaj_granu = Button(root, text='Dodaj granu', command=dodaj_granu, width=30)
    button_izbrisi_cvor = Button(root, text='Izbriši čvor', command=izbrisi_cvor, width=30)
    button_izbrisi_granu = Button(root, text='Izbriši granu', command=izbrisi_granu, width=30)
    button_reset = Button(root, text='Reset', command=reset, width=30)
    button_exit = Button(root, text='Exit', command= quit, width=30)
    button_dodaj_prepreku = Button(root, text='Dodaj prepreku', command = dodaj_prepreku, width=30)
    global canvas
    canvas = Canvas(root, width = 800, height = 700, bg='white')

    # TODO: Namestiti da dugmici budu responsive prema menjanu velicine prozora

    button_alg_1.grid(column=0, row = 0)
    button_alg_2.grid(column=1, row = 0)
    button_alg_3.grid(column=2, row = 0)
    button_pocetak.grid(column=3, row=1)
    button_kraj.grid(column=4, row=1)
    button_dodaj_cvor.grid(column = 3, row = 2)
    button_dodaj_granu.grid(column=4, row = 2)
    button_izbrisi_cvor.grid(column=3, row=3)
    button_izbrisi_granu.grid(column=4, row=3)
    button_exit.grid(column=4, row=0)
    button_reset.grid(column = 4, row=4)
    button_dodaj_prepreku.grid(column = 3, row=4)
    canvas.grid(row=1, column=0, columnspan=3, rowspan=4)

    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_columnconfigure(3,weight=1)
    root.grid_columnconfigure(4,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.grid_rowconfigure(2,weight=1)
    root.grid_rowconfigure(3,weight=1)
    root.grid_rowconfigure(4,weight=1)

    canvas.bind('<Button-1>', canvas_klik)

    root.mainloop()

if __name__ == '__main__':
    main()
