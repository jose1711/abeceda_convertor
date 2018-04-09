#!/usr/bin/env python3
"""
abeceda.py
Prida do cisteho textu specialne symboly, ktore
pouziva font pisaneho pisma abeceda_v4.ttf na
vykreslenie dotahovych a nabehovych ciar, spojok
a pod.

Spracovanie vychadza z MS Word makier od p. Stanislava Filu
a jeho poznamok, ktore mi laskavo spristupnil.

Panovi Filovi by som tiez rad podakoval za velku pomoc
pri testovani tohto skriptu i jeho pripomienkovani. Samotny
font i navody na pouzitie tohto skriptu i makier pre MS Word
najdete na http://www.cpppap.svsbb.sk/files/im_font.html

Pouzitie:
 -a                 Zarovnať začiatky riadkov
 -d                 Doťahovať konce písmen
 -f vstupny_subor   Súbor s textom na konverziu
 -g                 Zapnúť GUI
 -o vystupny_subor  Súbor, kam pôjde výstup (nedefinovaný = obrazovka)
 -p                 Použiť české p
 -u                 Použiť všade úzke o
 -z                 Zmeniť z za sľučkové

Ak nie je zadany vstupny subor ani rezim GUI, je pouzity standardny
vstup.

Priklady spustenia:
 echo 'Adam v škole nesedel, abecedu nevedel' | abeceda.py
 abeceda.py -g


Zoznam a vyznam specialnych znakov:
ņ - medzera pred velkymi pismenami s bruskom (okrem P) na zaciatku riadku
ŉ - medzera pred malymi pismenami s bruskom a P na zaciatku riadku
& - dotahova ciarka za koncom slova
¤ - vseobecna spojka
Ŋ - spojka za P
ß - nabehova ciarka pred malymi pismenami
© - prehnuta nabehova ciarka pred malymi pismenami
÷ - nabehova ciarka pred x
đ - siroke s
Đ - siroke š
™ - gs, js, qs, ys na konci slov
® - gš, jš, qš, yš na konci slov
¨ - sn, sv, šn, šv + vseobecna spojka
Ç,‹,ç,î,›,ŏ,ō - skratene verzie b, o, v, w, ó, ô, ö
Î - ceske p
chr(8355), chr(8710), chr(8706), chr(8225) - sluckove varianty z

"""
import re
import sys
import os
import argparse
from tkinter import Tk, Text, Button, BooleanVar, Checkbutton, Label, Frame, \
                    LEFT, RIGHT, BOTTOM

parser = argparse.ArgumentParser(description='Upraví text pre písmo Abeceda_v4.ttf')
parser.add_argument('-a', action='store_true',
                    help='Zarovnať začiatky riadkov')
parser.add_argument('-d', action='store_true',
                    help='Doťahovať konce písmen')
parser.add_argument('-f', nargs=1, metavar='vstupny_subor',
                    help='Súbor s textom na konverziu')
parser.add_argument('-g', action='store_true',
                    help='Zapnúť GUI')
parser.add_argument('-o', nargs=1, metavar='vystupny_subor',
                    help='Súbor, kam pôjde výstup (nedefinovaný = obrazovka)')
parser.add_argument('-p', action='store_true',
                    help='České p')
parser.add_argument('-u', action='store_true',
                    help='Vždy použiť úzke o')
parser.add_argument('-z', action='store_true',
                    help='Zmeniť z za sľučkové')
args = parser.parse_args()
# vo Windows vzdy zobraz okno
if os.name == 'nt':
    args.g = True

velke = 'BDĎFIÍOÓÖŐÔSŚŠTŤVW'
male1 = 'mnňńvwyýzžźż'
male2 = 'beéěęfhiíjklĺľłprŕřsšśtťżuúůüű'
zavinacove_male = 'aáäcčdďgoóôöőq'
velke_bruskate = "AÁÄĄBCČĆEÉĚĘFGHIÍJKLĽĹŁOÓÔÖŐQRŘŔTŤUÚŮÜŰVWXYÝZŽŹŻ!#$%&()*+,-/:;<=>?@[\]_{|}~°––—€"
male_bruskate = "aáäącčćdďgłńoóôöőq‹›ŏōŌ"
P = 'P'
x = 'x'
s = 's'
ss = '[šś]'
sirokes = '©s'
sirokess = '©š'
sirokes2 = 's¤'
sirokess2 = 'š¤'
sirokes3 = 'đ¤'
sirokess3 = 'Đ¤'
sirokess4 = 'ś¤'
znaky = '- \n\xa0\r\x0b\t0123456789\.,:;?!+*/<=>\()\[\]{}\\\'`"“”„–_'
dotiahni = ''
dotiahni += 'aáäąbcčćdďeéěęfghiíjklľĺłmnňńoóöőôpqrřŕtťżuúůüűvwxyýzžź'
dotiahni += 'AÁÄĄCČĆEÉĚĘGHJKLĽĹŁMNŇŃQRŘŔUÚŮÜŰXYÝZŽŹĆ'
cisla = '0123456780'
gsjs = 'GgJjQqYyÝý'
snsv = 'nv'
# uzsie verzie pismen pri spojeniach bm, bn, om..
nahrady = {'b': 'Ç',
           'o': '‹',
           'v': 'ç',
           'w': 'î',
           'ó': '›',
           'ô': 'ŏ',
           'ö': 'ō',
           'ő': 'Ō',
           }

