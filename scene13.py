#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
from tree import *
from LabeledNode import LabeledNode

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

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
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.get_pos()[0]))

    for n in Nodes :

        #ajout du noeud
        if isinstance(n, Tree_filled): #cas où le noeud contient de l'écriture
            nText = Text(n.label, color=BLACK, font_size=15).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

            # le noeud décrit une séparation des données donc on ajoute la ligne de séparation correspondante dans la bonne liste
            if region :
                #on utilise coord_to_point pour avoir la position relative au repère créé plus tôt.
                sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]), color=YELLOW)
                L += (sep_line,)

        else: #cas où le noeud est une feuille
            G += (Dot(point=[n.get_pos()[0], n.get_pos()[1], 0]).set(width=0.15, color=WHITE),)

        # ajout de la ligne qui va du parent à l'actuel noeud
        if n.parent:
            if isinstance(n, Tree_filled):
                G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0],
                                   end=G[-1].get_critical_point(UP),
                                   z_index=-1,
                                   color=LIGHT_GRAY),) + (G[-1],)
            else:
                G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0],
                                   end=[n.get_pos()[0], n.get_pos()[1], 0],
                                   z_index=-1,
                                   color=LIGHT_GRAY),) + (G[-1],)

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
        T6 = Tree_filled(T5, T4, 1 / 2, "y", scale=1.5)

        #génération des lignes
        T6.lines(region)

        self.create_tree(T6, region)

    def create_tree(self, T, region=None):
        # création des éléments à animer
        E, S = elements_in_order(T, region=region)

        # réorganisation
        E.shift(2 * RIGHT + UP).scale(1.5)
        S.update()

        # ajout de labels sur l'axe
        labels = S[0].get_axis_labels(Tex("x"), Text("y").scale(0.7))

        self.play(Create(S[0]), Create(labels))  # création du repère
        k = 1
        for e in E:
            if isinstance(e, LabeledNode):
                # si le noeud est associé à une séparation, on crée en même temps la ligne correspondante
                anims = (Create(e), Create(S[k]),)
                k += 1
            elif isinstance(e, Dot):
                # si le noeud est une feuille, on effectue GrowFromCenter
                anims = (GrowFromCenter(e),)
            else:
                # si on trace une ligne entre deux noeuds, on utilise Create
                anims = (Create(e),)

            self.play(AnimationGroup(*anims), run_time=0.5)
