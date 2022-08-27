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
    abstract class for tree structure

    Class Attributes
    ----------
    n_tot : int
        total nodes counter
    all_nodes : list[Tree]
        list of all the created nodes ordered by ids
    ROOT : Tree
        the tree's root

    Attributes
    ----------
    id : int
        node id
    depth : int
        node depth (0 for the root, 1 for its children, 2 for the grandchildren...)
    pos : list
        [x,y] the position of the node in the graphic representation
    parent : Tree
        the reference to the parent node, except for the ROOT that has None parent
    scale : (float,float)
        (scale_x, scale_y) multiplicative ratio to adjust the position of the nodes
    xy_ratio : float
        ratio that will widen the distance between two children of the same node if bigger
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
        # display and scaling attributes
        self.scale = (1,1)
        self.xy_ratio = 1
        # adding node to the static list of nodes
        self.all_nodes.append(self)

    def define_parent(self, parent:Tree):
        """
        assigns parent to the node

        Parameters
        ----------
        parent : Tree
            parent node
        """
        self.parent = parent

    def get_pos(self):
        """
        position getter, using the scaling factors

        Returns
        -------
        (float, float)
            node position
        """
        return (self.pos[0]*self.scale[0], self.pos[1]*self.scale[1])

    @staticmethod
    def update_params(self, depth:int=0):
        """
        update position, depth and tree ROOT
        the parent parameter is given to its children, and not defined by children

        Parameters
        ----------
        depth : int
            (default 0, optional) parent's depth
        """
        ...

    @staticmethod
    def isempty(self):
        """
        where or not the node is empty

        Returns
        -------
        bool
        """
        ...

    @staticmethod
    def __str__(self):
        ...

    @classmethod
    def reset(cls):
        """
        empty the class attributes for the creation of a new Tree
        """
        cls.n_tot = 0
        cls.all_nodes = []
        cls.ROOT = None

    
class Tree_empty(Tree):
    """
    subclass of the leaf nodes, cannot be a parent node.
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

    def update_params(self, depth:int=0):
        self.depth = depth
        if self.depth == 0 :
            Tree.ROOT = self
    
    def lines(self, region:list):
        pass

    def __str__(self):
        """
        to string function

        Returns
        -------
        str
            "EmptyNode : depth, id"
        """
        return f"EmptyNode : depth={self.depth}, id={self.id}"
    
class Tree_filled(Tree):
    """
    subclass of parent node
    
    Attributs
    ----------
    l : Tree
        left child node
    r : Tree
        right child node
    s : float
        node's value for the bifurcation rule
    div : string
        ("x" or "y") axis where the division occurs
    label : str
        node's label
    line : list
        [[x0,y0],[x1,y1]] separation line associated with the node
    """
    
    def __init__(self,
                 left:Tree,
                 right:Tree,
                 sep:float,
                 div="",
                 scale=(1,1),
                 xy_ratio=1):
        super().__init__()
        # if separation is vertical,
        self.l = left # this is the bottom
        self.r = right # and this is the top
        # adding parent parameter for the two children
        self.l.define_parent(self)
        self.r.define_parent(self)

        # generating the elements for the separation plot and the node's label
        self.s = sep
        self.div = div
        self.label = div + "<" + str(sep)
        self.line = []

        # scaling and display parameters
        self.scale=scale
        self.xy_ratio=xy_ratio
        self.update_params()

    def __str__(self):
        """
        to string function

        Returns
        -------
        str
            "FilledNode : depth, id, label, left, right"
        """
        return f"FilledNode : depth={self.depth}, id={self.id}, label={self.label}, left={self.l.id}, right={self.r.id}"
    
    def isempty(self):
        return False
    
    def isleaf(self):
        """
        whether or not the node has empty children

        Returns
        -------
        bool
        """
        return (self.l.isempty() and self.r.isempty())

    
    def Tdeepcopy(self):
        """
        returns a deep copy of the current node and its children, no aliasing
        """
        return Tree_filled(self.l.Tdeepcopy(), self.r.Tdeepcopy(), self.s, self.div)

    def update_params(self, depth:int=0):
        """
        update tree parameters

        Parameters
        ----------
        depth : int
            (default:0, optionnal) parent's node depth
        """
        # update depth
        self.depth = depth
        # update ROOT
        if self.depth == 0 :
            Tree.ROOT = self
        # update children positions
        self.l.pos = (self.pos[0] - self.xy_ratio/(1+self.depth), self.pos[1] - 0.5)
        self.r.pos = (self.pos[0] + self.xy_ratio/(1+self.depth), self.pos[1] - 0.5)
        # transitive relation of the scaling factors
        self.l.xy_ratio = self.xy_ratio
        self.r.xy_ratio = self.xy_ratio
        self.l.scale = self.scale
        self.r.scale = self.scale
        # recursion on the children
        self.l.update_params(depth + 1)
        self.r.update_params(depth + 1)
    
    def lines(self, region:list[list]):
        """
        compute the separation line associated to the node

        Parameters
        ----------
        region : list[list]
            region to decompose by the current node
            [[x1,y1],[x2,y2]] are the corner describing a region of the plan
        """
        
        if self.isleaf():
            # if it is a leaf, we cut on the axis

            if self.div == "x":
                self.line = [[self.s, region[0][1]], [self.s ,region[1][1]]]
            elif self.div == "y" :
                self.line = [[region[0][0], self.s], [region[1][0], self.s]]
        
        else :
            # if it is not a leaf, we cut and we compute the two new regions
            if self.div=="x" :
                #on calcule les deux nouvelles régions créées
                rightRegion= [[self.s,region[0][1]],[region[1][0],region[1][1]]]
                leftRegion = [[region[0][0],region[0][1]],[self.s,region[1][1]]]
                l = [[self.s, region[0][1]], [self.s ,region[1][1]]]
                
                # we add the line to the list and we do a recursion on the child nodes
                self.line = l
                self.l.lines(leftRegion)
                self.r.lines(rightRegion)

            # same thing
            elif self.div=="y" :
                botRegion = [[region[0][0],region[0][1]],[region[1][0],self.s]]
                topRegion = [[region[0][0],self.s],[region[1][0],region[1][1]]]
                l = [[region[0][0], self.s], [region[1][0], self.s]]

                self.line = l
                self.l.lines(botRegion)
                self.r.lines(topRegion)