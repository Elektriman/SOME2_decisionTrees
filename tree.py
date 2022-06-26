# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 11:26:25 2022

@author: Crambes
"""

#  _____                            _       
# |_   _|                          | |      
#   | |  _ __ ___  _ __   ___  _ __| |_ ___ 
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |                       
#                 |_|

from abc import ABC

#   _____ _                         
#  / ____| |                        
# | |    | | __ _ ___ ___  ___  ___ 
# | |    | |/ _` / __/ __|/ _ \/ __|
# | |____| | (_| \__ \__ \  __/\__ \
#  \_____|_|\__,_|___/___/\___||___/

class Tree(ABC) :
    """
    classe abstraite pour créer une structure d'arbre

    Class Attributes
    ----------
    ID : int
        entier qui augmente à chaque création de noeud

    Attributes
    ----------
    id : int
        identifiant du noeud
    depth : int
        donne la profondeur du noeud
    """
    ID = 0

    def __init__(self):
        self.id = Tree.ID
        Tree.ID += 1
        self.depth = 0
    
class Tree_empty(Tree):
    """
    sous classe d'arbre vide (fin les branches), ne peut pas être parent d'autre noeuds
    """
    def __init__(self):
        super().__init__()
        self.label=""
    
    def isempty(self):
        return True
    
    def Tdeepcopy(self):
        return Tree_empty()
    
    def returnLNR(self):
        return []

    def update_depth(self, depth):
        pass
    
    def lines(self, region):
        return []
    
class Tree_filled(Tree):
    """
    sous classe d'arbre plein
    
    Attributs
    ----------
    l : Tree
        branche de gauche
    r : Tree
        branche de droite
    s : float
        seuil associé au noeud
    div : string
        indicateur de l'axe sur lequel faire la division ("x" ou "y")
    """
    
    def __init__(self, left:Tree, right:Tree, seuil:float, div=""):
        super().__init__()
        self.l = left #également bottom
        self.r = right #également top
        self.s = seuil
        self.div = div
        self.label = div + "<" + str(seuil)
    
    def isempty(self):
        """
        renvoie True si le noeud est vide
        """
        return False
    
    def isleaf(self):
        """
        renvoie True si le noeud est une feuille
        """
        return (self.l.isempty() and self.r.isempty())
    
    def Tdeepcopy(self):
        """
        renvoie une copie profonde de l'arbre (pas d'aliasing)
        """
        return Tree_filled(self.l.Tdeepcopy(), self.r.Tdeepcopy(), self.s, self.div)
    
    def returnLNR(self):
        """
        renvoie un affichage Gauche Millieu Droite de l'arbre dans une liste de tuples (seuil, axe de division)
        """
        return self.l.returnLNR() + [(self.s, self.div)] + self.r.returnLNR()

    def update_depth(self, depth=0):
        """
        mise à jour de la profondeur quand on rajoute un parent

        Parameters
        ----------
        depth : int, optional
            profondeur du parent. La valeur par défaut est 0.
        """
        self.depth = depth
        self.l.update_depth(depth + 1)
        self.r.update_depth(depth + 1)
    
    def lines(self, region):
        """
        renvoie une liste des lignes à tracer pour afficher la séparation de l'espace correspondant à l'arbre

        Parameters
        ----------
        region : list[list]
            région à décomposer en deux selon le noeud actuel. 
            La région est la zone rectangulaire entre deux points [[x1,y1],[x2,y2]]

        Returns
        -------
        list[list]
            liste de segments définis pas leurs extrémités.
            segment = [[x1,y1],[x2,y2]]

        """
        
        if self.isleaf():
            #si c'est une feuille
            #on coupe en deux selon le seuil et l'axe
            
            if self.div == "x":
                return [[[self.s, region[0][1]], [self.s ,region[1][1]]]]
            elif self.div == "y" :
                return [[[region[0][0], self.s], [region[1][0], self.s]]]
        
        else :
            #si ce n'est pas une feuille
            #on coupe en fonction du seuil et de l'axe
            if self.div=="x" :
                #on calcule les deux nouvelles régions créées
                rightRegion= [[self.s,region[0][1]],[region[1][0],region[1][1]]]
                leftRegion = [[region[0][0],region[0][1]],[self.s,region[1][1]]]
                line = [[[self.s, region[0][1]], [self.s ,region[1][1]]]]
                
                #puis on ajoute les division des sous régions en plus de l'actuelle séparation
                return line + self.l.lines(leftRegion) + self.r.lines(rightRegion)
            
            elif self.div=="y" :
                botRegion = [[region[0][0],region[0][1]],[region[1][0],self.s]]
                topRegion = [[region[0][0],self.s],[region[1][0],region[1][1]]]
                line = [[[region[0][0], self.s], [region[1][0], self.s]]]
                return line + self.l.lines(botRegion) + self.r.lines(topRegion)
                
#  _            _       
# | |          | |      
# | |_ ___  ___| |_ ___ 
# | __/ _ \/ __| __/ __|
# | ||  __/\__ \ |_\__ \
#  \__\___||___/\__|___/

if __name__=="__main__":
    #création d'un arbre test
    region =  [[0,0],[1,1]]
    T1 = Tree_filled(Tree_empty(),Tree_empty(),3/4,"x")
    T2 = Tree_filled(Tree_empty(),Tree_empty(),1/4,"y")
    T3 = Tree_filled(Tree_empty(),T1,3/4,"y")
    T4 = Tree_filled(Tree_empty(),T2,1/2,"x")
    T5 = Tree_filled(Tree_empty(),T3,1/4,"x")
    T6 = Tree_filled(T4,T5,1/2,"y")
    Lines = T6.lines(region)
    #vérification de la fonction profondeur
    print(T1.depth,T2.depth,T3.depth,T4.depth,T5.depth, T6.depth)

    import matplotlib.pyplot as plt

    print(Lines)
    for l in Lines :
        plt.plot([l[0][0],l[1][0]], [l[0][1],l[1][1]])
    plt.xlim(region[0][0], region[1][0])
    plt.xlim(region[0][1], region[1][1])