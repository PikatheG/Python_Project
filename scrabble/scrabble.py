#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_XXXX_YYYY_projet.py : CR projet « srabble », groupe ZZZ

XXXX <esteban.vilaverde@etu-univ-grenoble-alpes.fr>
YYYY <liam.thompson--grenier@univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import random as ran


# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel


# PARTIE 1 : LE PLATEAU ########################################################

def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1) : lst.append(copie_lst[-i])


def init_bonus() :
    """
    Q1) Initialise le plateau des bonus.
    """
    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus : symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus

def init_jetons():
    plateau = [  # quart-supérieur gauche + ligne et colonne centrales
        ['', ''  , ''  , '', ''  , ''  , ''  , ''],
        [''  , '', ''  , ''  , ''  , '', ''  , ''],
        [''  , ''  , '', ''  , ''  , ''  , '', ''],
        ['', ''  , ''  , '', ''  , ''  , ''  , ''],
        [''  , ''  , ''  , ''  , '', '' , '' , ''],
        [''  , '', ''  , ''  , ''  , '', ''  , ''],
        [''  , ''  , '', ''  , ''  , ''  , '', ''],
        ['', ''  , ''  , '', ''  , ''  , ''  , '']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plateau : symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plateau)

    return plateau

def affiche_jetons(listPos):
    taille = 15

    #donner l'espacement de nos num de colonnes
    print('    ', end='')

    #1ers numero
    for i in range(1, taille+1):
        if i < 10:
            print('0' + str(i), end = '  ')
        else:
            print(str(i), end='  ')

    print()

    for j in range(1,taille+1):

        print('   ', end = '')
        for jj in range(taille):
            print('|---', end='')
        print('|')

        if j < 10:
            print('0' + str(j) + ' ', end = '')
            for k in range(taille):
                print('|', end='')
                if listPos[j-1][k] == '':
                    print('   ', end='')
                else:
                    print(' '+listPos[j-1][k]+' ', end = '')
            print('|')
        else:
            print(str(j) + ' ', end = '')
            for k in range(taille):
                print('|', end='')
                if listPos[j-1][k] == '':
                    print('   ', end = '')
                else:
                    print(' '+listPos[j-1][k]+' ', end = '')
            print('|')

    print('   ', end = '')
    for l in range(taille):
        print('|---', end='')
    print('|')


#def affiche_jetons(j):



# PARTIE 2 : La pioche ##########################

def init_pioche_alea()->list:
    i = 1
    sac = []
    sac.append('?')
    sac.append('?')
    for j in range(26):
        sac.append(chr(ord('A')+j))
    while i <= 74:
        letter = ran.randint(ord('A'), ord('Z'))
        sac.append(chr(letter))
        i +=1
    return sac

def piocher(x,sac):
  i=1
  main=[]
  while i<=x and i<=7 and len(sac)>=1:
    a=ran.choice(sac)
    main.append(a)
    sac.remove(a)
    i=i+1
  return main

def completer_main(main,sac):
  while len(main)<7 and len(sac)>=1:
    a=ran.choice(sac)
    main.append(a)
    sac.remove(a)
  return main

def completer_main(main,sac):
  while len(main)<7:
    a=ran.choice(sac)
    main.append(a)
    sac.remove(a)
  return main

def echanger(jetons,main,sac):
    user=""
    i=0
    jetdef=[]
    booli=False
    while user!="stop" and i<7 and len(sac)>=1:
        user=input("Quel jeton voulez vous échanger ? Saisissez stop pour arreter.")
        if user in main:
            jetdef.append(user)
            main.remove(user)
            i=i+1
            booli=True
        else:
            print("Pas dans votre main. ERREUR")
    completer_main(main, sac)
    sac.extend(jetdef)
    if booli:
        return "échange reussi"
    else:
        return "échange échoué"






# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################

def generer_dictfr(nf='littre.txt') :
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots :
        for line in fich_mots : mots.append(line.strip().upper())
    return mots

mots_fr = generer_dictfr(nf='littre.txt')

def select_mot_initiale(motsfr : str, let : str) -> list:
    motslet = []
    for i in motsfr:
        if i[0] == let:
            motslet.append(i)
    return motslet

def select_mot_longueur(motsfr : str, lgr : int) ->list:
    motslen = []
    for i in motsfr:
        if len(i) == lgr:
            motslen.append(i)

    return motslen

