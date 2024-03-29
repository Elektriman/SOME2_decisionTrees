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
import random

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def elements_in_order(T: Tree, label_leaves: bool = False) -> Group:
    """
    turns a tree object into manim objects to display to show the same tree,
    in the order they must be when contructed (aka top left to bottom right)

    Parameters
    ----------
    T : Tree
        the tree to translate into manim mobjects
    label_leaves : bool
        wether or not to put labels on the leaves

    Returns
    -------
    graph : Group[Mobject]
        the Group containing all the mobjects of the tree
    """
    G = tuple()

    # sorting the nodes TL-BR
    Nodes = sorted(T.all_nodes, key=lambda t: (t.depth, t.get_pos()[0]))
    k = 1

    for n in Nodes :

        #case where the node is either the root or a non-special node
        if isinstance(n, Tree_filled):
            nText = Text(n.label, color=BLACK, font_size=15, z_index=1).move_to([n.get_pos()[0], n.get_pos()[1], 0])
            G += (LabeledNode(nText),)

        else: #case the the node is a leaf
            if label_leaves :
                G += (Text(f"decision {k}", color=BLACK, font_size=10)\
                      .add_background_rectangle(color=WHITE, opacity=1, buff=0.1)\
                      .move_to([n.get_pos()[0], n.get_pos()[1], 0]),)
                k += 1
            else :
                G += (Dot(point=[n.get_pos()[0], n.get_pos()[1], 0]).set(width=0.3, color=WHITE),)

        #adding the line from the parent node to the current node
        if n.parent:
            G = G[:-1] + (Line(start=[n.parent.get_pos()[0], n.parent.get_pos()[1], 0],
                               end=[n.get_pos()[0], n.get_pos()[1], 0],
                               z_index=-1,
                               color=LIGHT_GRAY),) + (G[-1],)

    return Group(*G)


def add_yes_no(line: Line, text: str, font_size: int = 15) -> Text:
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

    # position updater to stick to the line if it moves
    def x_updater(m, line, direction):
        m.move_to(line).shift(0.5 * direction)

    if text == "yes":
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).shift(0.5 * RIGHT)
        txt.add_updater(lambda m: x_updater(m, line, RIGHT))
    elif text == "no":
        txt = Text(text, color=WHITE, font_size=font_size).move_to(line).shift(0.5 * LEFT)
        txt.add_updater(lambda m: x_updater(m, line, LEFT))
    else:
        raise ValueError('bad argument for "text" : can be only "yes" or "no"')

    return txt


def remake_node(old_node: Mobject, *text: str, color = BLUE_C) -> Mobject:
    """
    a function that will copy parameters from old node and apply a new text and color to return a new node

    Parameters
    ----------
    old_node : Mobject
        any node from the tree, either standard node or root, but not leaf
    text : str
        the text that will be put inside the new node
    color : Color
        (default:Blue_C, optionnal) if the color needs to be changed, pass the new color in this argument

    Returns
    -------
    Mobject
        the new node mobject
    """
    N = LabeledNode(Paragraph(*text,
                              alignment="center",
                              font_size=old_node[0].font_size,  # copy font size
                              color=BLACK))\
        .move_to(old_node) # copy position
    N[0].set_z_index(3, True)
    N[1].set(fill_color=color, color=color, z_index=1)  # set the color and z_index
    return N

def remake_leaf(old_leaf: Mobject, *text: str) -> Mobject:
    """
    remake a leaf node

    Parameters
    ----------
    old_leaf : Mobject
        the old leaf to modify
    text : str
        if we want to add text to the node

    Returns
    -------
    Mobject
        the new leaf node mobject
    """
    # we use paragraph to be able to put text on two lines
    return Paragraph(*text,
                     alignment="center",
                     color=BLACK,
                     font_size=int(old_leaf.font_size * 0.4)) \
        .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
        .move_to(old_leaf)
    # copy font size and position

