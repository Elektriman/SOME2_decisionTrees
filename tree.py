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
    n_tot : int
        nombre total de noeuds
    all_nodes : list[Tree]
        la liste de tous les noeuds de l'arbre par ordre d'identifiant
    ROOT : Tree
        la racine de l'arbre

    Attributes
    ----------
    id : int
        identifiant du noeud
    depth : int
        donne la profondeur du noeud
    pos : list
        [x,y] la position du noeud dans la représentation graphique
    parent : Tree
        le noeud parent, None si le noeud est la racine
    scale : float
        ajustement des distances entre les noeuds
    xy_ratio : float
        ratio qui permet d'avoir un arbre plus large (<1) ou plus haut (>1)
    """
    n_tot = 0
    all_nodes = []
    ROOT = None

    def __init__(self):
        self.id = Tree.n_tot
        Tree.n_tot += 1
        self.depth = 0
        self.pos = (0,0)
        self.parent = None
        # attributs de scaling pour l'affichage
        self.scale = 1
        self.xy_ratio = 1
        #ajout à la liste totale de tous les neouds
        self.all_nodes.append(self)

    def define_parent(self, parent):
        """
        permet d'assigner un parent à un noeud

        Parameters
        ----------
        parent : Tree
            noeud parent
        """
        self.parent = parent

    def get_pos(self):
        """
        getter pour la position
        Returns
        -------
        tupe
            position du noeud
        """
        return (self.pos[0]*self.scale, self.pos[1]*self.scale)

    @staticmethod
    def update_params(self, depth=0):
        """
        mise à jour des paramètres de profondeur, de la position du noeud et mise à jour du noeud racine.
        seul un noeud parent modifie la position de ses noeuds enfants.

        Parameters
        ----------
        depth : int, optional
            profondeur du parent. La valeur par défaut est 0.
        """
        ...

    @staticmethod
    def __str__(self):
        ...

    
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

    def update_params(self, depth=0):
        self.depth = depth
        if self.depth == 0 :
            Tree.ROOT = self
    
    def lines(self, region):
        pass

    def __str__(self):
        """
        réécriture de la fonction str pour un affichage plus propre

        Returns
        -------
        str
            "EmptyNode : depth, id"
        """
        return f"EmptyNode : depth={self.depth}, id={self.id}"
    
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
    label : str
        le label associé au noeud
    line : list
        [[x0,y0],[x1,y1]] la ligne de séparation associée au noeud
    """
    
    def __init__(self, left:Tree, right:Tree, seuil:float, div="", scale=1, xy_ratio=1):
        super().__init__()
        self.l = left #également bottom
        self.r = right #également top
        #ajout du parent pour les deux enfants
        self.l.define_parent(self)
        self.r.define_parent(self)

        self.s = seuil
        self.div = div
        self.label = div + "<" + str(seuil)
        self.line = []

        #paramètres communs à tout l'arbre
        self.scale=scale
        self.xy_ratio=xy_ratio
        self.update_params()

    def __str__(self):
        """
        réécriture de la fonction str pour un affichage plus propre

        Returns
        -------
        str
            "FilledNode : depth, id, label, left, right"
        """
        return f"FilledNode : depth={self.depth}, id={self.id}, label={self.label}, left={self.l.id}, right={self.r.id}"
    
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

    def update_params(self, depth=0):
        """
        met à jour les paramètres de l'arbre

        Parameters
        ----------
        depth : int
            la profondeur du noeud parent
        """
        #mise à jour de la profondeur
        self.depth = depth
        #mise à jour du noeud racine
        if self.depth == 0 :
            Tree.ROOT = self
        #mise à jour de la position des noeuds enfants
        self.l.pos = (self.pos[0] - self.xy_ratio/(1+self.depth), self.pos[1] - 0.5)
        self.r.pos = (self.pos[0] + self.xy_ratio/(1+self.depth), self.pos[1] - 0.5)
        #transmission des valeurs de scaling pour l'affichage
        self.l.xy_ratio = self.xy_ratio
        self.r.xy_ratio = self.xy_ratio
        self.l.scale = self.scale
        self.r.scale = self.scale
        #récursion sur les arbres enfants
        self.l.update_params(depth + 1)
        self.r.update_params(depth + 1)
    
    def lines(self, region):
        """
        associe la ligne associée à la séparation du noeud

        Parameters
        ----------
        region : list[list]
            région à décomposer en deux selon le noeud actuel. 
            La région est la zone rectangulaire entre deux points [[x1,y1],[x2,y2]]
        """
        
        if self.isleaf():
            #si c'est une feuille
            #on coupe en deux selon le seuil et l'axe

            if self.div == "x":
                self.line = [[self.s, region[0][1]], [self.s ,region[1][1]]]
            elif self.div == "y" :
                self.line = [[region[0][0], self.s], [region[1][0], self.s]]
        
        else :
            #si ce n'est pas une feuille
            #on coupe en fonction du seuil et de l'axe
            if self.div=="x" :
                #on calcule les deux nouvelles régions créées
                rightRegion= [[self.s,region[0][1]],[region[1][0],region[1][1]]]
                leftRegion = [[region[0][0],region[0][1]],[self.s,region[1][1]]]
                l = [[self.s, region[0][1]], [self.s ,region[1][1]]]
                
                #puis on ajoute les division des sous régions en plus de l'actuelle séparation
                self.line = l
                self.l.lines(leftRegion)
                self.r.lines(rightRegion)

            elif self.div=="y" :
                botRegion = [[region[0][0],region[0][1]],[region[1][0],self.s]]
                topRegion = [[region[0][0],self.s],[region[1][0],region[1][1]]]
                l = [[region[0][0], self.s], [region[1][0], self.s]]
                self.line = l
                self.l.lines(botRegion)
                self.r.lines(topRegion)
                
#  _            _       
# | |          | |      
# | |_ ___  ___| |_ ___ 
# | __/ _ \/ __| __/ __|
# | ||  __/\__ \ |_\__ \
#  \__\___||___/\__|___/

if __name__=="__main__":
    #création d'un arbre test
    region =  [[30,70],[0,12]]




