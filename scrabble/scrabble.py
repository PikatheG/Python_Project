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

tour = 1

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

#fonction pour simplifier le code de affiche_jetons(j, b)
def case(sq : str)->str:
    if sq == 'MT':
        return '^'   
    elif sq == 'MD':
        return '⋅'
    elif sq == 'LT':
        return '*'
    elif sq == 'LD':
        return '+'
    elif sq == '':
        return ' '
    else:
        return sq

def affiche_jetons(listPos: list, bonus:list) -> str:
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

    #affichage des num de lignes et de leur objet
    for j in range(1,taille+1):

        print('   ', end = '')
        for jj in range(taille):
            print('|---', end='')
        print('|')

        if j < 10:
            lineNum = '0' + str(j)
        else:
            lineNum = str(j)
       
        print(lineNum + ' ', end = '')
        
        for k in range(taille):
            print('|', end='')    
            print(case(listPos[j-1][k]) + case(bonus[j-1][k]) + ' ', end = '')
        print('|')
        
    print('   ', end = '')
    for l in range(taille):
        print('|---', end='')
    print('|')

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


def echanger(jetons,main,sac):
    flag=False
    if len(sac)<len(jetons):
        print("Pas assez de lettre")
    elif len(jetons)>=1:
        flag=True
    completer_main(main,sac)
    sac.extend(jetons)
    return flag


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

def mot_jouable(mot:str, main: list, manque: int)->bool:
    main2 = list(main)
    jokerCount = main2.count(JOKER)

    cpt = 0
    
    while cpt < len(mot):
         
        if mot[cpt] not in main2 and jokerCount == 0 and manque == 0:
            return False
        
        elif mot[cpt] not in main2 and (jokerCount == 1 or jokerCount == 2):
            jokerCount -= 1
            main2.remove(JOKER)
            
        elif manque > 0 and mot[cpt] not in main2:
            manque -= 1
            
        else:
            main2.remove(mot[cpt])
            
    return True


def mots_jouables(motsfr : str, main: list, manque: int) -> list:
    motsPossibles = []
    for i in motsfr:
        if mot_jouable(i, main, manque) == True:
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

def tour_joueur(indexJ,main,sac,dico,joueurs,score): 

    user=""
    usere=""
    jetons=[]
    flag=False
    joueuractu=joueurs[indexJ]
    print(main)
    while user!="P" and user!="E" and user!="S":
        user=input("Que voulez faire ? \n~passer (P) \n~échanger (E)\n~proposer (S)\n ")
        user = user.upper()
        if user!="P" and user!="E" and user!="S":
            print("Erreur. Saisissez à nouveau.")

        elif user.upper() == "E":
            p=0
            jetons=[]
            usere=input("Saisissez une lettre. Entrer stop pour arreter la saisie : ")
            usere=usere.upper()
            while usere != "STOP" and len(main)>=1 and 7-len(main)<len(sac) and p<7:
                if usere in main:
                    jetons.append(usere)
                    main.remove(usere)
                    p=p+1
                elif usere not in main :
                    print("Erreur. Pas dans votre main. Rentrez une nouvelle lettre.")
                usere=input("Nouvelle lettre : ")
                usere=usere.upper()
            print('Vous avez echangé.')
            echanger(jetons,main,sac)
            flag=True

        elif user.upper() == "S":
            direction=""
            while direction!="H" and direction!="V":
                direction=input("Saisissez H pour placer horizontalment votre mot.\nSaisissez V pour le mettre à la verticale. ")
                direction = direction.upper()
                mot=input("Entrez votre mot : ")
                mot = mot.upper()
          
            i, j = lire_coords()
          
            a = tester_placement(plateau,i,j,direction,mot)
            
            while len(mot)>len(main) or len(mot)>len(sac):
                print("Votre mot dépasse la longueur du sac ou celle de votre main.")
                mot=input("Entrez votre mot : ")
                mot = mot.upper()
            while mot not in mots_jouables(mots_fr,main,a[1]):
                print("Votre mot n'est pas jouable.")
                mot = input("Entrez votre mot : ")
                mot = mot.upper()
            
            placer_mot(plateau, main, mot, i, j, direction)
            
            completer_main(main, sac)
            
            v=valeur_mot(mot,dico)
            
            print("Votre mot rapporte",v,"point.")
            score[joueuractu]+=v
            print("Votre score est de",score[joueuractu])
            flag=True


        elif user.upper() == "P":
            flag=True
            print("Tour passé.")
    return flag


def prochain_joueur(indexJ,joueurs):

    if indexJ==len(joueurs)-1:
        indexJ = 0
    else:
        indexJ += 1
        
    return indexJ



def fin_partie(main,sac):
    a=7-len(main)
    if a!=0 and a>len(sac):
        print("Fin de la partie")
        return True
    else:
        return False

