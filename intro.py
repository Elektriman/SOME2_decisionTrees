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

def elements_in_order(T:Tree, region=None, label_leaves=False)->tuple :
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
        dy = abs(region[0][1] - region[1][1]) / 10

        axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[0, 1, 0.5],
            x_length=6,  # ajustement de la taille originale, peut être modifié ultérieurement
            y_length = 6,
            x_axis_config={"include_numbers": True, "numbers_to_include": [0, 1, 2, 3]},
            axis_config={"color": WHITE, "exclude_origin_tick":False},
            tips=False
        )

        #édition manuelle de l'axe y
        y_pos = [0.3, 0.7]
        y_ticks = ["No", "Yes"]
        y_dict = dict(zip(y_pos, y_ticks))
        axes.add_coordinates(None, y_dict)

        L = tuple() #liste des lignes de séparations

    #tri des noeuds du moins profond au plus profond, puis de gauche à droite
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.get_pos()[0]))
    k = 1

    for n in Nodes :

        #ajout du noeud
        if isinstance(n, Tree_filled): #cas où le noeud contient de l'écriture
            nText = Text(n.label, color=BLACK, font_size=15, z_index=1).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

            # le noeud décrit une séparation des données donc on ajoute la ligne de séparation correspondante dans la bonne liste
            if region :
                #on utilise coord_to_point pour avoir la position relative au repère créé plus tôt.
                sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]))
                L += (sep_line,)

        else: #cas où le noeud est une feuille
            if label_leaves :
                G += (Text(f"decision {k}", color=BLACK, font_size=10)\
                      .add_background_rectangle(color=WHITE, opacity=1, buff=0.1)\
                      .move_to([n.get_pos()[0], n.get_pos()[1], 0]),)
                k += 1
            else :
                G += (Dot(point=[n.get_pos()[0], n.get_pos()[1], 0]).set(width=0.3, color=WHITE),)

        # ajout de la ligne qui va du parent à l'actuel noeud
        if n.parent:
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

def add_yes_no(line, text, font_size=15):
    """
    génère un texte "yes" ou "no" à coté d'une ligne du graphe
    Parameters
    ----------
    line : Line
        la ligne à côté de laquelle afficher le texte
    text : str
        "yes" ou "no" pour définir si le texte sera à droite ou à gauche, et si le texte sera yes ou no
    font_size : int
        la taille de la police

    Returns
    -------
    Text Mobject
        le Text Mobject prêt à être affiché
    """
    #updater de position
    def x_updater(m, line, direction):
        m.move_to(line).shift((m.width/2+(line.get_length()*0.1)) * direction)

    if text=="yes" :
        #une ligne yes va vers la droite
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).set_z_index(line.z_index, True)
        txt.shift((txt.width/2+(line.get_length()*0.1)) * RIGHT)
        txt.add_updater(lambda m: x_updater(m, line, RIGHT))
    else :
        #une ligne no va vers la gauche
        txt = Text("no", color=WHITE, font_size=font_size).move_to(line).set_z_index(line.z_index, True)
        txt.shift((txt.width/2+(line.get_length()*0.1)) * LEFT)
        txt.add_updater(lambda m:x_updater(m, line, LEFT))

    return txt

def remake_node(old_node, *text, color=BLUE_C, cr=0.07):
    N = LabeledNode(Paragraph(*text,
                              fill_opacity=0.,
                              alignment="center",
                              font_size=15,
                              color=BLACK),
                    cr=cr).move_to(old_node).set_z_index(old_node.z_index, True)
    N[1].set(fill_color=color, color=color, corner_radius=cr)
    N[0].set_z_index(N[1].z_index + 1, True)
    return N

def remake_leaf(old_leaf, *text):
    L = Paragraph(*text,
                  fill_opacity=0.,
                  alignment="center",
                  color=BLACK,
                  font_size=int(old_leaf.font_size * 0.4))\
        .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
        .move_to(old_leaf)
    L.set_z_index(L.submobjects[0].z_index+1, True)
    L.submobjects[0].set_z_index(L.submobjects[0].z_index - 1)
    return L

