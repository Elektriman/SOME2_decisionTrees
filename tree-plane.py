# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 11:26:25 2022

@author: Crambes
"""

from abc import ABC
import matplotlib.pyplot as plt

class tree(ABC) :
    """
    classe abstraite pour créer une structure d'arbre
    """
    pass
    
class tree_empty(tree):
    """
    sous classe d'arbre vide (fin les branches), ne contient aucune valeur
    """
    def __init__(self):
        self.height = 0
    
    def isempty(self):
        return True
    
    def Tdeepcopy(self):
        return tree_empty()
    
    def returnLNR(self):
        return []
    
    def update_depth(self, depth):
        pass
    
    def lines(self, region):
        return []
    
class tree_filled(tree):
    """
    sous classe d'arbre plein
    
    Attributs
    ----------
    l : tree
        branche de gauche
    r : tree
        branche de droite
    s : float
        seuil associé au noeud
    div : string
        indicateur de l'axe sur lequel faire la division ("x" ou "y")
    depth : int
        donne la profondeur du noeud
    """
    
    def __init__(self, left:tree, right:tree, seuil:float, div=""):
        self.l = left #également bottom
        self.r = right #également top
        self.s = seuil
        self.div = div
        self.depth = 0
        self.update_depth()
    
    def update_depth(self, depth=0):
        """
        mise à jour de la profondeur quand on rajoute un parent

        Parameters
        ----------
        depth : int, optional
            profondeur du parent. La valeur par défaut est 0.
        """
        self.depth = depth
        self.l.update_depth(depth+1)
        self.r.update_depth(depth+1)
    
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
        return tree_filled(self.l.Tdeepcopy(), self.r.Tdeepcopy(), self.s, self.div)
    
    def returnLNR(self):
        """
        renvoie un affichage Gauche Millieu Droite de l'arbre dans une liste de tuples (seuil, axe de division)
        """
        return self.l.returnLNR() + [(self.s, self.div)] + self.r.returnLNR()
    
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
                


if __name__=="__main__":
    #création d'un arbre test
    region =  [[0,0],[1,1]]
    T1 = tree_filled(tree_empty(),tree_empty(),3/4,"x")
    T2 = tree_filled(tree_empty(),tree_empty(),1/4,"y")
    T3 = tree_filled(tree_empty(),T1,3/4,"y")
    T4 = tree_filled(tree_empty(),T2,1/2,"x")
    T5 = tree_filled(tree_empty(),T3,1/4,"x")
    T6 = tree_filled(T4,T5,1/2,"y")
    Lines = T6.lines(region)
    #vérification de la fonction profondeur
    print(T1.depth,T2.depth,T3.depth,T4.depth,T5.depth, T6.depth)
    
    #déboggage en cours
    print(Lines)
    for l in Lines :
        plt.plot([l[0][0],l[1][0]], [l[0][1],l[1][1]])
    plt.xlim(region[0][0], region[1][0])
    plt.xlim(region[0][1], region[1][1])
































