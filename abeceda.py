#!/usr/bin/env python3
"""
abeceda.py
Prida do cisteho textu specialne symboly, ktore
pouziva font pisaneho pisma abeceda_v4.ttf na
vykreslenie dotahovych a nabehovych ciar, spojok
a pod.

Pouzitie:
 -a                 Zarovnať začiatky riadkov
 -f vstupny_subor   Súbor s textom na konverziu
 -o vystupny_subor  Súbor, kam pôjde výstup (nedefinovaný = obrazovka)
 -d                 Doťahovať konce písmen
 -g                 Zapnúť GUI

Ak nie je zadany vstupny subor ani rezim GUI, je pouzity standardny
vstup.

Priklady spustenia:
 echo 'Adam v škole nesedel, abecedu nevedel' | abeceda.py
 abeceda.py -g

Spracovanie vychadza z MS Word makier od p. Stanislava Filu
a jeho poznamok, ktore mi laskavo spristupnil.

Zoznam a vyznam specialnych znakov:
⌐ - medzera pred velkymi pismenami s bruskom na zaciatku riadku
⌂ - medzera pred malymi pismenami s bruskom na zaciatku riadku
& - dotahova ciarka za koncom slova
¤ - vseobecna spojka
× - spojka za P
ß - nabehova ciarka pred malymi pismenami
© - prehnuta nabehova ciarka pred malymi pismenami
÷ - nabehova ciarka pred x
đ - siroke s
Đ - siroke š
™ - gs, js, qs, ys na konci slov
® - gš, jš, qš, yš na konci slov
¨ - sn, sv, šn, šv + vseobecna spojka
Ç,‹,ç,î,›,ŏ,ō - skratene verzie b, o, v, w, ó, ô, ö

"""
import re
import sys
import os
import argparse
from tkinter import Tk, Text, Button, BooleanVar, Checkbutton, Label, Frame, LEFT, RIGHT

parser = argparse.ArgumentParser(description='Upraví text pre písmo Abeceda_v4.ttf')
parser.add_argument('-a', action='store_true',
                    help='Zarovnať začiatky riadkov')
parser.add_argument('-f', nargs=1, metavar='vstupny_subor',
                    help='Súbor s textom na konverziu')
parser.add_argument('-o', nargs=1, metavar='vystupny_subor',
                    help='Súbor, kam pôjde výstup (nedefinovaný = obrazovka)')
parser.add_argument('-d', action='store_true',
                    help='Doťahovať konce písmen')
parser.add_argument('-g', action='store_true',
                    help='Zapnúť GUI')
args = parser.parse_args()
# vo Windowse vzdy zobraz okno
if os.name == 'nt':
    args.g = True

velke = 'BDĎFIÍOÓÖŐÔSŠTŤVW'
male1 = 'mnňńvwyýzžźż'
male2 = 'beéěęfhiíjklĺľłprŕřsšśtťżuúůüű'
zavinacove_male = 'aáäcčdďgoóôöőq'
velke_bruskate = "AÁÄĄBCČĆEÉĚĘFGHIÍJKLĽĹŁOÓÔÖŐPQRŘŔTŤUÚŮÜŰVWXYÝZŽŹŻ!#$%&()*+,-/:;<=>?@[\]_{|}~°––—€"
male_bruskate = "aáäącčćdďgłńoóôöőq‹›ŏōŌ"
P = 'P'
x = 'x'
s = 's'
ss = 'š'
sirokes = '©s'
sirokess = '©š'
sirokes2 = 's¤'
sirokess2 = 'š¤'
sirokes3 = 'đ¤'
sirokess3 = 'Đ¤'
znaky = '- \n\xa0\r\x0b\t0123456789\.,:;?!+*/<=>\()\[\]{}\\\'`"“”„–'
dotiahni = ''
dotiahni += 'aáäąbcčćdďeéěęfghiíjklľĺłmnňńoóöőôpqrřŕtťżuúůüűvwxyýzžź'
dotiahni += 'AÁÄĄCČĆEÉĚĘGHJKLĽĹŁMNŇŃQRŘŔUÚŮÜŰXYÝZŽŹĆ'
cisla = '0123456780'
gsjs = 'GgJjQqYyÝý'
snsv = 'nv'
nahrady = {'b': 'Ç',
           'o': '‹',
           'v': 'ç',
           'w': 'î',
           'ó': '›',
           'ô': 'ŏ',
           'ö': 'ō',
           'ő': 'Ō',
           }

