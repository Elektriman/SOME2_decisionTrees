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

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def elements_in_order(T:Tree)->Group :
    """
    turns a tree object into manim objects to display to show the same tree,
    in the order they must be when contructed (aka top left to bottom right)

    Parameters
    ----------
    T : Tree
        the tree to translate into manim mobjects

    Returns
    -------
    graph : Group[Mobject]
        the Group containing all the mobjects of the tree
    """
    G = tuple()

    #sorting the nodes TL-BR
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.get_pos()[0]))
    k = 1

    for n in Nodes :

        #case where the node is either the root or a non-special node
        if isinstance(n, Tree_filled):
            nText = Text(n.label, color=BLACK, font_size=15, z_index=3).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

        else: #case the the node is a leaf
            G += (Text(f"decis ion {k}", color=BLACK, font_size=10)\
                  .add_background_rectangle(color=WHITE, opacity=1, buff=0.1)\
                  .move_to([n.get_pos()[0], n.get_pos()[1], 0])\
                  .set_z_index(3, True),)
            k += 1

        #adding the line from the parent node to the current node
        if n.parent:
            G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0],
                               end=[n.get_pos()[0], n.get_pos()[1], 0],
                               z_index=0,
                               color=LIGHT_GRAY),) + (G[-1],)

    return Group(*G)

