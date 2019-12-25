import pygame


class Vaisseau:
    """2 vaisseaux dans le jeu, un de chaque cote !"""
    V = 1
    wait_m = 1000
    wait_l = 300
    vie = 100
    
    def __init__(self,ecran,image,num):
        self.ecran = ecran
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        #self.missile = missile
        #self.laser = laser
        
        self.joueur = num
        self.immunite = False
        self.max = ecran.get_height() - self.image.get_height()
        self.min = 0
        if num == 1:
            self.x = 0
        else:
            self.x = self.ecran.get_width()-self.image.get_width()
        self.y = self.max//2
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

    
    def effacer(self):
        self.ecran.fill((0,0,0),self.rect)
        
    def deplacer(self,dir,dt):
        if self.min<=self.y + dir*self.V*dt <= self.max:
            self.y += dir*self.V*dt
            self.rect = self.image.get_rect(topleft = (self.x,self.y))
            
    def charger(self):
        self.ecran.blit(self.image,self.rect)
            
    def tirer_m(self):
        if self.joueur == 1:
            x,y = self.rect.midright
            dir = 1
        else:
            x,y = self.rect.midleft
            dir = -1
        m = Missile(self.ecran,x,y,dir,self.joueur)
        pygame.time.set_timer(24+self.joueur,self.wait_m)
        return m
    
    def tirer_l(self):
        if self.joueur == 1:
            x,y = self.rect.midright
            dir = 1
        else:
            x,y = self.rect.midleft
            dir = -1
        m = Laser(self.ecran,x,y,dir,self.joueur)
        pygame.time.set_timer(26+self.joueur,self.wait_l)
        return m
    
    def collision(self,elt,explosions):
        offset = [elt.rect[0]-self.rect[0],elt.rect[1]-self.rect[1]]
        pos = self.mask.overlap(elt.mask,offset)
        if pos != None:
            if isinstance(elt,Missile):
                destruction = elt.explosion(explosions)
                self.vie -= elt.dommage
                if self.vie <= 0:
                    pos =(self.x+self.image.get_width()/2,self.y+self.image.get_height()/2)
                    explosions.append(Explosion(self.ecran,pos))
                    self.image = pygame.Surface((1,1))
                    self.rect = self.image.get_rect(topleft = (self.x,self.y))
                    self.image.fill((0,0,0))
                    pygame.time.set_timer(29,1000)
                    
                return destruction
                #enleve de la vie etc
                #immunite avec  timer ?
            else:
                pass#d'autres chose : bonus etc
            
        
   
    
class Missile:
    V = 0.75
    image = None
    dommage = 33
    def __init__(self,ecran,x,y,dir,num):
        self.ecran = ecran
        self.x = x
        self.y = y
        self.joueur = num
        #self.image = image
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = dir #{-1,1}
        self.limite = 0
        if dir == 1:
            self.limite = ecran.get_width()
        
    def effacer(self):
        self.ecran.fill((0,0,0),self.rect)
    
    def deplacer(self,dt,explosions):
        x_suiv = self.x + self.dir * self.V * dt
        if -1*self.dir * x_suiv < -1*self.dir*self.limite:
            return self.explosion(explosions)
        
        self.x = x_suiv
        self.rect = self.image.get_rect(center = (self.x,self.y))
    
    def charger(self):
        self.ecran.blit(self.image,self.rect)
        
        
    def explosion(self,explosions,pos = None):
        self.ecran.fill((0,0,0),self.rect)
        if pos == None:
            pos = (self.x,self.y)
        explosions.append(Explosion(self.ecran,pos))
        return True
        
 
class Laser(Missile):
    V = 1.5
    image = None
    dommage = 5
    def explosion(self,explosions,pos = None):
        self.ecran.fill((0,0,0),self.rect)
        return True
        
        
class Explosion:
    T = 1000 #temps de l'explosion
    images = None
    def __init__(self,ecran,pos):
        self.ecran = ecran
        self.t = 0
        self.n = len(self.images)*len(self.images[0])
        self.pos = pos
        self.image = self.images[0][0]
        self.rect = self.image.get_rect(center = pos)
        self.ecran.fill((0,0,0),self.rect)
        self.ecran.blit(self.image,self.rect)
    
    def effacer(self):
        self.ecran.fill((0,0,0),self.rect)
    
    def charger(self,dt):
        self.t+=dt
        k = (self.n*self.t)//self.T
        if k<self.n:
            i = k//8
            j = k-i*8
            self.image = self.images[i][j]
            self.rect = self.image.get_rect(center = self.pos)
            self.ecran.blit(self.image,self.rect)
        else:
            return True
                 
class BarreVie:
    def __init__(self,ecran,x,y,largeur,hauteur,color,vaisseau):
        self.ecran = ecran
        self.vaisseau = vaisseau
        self.color = color
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.rect = pygame.Rect(x,y,largeur,hauteur)
        self.barre = pygame.Rect(x+5,y+5,largeur-10,hauteur-10)
    
    def charger(self):
        pygame.draw.rect(self.ecran,(255,255,255),self.rect,5)
        if self.vaisseau.vie >= 0:
            self.barre.width = (self.largeur-10)*float(self.vaisseau.vie)/float(Vaisseau.vie)
            pygame.draw.rect(self.ecran,self.color,self.barre)
    
    def effacer(self):
        self.ecran.fill((0,0,0),self.rect)
        
        