from math import *
from tkinter import *
import tkinter as tkint

VITESSEJEU = 25
ACCELERATION = 25 / VITESSEJEU
SAUT = 200 / VITESSEJEU
G = 15 / VITESSEJEU
VITESSEMAX = 150 / VITESSEJEU
FROTTEMENT = 5 / VITESSEJEU

LARGEUR = 40
HAUTEUR = 60

# class trouvée et adaptée de : https://openclassrooms.com/forum/sujet/gif-anime-dans-tkinter
class GifAnimatedLabel(tkint.Label):
    """Label containing a GIF animated image

    Args:
        `master`: the master Widget for this GifAnimatedLabel
        `filename`: the file name contaning the GIF image
        `speed`: the delay in millisecond between each frame
    """
    def __init__(self, master, monde, filename, speed, objet,  *args, **kwargs):
        self.speed = speed
        self.tk = master
        self.frames = []
        self.monde = monde
        self.regarde = 1 # droite
        self.filename = filename
        i = 0
        while True:
            try:
                p = PhotoImage(file=filename, format="gif - {}".format(i))
            except tkint.TclError:
                break
            self.frames.append(p)
            i += 1

        #super().__init__(master, image=self.frames[0], *args, **kwargs)
        #print(i)
        self.num_frames = i
        if self.num_frames == 18:
            repere = 9
        else:
            repere = 0
        self.centrage = floor((objet.l - self.frames[repere].width()) / 2)
        self.image = self.monde.canvas.create_image(objet.x + objet.l / 2 + self.centrage, objet.y + objet.h / 2, image = self.frames[repere])
        self.objet = objet
        self.frame_idx = 0
        self.after(self.speed, self._animate)

    def _animate(self):
        if self.num_frames == 18: # perso et monstres = 18 frames
            if self.objet.v.dx >= 0.2: # Vers la droite
                self.regarde = 1
                if self.frame_idx < 10:
                    self.frame_idx = 10
                else:
                    self.frame_idx = (self.frame_idx - 9) % 8 + 10
            elif self.objet.v.dx > -0.2:
                self.frame_idx = 8 + self.regarde
            else:
                self.regarde = 0
                if self.frame_idx > 7:
                    self.frame_idx = 0
                else:
                    self.frame_idx = (self.frame_idx + 1) % 8
        else:
            self.frame_idx = (self.frame_idx + 1) % self.num_frames

        self.monde.canvas.itemconfig(self.image, image = self.frames[self.frame_idx])
            #self.monde.canvas.['image'] = self.frames[self.frame_idx]

        self.after(self.speed, self._animate)

class monde:
    def __init__(self,  tk, w = 2480, h = 2220):
        self.l = w
        self.h = h
        self.c = camera()
        self.tk = tk
        self.canvas = Canvas(tk,width = self.c.l, height = self.c.h , bd=0, bg="#222222")
        self.canvas.pack(padx=10,pady=10)
        self.canvas.focus_set()
    def stay_in(self, joueur):
        if joueur.x < 0:
            joueur.x = 0
            joueur.v.dx = 0
        if joueur.x > self.l - joueur.l:
            joueur.x = self.l - joueur.l
            joueur.v.dx = 0

        if joueur.y < 0:
            joueur.y = 0
            joueur.v.dy = 0
        if joueur.y > self.h - joueur.h:
            joueur.y = self.h - joueur.h
            joueur.v.dy = 0

class camera():
    def __init__(self, x = 0, y = 0, l = 1000, h = 500):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
#    def center(self, om):
#        return om.x < self.x or om.x + om.l > self.x + self.l or om.y < self.y or om.y + om.h > self.y + self.h

class velocite:
    def __init__(self, dx = 0, dy = 0):
        self.dx = dx
        self.dy = dy
        self.max = VITESSEMAX
    def accelere(self, ax, ay):
        self.dx += ax
        if abs(self.dx) > self.max :
            self.dx = self.max * self.dx / abs(self.dx)
        if abs(self.dx) < 0.2 :
            self.dx = 0
        self.dy += ay
        if self.dy > self.max :
            self.dy = self.max * self.dy / abs(self.dy)

#defini tous les objets fixes
class objet_fixe:
    def __init__(self, world, x = 0, y = 0, l = 0, h = 0, couleur = ''):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.w = world
        self.g = self.w.canvas.create_rectangle(self.x,self.y,self.x+self.l,self.y+self.h,fill= couleur, tag='item', outline = "")

    def collision(self, joueur):
        return joueur.x < self.x + self.l and joueur.x + joueur.l > self.x and joueur.y < self.y + self.h and joueur.y + joueur.h > self.y

    def dessine(self):
        self.w.canvas.coords(self.g,self.x - self.w.c.x, self.y - self.w.c.y, self.x - self.w.c.x +self.l, self.y - self.w.c.y +self.h)