def path_along_line(line: Line,
                    start_point: Dot,
                    end_point: Dot,
                    exit_node: Mobject,
                    entry_node: Mobject
                    ) -> VMobject :
    """
    returns a Bezier curve that a point going from one node to another should follow

    Parameters
    ----------
    line : Line
        the line between the two nodes
    start_point : Dot
        the point where the dot is now
    end_point : Mobject
        the target point
    exit_node : Mobject
        the node to exit
    entry_node : Mobject
        the arrival node
    Returns
    -------
    VMobject
        the path the point should follow
    """
    P = VMobject()
    P.points = np.array([start_point.get_center()]) #the points will go throught the middle of the line
    # each bezier curve goes from either start or end point to the line middle,
    # with the center of the local node as both anchors
    P.add_cubic_bezier_curve_to(start_point.get_center(), exit_node.get_center(), line.get_center())
    P.add_cubic_bezier_curve_to(line.get_center(), entry_node.get_center(), end_point.get_center())
    return P

def random_placement(D:Group, node:Mobject)->list[list[float, float, float]]:
    """
    gives a random (normal distribution) position for each point is the collection D

    Parameters
    ----------
    D : Group
        the collection of dots to rearrange
    node
        the node where the points should be randomly dispersed

    Returns
    -------
    list[positions]
        the list of the positions attributed to the dots
    """
    res = []
    for d in D :
        res.append(node.get_center()+np.array([random.normalvariate(0, 1)*node.width*0.1,
                                               random.normalvariate(0, 1)*node.height*0.1,
                                               0]))
    return res

#      _       __ _       _ _   _
#     | |     / _(_)     (_) | (_)
#   __| | ___| |_ _ _ __  _| |_ _  ___  _ __  ___
#  / _` |/ _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
# | (_| |  __/ | | | | | | | |_| | (_) | | | \__ \
#  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/

