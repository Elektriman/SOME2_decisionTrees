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
    """
    animation used for the introduction
    it's a decision tree without text slowly being built
    """
    def construct(self):

        # create the tree, and a title
        A = treeA()
        title = Text("Decision Trees", font_size=40).next_to(A, UP, buff=0.5)
        view = Group(A,title)

        # camera setup
        self.camera.frame.move_to(view).match_width(view).scale(1.2)
        self.wait()

        # create the tree, and write the title in the middle of the animation
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