# velke osamotene pismena
rvelke = re.compile('[{0}](?![{1}]|$)'.format(velke, znaky))
rP = re.compile('[{0}](?![{1}]|$)'.format(P, znaky))

# nabehova ciarka pred znak + male1 pismena
rmale1 = re.compile('([{0}]|^)(?=[{1}])'.format(znaky,
                                                male1))

# prehnuta nabehova ciarka pred znak + male2 pismena
rmale2 = re.compile('([{0}]|^)(?=[{1}])'.format(znaky,
                                                male2))

# prehnuta nabehova ciarka pred znak + male x
rx = re.compile('[{0}](?=[{1}])'.format(znaky, x))

# s + obecna spojka
rs = re.compile(s)

# š + obecna spojka
rss = re.compile(ss)

# siroke s na zaciatku slova
rsirokes = re.compile(sirokes)

# siroke š na zaciatku slova
rsirokess = re.compile(sirokess)

# siroke s + obecna spojka a za nim znak
rsirokes_znak = re.compile('({0}|{1})(?=[{2}])'.format(sirokes2,
                                                       sirokes3,
                                                       znaky))

# siroke š + obecna spojka a za nim znak
rsirokess_znak = re.compile('({0}|{1})(?=[{2}])'.format(sirokess2,
                                                        sirokess3,
                                                        znaky))

# kombinacie gs, js, qs, ys na konci slov
rgsjs = re.compile('[{0}]s(?=[{1}])'.format(gsjs, znaky))

# kombinacie gš, jš, qš, yš na konci slov
rgssjss = re.compile('[{0}]š(?=[{1}])'.format(gsjs, znaky))

# kombinacie sn, sv + obecna spojka
rsnsv = re.compile('({0}|{1})([nv])'.format(sirokes2, sirokes3))

# kombinacie sn, sv + obecna spojka
rssnssv = re.compile('({0}|{1})([nv])'.format(sirokess2, sirokess3))

# obecna spojka medzi zavinac a pismena, ktore ju bezne nepotrebuju
rzavinacove_male = re.compile('@(?=[{0}])'.format(zavinacove_male))

rdotiahni = re.compile('([{0}])(?=[{1}])'.format(dotiahni,
                                                 znaky))

# minimedzera pred velke bruskate pismena na zaciatku riadku
rvelke_bruskate = re.compile('( |^)([{0}])'.format(velke_bruskate), re.M)

# minimedzera pred male bruskate pismena na zaciatku riadku
rmale_bruskate = re.compile('( |^)([{0}])'.format(male_bruskate), re.M)


