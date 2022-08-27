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
import pickle

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def elements_in_order(T:Tree)->tuple :
    """
    turns a tree object into manim objects to display to show the same tree,
    in the order they must be when contructed (aka top left to bottom right)

    Also returns the associated plane decomposition

    Parameters
    ----------
    T : Tree
        the tree to translate into manim mobjects

    Returns
    -------
    graph : Group[Mobject]
        the Group containing all the mobjects of the tree
    separation : Group[Mobject]
        the Group containing the axes and the separation lines
    """

    #creating axes
    """the numbers were put manually here, instead of having some level of abstraction, because I used this part only once"""
    axes = Axes(
        x_range=[-0.5, 3.5, 1],
        y_range=[0, 1, 0.5],
        x_length=6,
        y_length = 6,
        x_axis_config={"include_numbers": True, "numbers_to_include": [0, 1, 2, 3]},
        axis_config={"color": WHITE, "exclude_origin_tick":False},
        tips=False
    )

    #editing the y axis manually
    y_pos = [0.3, 0.7]
    y_ticks = ["No", "Yes"]
    y_dict = dict(zip(y_pos, y_ticks))
    axes.add_coordinates(None, y_dict)

    L = tuple() #separation lines

    #sorting the nodes TL-BR
    Nodes = sorted(T.all_nodes, key = lambda t:(t.depth, t.get_pos()[0]))
    k = 1
    G = tuple()

    for n in Nodes :

        #case where the node is either the root of a non-special node
        if isinstance(n, Tree_filled):
            nText = Text(n.label, color=BLACK, font_size=15, z_index=1).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

            #usage of the coordinate_to_point alias to get the position relative to the axis
            sep_line = Line(start=axes.coords_to_point(n.line[0][0], n.line[0][1]), end=axes.coords_to_point(n.line[1][0], n.line[1][1]))
            L += (sep_line,)

        else: #case where the node is a leaf
            G += (Text(f"decision {k}", color=BLACK, font_size=10)\
                  .add_background_rectangle(color=WHITE, opacity=1, buff=0.1)\
                  .move_to([n.get_pos()[0], n.get_pos()[1], 0]),)
            k += 1

        #adding the line from the parent node to the current node
        if n.parent:
            G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0],
                               end=[n.get_pos()[0], n.get_pos()[1], 0],
                               z_index=-1,
                               color=LIGHT_GRAY),) + (G[-1],)

    graph = Group(*G)
    separation = Group(axes, *L)
    #editing the sizes and putting both figures next to each other
    separation.match_height(graph).next_to(graph, LEFT)
    separation.add_updater(lambda m:m.match_height(graph).next_to(graph, LEFT))
    return graph, separation


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

