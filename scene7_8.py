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
import numpy as np

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
        dy = abs(region[0][1] - region[1][1]) / 10

        axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[0, 1, 0.5],
            x_length=6,  # ajustement de la taille originale, peut être modifié ultérieurement
            y_length = 6,
            x_axis_config={"include_numbers": True, "numbers_to_include": [0, 1, 2, 3]},
            axis_config={"color": GREEN, "exclude_origin_tick":False},
            tips=False
        )

        y_pos = [0.3, 0.7]
        y_ticks = ["No", "Yes"]
        y_dict = dict(zip(y_pos, y_ticks))
        axes.add_coordinates(None, y_dict)
        L = tuple() #liste des lignes de séparations

    #tri des noeuds du moins profond au plus profond, puis de gauche à droite
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.get_pos()[0]))

    for n in Nodes :

        #ajout du noeud
        if isinstance(n, Tree_filled): #cas où le noeud contient de l'écriture
            nText = Text(n.label, color=BLACK, font_size=15, z_index=1).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

            # le noeud décrit une séparation des données donc on ajoute la ligne de séparation correspondante dans la bonne liste
            if region :
                #on utilise coord_to_point pour avoir la position relative au repère créé plus tôt.
                sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]), color=YELLOW)
                L += (sep_line,)

        else: #cas où le noeud est une feuille
            G += (Dot(point=[n.get_pos()[0], n.get_pos()[1], 0]).set(width=0.3, color=WHITE),)

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

def path_along_line(line:Line, start_point, end_point, exit_node, entry_node):
    P = VMobject()
    P.points = np.array([start_point.get_center()])
    P.add_cubic_bezier_curve_to(start_point.get_center(), exit_node.get_center(), line.get_center())
    P.add_cubic_bezier_curve_to(line.get_center(), entry_node.get_center(), end_point.get_center())
    return P

