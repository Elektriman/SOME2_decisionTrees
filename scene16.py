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

#background color
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

def treeE():
    Tree.reset()
    # create tree
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 0)
    T2 = Tree_filled(Tree_empty(), Tree_empty(), 0)
    T3 = Tree_filled(T1, T2, 0, scale=(2,2), xy_ratio=1)

    G = elements_in_order(T3, label_leaves=True)

    G0 = remake_node(G[0], "Rule 1", color=BLUE_E).scale(1.5)
    G2 = remake_node(G[2], "Left node", color=BLUE_D)
    G4 = remake_node(G[4], "Right node", color=BLUE_D)

    remake = [G0, G2, G4]
    remade = [g for g in G]

    for i in range(len(remake)):
        remade[2 * i] = remake[i]

    return Group(*remade[:5])

def get_ratio(D: Group) -> tuple[int, int]:
    """
    accounts for the populations of green and red dots in the given collection of dots

    Parameters
    ----------
    D : Group
        the group of dots from which compute the number of reds and greens

    Returns
    -------
    tuple[int, int]
        the integers representing respectively the number of red dots and the number of green dots in the collection
    """
    reds, greens = 0, 0
    for d in D:
        if d.fill_color == Dot(color=RED).color:
            reds += 1
        elif d.fill_color == Dot(color=GREEN).color:
            greens += 1
    return reds, greens

def under_ratio(D: Group, text: str, v: ValueTracker) -> Mobject:
    """
    creates and return a label to display under a collection of dots.
    the label here contains the percentage of passing students

    Parameters
    ----------
    D : Group
        the collection of dots
    text : str
        the name of the stat to display
    v : Valuetracker
        the storage of the value of the percentage

    Returns
    -------
    Mobject
        the label to display
    """
    reds, greens = get_ratio(D)
    v.set_value(100*max(reds, greens)/(reds+greens))

    T = always_redraw(lambda: Text(f"{text}:{int(v.get_value())}%", color=LIGHTER_GREY, font_size=10) \
                      .next_to(D.submobjects[0], DOWN, buff=0.3))

    return T

def under_ratio2(D: Group, text: str, v: ValueTracker) -> Mobject:
    """
        creates and return a label to display under a collection of dots.
        the label here contains the value of Impurity of the dot collection

        Parameters
        ----------
        D : Group
            the collection of dots
        text : str
            the name of the stat to display
        v : Valuetracker
            the storage of the value of the Impurity

        Returns
        -------
        Mobject
            the label to display
        """
    reds, greens = get_ratio(D)
    v.set_value(Impurity(greens, reds))

    T = always_redraw(lambda: Text(f"{text}:{truncate(v.get_value(), 2)}", color=LIGHTER_GREY, font_size=10) \
                      .next_to(D.submobjects[0], DOWN, buff=0.3))

    return T

def weighted_mean(lr: int, lg: int, Il: float, rr: int, rg: int, Ir: float) -> float:
    """
    computes the weighted mean of a parent node

    Parameters
    ----------
    lr : int
        the number of red dots in the left child node
    lg : int
        the number of green dots in the left child node
    Il : float
        the impurity of the left child node
    rr : int
        the number of red dots in the right child node
    rg : int
        the number of green dots in the right child node
    Ir : float
        the impurity of the right child node

    Returns
    -------
    float
        the value of the weighted mean
    """
    nl = lr + lg
    nr = rr + rg
    return (nl * Il + nr * Ir) / (nl + nr)

def Impurity(G: int, R: int) -> float:
    """
    computes the impurity value of a node

    Parameters
    ----------
    G : int
        number of green data points in the node
    R : int
        number of red data points in the node

    Returns
    -------
    float
        the impurity of the node
    """
    N = G + R
    return 1 - (R/N)**2 - (G/N)**2

