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

def treeF():
    # create tree
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 16.5, "x")
    T2 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")
    T3 = Tree_filled(T1, T2, 0, "y")
    T4 = Tree_filled(Tree_empty(), Tree_empty(), 2.5, "y")
    T5 = Tree_filled(T3, T4, 0, "y", scale=(2.5,2.5), xy_ratio=1)

    G = elements_in_order(T5, label_leaves=True)

    # edit the nodes
    G0 = remake_node(G[0], "Ever failed", "a class ?", color=BLUE_E)
    G2 = remake_node(G[2], "Extra support ?", color=BLUE_D)
    G4 = remake_node(G[4], "Study time", ">2                .5h/week ?", color=BLUE_D)
    G6 = remake_node(G[6], "Age>16.5 ?")
    G8 = remake_node(G[8], "Good health ?")
    L10 = remake_leaf(G[10], "FAIL", "(      100%)")
    L12 = remake_leaf(G[12], "PASS", "(    67%)")
    L14 = remake_leaf(G[14], "FAIL", "(    77%)")
    L16 = remake_leaf(G[16], "PASS", "(    56%)")
    L18 = remake_leaf(G[18], "FAIL", "(    80%)")
    L20 = remake_leaf(G[20], "PASS", "(    56%)")

    remake = [G0, G2, G4, G6, G8, L10, L12, L14, L16, L18, L20]
    remade = [g for g in G]

    for i in range(len(remake)):
        remade[2 * i] = remake[i]

    F = Group(*remade)

    # enlarge upper nodes
    F[0][0].scale(1.4)
    F[0][1].scale(1.4)
    F[2][0].scale(1.2)
    F[2][1].scale(1.2)
    F[4][0].scale(1.2)
    F[4][1].scale(1.2)

    return F


def treeK():
    Tree.reset()
    # create the tree
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 0)
    T2 = Tree_filled(Tree_empty(), Tree_empty(), 0)
    T3 = Tree_filled(T1, Tree_empty(), 0)
    T4 = Tree_filled(T2, Tree_empty(), 0)
    T5 = Tree_filled(T3, Tree_empty(), 0)
    T6 = Tree_filled(T4, Tree_empty(), 0)
    T7 = Tree_filled(T5, T6, 0, scale=(2,2), xy_ratio=1)

    G = elements_in_order(T7, label_leaves=True)

    # edit the nodes
    G0 = remake_node(G[0], "Ever failed", "a class ?", color=BLUE_E)
    G2 = remake_node(G[2], "More than 10", "absences ?", color=BLUE_D)
    G4 = remake_node(G[4], "Parents with", "hi                gh education ?", color=BLUE_D)
    G6 = remake_node(G[6], "Extra support ?", color=BLUE_C)
    G10 = remake_node(G[10], "Ever failed", "a class ?", color=BLUE_C)
    G14 = remake_node(G[14], "Extra support ?", color=BLUE_B)
    G18 = remake_node(G[18], "Ever failed", "a class ?", color=BLUE_B)
    L8 = remake_leaf(G[8], "FAIL")
    L12 = remake_leaf(G[12], "PASS")
    L16 = remake_leaf(G[16], "FAIL")
    L20 = remake_leaf(G[20], "FAIL")
    L22 = remake_leaf(G[22], "FAIL")
    L24 = remake_leaf(G[24], "FAIL")
    L26 = remake_leaf(G[26], "FAIL")
    L28 = remake_leaf(G[28], "FAIL")

    remake = [G0, G2, G4, G6, L8, G10, L12, G14, L16, G18, L20, L22, L24, L26, L28]
    remade = [g for g in G]

    for i in range(len(remake)):
        remade[2 * i] = remake[i]

    K = Group(*remade)

    return K

def treeQ():
    Tree.reset()
    # create tree
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 0)
    T2 = Tree_filled(T1, Tree_empty(), 0, scale=(2,2), xy_ratio=1)

    G = elements_in_order(T2, label_leaves=True)

    # edit nodes
    G0 = remake_node(G[0], "Failed a class", "at l                east twice ?", color=BLUE_E)
    G2 = remake_node(G[2], "Extra support ?", color=BLUE_D)
    L4 = remake_leaf(G[4], "FAIL")
    L6 = remake_leaf(G[6], "PASS")
    L8 = remake_leaf(G[8], "FAIL")


    remake = [G0, G2, L4, L6, L8]
    remade = [g for g in G]

    for i in range(len(remake)):
        remade[2 * i] = remake[i]

    Q = Group(*remade)

    return Q

