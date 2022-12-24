from tkinter import *
from init import *
from tkinter.messagebox import *

collision = False

#Deplacement du personnage:
def gravity():
    global pj, monstres, world, plateformes, piege, sol, collision, p, ground, fond, img_x, img_y
    pj.gravite()
    world.stay_in(pj)

    # Gestion des collisions avec les plateformes
    # remise à zéro des collisions
    pj.reset_collision()
    # ajout de l'ensemble des objets en collision
    if sol.collision(pj):
        pj.add_collision(sol)
    for plateforme in plateformes:
        if plateforme.collision(pj):
            pj.add_collision(plateforme)
    # traitement des collisions
    pj.move_collision()

    # Gestion des collisions des monstres avec le reste du jeu
    i = 0
    while i < len(monstres):
        #print(str(i)+" "+str(len(monstres)))
        monstre = monstres[i]
        monstre.reset_collision()
        if sol.collision(monstre):
            monstre.add_collision(sol)
        for plateforme in plateformes:
            if plateforme.collision(monstre):
                monstre.add_collision(plateforme)

        monstre.move_collision()

        if pj.feu and monstre.collision(pj.attaque):
                monstre.meurt()
                del monstres[i]
                pj.stopfire()
        else:
            if pj.collision(monstre): # Plutôt une fonction de gestion des PV et mort
                #print("PJ avec Monstre")
                pj.x = 85
                pj.y = 10

            # Si deux monstres sont trop proches
            for othermonstre in monstres:
                if othermonstre != monstre:
                    if othermonstre.collision(monstre):
                        #print("Monstre avec Monstre")
                        othermonstre.changedirection()
                        monstre.changedirection()
            # Mettre en mouvement les monstres
            monstre.bouge()
            # Gravité affecte aux monstres
            monstre.gravite()
            monstre.dessine()
        i += 1


    if piege.collision(pj):
        showinfo('Remerciment!', "Merci d'avoir joué à la première version de Cut'n'Dodge")
        tk.destroy()

    # Gestion de la caméra-
    world.c.x = pj.x - world.c.l / 2
    world.c.y = pj.y - world.c.h / 2
    if world.c.x < 0:
        world.c.x = 0
    if world.c.x + world.c.l > world.l:
        world.c.x = world.l - world.c.l
    if world.c.y < 0:
        world.c.y = 0
    if world.c.y + world.c.h > world.h:
        world.c.y = world.h - world.c.h
    # print(str(world.c.x)+' '+str(world.c.y))
    sol.dessine()
    for plateforme in plateformes:
        plateforme.dessine()


    pj.dessine()
    c_x = world.canvas.bbox(fond)[0]
    c_y = world.canvas.bbox(fond)[1]
    #print(str(img_x)+","+str(img_y)+","+str(world.c.x)+","+str(world.c.y))
    world.canvas.move(fond, img_x - c_x - world.c.x, img_y - c_y - world.c.y)

    piege.dessine()
    # print(pj.l,pj.h,pj.x,pj.y)
    tk.after(VITESSEJEU,gravity)

# Gestion du mouvement

def droite(event):
    global pj
    pj.deplace(1,0)
def gauche(event):
    global pj
    pj.deplace(-1,0)
def haut(event):
    global pj
    if pj.v.dy == 0 and pj.ausol:
        pj.deplace(0,-1, SAUT)
def bas (event): # bouclier ?
    global pj
def feu(event):
    global pj
    pj.fire()


# on crée une fenêtre et un canevas:
tk = Tk()
tk.title('Cut n Dodge')

icon = "Cut-n-Dodge.ico"
tk.iconbitmap(icon)

world = monde(tk)
pj = personnage(world, "joueur_m.gif",  100, 85,10, 29, 48, '')
# création de la liste contenant les monstres
liste_monstres = [
[16,5,40,50],
[28,5,40,50],
[43,5,40,50],
[43,22,40,50],
[31,23.2,40,50],
[8,28,40,50],
[18,28,40,50],
[36,32, 40, 50]
]

# création des monstres
monstres = []
for monstre in liste_monstres:
    monstres.append(objet_monstre(world, "monstre.gif", 100, monstre[0]*LARGEUR, monstre[1]*HAUTEUR, monstre[2], monstre[3], ''))

# sol et piège (pour test)
sol = objet_fixe(world, 0,world.h - 10, world.l, 10, '')
piege = objet_fixe(world, world.l - 260, world.h - 20, 260, 10, '')