def truncate(num:float, n:int)->float:
    """
    equivalent of the floor function

    Parameters
    ----------
    num : float
        number to truncate
    n : int
        number of decimals to keep after the coma

    Returns
    -------
    float
        the truncated number
    """
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)
    return float(temp)

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene16(MovingCameraScene):
    """
    This scene shows the principles behind the choice of the rules of the nodes in a decision tree
    """
    def construct(self):
        # camera setup
        self.camera.frame.move_to(E).match_width(E).scale(1.5)

        # create tree
        E = treeE()
        self.create_tree(E)
        self.wait()

        # move camera further back
        self.play(self.camera.frame.animate.move_to(Group(E,D)).scale(1.2))

        # adding data points above the node
        colors = [GREEN, GREEN, RED, RED, RED, RED, RED, RED,
                  GREEN, GREEN, RED, RED, RED, RED, RED, RED,
                  GREEN, GREEN, GREEN, RED, RED, RED, RED, RED,
                  GREEN, GREEN, GREEN, GREEN, RED, RED, RED, RED]

        D = Group(*[Dot(color=c, z_index=1) for c in colors]).arrange_in_grid(4, 8, buff=0.05)
        D.add_background_rectangle(color=rgb_to_color((50 / 255,) * 3), buff=0.05)
        D.next_to(E[0], UP, buff=0.5).scale_to_fit_width(E[0].width * 2)

        self.play(DrawBorderThenFill(D.submobjects[0]))
        self.play(AnimationGroup(*[GrowFromCenter(d) for d in D.submobjects[1:]], group = D, lag_ratio=0.15))
        self.wait()

        # create a place to recieve the data points after going throught the node
        Left_D = Group(*[Dot(z_index=1) for i in range(11)]).arrange_in_grid(3, 4, buff=0.05)
        Left_D.add_background_rectangle(color=rgb_to_color((50 / 255,) * 3), buff=0.05)
        Left_D.next_to(E[2], DOWN, buff=0.5).scale_to_fit_width(D.width * 0.5)

        Right_D = Group(*[Dot(z_index=1) for i in range(21)]).arrange_in_grid(4, 6, buff=0.05)
        Right_D.add_background_rectangle(color=rgb_to_color((50 / 255,) * 3), buff=0.05)
        Right_D.next_to(E[4], DOWN, buff=0.5).scale_to_fit_width(D.width * 0.75)

        # camera adjustments to include the new parts
        self.play(self.camera.frame.animate.move_to(Group(E, D, Left_D, Right_D)).scale(1.3))

        # draw the new rectangles
        self.play(DrawBorderThenFill(Left_D.submobjects[0]), DrawBorderThenFill(Right_D.submobjects[0]))
        self.wait()

        # moving the data points below their corresponding node
        # the first sorting is done by color : green->left, red->right
        Anims=[]
        l, r = 1, 1
        for i in range(len(colors)):
            if colors[i]==GREEN :
                Anims.append(D[1+i].animate.move_to(Left_D[l]))
                Left_D[l].become(D[1 + i])
                l += 1
            if colors[i]==RED :
                Anims.append(D[1+i].animate.move_to(Right_D[r]))
                Right_D[r].become(D[1 + i])
                r += 1

        self.play(AnimationGroup(*Anims, group=D, lag_ratio=0.15))
        self.wait()

        # recount the points for each rectangle as statistics will be computed from their populations
        l, r = 1, 1
        for i in range(len(colors)):
            if colors[i] == GREEN:
                Left_D[l].become(D[1 + i])
                l += 1
            if colors[i] == RED:
                Right_D[r].become(D[1 + i])
                r += 1

        # invisible replacement of the dots that belonged to the upper rectangle, and now belong to their respective
        # bottom left or bottom right rectangle
        self.add(Left_D, Right_D).remove(D)

        # removing empty top rectangle and camera reframing
        self.play(FadeOut(D.submobjects[0]),
                  self.camera.frame.animate.scale(0.7).move_to(Group(E, Left_D, Right_D)).shift(DOWN*0.3))

        # adding to the the parent node a "perfect rule" label
        New_E0 = remake_node(E[0], "Perfect rule", color=BLUE_E).scale(1.5)
        New_E0[0].set(color=GOLD)

        self.play(GrowFromCenter(E[0][0], reverse_rate_function=True),
                  GrowFromCenter(New_E0[0]),
                  ReplacementTransform(E[0][1], New_E0[1]),
                  Flash(New_E0[0], color=GOLD))
        self.wait()

        # adding statistics under the bottom rectangles
        # for now they are accounting for the percentage of passing students
        left_v = ValueTracker(0)
        right_v = ValueTracker(0)
        left_T = under_ratio(Left_D, "PASS", left_v)
        right_T = under_ratio(Right_D, "FAIL", right_v)

        self.play(Create(left_T), Create(right_T))
        self.wait()

        # exhanges some points and change the stats accordingly
        exchanges = {3:17, 4:18, 7:19, 8:20, 11:21}

        self.exchange_points(exchanges, Left_D, Right_D, left_v, right_v, do_percent=True)
        self.wait()

        # give the parent node the label "Good rule"
        BRONZE = "#574327"
        New_New_E0 = remake_node(New_E0, "Good rule", color=BLUE_E).scale(1.5)
        New_New_E0[0].set(color=BRONZE)

        self.play(GrowFromCenter(New_E0[0], reverse_rate_function=True),
                  GrowFromCenter(New_New_E0[0]),
                  ReplacementTransform(New_E0[1], New_New_E0[1]),
                  Flash(New_New_E0[0], color=BRONZE))
        self.wait()

        # change the statistic displayed to an impurity computation
        left_T2 = under_ratio2(Left_D, "Impurity", left_v)
        right_T2 = under_ratio2(Right_D, "Impurity", right_v)
        self.play(ReplacementTransform(left_T, left_T2),
                  ReplacementTransform(right_T, right_T2))
        self.wait()

        """DISCUSSION ON THE SIDE OF THE IMPURITY COMPUTATION"""

        # create text elements that will be used in the forulas
        o = ValueTracker(0) #opacity
        xl = ValueTracker(left_T2.get_x()) # x coordinate of the left text
        xr = ValueTracker(right_T2.get_x()) # x coordinate of the right text
        Il = always_redraw(lambda : MathTex("Impurity_l", fill_opacity=o.get_value())
                           .match_height(left_T2)
                           .move_to([left_T2.get_x()+xl.get_value(), left_T2.get_y(), 0]))
        Ir = always_redraw(lambda : MathTex("Impurity_r", fill_opacity=o.get_value())
                           .match_height(right_T2)
                           .move_to([right_T2.get_x()+xr.get_value(), right_T2.get_y(), 0]))
        self.add(Il, Ir)

        # we go out of the figure to study the formula. The texts shift right while having their opacity set to 1
        self.play(self.camera.frame.animate.shift(RIGHT*10),
                  xl.animate.set_value(10),
                  xr.animate.set_value(10),
                  o.animate.set_value(1))
        self.wait()

        # standard mean formula
        formula1 = MathTex("Impurity_l","+","Impurity_r","\over","2").move_to(self.camera.frame)
        self.play(TransformMatchingTex(VGroup(Il, Ir), formula1))
        self.wait()

        # cross the previous formula, put it aside
        # instead show the formula of a mean weighted by the number of data of each child node
        formula2 = MathTex("{\#_l \cdot", "Impurity_l", "+ \#_r \cdot ", "Impurity_r", "\over", " \#_l+\#_r}")\
            .move_to(self.camera.frame)

        C = Cross(formula1, color=RED)[0] #take only one line of the cross
        C.add_updater(lambda m:m.move_to(formula1)) #stick the cross and the formula together
        self.play(Create(C))
        self.wait()
        self.play(self.camera.frame.animate.scale(1.1),
                  formula1.animate.next_to(formula2, LEFT, buff=3),
                  Write(formula2))
        self.play(FadeOut(formula1), FadeOut(C))
        self.wait()

        # evaluate the formula in our special case
        res_value = ValueTracker(0.0)
        res_value.set_value((left_v.get_value() * 11 + right_v.get_value() * 21) / 32)

        # add the equal sign in the end
        formula3 = MathTex("{\#_l \cdot", "Impurity_l", "+ \#_r \cdot ", "Impurity_r", "\over", " \#_l+\#_r}", "=")\
            .next_to(formula1, RIGHT, buff=2)

        #create an invisible mobject that will store the result position and size
        res_center = Dot(fill_opacity=0., stroke_opacity=0.).next_to(formula3, RIGHT, buff=0.75).scale_to_fit_height(formula3.height / 3)

        result = always_redraw(lambda : DecimalNumber(0.01*int(100*res_value.get_value()))\
                               .move_to(res_center)\
                               .match_height(res_center))

        # add equal sign and write the evaluation
        self.play(self.camera.frame.animate.scale(1.2),
                  TransformMatchingTex(formula2, formula3),
                  Write(result))
        self.wait()

        # go back to the figure and bring the formula with us
        self.play(self.camera.frame.animate.move_to(E).shift(DOWN*1.5).scale(0.8),
                  formula3.animate.next_to(Group(E, Left_D, Right_D), DOWN, buff=0.5).shift(LEFT*0.3).scale(0.5),
                  res_center.animate.next_to(Group(E, Left_D, Right_D), DOWN, buff=0.87).shift(RIGHT*2).scale(0.5))
        self.wait()

        # exchange some points in the rectangles and change the stats accordingly
        exchanges = {3:17, 4:18}

        self.exchange_points(exchanges, Left_D, Right_D, left_v, right_v, res_value=res_value, s=-1)
        self.wait()

        # give the parent node the label "better rule"
        New_New_New_E0 = remake_node(New_New_E0, "Better rule", color=BLUE_E).scale(1.5)
        New_New_New_E0[0].set(color=LIGHT_GREY)

        self.play(GrowFromCenter(New_New_E0[0], reverse_rate_function=True),
                  GrowFromCenter(New_New_New_E0[0]),
                  ReplacementTransform(New_New_E0[1], New_New_New_E0[1]),
                  Flash(New_New_New_E0[0], color=LIGHT_GREY),
                  Circumscribe(result))
        self.wait()

        # fade out everything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()

    def exchange_points(self,
                        exchange_dict:dict,
                        LD:Group,
                        RD:Group,
                        lv: ValueTracker,
                        rv: ValueTracker,
                        res_value:ValueTracker=ValueTracker(0),
                        do_percent:bool=False,
                        s:int=1):
        """
        exchanges the points from the two bottom rectangles and updates the statistics accordingly

        Parameters
        ----------
        exchange_dict : dict
            the dictionnary of the points to exchange. key->left point, value->right point
        LD : Group
            the collection of points on the left rectangle
        RD : Group
            the collection of points on the right rectangle
        lv : ValueTracker
            the stored value of the left rectangle either for the percentage of passing students, or for the impurity
        rv : ValueTracker
            the stored value of the right rectangle either for the percentage of passing students, or for the impurity
        res_value : ValueTracker
            the stored value of the weighted mean
        do_percent : bool
            (default False) wether or not we are doing percentage (True) or impurity (False) computation
        s : int
            (either 1 or -1, default 1) symbolises the number of green dots gained by the right rectangle.
            It is for computation simplification.
        """
        for l, r in exchange_dict.items():
            # recover the number of red and green dots in each rectangle
            l_reds, l_greens = get_ratio(LD)
            r_reds, r_greens = get_ratio(RD)
            # precompute the same numbers after this exchange
            l_reds, l_greens = l_reds + s, l_greens - s
            r_reds, r_greens = r_reds - s, r_greens + s

            if do_percent :
                # move left dot to right dots position
                # move right dot to left dot's position (the left dot has not moved yet so no aliasing problem here)
                # recompute the left rectangle percentage
                # recompute the right rectangle percentage
                self.play(LD[l].animate.move_to(RD[r]),
                          RD[r].animate.move_to(LD[l]),
                          lv.animate.set_value(100 * max(l_greens, l_reds) / (l_reds + l_greens)),
                          rv.animate.set_value(100 * max(r_greens, r_reds) / (r_reds + r_greens)))
            else :
                # move left dot to right dots position
                # move right dot to left dot's position (the left dot has not moved yet so no aliasing problem here)
                # recompute the left rectangle impurity
                # recompute the right rectangle impurity
                # recompute the weighted mean
                self.play(LD[l].animate.move_to(RD[r]),
                          RD[r].animate.move_to(LD[l]),
                          lv.animate.set_value(Impurity(l_greens, l_reds)),
                          rv.animate.set_value(Impurity(r_greens, r_reds)),
                          res_value.animate.set_value(weighted_mean(l_reds, l_greens, lv.get_value(), r_reds, r_greens, rv.get_value())))

            # apply the dot changes to the counts for each rectangles
            save = RD[r].copy() #prevent aliasing with this storage variable
            RD[r].become(LD[l])
            LD[l].become(save)

    def create_tree(self, E: Group):
        """
        Creates a tree node by node

        Parameters
        ----------
        E : Group
            the group of mobjects forming the tree
        """

        for e in E:
            if isinstance(e, LabeledNode):
                # create the node
                self.play(AnimationGroup(FadeIn(e[1]), Write(e[0]), lag_ratio=0.4))
            elif isinstance(e, Text) or isinstance(e, Paragraph):
                # if the node is a leaf with label
                anims = [FadeIn(e[0]), Write(e[1]), Write(e[2])]
                self.play(AnimationGroup(*anims, group=e, lag_ratio=0.4))
            elif isinstance(e, Line):
                # if the object to draw is a line between two nodes
                # we check first whether the lines goes right or left to add the yes/no label
                if e.start[0] < e.end[0]:
                    # going right, add "yes"
                    self.play(Create(e), Write(add_yes_no(e, "yes", font_size=10)))
                else:
                    # going left, add "no"
                    self.play(Create(e), Write(add_yes_no(e, "no", font_size=10)))