nahrady_o = {'o': '‹',
             'ó': '›',
             'ô': 'ŏ',
             chr(148): 'ō',
             chr(139): 'Ō',
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

# š/ś + obecna spojka
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
rsirokess_znak = re.compile('({0}|{1}|{2})(?=[{3}])'.format(sirokess2,
                                                            sirokess3,
                                                            sirokess4,
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

# nabehova ciarka medzi podciarkovnikom a malym zavinacovym pismenom
rzavinacove_male_podciarkovnik = re.compile('_(?=[{0}])'.format(zavinacove_male))

rdotiahni = re.compile('([{0}])(?=[{1}])'.format(dotiahni,
                                                 znaky))

# minimedzera pred velke bruskate pismena na zaciatku riadku
rvelke_bruskate = re.compile('( |^)([{0}])'.format(velke_bruskate), re.M)

# minimedzera pred male bruskate pismena a velke P na zaciatku riadku
rmale_bruskate = re.compile('( |^)([{0}])'.format(male_bruskate + 'P'), re.M)


def convert(retazec, dotahovat=False, zarovnat=False, ceske_p=False,
            sluckove_z=False, uzke_o=False):
    retazec = re.sub(rvelke, lambda n: n.group(0) + '¤', retazec)
    retazec = re.sub(rP, lambda n: n.group(0) + 'Ŋ', retazec)
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
    # retazec = re.sub(rzavinacove_male_podciarkovnik, '_ß', retazec)
    retazec = re.sub('@s', '@đ', retazec)
    if dotahovat:
        retazec = re.sub(rdotiahni, lambda n: n.group(0) + '&', retazec)
    if zarovnat:
        retazec = re.sub(rvelke_bruskate, lambda n: n.group(1) + 'ņ' + n.group(2), retazec)
        retazec = re.sub(rmale_bruskate, lambda n: n.group(1) + 'ŉ' + n.group(2), retazec)
    if sluckove_z:
        retazec = retazec.replace('z', chr(8355))
        retazec = retazec.replace('ž', chr(8710))
        retazec = retazec.replace('ż', chr(8706))
        retazec = retazec.replace('ź', chr(8225))
    if ceske_p:
        retazec = retazec.replace('p', 'Î')
    if uzke_o:
        retazec = re.sub('([{}])'.format(''.join(nahrady_o)), lambda n: nahrady[n.group(1)], retazec)

    return retazec


if args.g:
    def convert_and_display():
        input = textin.get(0.0, 9999.0)
        output = convert(input, dotahovat.get(), zarovnat.get(),
                         ceskep.get(), sluckovez.get(), uzkeo.get())
        textout.delete(0.0, 9999.0)
        textout.insert(0.0, output)
        return output

    def dotahovat_btn_cback():
        convert_and_display()

    def ceskep_btn_cback():
        convert_and_display()

    def sluckovez_btn_cback():
        convert_and_display()

    def uzkeo_btn_cback():
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

    def clear_all():
        textin.delete(0.0, 9999.0)
        convert_and_display()

    tk = Tk()
    tk.title("Abeceda_v4 konvertor")
    labelin = Label(tk, text='Vstupný text')
    labelin.pack()
    textin = Text(tk, width=80, height=15)
    textin.pack()

    dotahovat = BooleanVar()
    zarovnat = BooleanVar()
    ceskep = BooleanVar()
    sluckovez = BooleanVar()
    uzkeo = BooleanVar()
    abeceda_font = BooleanVar()

    options_frame = Frame(tk)
    options_frame.pack()
    options2_frame = Frame(tk)
    options2_frame.pack()
    left_buttons_frame = Frame(tk)
    left_buttons_frame.pack()
    right_buttons_frame = Frame(left_buttons_frame)
    right_buttons_frame.pack(side=BOTTOM)
    button1 = Button(left_buttons_frame, text='Previesť', command=convert_and_display)
    button2 = Button(left_buttons_frame, text='Kopírovať do schránky',
                     command=copy_to_clipboard)
    button3 = Button(right_buttons_frame, text='Vyčistiť',
                     command=clear_all)
    button1.pack(side=LEFT)
    button2.pack(side=LEFT)
    button3.pack(side=RIGHT)
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

    ceskep_btn = Checkbutton(options2_frame, text='České "p"',
                             variable=ceskep, command=ceskep_btn_cback)
    ceskep_btn.deselect()
    ceskep_btn.pack(side=LEFT)

    zluckovez_btn = Checkbutton(options2_frame, text='Sľučkové "z"',
                                variable=sluckovez, command=sluckovez_btn_cback)
    zluckovez_btn.select()
    zluckovez_btn.pack(side=LEFT)

    uzkeo_btn = Checkbutton(options2_frame, text='Úzke "o" všade',
                            variable=uzkeo, command=uzkeo_btn_cback)
    uzkeo_btn.select()
    uzkeo_btn.pack(side=LEFT)

    hline = Frame(tk, height=1, width=520, bg="black")
    hline.pack()
    labelout = Label(tk, text='Výstupný text')
    labelout.pack()
    textout = Text(tk, width=80, height=15, font=('Arial', 10))
    textout.pack()
    labelver = Label(tk, text='v0.9.4')
    labelver.pack(side=RIGHT)
    tk.mainloop()
else:
    if not args.f:
        if sys.stdin.isatty():
            print("Zadajte text na konverziu a ukončite vstup stlačením Ctrl-D")
        retazec = '\n'.join(sys.stdin.readlines())
    else:
        retazec = open(args.f[0]).read()

    retazec = convert(retazec, dotahovat=args.d, zarovnat=args.a,
                      ceske_p=args.p, uzke_o=args.u, sluckove_z=args.z)

    if not args.o:
        print(retazec)
    else:
        print(retazec, file=open(args.o[0], 'w'))