def convert(retazec, dotahovat=False, zarovnat=False):
    retazec = re.sub(rvelke, lambda n: n.group(0) + '¤', retazec)
    retazec = re.sub(rP, lambda n: n.group(0) + '×', retazec)
    retazec = re.sub(rmale1, lambda n: n.group(1) + 'ß', retazec)
    retazec = re.sub(rmale2, lambda n: n.group(1) + '©', retazec)
    retazec = re.sub(rs, lambda n: n.group(0) + '¤', retazec)
    retazec = re.sub(rss, lambda n: n.group(0) + '¤', retazec)
    retazec = re.sub(rsirokes, 'đ', retazec)
    retazec = re.sub(rsirokess, 'Đ', retazec)
    retazec = re.sub(rx, lambda n: n.group(0) + '÷', retazec)
    retazec = re.sub(rsirokes_znak, lambda n: n.group(0)[:-1], retazec)
    retazec = re.sub(rsirokess_znak, lambda n: n.group(0)[:-1], retazec)
    retazec = re.sub(rgsjs, lambda n: n.group(0)[:-1] + '™', retazec)
    retazec = re.sub(rgssjss, lambda n: n.group(0)[:-1] + '®', retazec)
    retazec = re.sub(rsnsv, lambda n: n.group(1)[:-1] + '¨' + n.group(2), retazec)
    retazec = re.sub(rssnssv, lambda n: n.group(1)[:-1] + '¨' + n.group(2), retazec)
    retazec = re.sub('([boóôövw])(?=[mnňvwyýzž])', lambda n: nahrady[n.group(1)], retazec)
    retazec = re.sub(rzavinacove_male, '@¤', retazec)
    retazec = re.sub('@s', '@đ', retazec)
    if dotahovat:
        retazec = re.sub(rdotiahni, lambda n: n.group(0) + '&', retazec)
    if zarovnat:
        retazec = re.sub(rvelke_bruskate, lambda n: n.group(1) + '⌐' + n.group(2), retazec)
        retazec = re.sub(rmale_bruskate, lambda n: n.group(1) + '⌂' + n.group(2), retazec)
    return retazec


if args.g:
    def convert_and_display():
        input = textin.get(0.0, 9999.0)
        output = convert(input, dotahovat.get(), zarovnat.get())
        textout.delete(0.0, 9999.0)
        textout.insert(0.0, output)
        return output

    def dotahovat_btn_cback():
        convert_and_display()

    def font_btn_cback():
        convert_and_display()
        if abeceda_font.get():
            textout.config(font=('Abeceda_v4', 18), height=10)
        else:
            textout.config(font=('Arial', 10), height=15)

    def align_btn_cback():
        convert_and_display()

    def copy_to_clipboard():
        tk.clipboard_clear()
        tk.clipboard_append(convert_and_display())

    tk = Tk()
    tk.title("Abeceda_v4 konvertor")
    labelin = Label(tk, text='Vstupný text')
    labelin.pack()
    textin = Text(tk, width=80, height=15)
    textin.pack()
    dotahovat = BooleanVar()
    zarovnat = BooleanVar()
    abeceda_font = BooleanVar()
    options_frame = Frame(tk)
    options_frame.pack()
    buttons_frame = Frame(tk)
    buttons_frame.pack()
    button1 = Button(buttons_frame, text='Previesť', command=convert_and_display)
    button2 = Button(buttons_frame, text='Kopírovať do schránky',
                     command=copy_to_clipboard)
    button1.pack(side=LEFT)
    button2.pack(side=RIGHT)
    dotahovat_btn = Checkbutton(options_frame, text='Doťahovať písmená',
                                variable=dotahovat, command=dotahovat_btn_cback)
    dotahovat_btn.select()
    dotahovat_btn.pack(side=LEFT)
    font_btn = Checkbutton(options_frame, text='Písmo Abeceda_v4',
                           variable=abeceda_font, command=font_btn_cback)
    font_btn.deselect()
    font_btn.pack(side=LEFT)
    align_btn = Checkbutton(options_frame, text='Zarovnať riadky', variable=zarovnat,
                            command=align_btn_cback)
    align_btn.deselect()
    align_btn.pack(side=LEFT)

    hline = Frame(tk, height=1, width=520, bg="black")
    hline.pack()
    labelout = Label(tk, text='Výstupný text')
    labelout.pack()
    textout = Text(tk, width=80, height=15, font=('Arial', 10))
    textout.pack()
    labelver = Label(tk, text='v0.9.0')
    labelver.pack(side=RIGHT)
    tk.mainloop()
else:
    if not args.f:
        if sys.stdin.isatty():
            print("Zadajte text na konverziu a ukončite vstup stlačením Ctrl-D")
        retazec = '\n'.join(sys.stdin.readlines())
    else:
        retazec = open(args.f[0]).read()

    retazec = convert(retazec, dotahovat=args.d, zarovnat=args.a)

    if not args.o:
        print(retazec)
    else:
        print(retazec, file=open(args.o[0], 'w'))
