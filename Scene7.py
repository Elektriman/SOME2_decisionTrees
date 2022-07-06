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
                sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]))
                L += (sep_line,)

        else: #cas où le noeud est une feuille
            G += (Dot(point=[n.get_pos()[0], n.get_pos()[1], 0]).set(width=0.15, color=BLUE),)

        # ajout de la ligne qui va du parent à l'actuel noeud
        if n.parent:
            if isinstance(n, Tree_filled):
                G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0], end=G[-1].get_critical_point(UP), z_index=-1),) + (G[-1],)
            else:
                G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0], end=[n.get_pos()[0], n.get_pos()[1], 0], z_index=-1),) + (G[-1],)

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

class Scene7(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        #graphes

        vertices1 = [i for i in range(6)]
        vertices1b = [i for i in range(6,12)]

        edges1 = [(0,1), (1,2), (1,3), (2,3), (3,4), (3,5), (0,5)]
        edges1b = [(6,7), (7,8), (8,9), (7,9), (9,10), (9,11)]

        layout1 = {0:[0,0,0], 1:[-1,-1,0], 2:[-2,-1.1,0], 3:[-1.1, -2, 0],
                  4:[-2.1, -3, 0], 5:[0.3, -2.7, 0]}
        layout1b = {6:[1.5, 0.1, 0], 7:[3, -0.3, 0], 8:[4, -1.5, 0],
                    9:[2.5, -1.6, 0], 10:[1.6, -2.3, 0], 11:[3.5, -2.4, 0]}

        dot_conf = {"fill_color":BLUE, "radius":0.2}
        vc1 = {i:dot_conf for i in range(6)}
        vc1b = {i: dot_conf for i in range(6,12)}

        G1 = Graph(vertices1, edges1, layout=layout1, vertex_config=vc1)
        G1b = Graph(vertices1b, edges1b, layout=layout1b, vertex_config=vc1b)

        T1 = Tree_filled(Tree_empty(), Tree_empty(), 0.5, "x")
        T1.label = "X[5] <= 1.5\ngini = 0.481\nsamples = 316\nvalue = [127, 189]"
        T2 = Tree_filled(T1, Tree_empty(), 1.5, "x", scale=3, xy_ratio=0.5)
        T2.label = "X[31] <= 0.5\ngini = 0.453\nsamples = 286\nvalue = [99, 187]"

        #animation

        self.camera.frame.move_to(Group(G1,G1b)).scale(0.7)

        #creation
        self.play(Create(G1), Create(G1b))
        self.wait(2)

        #retirer les parties non connexes
        self.play(FadeOut(G1b))
        self.play(self.camera.frame.animate.scale(0.8).move_to(G1))
        self.wait(2)

        #retirer les cycles
        self.play(G1.animate.remove_edges((2,3), (3,5)))
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN*0.1),
                  G1.animate.add_edges((2,6),(5,7), positions={6:[-2.5, -1.9, 0], 7:[-0.5, -3.5, 0]},
                                       vertex_config={6:dot_conf, 7:dot_conf}))
        self.wait(2)

        #mise sous forme d'arbre
        self.play(G1.animate.remove_edges((2,6), (3,4), (5,7)), G1.animate.remove_vertices(6,4,7))
        camera_follow= lambda c: c.move_to(G1)
        self.camera.frame.add_updater(camera_follow)
        self.play(G1.animate.change_layout("tree", root_vertex=0).flip(), self.camera.frame.animate.scale(1.1))
        self.camera.frame.remove_updater(camera_follow)
        self.wait(2)

        #transformation en arbre CART
        G_copy = [g for g in G1]
        Graph_group = Group(G_copy[0], G_copy[5], G_copy[1], G_copy[8], G_copy[4], G_copy[6], G_copy[2], G_copy[7], G_copy[3])

        E = elements_in_order(T2)
        E.scale_to_fit_width(G1.width*1.5)
        E.move_to(G1)
        for e in E :
            if isinstance(e, Dot):
                e.set(width=0.3)

        A = tuple(Transform(Graph_group[i], E[i]) for i in range(9))
        self.play(AnimationGroup(*A))
        self.play(Write(E[0][0]), Write(E[2][0]))
        self.wait(2)



    def create_tree(self, T, region=None):
        if region :
            # création des éléments à animer
            E, S = elements_in_order(T, region=region)
            # ajout de labels sur l'axe
            labels = S[0].get_axis_labels(Tex("x"), Text("y").scale(0.7))
            self.play(Create(S[0]), Create(labels))  # création du repère
        else :
            E = elements_in_order(T)

        # réorganisation
        E.scale(2).shift(2 * RIGHT + UP)
        if region :
            S.update()
            k = 1

        for e in E:
            if isinstance(e, LabeledNode):
                # si le noeud est associé à une séparation, on crée en même temps la ligne correspondante
                if region :
                    anims = (Create(e), Create(S[k]),)
                    k += 1
                else :
                    anims = (Create(e),)
            elif isinstance(e, Dot):
                # si le noeud est une feuille, on effectue GrowFromCenter
                anims = (GrowFromCenter(e),)
            else:
                # si on trace une ligne entre deux noeuds, on utilise Create
                anims = (Create(e),)

            self.play(AnimationGroup(*anims), run_time=0.5)