class Scene8bis(MovingCameraScene):
    """
    this scene shows the bijection between a tree and the associated fragmentation of the plane
    """
    def construct(self):
        #creating the tree to display
        T1 = Tree_filled(Tree_empty(), Tree_empty(), 0.5, "y")
        T2 = Tree_filled(T1, Tree_empty(), 1.5, "x", scale=(2,2), xy_ratio=0.6)

        #recovering the mobjects
        G = elements_in_order(T1)

        #editing the nodes
        G0 = LabeledNode(Paragraph("Ever failed", "a class ?",
                                   alignment="center",
                                   font_size=G[0][0].font_size,
                                   color=BLACK)).move_to(G[0]).set_z_index(G[0].z_index, True)
        G0[1].set(fill_color=BLUE_E, color=BLUE_E)
        G2 = LabeledNode(Text("Extra support ?",
                              font_size=G[2][0].font_size,
                              color=BLACK)).move_to(G[2]).set_z_index(G[2].z_index, True)
        G2[1].set(fill_color=BLUE_D, color=BLUE_D)

        G4 = Paragraph("FAIL", "(     74%)", alignment="center", color=BLACK, font_size=int(G[4].font_size * 0.4)) \
            .add_background_rectangle(color=RED_C, opacity=1, buff=0.1) \
            .move_to(G[4])
        G6 = Paragraph("PASS", "(    70%)", alignment="center", color=BLACK, font_size=int(G[6].font_size * 0.4)) \
            .add_background_rectangle(color=GREEN_C, opacity=1, buff=0.1) \
            .move_to(G[6])
        G8 = Paragraph("FAIL", "(    67%)", alignment="center", color=BLACK, font_size=int(G[8].font_size * 0.4)) \
            .add_background_rectangle(color=RED_C, opacity=1, buff=0.1) \
            .move_to(G[8])

        F = Group(G0, G[1], G2, G[3], G4, G[5], G6, G[7], G8)

        #generating the coordinates of the lines in the Tree object
        region = [[-0.5, 0], [3, 1]]
        T2.lines(region)
        #camera setup
        self.camera.frame.move_to(F.get_critical_point(LEFT)+RIGHT*0.2).scale(0.55)
        #create the tree and the plot simultaneously
        F, S = self.create_tree(*elements_in_order(T2))

        # import the data points to display on the plot, together with their colors
        with open('imported_data\scene8bis_data', 'rb') as f:
            x, y, color = pickle.load(f)

        # changing the color stored in "color" to a manim equivalent
        C = []
        for c in color:
            if c == "green":
                C.append(GREEN_E)
            else:
                C.append(RED_D)
        color = C

        # shifting the data as the axes are shifted too to be able to display the 0
        y = ((y - 0.5) / 2) + 0.5
        x += 0.5

        #show the data points
        points = [Dot(point=S[0].c2p(a,b), color=c, radius=0.03) for a,b,c in zip(x,y,color)]
        Anims = [GrowFromCenter(p) for p in points]
        self.play(AnimationGroup(*Anims, group = Group(*points), lag_ratio=0.01))

        #show the association between any leaf and a region of the plan
        #create zones associated with leaves in order TL-BR
        Z1 = Rectangle(height=S[1].height,
                       width=S[2].width,
                       fill_color=RED_C,
                       fill_opacity=0.2,
                       stroke_width=0) \
            .move_to(S[0].c2p(3, 0.5))

        Z2 = Rectangle(height=S[1].height/2,
                       width=S[2].width,
                       fill_color=GREEN_C,
                       fill_opacity=0.2,
                       stroke_width=0) \
            .move_to(S[0].c2p(1, 0.25))

        Z3 = Rectangle(height=S[1].height/2,
                       width=S[2].width,
                       fill_color=RED_C,
                       fill_opacity=0.2,
                       stroke_width=0) \
            .move_to(S[0].c2p(1, 0.75))

        self.play(TransformFromCopy(F[4][0], Z1))
        self.wait()
        self.play(TransformFromCopy(F[6][0], Z2))
        self.wait()
        self.play(TransformFromCopy(F[8][0], Z3))
        self.wait(3)

        #fadeout eveything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])

    def create_tree(self, E:Group, S:Group):
        """
        function that animates the creation of the tree together with the separation of the plane

        Parameters
        ----------
        E : Group
            the mobjects of the tree to create progressively
        S : Group
            the Group with the axis and the lines to build
        """

        #adding label on the axis
        x_label = S[0].get_x_axis_label(Tex("classes failed", font_size=17),
                                        edge=DOWN,
                                        direction=DOWN,
                                        buff=0.1)
        y_label = S[0].get_y_axis_label(
            Tex("tutoring", font_size=17).rotate(-90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.5)

        #modifiying the NumberLine mobject to display a tick at the origin
        S[0].get_axes()[0].become(NumberLine(x_range=[-0.5, 3.5, 1],
                                             length=7,
                                             color=WHITE,
                                             include_numbers=True,
                                             numbers_to_include=[0, 1, 2, 3])\
        .move_to(S[0].get_axes()[0])\
        .match_width(S[0].get_axes()[0]))

        #shifting the y axis to be able to plot points at x=0 without overlapping
        S[0].get_axes()[1].move_to([S[0].get_axes()[0].points[0][0]-S[0].get_axes()[1].width/2+0.04 , S[0].get_axes()[1].get_y(), 0])
        S[0].set(color=LIGHT_GRAY).set_z_index(2, True)

        #animate the creation of the axis
        self.play(Create(S[0]), Create(x_label), Create(y_label))
        self.wait(1)
        k = 1

        for e in E:
            if isinstance(e, LabeledNode): #if the node is associated to a separation
                #create the line
                self.play(Create(S[k]))

                #orientation of the movement to give to the line wobbling
                if S[k].width > S[k].height:
                    direction = UP
                else:
                    direction = LEFT

                #make the line wooble around before siting on the right value
                self.play(S[k].animate.shift(direction), rate_func=wiggle, run_time=3)
                #create the correcponding node
                self.play(AnimationGroup(FadeIn(e[1]), Write(e[0]), lag_ratio=0.4))
                k += 1
            elif isinstance(e, Text) or isinstance(e, Paragraph): #leaf node
                anims = [FadeIn(e[0]), Write(e[1]), Write(e[2])]
                self.play(AnimationGroup(*anims, group=e, lag_ratio=0.4))
            elif isinstance(e, Line):
                #create a line between to nodes

                if e.start[0] < e.end[0]: #check first if the lines goes left or right
                    #if the direction is right, the label is "yes"
                    self.play(Create(e), Write(add_yes_no(e, "yes", font_size=int(0.7 * Q[0][0].font_size))))
                else:
                    #otherwise, the label is "no"
                    self.play(Create(e), Write(add_yes_no(e, "no", font_size=int(0.7 * Q[0][0].font_size))))
        return E, S