# création de la liste des plateformes : coordonnées (x;y) dans une grille sur une feuille dessinée à la main plus longueur et largeur
liste_plateformes=[
[0, 0, 2, 12],
[2, 3, 1, 4],
[2, 6, 20, 4],
[5, 4, 1, 2],
[25, 6, 13,3],
[35, 9, 3, 1],
[26, 9, 1, 2],
[22, 7, 3, 2],
[18, 10, 7, 2],
[40, 6, 10, 4],
[13, 12, 39, 3],
[29, 11, 8, 1],
[43, 10, 10, 2],
[50, 7, 3, 3],
[57, 7, 3, 22],
[60, 3, 2, 27],
[17, 15, 36, 4],
[17, 23, 14, 3],
[31, 24, 5, 2],
[36, 23, 21, 3],
[0, 17, 14, 10],
[0, 10, 2, 2],
[0, 12, 11, 3],
[0, 15, 4, 2],
[17, 19, 2, 2],
[17, 26, 10, 1],
[0, 29, 27, 8],
[0, 27, 8, 2],
[27, 35, 28, 2],
[46, 26, 11, 3],
[46, 29, 7, 4],
[44, 21, 6, 1],
[49, 19, 1, 2],
[3, 0, 9, 1],
[19, 0, 42, 3],
[28, 4, 7, 1],
[31, 3 , 2, 1],
# mini plateformes à partir d'ici
[4, 5, 1, 0.2],
[38, 7, 1, 0.2],
[39, 8, 1, 0.2],
[38, 9, 1, 0.2],
[39, 10, 1, 0.2],
[56, 7.1, 1, 0.2],
[54, 8, 2, 0.2],
[53, 9, 1, 0.2],
[54,10, 2, 0.2],
[56,11, 1, 0.2],
[54,12, 2, 0.2],
[53,13, 1, 0.2],
[54,14, 2, 0.2],
[56,15, 1, 0.2],
[54,16, 2, 0.2],
[53,17, 1, 0.2],
[54,18, 2, 0.2],
[56,19, 1, 0.2],
[54,20, 2, 0.2],
[56,21, 1, 0.2],
[54,22, 2, 0.2],
[56,23, 1, 0.2],
[32,23.1, 1, 0.1],
[34,23.1, 1, 0.1],
[14,17, 1, 0.2],
[16,18, 1, 0.2],
[14,19, 1, 0.2],
[16,20, 1, 0.2],
[14,21, 1, 0.2],
[16,22, 1, 0.2],
[14,23, 1, 0.2],
[16,24, 1, 0.2],
[14,25, 1, 0.2],
[16,26, 1, 0.2],
[14,27, 1, 0.2],
[15,28, 1, 0.2],
[11,12, 1, 0.2],
[12,13, 1, 0.2],
[11,14, 1, 0.2],
[12,15, 1, 0.2],
[11,16, 2, 0.2],
[32,34, 1, 0.2],
[35,33, 3, 0.2],
[40,34, 1, 0.2]
]

# création des plateformes avec mise à l'échelle : ce sont des rectangles qui serviront à faire les collisions avec les joueurs et monstres
plateformes = []

for plateforme in liste_plateformes:
    plateformes.append(objet_fixe(world, plateforme[0]*LARGEUR, plateforme[1]*HAUTEUR, plateforme[2]*LARGEUR, plateforme[3]*HAUTEUR))

# plaquage du graphisme du monde sur les rectangles dessiné juste au dessus
md = PhotoImage(file = 'monde.gif')
fond = world.canvas.create_image(world.l / 2, world.h / 2, image = md)

# calage de l'image en haut à gauche car il y a des écarts de quelques pixels à la mise à l'échelle
img_x = world.canvas.bbox(fond)[0]
img_y = world.canvas.bbox(fond)[1]

world.canvas.move(fond, -img_x, -img_y)

img_x = 0
img_y = 0

# création  d'un bouton "Quitter":
Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)
Bouton_Quitter.pack()

# lancement de la boucle principale de gestion des éléments du jeu
gravity()

# on associe les touches pour déplacer le joueur
world.canvas.bind_all('<Right>', droite)
world.canvas.bind_all('<Left>', gauche)
world.canvas.bind_all('<Up>', haut)
world.canvas.bind_all('<Down>', bas)
world.canvas.bind_all('<space>', feu)

#On lance la boucle principale de gestion des graphismes par tkinter
tk.mainloop()