def malus(score,main):
    m=0
    for j in main:
        if len(main)==7:
            m=m-50
        m=valeur_mot(main, dico)
        score[joueuractu]-=m
    return score[joueuractu]

def affiche_score(score):
    gagnant=""
    maxx=-62
    for joueur in score:
        print(joueur,score[joueur])
        if score[joueur]>maxx:
            maxx=score[joueur]
            gagnant=joueur
    print("Le gagnant est",gagnant,"avec",maxx,"points !!!")



#PARTIE 6######################################################################

def casePossible(plateau :list, i:int, j:int)-> bool:
    if plateau[i-1][j-1] == '':
        return True
    elif plateau[i-1][j-1] != '' or i < 1 or i > 15 or j < 1 or j > 15:
        return False

def lire_coords() -> tuple :
    
    askCoordI= int(input('Entrez une coordonée de ligne : '))
    askCoordJ= int(input('Entrez une coordonée de colonne : '))


    while casePossible(plateau, askCoordI, askCoordJ) == False:
        print('Case non vide ou pas dans le plateau')
        askCoordI= int(input('Entrez une coordonée de ligne : '))
        askCoordJ= int(input('Entrez une coordonée de colonne : '))

    return askCoordI, askCoordJ


def tester_placement(plateau: list, i: int, j: int, dir: str, mot:str) -> tuple:   
    
    global tour
    
    connected = False
    
    #manque sert a faire en sorte qu'on puisse poser le mot avec les lettres du plateau
    
    lettreNec = []
    manque = 0
    decalY = 0
    decalX = 0
    
    
    #on regarde si le mot est connecte avec un autre pour le placer
    if dir == 'H':
        for k in range(len(mot)):
            if plateau[i-1][j-1+k] != '':
                connected = True
    elif dir == 'V':
        for k in range(len(mot)):
            if plateau[i-1+k][j-1] != '':
                connected = True
    
    #si le mot depasse, ou si il n'est pas place au centre lors du premier tour, ou si il n'est pas connecte
    if i + len(mot) - 1 > 15 or j + len(mot) - 1 > 15 or (tour == 1 and i, j != 8,8) or connected == False:
        return [], 0

    tour += 1

    for letter in mot:
    
        #si la lettre du mot ne correspond pas a la lettre sur le plateau 
        if (letter != plateau[i - 1 + decalY][j - 1 + decalX] and plateau[i - 1 + decalY][j - 1 + decalX] != ''):
            return [], 0
        
        #on ajoute a la liste des lettre necessaires si la case est vide
        elif plateau[i - 1 + decalY][j - 1 + decalX] == '':
            lettreNec.append(letter)
            manque += 1
                       
        if dir == 'H':
            decalX +=1
        elif dir == 'V':
            decalY += 1
    
    
    return lettreNec, manque

def placer_mot(plateau: list, main: list, mot: str, i:int, j:int, dir: str) -> bool:
    
    cpt = 0
    
    success = True
    
    lettreNec = tester_placement(plateau, i, j, dir, mot)
    
    if lettreNec[0] == []:
        return False
    
    motsPossibles = mots_jouables(mots_fr, main, lettreNec[1])
    
    if lettreNec[0] in main and mot in motsPossibles and len(mot) > 2:
        
        while cpt < len(mot):
            for k in mot:
                if dir == 'H':
                    if k in main:
                        plateau[i-1][k-1+cpt] == k
                        main.remove(k)
                    elif k not in main and plateau[i-1][k-1+cpt] == '' and JOKER in main:
                        plateau[i-1][k-1+cpt] = JOKER
                        main.remove(JOKER)
                cpt += 1
                           
    return success
    

#programme principal
dico = generer_dico()

nbJoueur = int(input("Combien de joueurs ? "))
joueurs = []
for i in range(nbJoueur):
    name = input("Entrez votre nom : ")
    joueurs.append(name)

sac = init_pioche_alea()

plateau = init_jetons()
b = init_bonus()

score={}
for i in joueurs:
    score[i]=0

mains=[]
for i in joueurs:
    a=piocher(7, sac)
    mains.append(a)


indexJ=0
joueuractu = joueurs[indexJ]
main=mains[indexJ]
while not (fin_partie(main,sac)):
    joueuractu = joueurs[indexJ]
    main=mains[indexJ]
    affiche_jetons(plateau, b)
    print("C'est au tour de",joueuractu)
    f=tour_joueur(indexJ,main,sac,dico,joueurs,score)
    mains[indexJ]=main

    if f:
        indexJ=prochain_joueur(indexJ,joueurs)
        
for r in range(len(joueurs)):
    malus(score,main[r])
    affiche_score(score)
    
    