def add_yes_no(line, text, font_size=15):
    def x_updater(m, line, direction):
        m.move_to(line).shift(0.5 * direction)

    if text=="yes" :
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).shift(0.5 * RIGHT)
        txt.add_updater(lambda m: x_updater(m, line, RIGHT))
    else :
        txt = Text("no", color=WHITE, font_size=font_size).move_to(line).shift(0.5 * LEFT)
        txt.add_updater(lambda m:x_updater(m, line, LEFT))

    return txt

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene7_8(MovingCameraScene):
    def construct(self):
        E, T, YN = self.scene7()
        self.scene8(E, T, YN)

    def scene7(self):
        self.camera.frame.save_state()

        # graphes

        vertices1 = [i for i in range(6)]
        vertices1b = [i for i in range(6, 12)]

        edges1 = [(0, 1), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (0, 5)]
        edges1b = [(6, 7), (7, 8), (8, 9), (7, 9), (9, 10), (9, 11)]

        layout1 = {0: [0, 0, 0], 1: [-1, -1, 0], 2: [-2, -1.1, 0], 3: [-1.1, -2, 0],
                   4: [-2.1, -3, 0], 5: [0.3, -2.7, 0]}
        layout1b = {6: [1.5, 0.1, 0], 7: [3, -0.3, 0], 8: [4, -1.5, 0],
                    9: [2.5, -1.6, 0], 10: [1.6, -2.3, 0], 11: [3.5, -2.4, 0]}

        dot_conf = {"fill_color": WHITE, "radius": 0.2}
        edge_conf = {"color": LIGHT_GRAY}
        vc1 = {i: dot_conf for i in range(6)}
        vc1b = {i: dot_conf for i in range(6, 12)}

        G1 = Graph(vertices1, edges1, layout=layout1, vertex_config=vc1, edge_config=edge_conf)
        G1b = Graph(vertices1b, edges1b, layout=layout1b, vertex_config=vc1b, edge_config=edge_conf)

        T1 = Tree_filled(Tree_empty(), Tree_empty(), 0.5, "y")
        T1.label = "Tutoring ?"
        T2 = Tree_filled(Tree_empty(), T1, 1.5, "x", scale=3, xy_ratio=0.5)
        T2.label = "# of past class failed ≤ 1 ?"

        # animation

        self.camera.frame.move_to(Group(G1, G1b)).scale(0.7)

        # creation
        self.play(Create(G1), Create(G1b))
        self.wait(2)

        # retirer les parties non connexes
        self.play(FadeOut(G1b))
        self.play(self.camera.frame.animate.scale(0.8).move_to(G1))
        self.wait(2)

        # retirer les cycles
        self.play(G1.animate.remove_edges((2, 3), (3, 5)))
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN * 0.1),
                  G1.animate.add_edges((2, 6), (5, 7), positions={6: [-2.5, -1.9, 0], 7: [-0.5, -3.5, 0]},
                                       vertex_config={6: dot_conf, 7: dot_conf}))
        self.wait(2)

        # mise sous forme d'arbre
        self.play(G1.animate.remove_edges((2, 6), (3, 4), (5, 7)), G1.animate.remove_vertices(6, 4, 7))
        camera_follow = lambda c: c.move_to(G1)
        self.camera.frame.add_updater(camera_follow)
        self.play(G1.animate.change_layout("tree", root_vertex=0), self.camera.frame.animate.scale(1.1))
        self.camera.frame.remove_updater(camera_follow)
        self.wait(2)

        # transformation en arbre CART
        Graph_group = Group(G1.submobjects[0], G1.submobjects[8], G1.submobjects[4], G1.submobjects[5],
                            G1.submobjects[1], G1.submobjects[7], G1.submobjects[3], G1.submobjects[6],
                            G1.submobjects[2])

        E = elements_in_order(T2)
        E.scale_to_fit_width(G1.width * 1.5)
        E.move_to(G1)

        self.play(Transform(Graph_group, E))
        self.remove(Graph_group)
        self.add(E)
        txt_yes = add_yes_no(E[3], "yes", font_size=1.5*E[0][0].font_size//2)
        txt_no = add_yes_no(E[1], "no", font_size=1.5*E[0][0].font_size//2)
        txt_yes2 = add_yes_no(E[7], "yes", font_size=1.5*E[0][0].font_size//2)
        txt_no2 = add_yes_no(E[5], "no", font_size=1.5*E[0][0].font_size//2)
        YN = Group(txt_yes, txt_no, txt_yes2, txt_no2)
        self.play(Write(E[0][0]), Write(E[4][0]), Write(txt_yes), Write(txt_no), Write(txt_yes2), Write(txt_no2))
        self.wait(2)

        return E, T2, YN

    def scene8(self, E, tree, YN):

        #point qui se balade
        Girl = ImageMobject("img/girl.png", z_index=2).move_to(E[0]).shift(1.3*LEFT*E[0].width/2).scale_to_fit_height(E[0].height*1.5)
        self.play(FadeIn(Girl))
        K = Dot(z_index=2).next_to(E[4], LEFT)
        self.play(MoveAlongPath(Girl, path_along_line(E[3], Girl, K, E[0], E[4])), run_time=4)
        self.wait(3)
        L = Dot(z_index=2).move_to(E[8])
        self.play(MoveAlongPath(Girl, path_along_line(E[7], Girl, L, E[4], E[8])), run_time=3)
        self.wait(3)

        self.play(FadeOut(Girl), FadeOut(E), FadeOut(YN))
        self.play(self.camera.frame.animate.shift(1.7*LEFT+1.2*DOWN))

        region = [[0, 0], [3, 1]]
        tree.lines(region)
        self.create_tree(tree, region)

    """
    fonction create tree
    """
    def create_tree(self, T, region=None):
        if region :
            # création des éléments à animer
            E, S = elements_in_order(T, region=region)
            # ajout de labels sur l'axe
            x_label = S[0].get_x_axis_label(Tex("class failed", font_size=17), edge=DOWN, direction=DOWN, buff=0.1)
            y_label = S[0].get_y_axis_label(
                Tex("tutoring", font_size=17).rotate(90 * DEGREES),
                edge=LEFT,
                direction=LEFT,
                buff=0.5,
            )
            S[0].get_axes()[1].shift(LEFT*0.38)
            S[0].get_axes()[0].become(NumberLine(x_range=[-0.5, 3.5, 1],
                                                 length=7,
                                                 color=GREEN,
                                                 include_numbers=True,
                                                 numbers_to_include=[0,1,2,3]).move_to(S[0].get_axes()[0]).match_width(S[0].get_axes()[0]))
            self.play(Create(S[0]), Create(x_label), Create(y_label))
            # création du repère
            self.wait(1)
        else :
            E = elements_in_order(T)

        if region :
            k = 1

        for e in E:
            if isinstance(e, LabeledNode):
                # si le noeud est associé à une séparation, on crée en même temps la ligne correspondante
                if region :
                    self.play(Create(S[k]))
                    if S[k].width > S[k].height :
                        direction = UP
                    else :
                        direction = LEFT

                    self.play(S[k].animate.shift(direction), rate_func=wiggle, run_time=3)
                    self.play(Create(e))
                    k += 1
                else :
                    self.play(Create(e))
            elif isinstance(e, Dot):
                # si le noeud est une feuille, on effectue GrowFromCenter
                self.play(GrowFromCenter(e))
            else:
                # si on trace une ligne entre deux noeuds, on utilise Create
                if e.start[0] < e.end[0] :
                    self.play(Create(e), Write(add_yes_no(e, "yes")))
                else :
                    self.play(Create(e), Write(add_yes_no(e, "no")))