def change_tree(Tree1: Group, Tree2: Group, identical: list[int]) -> list[Animation]:
    """
    changes one tree into another by trying to edit as little as possible

    Parameters
    ----------
    Tree1 : Group
        the initial tree
    Tree2 : group
        the target tree
    identical :
        the list of indexes of objects that should stay unchanged

    Returns
    -------
    list[Animation]
        a list of all the animations to play to show the transition from Tree1 to Tree2
    """

    Anims = []
    for i in identical :
        if type(Tree1[i])==type(Tree2[i]) : #same type of node
            Anims.append(ReplacementTransform(Tree1[i], Tree2[i]))
        if type(Tree1[i])==Paragraph and type(Tree2[i])==LabeledNode : #go from leaf node to normal node
            Anims.append(ReplacementTransform(Tree1[i].submobjects[0], Tree2[i][1])) #transform background rectangle
            Anims.append(ReplacementTransform(VGroup(*Tree1[i].submobjects[1:]), Tree2[i][0])) #transform text
        if type(Tree1[i])==LabeledNode and type(Tree2[i])==Paragraph : #go from normal node to leaf node
            Anims.append(ReplacementTransform(Tree1[i][1], Tree2[i].submobjects[0])) #transform background rectangle
            Anims.append(ReplacementTransform(Tree1[i][0], VGroup(*Tree2[i].submobjects[1:]))) #transform text

    #fade out elements of Tree1 not present in Tree2
    for i in range(len(Tree1)):
        if not i in identical :
            Anims.append(FadeOut(Tree1[i]))

    #fade in elements of Tree2 not present in Tree1
    for i in range(len(Tree2)):
        if not i in identical:
            Anims.append(FadeIn(Tree2[i]))

    return Anims


#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene15(MovingCameraScene):
    """
    this scene shows the unstable nature of a decision tree regarding the input data
    """
    def construct(self):
        self.camera.frame.save_state()

        #creating first tree
        F = treeF()

        #background color for a rectangle containing all the data points
        BGcolor = rgb_to_color((50/255,)*3)

        R = Rectangle(width = F.height/2,
                      height=F.height,
                      color=BGcolor,
                      fill_color=BGcolor,
                      fill_opacity=1.)\
            .next_to(F, LEFT)

        #create the data points with respective colors
        color = [RED] * 19 + [GREEN, RED, RED] + [GREEN] * 10
        D = Group(*[Dot(color=c, z_index=1) for c in color])\
            .arrange_in_grid(8, 4, buff=0.05).move_to(R)\
            .match_height(R).scale(0.95)

        #camera setup
        self.camera.frame.move_to(Group(F, R)).match_width(Group(F, R)).scale(1.2)

        """FIRST TREE"""

        #create tree, rectangle and data points
        self.play(FadeIn(F),
                  DrawBorderThenFill(R),
                  AnimationGroup(*[GrowFromCenter(d) for d in D], group=D, lag_ratio=0.05))
        self.wait(4)

        """SECOND TREE"""

        # save the data points to restore them after removing them
        to_remove1 = [1, 11, 16, 26, 28]
        for i in to_remove1:
            D[i].save_state()

        #create second tree
        K = treeK().move_to(F)

        #edition of data by removing some data points
        self.play(*change_tree(F, K, [1,2,3,4,5,6,7,9,11,12,13,15,16]),
                  *[GrowFromCenter(D[index], reverse_rate_function=True) for index in to_remove1])
        self.wait(4)

        """THIRD TREE"""

        # saving the state of data points to restore them
        to_remove2 = [2, 5, 19, 21, 24]
        for i in to_remove2:
            D[i].save_state()

        #creating new tree
        Q = treeQ().move_to(K)

        #restoring data points
        self.play(*[Restore(D[index]) for index in to_remove1])
        #deleting new data points, changes the tree into a new one
        self.play(*change_tree(K, Q, [i for i in range(9)]),
                  *[GrowFromCenter(D[index], reverse_rate_function=True) for index in to_remove2])
        self.wait(4)

        #restoring data points
        self.play(*[GrowFromCenter(D[index], reverse_rate_function=True) for index in to_remove2])
        self.wait()

        #fade out everything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])