def arbre1():
    #create the tree
    T0 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")

    T2 = Tree_filled(T0, Tree_empty(), 0, "x")
    T3 = Tree_filled(T1, Tree_empty(), 0, "x")
    T4 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")

    T5 = Tree_filled(T2, Tree_empty(), 0, "x")
    T6 = Tree_filled(T3, T4, 0, "x")

    T7 = Tree_filled(T5, T6, 0, "x", scale=(1.5,1.2), xy_ratio=1.2)

    G = elements_in_order(T7, label_leaves=True)

    #remake the nodes
    L26 = remake_node(G[26], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L28 = remake_node(G[28], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L30 = remake_node(G[30], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L32 = remake_node(G[32], "XXXX", color=GREEN_B, cr=0).scale(0.6)

    G14 = remake_node(G[14], "XXXXX", color=BLUE_E).scale(0.7)
    G18 = remake_node(G[18], "XXXXX", color=BLUE_E).scale(0.7)
    L16 = remake_node(G[16], "XXXXX", color=GREEN_B, cr=0).scale(0.7)
    L20 = remake_node(G[20], "XXXXX", color=GREEN_B, cr=0).scale(0.7)
    L22 = remake_node(G[22], "XXXXX", color=GREEN_B, cr=0).scale(0.7)
    L24 = remake_node(G[24], "XXXXX", color=GREEN_B, cr=0).scale(0.7)

    G6 = remake_node(G[6], "XXXXXX", color=BLUE_E).scale(0.8)
    G10 = remake_node(G[10], "XXXXXX", color=BLUE_E).scale(0.8)
    G12 = remake_node(G[12], "XXXXXX", color=BLUE_E).scale(0.8)
    L8 = remake_node(G[8], "XXXXXX", color=GREEN_B, cr=0).scale(0.8)

    G2 = remake_node(G[2], "XXXXXXX", color=BLUE_E).scale(0.9)
    G4 = remake_node(G[4], "XXXXXXX", color=BLUE_E).scale(0.9)

    G0 = remake_node(G[0], "XXXXXXXX", color=BLUE_E)

    remake = [G0, G2, G4, G6, L8, G10, G12, G14, L16, G18, L20, L22, L24, L26, L28, L30, L32]
    remade = [g for g in G]

    for i in range(len(remake)):
        remade[2 * i] = remake[i].scale(0.75)

    for i in range(1, len(remade), 2):
        remade[i] = remade[i]

    return Group(*remade)

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Intro(MovingCameraScene):
    def construct(self):

        #create an animation for the introduction
        #the animation is a tree without text being built
        A = arbre1()
        title = Text("Decision Trees", font_size=40).next_to(A, UP, buff=0.5)
        view = Group(A,title)

        self.camera.frame.move_to(view).match_width(view).scale(1.2)
        self.wait()

        Anims = self.create_tree(A)
        self.play(LaggedStart(AnimationGroup(*Anims, group=view, lag_ratio=1, run_time=15),
                              AnimationGroup(Write(title[:8]), Write(title[8:]), group=title, lag_ratio=0.9, run_time=10),
                              lag_ratio=5/15))
        self.wait()

    def create_tree(self, E):
        """
        creates a tree by creating nodes top to bottom then left to right

        Parameters
        ----------
        E : Group
            the tree to build
        """

        Anims = []

        for e in E:
            if isinstance(e, LabeledNode):
                #create the node
                Anims.append(GrowFromCenter(e[1]))
            elif isinstance(e, Text) or isinstance(e, Paragraph):
                #if its a leaf with label
                Anims.append(GrowFromCenter(e[0]))
            elif isinstance(e, Line):
                #if its a line we use Create
                Anims.append(Create(e))
        return Anims
