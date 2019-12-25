import os
import pygame
from pygame.locals import *

from constantes import *
from classe import *

pygame.init()

def load_image(nom, taille = None, colorkey=None):
    chemin = os.path.join("images", nom)
    try:
        image = pygame.image.load(chemin)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    if taille is not None:
        image = pygame.transform.scale(image,taille)
    return image

#Chargements des images et musiques
ecran = pygame.display.set_mode(TAILLE)
pygame.display.set_caption("Space Adventures") 

imageV1 = load_image("vaisseau1.png",(TAILLE[0]//10,TAILLE[0]//10))
imageV2 = load_image("vaisseau2.png",(TAILLE[0]//10,TAILLE[0]//10))
imageMiss = load_image("missile.png",(TAILLE[0]//20,TAILLE[0]//20))
imageLaser = load_image("laser.png",(TAILLE[0]//15,TAILLE[0]//20))
imageE = load_image("explosion.png")
#imageM = load_image("monstre.png")
pygame.mixer.music.load(os.path.join("musique","piste1.mp3"))
pygame.mixer.music.play(loops = -1, start = 12.0)

SIZE = imageE.get_size()
imageE = pygame.transform.scale(imageE,(int(SIZE[0]*0.7),int(SIZE[1]*0.7)))
SIZE = imageE.get_size()
imagesE = [[imageE.subsurface(pygame.Rect((j*SIZE[0]//8,i*SIZE[1]//6,SIZE[0]//8,SIZE[1]//6))) for j in range(8)] for i in range(6)]

#initialisation
Missile.image = imageMiss
Laser.image = imageLaser
Explosion.images = imagesE
J1 = Vaisseau(ecran,imageV1,1)
J2 = Vaisseau(ecran,imageV2,2)
Vie1 = BarreVie(ecran,5,5,100,20,(150,150,150),J1)
Vie2 = BarreVie(ecran,895,5,100,20,(150,150,150),J2)

projectiles = [[],[],[],[]] #missile J1,J2, laser J1,J2
droit_tir = [True,True,True,True]
tir = [J1.tirer_m,J2.tirer_m,J1.tirer_l,J2.tirer_l]
explosions = []

dir1 = 0
dir2 = 0
pressedUP1 = False
pressedUP2 = False
pressedDW1 = False
pressedDW2 = False


menu = False
continuer = True



#Menu
if menu == True:
    pass
    #afficher le menu
    #gestion des touches 
    #menu = False

#Boucle de jeu
timer = pygame.time.Clock()
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        

        
        if event.type == KEYDOWN:
            if event.key == K_UP1:
                dir1 = -1
                pressedUP1 = True
            if event.key == K_DW1:
                dir1 = 1
                pressedDW1 = True
            if event.key == K_UP2:
                dir2 = -1
                pressedUP2 = True
            if event.key == K_DW2:
                dir2 = 1
                pressedDW2 = True
                
            for k in [0,1,2,3]:
                if droit_tir[k] and event.key == K_SHOT[k]:
                    projectiles[k].append(tir[k]())
                    droit_tir[k] = False

            #event tirer/bouclier.
        if event.type == KEYUP:
            if event.key == K_UP1:
                dir1 = pressedDW1
                pressedUP1 = False
            if event.key == K_DW1:
                dir1 = -pressedUP1
                pressedDW1 = False
            if event.key == K_UP2:
                dir2 = pressedDW2
                pressedUP2 = False
            if event.key == K_DW2:
                dir2 = -pressedUP2
                pressedDW2 = False
            
        for k in range(4):
            if event.type == 25+k:
                droit_tir[k] = True
                pygame.time.set_timer(25+k,0)
                
            if event.type == 29:
                continuer = False
                
    

    dt = timer.tick(150)
    
    #1/ Efface tout
    J1.effacer()
    J2.effacer()
    Vie1.effacer()
    Vie2.effacer()
    for k in [0,1,2,3]:
        for proj in projectiles[k]:
            proj.effacer()
    for exp in explosions:
        exp.effacer()
    
    #2/ Bouge tout le monde
    for k in [0,1,2,3]:
        fin = []
        for i,proj in enumerate(projectiles[k]):
            mort = proj.deplacer(dt,explosions)
            if mort:
                fin.append(i)

        for i,j in enumerate(fin):
            del(projectiles[k][j-i])
            
    J1.deplacer(dir1,dt)    
    J2.deplacer(dir2,dt)
    
    #3/ Teste les collisions
    for k in [0,2]:
        fin = []
        for i,proj in enumerate(projectiles[k]):
            mort = J2.collision(proj,explosions)
            if mort:
                fin.append(i)
              
        for i,j in enumerate(fin): #en theorie fin a 1 seul elt mais bon au cas ou
            del(projectiles[k][j-i])
    
    for k in [1,3]:
        fin = []
        for i,proj in enumerate(projectiles[k]):
            mort = J1.collision(proj,explosions)
            if mort:
                fin.append(i)
              
        for i,j in enumerate(fin): #en theorie fin a 1 seul elt mais bon au cas ou
            del(projectiles[k][j-i])

    #4/ Affiche tout
    Vie1.charger()
    Vie2.charger()
    for k in [0,1,2,3]:
        for proj in projectiles[k]:
            proj.charger()
    J1.charger()
    J2.charger()
    fin = []
    for i,exp in enumerate(explosions):
        if exp.charger(dt):
            fin.append(i)
    for i,j in enumerate(fin):
        del(explosions[j-i])
            
            

    
    pygame.display.flip()
    
pygame.quit()   