def add_yes_no(line:Line, text:str, font_size:int=15)->Text:
    """
    generates a "yes" or "no" label next to a line in the tree

    Parameters
    ----------
    line : Line
        the line next to which display the label
    text : "yes" or "no"
        the label to display, eithe
    font_size : int
        font size parameter to enable better modeling

    Returns
    -------
    Text Mobject
        the mobject ready to be displayed
    """
    #position updater to stick to the line if it moves
    def x_updater(m, line, direction):
        m.move_to(line).shift(0.5 * direction)

    if text=="yes" :
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).shift(0.5 * RIGHT)
        txt.add_updater(lambda m: x_updater(m, line, RIGHT))
    elif text=="no" :
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).shift(0.5 * LEFT)
        txt.add_updater(lambda m:x_updater(m, line, LEFT))
    else :
        raise ValueError('bad argument for "text" : can be only "yes" or "no"')

    return txt

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene7_8(MovingCameraScene):
    def construct(self):
        #scenes 7 and 8 have common components so they must be built in the same piece of code
        E = self.scene7()
        self.scene8(E)

    def scene7(self):
        """
        the process of making a tree from a graph
        """

        #creating the initial graph
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

        #creating the tree resulting of all the transformations of the graph
        T1 = Tree_filled(Tree_empty(), Tree_empty(), 0)
        T1.label = "Rule 2"
        T2 = Tree_filled(T1, Tree_empty(), 0, scale=(2,2), xy_ratio=0.6)
        T2.label = "Rule 1"

        E = elements_in_order(T1)
        E[0][1].set(fill_color=BLUE, color=BLUE)
        E[2][1].set(fill_color=BLUE, color=BLUE)
        E[4][0].set(fill_color=GREEN)
        E[6][0].set(fill_color=GREEN)
        E[8][0].set(fill_color=GREEN)

        #camera setup
        self.camera.frame.move_to(Group(G1, G1b)).scale(0.7)

        #create the graph
        self.play(Create(G1), Create(G1b))
        self.wait(2)

        #remove the non connected part
        self.play(FadeOut(G1b))
        self.play(self.camera.frame.animate.scale(0.8).move_to(G1))
        self.wait(2)

        #z_index acting badly so it must be set manually
        for i in range(6):
            G1.submobjects[i].set_z_index(3)
        for i in range(6, len(G1.submobjects)):
            G1.submobjects[i].set_z_index(0)

        #showing where are the cycles
        self.play(LaggedStart(*[Indicate(G1.submobjects[i], scale_factor=1) for i in [1, 7, 2, 9, 3, 8]], lag_ratio=1/3))
        self.wait()
        self.play(LaggedStart(*[Indicate(G1.submobjects[i], scale_factor=1) for i in [0, 6, 1, 8, 3, 11, 5, 12]], lag_ratio=1/4))
        self.wait()

        #remove the cycles
        self.play(G1.animate.remove_edges((2, 3), (3, 5)))
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN * 0.1),
                  G1.animate.add_edges((2, 6), (5, 7),
                                       positions={6: [-2.5, -1.9, 0], 7: [-0.5, -3.5, 0]},
                                       vertex_config={6: dot_conf, 7: dot_conf}))
        self.wait(2)

        #remove the parts of the graph that are not corresponding to the future tree
        self.play(G1.animate.remove_edges((2, 6), (3, 4), (5, 7)), G1.animate.remove_vertices(6, 4, 7))

        #adding an updater for the camera to follow the mobject being transformed
        camera_follow = lambda c: c.move_to(G1)
        self.camera.frame.add_updater(camera_follow)

        #change the layout of the graph to make it look like a tree
        G2 = G1.copy().change_layout("tree", root_vertex=0).flip()
        self.play(G1.animate.become(G2), self.camera.frame.animate.scale(1.1))
        self.camera.frame.remove_updater(camera_follow)
        self.wait(2)

        self.play(G1[1].animate.set_color(BLUE_D))

        #showing that one non-special node has 3 edges only
        l1 = G1.submobjects[5].copy().set_z_index(1).set_color(YELLOW)
        l2 = G1.submobjects[6].copy().set_z_index(1).set_color(YELLOW)
        l3 = G1.submobjects[7].copy().set_z_index(1).set_color(YELLOW)
        l1.put_start_and_end_on(start=G1[1].get_center(), end=G1[0].get_center())

        self.play(Create(l1), Create(l2), Create(l3))
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(l3))
        self.wait()

        #labeling the important types of nodes
        root_label = Text("Root", color=BLUE_E, font_size=20).next_to(G1[0])
        leaf_label = Text("Leaf", color=GREEN_C, font_size=20).next_to(G1[5])

        self.play(G1[0].animate.set_color(BLUE_E), Write(root_label))
        self.wait()
        self.play(G1[2].animate.set_color(GREEN_C),
                  G1[3].animate.set_color(GREEN_C),
                  G1[5].animate.set_color(GREEN_C),
                  Write(leaf_label))
        self.wait()
        self.play(FadeOut(root_label), FadeOut(leaf_label))
        self.wait(2)

        """transformation into a tree with rules"""

        #reorganising the elements of G1 to match the organisation in E
        Graph_group = Group(G1.submobjects[0], G1.submobjects[5], G1.submobjects[1], G1.submobjects[8],
                            G1.submobjects[4], G1.submobjects[6], G1.submobjects[2], G1.submobjects[7],
                            G1.submobjects[3])

        #repositionning E
        E.scale_to_fit_height(G1.height)
        E.move_to(G1)
        #matching z_indexes and colours
        E[0][0].set_z_index(3, True)
        E[0][1].set_fill_color(BLUE_E).set_color(BLUE_E)
        E[2][0].set_z_index(3, True)
        E[2][1].set_fill_color(BLUE_D).set_color(BLUE_D)

        #transforming the graph
        Anims = [Transform(Graph_group[i], E[i]) for i in range(9)]
        #remake some animations that are not as intended
        Anims[4] = Transform(Graph_group[4], E[4].submobjects[0])
        Anims[6] = Transform(Graph_group[6], E[6].submobjects[0])
        Anims[8] = Transform(Graph_group[8], E[8].submobjects[0])
        self.play(*Anims)

        #adding "yes" and "no" texts to the branches
        txt_yes = add_yes_no(E[3], "yes", font_size=1.5*E[0][0].font_size//2)
        txt_no = add_yes_no(E[1], "no", font_size=1.5*E[0][0].font_size//2)
        txt_yes2 = add_yes_no(E[7], "yes", font_size=1.5*E[0][0].font_size//2)
        txt_no2 = add_yes_no(E[5], "no", font_size=1.5*E[0][0].font_size//2)

        #writing the rules of the nodes and the leaves
        Anims = [Write(E[0][0]), Write(txt_no), Write(E[2][0]), Write(txt_yes),
                 Write(E[4]), Write(txt_no2), Write(E[6]), Write(txt_yes2), Write(E[8])]
        self.play(AnimationGroup(*Anims, group=E, lag_ratio=1))
        self.wait(2)
        self.add(E)
        self.remove(G1)

        #remaking the nodes for a special case example
        E0 = LabeledNode(Paragraph("Ever failed", "a class ?",
                                   alignment="center",
                                   font_size=E[0][0].font_size,
                                   color=E[0][0].color)).move_to(E[0])
        E0[1].set(fill_color=BLUE_E, color=BLUE_E)
        E2 = LabeledNode(Text("Extra support ?",
                              font_size=E[2][0].font_size,
                              color=E[2][0].color)).move_to(E[2])
        E2[1].set(fill_color=BLUE_D, color=BLUE_D)
        E4 = Paragraph("FAIL", "(     74%)",
                       alignment="center",
                       color=BLACK,
                       font_size=int(E[4].font_size*0.4)) \
            .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
            .move_to(E[4])
        E6 = Paragraph("PASS", "(    70%)",
                       alignment="center",
                       color=BLACK,
                       font_size=int(E[6].font_size*0.4)) \
            .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
            .move_to(E[6])
        E8 = Paragraph("FAIL", "(    67%)",
                       alignment="center",
                       color=BLACK,
                       font_size=int(E[8].font_size*0.4)) \
            .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
            .move_to(E[8])

        start = [E[i] for i in [0, 2, 4, 6, 8]]
        end = [E0, E2, E4, E6, E8]

        for i in range(0, 2):
            self.play(Transform(start[i], end[i]))
        self.wait(2)
        for i in range(2, len(start)):
            self.play(Transform(start[i], end[i]))
        self.wait(4)

        #end of scene7, passing elements to scene8
        return E

    def scene8(self, E):
        """
        an example of the way a tree must be read
        """

        #adding an icon that represents one data element
        Alice = Text("Alice", color=WHITE, font_size=15).next_to(E[0], UP, buff=1).scale(2)
        Girl = Dot(radius=0.2, z_index=3, stroke_width=3, color=LIGHTER_GRAY, fill_color=WHITE).next_to(Alice, RIGHT)

        #camera setup
        self.play(self.camera.frame.animate.scale(1.4).shift(UP*0.7))

        #adding the girl
        self.play(GrowFromCenter(Girl), Write(Alice))
        self.wait(2)

        #starting the navigation inside the tree by starting at the root
        self.play(Girl.animate.move_to(E[0]))
        self.wait()

        #answer to the first uestion in no : go to the left node "tutoring ?"
        self.play(MoveAlongPath(Girl, E[1]), run_time=3)
        self.wait()

        #answer to the second question is no : go to the left leaf
        self.play(MoveAlongPath(Girl, E[5]), self.camera.frame.animate.shift(DOWN*0.4), run_time=3)

        #move the point out of the way
        self.play(Girl.animate.next_to(E[6], DOWN, buff=0.1))

        #transform the circle into a square to symbolise a prediction, and turn it green to symbolise passing the class
        Girl_sq = Square(0.4, z_index=3, stroke_width=2, fill_color=GREEN_E, fill_opacity=1.).move_to(Girl)
        self.wait()
        self.play(Girl.animate.become(Girl_sq))
        self.wait(4)

        #fade out everything, end of scene8
        self.play(*tuple(FadeOut(m) for m in self.mobjects))