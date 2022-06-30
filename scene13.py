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
import inspect

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def elements_in_order(T:Tree, region=None)->tuple :
    """
    renvoie les éléments à animer pour créer l'arbre dans l'ordre de création

    Parameters
    ----------
    T : Tree
        l'arbre à créer
    region : tuple
        [[x0, y0],[x1, y1]] la région correspondant au schéma de séparation associé à l'arbre

    Returns
    -------
    graph : Group[Mobject]
        le groupe de tous es Mobjects représentant l'arbre
    separation : Group[Mobject], optional
        (optionnel) le groupe de tous les mobjects représentant le schéma de séparation de l'arbre
    """
    G = tuple()

    if region : #si une région est spécifiée on renvoie le schéma de séparation

        #création des axes

        # on divise les axes en 10 segmentations par défaut
        dx = abs(region[0][0] - region[1][0]) / 10
        dy = abs(region[0][1] - region[1][1]) / 10

        axes = Axes(
            x_range=[region[0][0], region[1][0], dx],
            y_range=[region[0][1], region[1][1], dy],
            x_length=6,  # ajustement de la taille originale, peut être modifié ultérieurement
            y_length=6,
            axis_config={"color": GREEN, "include_numbers": True},
            tips=False
        )
        L = tuple() #liste des lignes de séparations

    #tri des noeuds du moins profond au plus profond, puis de gauche à droite
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.pos[0]))

    for n in Nodes :

        #ajout de la ligne qui va du parent à l'actuel noeud
        if n.parent :
            G += (Line(start = [n.parent.pos[0], n.parent.pos[1], 0], end = [n.pos[0], n.pos[1], 0], z_index=-1),)

        #ajout du noeud
        if isinstance(n, Tree_filled): #cas où le noeud contient de l'écriture
            G += (LabeledDot(n.label, point=[n.pos[0], n.pos[1], 0]).set(width=0.45),)

            # le noeud décrit une séparation des données donc on ajoute la ligne de séparation correspondante dans la bonne liste
            if region :
                #on utilise coord_to_point pour avoir la position relative au repère créé plus tôt.
                sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]))
                L += (sep_line,)

        else: #cas où le noeud est une feuille
            G += (Dot(point=[n.pos[0], n.pos[1], 0]).set(width=0.15),)

    if region : #si on renvoie le schéma
        graph = Group(*G)
        separation = Group(axes, *L)
        #on ajuste la taille du schéma et on l'accole à gauche de l'arbre
        separation.match_height(graph).next_to(graph, LEFT)
        separation.add_updater(lambda m:m.match_height(graph).next_to(graph, LEFT))
        return graph, separation
    else :
        return Group(*G)

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

        #génération des lignes
        T6.lines(region)

        #création des éléments à animer
        E, S = elements_in_order(T6, region = region)

        #réorganisation
        E.scale(3).shift(3*RIGHT+UP)
        S.update()

        #ajout de labels sur l'axe
        labels = S[0].get_axis_labels( Tex("x"), Text("y").scale(0.7))

        #animation
        self.play(Create(S[0]), Create(labels)) #création du repère
        k = 1
        for e in E :
            anims = (GrowFromCenter(e),) #création d'un noeud
            if isinstance(e, LabeledDot):
                anims += (Create(S[k]),) #si le noeud est associé à une séparation, on crée en même temps la ligne correspondante
                k+=1
            self.play(*anims)