def mot_jouable(mot:str, ll: list)->bool:
    ll2 = list(ll)
    jokerCount = ll2.count(JOKER)

    for i in mot:
        if i not in ll2 and jokerCount == 0:
            return False
        elif i not in ll2 and jokerCount == 1 or jokerCount == 2:
            jokerCount -= 1
        else:
            ll2.remove(i)

def mots_jouables(motsfr : str, ll: list) -> list:
    motsPossibles = []
    for i in motsfr:
        if mot_jouable(i, ll) == True:
            motsPossibles.append(i)

    return motsPossibles


# PARTIE 4 : VALEUR D'UN MOT ###################################################


def generer_dico() :
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'
    """
    jetons = {}
    with Path('lettres.txt').open(encoding='utf_8') as lettres :
        for ligne in lettres :
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}
    return jetons

def init_pioche(dico):
    pioche=[]
    for lettre in dico:
        for i in range (dico[lettre]["occ"]):
            pioche.append(lettre)
    return pioche

def valeur_mot(mot,dico):
    S=0
    for lettre in mot:
        valeur=dico[lettre]["val"]
        S=S+valeur
    if len(mot)==7:
      S=S+50
    return S

def meilleur_mot(motsfr,ll,dico):
    maxx=0
    for i in motsfr:
        if mot_jouable(i,ll):
            a=valeur_mot(i,dico)
            if a>maxx:
                a=maxx
                res=i
    return res


def meilleurs_mot(motsfr,ll,dico):
    mlrmot=[]
    maxx=valeur_mot(meilleur_mot(motsfr, ll, dico),dico)
    for i in mot_jouable:
        if valeur_mot(i,dico)==maxx:
            mlrmot.append(i)
    return mlrmot


#PARTIE5 ##################################################################


def tour_joueur(j,jetons,main,sac,dico,n,ll):
    user=""
    print(affiche_jetons(plateau))
    while user!="passer" and user!="échanger" and user!="proposer":
        user=input("Que voulez faire ? \n~passer\n~échanger\n~proposer\n")
        if user!="passer" and user!="échanger" and user!="proposer":
            print("Saisissez à nouveau :\n")
    if user=="échanger":
        echanger(jetons, main, sac)
    elif user=="proposer":
        n=input("Proposez un mot :")
        a=mot_jouable(n, ll)
        if a==False:
            print("Mot pas jouable")
        else:
            b=valeur_mot(n, dico)
            print("La valeur de",n,"est",b)


def fin_partie(main,sac):
    a=7-len(main)
    if a!=0 and a>len(sac):
        print("Fin de la partie")
        return True
    else:
        return False

#fonction qui doit faire le score

def malus(mains,sac,joueurs,score,dico,main):
    if fin_partie(main,sac):
        for i in range(len(joueurs)):
            main_joueur=mains[i]
            joueur=joueurs[i]
            score[joueur]-=valeur_mot(main_joueur, dico)

def affiche_score(joueurs,name):
    gagnant=""
    maxx=joueurs[name]
    for i in joueurs:
        print(joueurs[i])
        if joueurs[i]>maxx:
            maxx=joueurs[i]
            gagnant=i
    print("Le gagnant est",gagnant,"avec",joueurs[gagnant],"points !!!")

#def prochain_joueur(joueurs:list,main,sac):
 #   if fin_partie(main, sac)==False:



#PARTIE 6######################################################################

def caseVide(plateau :list, i:int, j:int)-> bool:
    if plateau[i-1][j-1] == '':
        return True
    else:
        return False

def lire_coords():
    askCoordI= int(input('Entrez une coordonée de ligne : '))
    askCoordJ= int(input('Entrez une coordonée de colonne : '))


    while caseVide(plateau, askCoordI, askCoordJ) == False:
        print('Case non vide.')
        askCoordI= int(input('Entrez une coordonée de ligne : '))
        askCoordJ= int(input('Entrez une coordonée de colonne : '))

    return askCoordI, askCoordJ

def tester_placement(plateau, i, j, dir, mot):
    



#programme principal


playeur=int(input("Combien de joueurs ? "))
joueurs={}
for i in range(playeur):
    name=input("Entrez votre nom: ")
    joueurs[name]= 0
    
print(joueurs)

sac = init_pioche_alea()
plateau = init_jetons()

'''

score={} :
for i in joueurs:
    score[joueurs]=0

mains=[]
for i in joueurs:
    a=piocher(7, sac)
    mains.append(a)

'''