#rajoute à l'objet la capacité à avoir du mouvement
class objet_mobile(objet_fixe):
    def __init__(self, world, filename, speed, x = 0, y = 0, l = 0, h = 0, couleur = 'green'):
        super().__init__(world, x, y, l, h, couleur)
        self.v = velocite()
        self.gif = GifAnimatedLabel(self.w.tk, world, filename, speed, self)
        self.ausol = False

    def deplace(self, gd, hb, a = ACCELERATION):
        self.v.accelere(gd * a, hb * a)
        self.x += self.v.dx
        self.y += self.v.dy
        self.x = round(self.x)
        self.y = round(self.y)

    def gravite(self):
        self.deplace(0, 1, G)
        if self.v.dx != 0:
            self.deplace(self.v.dx / abs(self.v.dx), 0 , -FROTTEMENT)

    def dessine(self):
        super().dessine()
        self.w.canvas.move(self.gif.image, self.x - self.w.canvas.bbox(self.gif.image)[0] - self.w.c.x + self.gif.centrage, self.y - self.w.canvas.bbox(self.gif.image)[1] - self.w.c.y)

    # Remise à zéro de la liste des objets en collision avec l'objet mobile
    def reset_collision(self):
        self.liste_collisions = []
    # Ajoute un objet à la liste des objets en collision avec l'objet mobile
    def add_collision(self, objet):
        self.liste_collisions.append(objet)
    # Gère les collisions de l'objet mobile avec les autres objets
    def move_collision(self):
        self.ausol = False
        for collision in self.liste_collisions:
            if self.y + self.h > collision.y and self.y < collision.y:
                #print("haut")
                self.y = collision.y - self.h
                self.v.dy = 0
                self.ausol = True # Essentiel pour savoir si l'objet mobile est sur le sol ou pas pour par exemple sauter
            # par le bas
            elif self.y < collision.y + collision.h and self.y + self.h > collision.y + collision.h:
                #print("bas")
                self.y = collision.y + collision.h
                self.v.dy = 1
            # par la gauche
            elif self.x + self.l > collision.x and self.x < collision.x:
                #print("gauche")
                self.x = collision.x - self.l
                self.v.dx = 0
            # par la droite
            elif self.x < collision.x + collision.l and self.x + self.l > collision.x + collision.l:
                #print("droite")
                self.x = collision.x + collision.l
                self.v.dx = 0
            else: # On a traversé un bloc à cause de la vitesse : ne dois pas arriver normalement si les paramètres sont bien réglés
                #print('boom')
                # On cherche la sortie la plue "proche"
                exit.gauche = abs(self.x - collision.x)
                exit.droite = abs((self.x + self.l) - (collision.x + collision.l))
                if exit.gauche < exit.droite:
                    self.x = collision.x - self.l
                    self.v.dx = 0
                else:
                    self.x = collision.x + collision.l
                    self.v.dx = 0
                self.y = self.y - self.v.dy
                self.v.dy = 0

    def stopexplosion(self):
        self.w.canvas.delete(self.g)
        self.w.canvas.delete(self.gif.image)
        del self

# définit le personnage et ses particularités
class personnage(objet_mobile):
    def __init__(self, world, filename, speed, x = 0, y = 0, l = 0, h = 0, couleur = 'red'):
        super().__init__(world, filename, speed, x, y, l, h, couleur)
        self.feu = False   

    def fire(self):
        if not self.feu:
            if self.gif.regarde == 1:
                self.attaque = objet_mobile(self.w, 'fbdr.gif', 100, self.x+self.l, self.y + 10, 42, 24, "")
                self.attaque.v.dx = VITESSEMAX
            else:
                self.attaque = objet_mobile(self.w, 'fbgr.gif', 100, self.x - 40, self.y + 10, 42, 24, "")
                self.attaque.v.dx = - VITESSEMAX
            self.feu = True
            self.w.tk.after(30 * VITESSEJEU, self.stopfire)

    def stopfire(self):
        if self.feu:
            self.feu = False
            self.w.canvas.delete(self.attaque.g)
            self.w.canvas.delete(self.attaque.gif.image)
            del self.attaque

    def dessine(self):
        super().dessine()
        if self.feu:
            self.attaque.deplace(self.attaque.v.dx/abs(self.attaque.v.dx), 0)
            self.attaque.dessine()


# définit les monstres et leurs particularités
class objet_monstre(objet_mobile):
    def __init__(self, world, filename, speed, x = 0, y = 0, l = 0, h = 0, couleur = 'blue'):
        super().__init__(world, filename, speed, x, y, l, h, couleur)
        self.sens = 1

    # Mouvement des monstres
    def bouge(self, a = ACCELERATION / 2):
        self.v.accelere(a * self.sens, 0)
        if abs(self.v.dx) >= VITESSEMAX:
            self.changedirection()
    # Changement de direction
    def changedirection(self):
        self.sens = - self.sens
        #self.v.dx = 0

    def meurt(self):
        self.w.canvas.delete(self.g)
        self.w.canvas.delete(self.gif.image)
        explosion = objet_mobile(self.w, 'explosion.gif', 100, self.x + 9, self.y + 4, 32, 32, '')
        explosion.dessine()
        self.w.tk.after(30 * VITESSEJEU, explosion.stopexplosion)
        del self