def treeA() -> Group :
    #create the tree
    T0 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")

    T2 = Tree_filled(T0, Tree_empty(), 0, "x")
    T3 = Tree_filled(T1, Tree_empty(), 0, "x")
    T4 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")

    T5 = Tree_filled(T2, Tree_empty(), 0, "x")
    T6 = Tree_filled(T3, T4, 0, "x")

    T7 = Tree_filled(T5, T6, 0, "x", scale=(1.5,1), xy_ratio=1.2)

    G = elements_in_order(T7, label_leaves=True)

    #remake the nodes
    L24 = remake_node(G[24], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L26 = remake_node(G[26], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L28 = remake_node(G[28], "XXXX", color=RED_B, cr=0).scale(0.6)
    L30 = remake_node(G[30], "XXXX", color=GREEN_B, cr=0).scale(0.6)
    L32 = remake_node(G[32], "XXXX", color=RED_B, cr=0).scale(0.6)

    G14 = remake_node(G[14], "XXXXX", color=BLUE_E).scale(0.7)
    G18 = remake_node(G[18], "XXXXX", color=BLUE_E).scale(0.7)
    L16 = remake_node(G[16], "XXXXX", color=RED_B, cr=0).scale(0.7)
    L20 = remake_node(G[20], "XXXXX", color=GREEN_B, cr=0).scale(0.7)
    L22 = remake_node(G[22], "XXXXX", color=RED_B, cr=0).scale(0.7)

    G6 = remake_node(G[6], "XXXXXX", color=RED_B, cr=0).scale(0.8)
    G10 = remake_node(G[10], "XXXXXX", color=GREEN_B, cr=0).scale(0.8)
    G12 = remake_node(G[12], "XXXXXX", color=RED_B, cr=0).scale(0.8)
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

class Scene17bis(MovingCameraScene):
    """
    shorter version of the scene17, where we stop at depth 2 regardless of the purity of the nodes
    """
    def construct(self):
        # create tree
        A = treeA()

        # at position n is the parent of A[n]
        parents = [None, None, A[0], None, A[0], None, A[2], None, A[2], None, A[4], None, A[4], None, A[6], None, A[6],
                   None, A[10], None, A[10], None, A[12], None, A[12], None, A[14], None, A[14], None, A[18], None,
                   A[18], None]

        # adding data points
        colours = [GREEN_E] * 37 + [RED_E] * 27
        Z_index = [i + 1 for i in range(len(colours))]

        # setting the seed for the random package
        random.seed(69420)
        random.shuffle(Z_index)

        # create the collection of dots
        D = Group(*[Dot(color=colours[i], z_index=Z_index[i], radius=0.05) for i in range(len(colours))])\
            .arrange_in_grid(4, 16,buff=0.05) \
            .next_to(A[0], UP) \
            .add_background_rectangle(fill_color=rgb_to_color((50 / 255,) * 3, ), buff=0.02)

        # place the dots in random positions inside the root node
        P0 = random_placement(D, A[0])
        for (d, p) in zip(D, P0):
            d.move_to(p)

        # extract the background rectangle
        R = D.submobjects[0].copy()
        D.submobjects = D.submobjects[1:]

        # camera setup
        self.camera.frame.move_to(Group(D, A[0])).match_width(Group(D, A[0])).scale(3)

        # initial creation
        self.play(DrawBorderThenFill(A[0][1]))
        self.play(AnimationGroup(*[GrowFromCenter(d) for d in D], group=D, lag_ratio=0.01))
        self.wait()

        """LEVEL 1"""

        N = [2, 4]  # nodes that will recieve new points
        # dictionnary of the distribution of the data points.
        # key->index of the node in A, value->list of the indexes of the points that will go to the node given by the key
        separation = {2: [i for i in range(15)] + [i for i in range(37, 52)],
                      4: [i for i in range(15, 37)] + [i for i in range(52, 64)]}

        Anims = []
        for k, v in separation.items():
            new_pos = random_placement([D[i] for i in v], A[k]) # compute new positions in the new node
            for i, p in zip(v, new_pos):
                # add the animation moving along a smooth path for each point
                Anims.append(MoveAlongPath(D[i], path_along_line(A[k - 1],
                                                                 D[i],
                                                                 D[i].copy().move_to(p),
                                                                 parents[k],
                                                                 A[k])))

        # mix up the order of the animations so that we don't get the green dot moving and the the red ones
        # but rather a mix of both colors moving together
        random.shuffle(Anims)

        # move camera to view
        view = Group(*A[:5])  # camera view
        self.play(self.camera.frame.animate.move_to(view).match_width(view).scale(1.2))

        self.play(
            *[Create(A[i]) for i in [n - 1 for n in N]]) # create the lines from the parent node to the child nodes
        self.play(AnimationGroup(*Anims, group=D, lag_ratio=0.02)) # move the dots
        self.play(*[DrawBorderThenFill(A[i][1]) for i in N]) # create the nodes backgrounds
        self.wait()

        """LEVEL 2"""
        # its the same thing but with more branches

        N = [6,8,10,12] # nodes that will recieve new points
        # distribution of the dots
        separation = {6: [i for i in range(9)] + [i for i in range(37, 52)],
                      8: [i for i in range(9, 15)],
                      10: [i for i in range(15, 31)] + [i for i in range(52, 57)],
                      12: [i for i in range(31, 37)] + [i for i in range(57, 64)]}

        Anims = []
        for k, v in separation.items():
            new_pos = random_placement([D[i] for i in v], A[k]) # compute new positions in the new node
            for i, p in zip(v, new_pos):
                # add the animation moving along a smooth path for each point
                Anims.append(MoveAlongPath(D[i], path_along_line(A[k - 1],
                                                                 D[i],
                                                                 D[i].copy().move_to(p),
                                                                 parents[k],
                                                                 A[k])))

        # mix up the order of the animations
        random.shuffle(Anims)

        # change camera view
        view = Group(*A[:13])
        self.play(self.camera.frame.animate.move_to(view).match_width(view).scale(1.15))

        self.play(*[Create(A[i]) for i in [n - 1 for n in N]]) # create the lines from the parent node to the child nodes
        self.play(AnimationGroup(*Anims, group=D, lag_ratio=0.02)) # move the dots
        self.play(*[DrawBorderThenFill(A[i][1]) for i in N]) # create the nodes backgrounds
        self.wait()

        #fade out everything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()