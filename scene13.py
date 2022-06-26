#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import networkx as nx
from tree import *

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def manimise_tree(T:Tree)->tuple[Mobject, dict] :
    """
    transforme un objet de type Tree en un objet Manim de type Graph associé à un dictionnaire du contenu à écrire sur chaque noeud
    Parameters
    ----------
    T : Tree
        Arbre à mettre au format Manim

    Returns
    -------
        G : Graph
            un objet Manim consitué d'une liste de points et de traits
        L : dict[int:str]
            un dictionnaire ayant pour clé l'identifiant d'un noeud et pour valeur associée la chaine de caractères à écrire sur ce noeud
    """
    G = nx.Graph()
    G.add_node(T.id)
    L = {}
    L[T.id] = T.label

    #fonction récursive pour ajouter les points et traits au graphe
    def graph_from_tree(T:Tree):
        #noeud vide ?
        if T.isempty():
            return None #condition d'arrêt
        else :
            #sinon on ajoute les noeuds de gauche et droite
            G.add_node(T.r.id)
            G.add_edge(T.id, T.r.id)
            L[T.r.id] = T.r.label

            G.add_node(T.l.id)
            G.add_edge(T.id, T.l.id)
            L[T.l.id] = T.l.label

            #si les noeuds enfants ne sont pas vides on répète l'opération
            if not T.r.isempty() :
                graph_from_tree(T.r)

            if not T.l.isempty():
                graph_from_tree(T.l)

    graph_from_tree(T)

    return G,L

def manimise_separation(L:list, region:tuple)->Mobject :
    """
    génère un Vectorised Mobject avec des axes et la séparation du plan en suivant les lignes données dans la liste L

    Parameters
    ----------
    L : list[list]
        liste des segments à tracer de la forme [[début, fin], ...]
    region : list[list]
        liste des deux points formant les coins de l'espace sur lequel on a effectué la séparation

    Returns
    -------
    VGroup[Axes, VGroup[Line]]
        renvoie un groupe de 2 mobjects, un étant les axes du shéma, l'autre étant l'ensemble des segments représentant les séparations
    """
    #on divise les axes en 10 segmentations par défaut
    dx = abs(region[0][0]-region[1][0])/10
    dy = abs(region[0][1]-region[1][1])/10

    #création des axes x et y
    axes = Axes(
        x_range = [region[0][0], region[1][0], dx],
        y_range = [region[0][1], region[1][1], dy],
        x_length = 6, #ajustement de la taille originale, peut être modifié ultérieurement
        y_length = 6,
        axis_config={"color": GREEN, "include_numbers": True},
        tips=False
    )
    #création du groupe de lignes
    Sep = VGroup()  # groupe des séparations
    for el in L : #ajout de chaque ligne
        Sep.add(Line(el[0]+[0], el[1]+[0]))
    Sep.move_to([0,0,0]).scale(6) #alignement avec les axes

    return VGroup(axes,Sep)

def adjust_dot_size(G:Graph):
    """
    procédure qui ajuste la taille des points : plus gros si il y a du texte dedans
    Parameters
    ----------
    G : Graph
        le graphe dont on veut ajuster la taille des points
    """
    for m in G: #on parcourt les mobjects qui composent le graphe
        if m.__class__.__name__ == "LabeledDot": #on ne conserve que les points
            if len(a[1]) > 0: #on vérifie si les points ont un texte non-vide
                m.set(width=0.7)
            else:
                m.set(width=0.3)

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene13(Scene):
    def construct(self):
        #création d'un arbre
        region = [[0, 0], [1, 1]]
        T1 = Tree_filled(Tree_empty(), Tree_empty(), 3 / 4, "x")
        T2 = Tree_filled(Tree_empty(), Tree_empty(), 1 / 4, "y")
        T3 = Tree_filled(T1, Tree_empty(), 3 / 4, "y")
        T4 = Tree_filled(Tree_empty(), T3, 1 / 4, "x")
        T5 = Tree_filled(Tree_empty(), T2, 1 / 2, "x")
        T6 = Tree_filled(T5, T4, 1 / 2, "y")

        #manimisation de l'arbre
        G6,Labels = manimise_tree(T6)
        G = Graph(list(G6.nodes), list(G6.edges), layout="tree", root_vertex=T6.id, labels=Labels)
        adjust_dot_size(G)

        #création et manimisation du schéma associé
        L = T6.lines(region)
        S = manimise_separation(L, region)

        #ajustement
        G.move_to([4,0,0]).scale(1.5)
        S.move_to([-3, 0, 0])

        #animation
        self.play(Create(G), Create(S), run_time=10)