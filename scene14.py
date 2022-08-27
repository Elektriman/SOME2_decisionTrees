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

def elements_in_order(T:Tree, label_leaves:bool=False)->tuple :
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

def remake_node(old_node:Mobject, *text:str, color=BLUE_C)->Mobject:
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
                               font_size=old_node[0].font_size, #copy font size
                               color=BLACK)).move_to(old_node).set_z_index(old_node.z_index, True) #copy position and z_index
    N[1].set(fill_color=color, color=color) #set the color
    return N

def remake_leaf(old_leaf:Mobject, *text:str)->Mobject:
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
    #we use paragraph to be able to put text on two lines
    return Paragraph(*text,
                     alignment="center",
                     color=BLACK,
                     font_size=int(old_leaf.font_size * 0.4))\
        .add_background_rectangle(color=GREEN, opacity=1, buff=0.1) \
        .move_to(old_leaf)
    #copy font size and position

#      _       __ _       _ _   _
#     | |     / _(_)     (_) | (_)
#   __| | ___| |_ _ _ __  _| |_ _  ___  _ __  ___
#  / _` |/ _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
# | (_| |  __/ | | | | | | | |_| | (_) | | | \__ \
#  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/

def treeA() -> Group :
    # creating tree
    T1 = Tree_filled(Tree_empty(), Tree_empty(), 16.5, "x")
    T2 = Tree_filled(Tree_empty(), Tree_empty(), 0, "x")
    T3 = Tree_filled(T1, T2, 0, "y")
    T4 = Tree_filled(Tree_empty(), Tree_empty(), 2.5, "y")
    T5 = Tree_filled(T3, T4, 0, "y", scale=(2.5, 2.5), xy_ratio=1)

    G = elements_in_order(T5, label_leaves=True)

    # remake the nodes
    G0 = remake_node(G[0], "Ever failed", "a class ?", color=BLUE_E)
    G2 = remake_node(G[2], "Extra support ?", color=BLUE_D)
    G4 = remake_node(G[4], "Study time", ">2                .5h/week ?", color=BLUE_D)
    G6 = remake_node(G[6], "Age>16.5 ?")
    G8 = remake_node(G[8], "Good health ?")
    #the spaces compensate for an error of latex when adding Paragraph mobjects
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

    return Group(*remade)

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene14(ZoomedScene):
    """
    Ths scene shows the concept of greedy process used when creating tree nodes
    """
    def __init__(self, **kwargs):
        """using the detached camera frame"""
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=1,
            image_frame_stroke_width=10,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        #camera setup
        self.camera.frame.save_state()

        #creating tree
        F = treeA()

        """START OF ANIMATION"""
        self.camera.frame.move_to(F).scale(0.7)
        self.create_tree(F)

        #enlarging upper nodes
        self.play(F[0][0].animate.scale(1.4), F[0][1].animate.scale(1.4))
        self.play(F[2][0].animate.scale(1.2), F[2][1].animate.scale(1.2),  F[4][0].animate.scale(1.2), F[4][1].animate.scale(1.2))
        self.wait(2)

        """ZOOMED CAMERA SCENE"""

        self.camera.frame.save_state()

        #getting variable names
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        #creating the differents views
        view_1 = Group(F[0], F[2], F[4])
        view_2 = Group(F[2], F[6], F[8])
        view_3 = Group(F[4], F[10], F[12])
        view_4 = Group(F[6], F[14], F[16])
        view_5 = Group(F[8], F[18], F[20])

        #reframing camera
        frame.become(Rectangle(width=16, height=9, color=RED).move_to(view_1).match_width(view_1).scale(1.1))

        #initiating the zoomed_display
        zoomed_display.next_to(F, RIGHT, buff=10)
        zoomed_display_frame.set_color(RED).set_stroke_width(0)
        zoomed_display.scale([16, 9, 0]).match_width(frame)

        #adding some color to the zoomed camera
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        #special function that operates the swap between a unseen rectangle and the actual zoomed frame
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        #création de la découpe de caméra
        self.play(Create(frame), self.camera.frame.animate.move_to(frame).match_height(frame).scale(2).shift(UP*0.5))
        self.activate_zooming()

        #synchronising cameras
        frame_updater = lambda m:m.move_to(zoomed_display).shift(UP*0.5).scale_to_fit_height(zoomed_display.height*2)
        self.camera.frame.add_updater(frame_updater)

        #detach camera from zoomed display
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        zoomed_display_label = Text("Greedy Algorithm's view", font_size=30, color=WHITE).next_to(zoomed_display, UP)
        self.play(Write(zoomed_display_label))
        self.wait()

        #going throught the different views
        self.change_view(frame, view_2)
        self.wait(3)
        self.change_view(frame, view_1)
        self.change_view(frame, view_3)
        self.wait(3)
        self.change_view(frame, view_1)
        self.change_view(frame, view_2)
        self.change_view(frame, view_4)
        self.wait(3)
        self.change_view(frame, view_2)
        self.change_view(frame, view_5)
        self.wait(3)

        #puting back the camera and the frame together
        self.play(self.get_zoomed_display_pop_out_animation(),
                  unfold_camera,
                  FadeIn(zoomed_display_label, remover=True),
                  rate_func=lambda t: smooth(1 - t))

        #removing the frames
        zoomed_display_frame.set_stroke_width(5)
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame, run_time=0.1))
        self.camera.frame.remove_updater(frame_updater)
        self.wait()

        #reinitialisation of the camera
        self.play(Restore(self.camera.frame))
        self.wait()

        #fade out everything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])


    def change_view(self, frame, new_view):
        """
        changes the position of the zoomed camera frame to see a new view

        Parameters
        ----------
        frame : Rectangle
            the rectangle defining the zone displayed on the zoomed camera
        new_view : Group
            the view where to put the camera frame
        """

        if new_view.width/new_view.height > 16/9 :
            self.play(frame.animate.move_to(new_view).match_width(new_view).scale(1.1))
        else :
            self.play(frame.animate.move_to(new_view).match_height(new_view).scale(1.1))


    def create_tree(self, E:Group):
        """
        Creates a tree node by node

        Parameters
        ----------
        E : Group
            the group of mobjects forming the tree
        """

        for e in E:
            if isinstance(e, LabeledNode):
                #create the node
                self.play(AnimationGroup(FadeIn(e[1]), Write(e[0]), lag_ratio=0.4))
            elif isinstance(e, Text) or isinstance(e, Paragraph):
                #if the node is a leaf with label
                anims = [FadeIn(e[0]), Write(e[1]), Write(e[2])]
                self.play(AnimationGroup(*anims, group=e, lag_ratio=0.4))
            elif isinstance(e, Line):
                #if the object to draw is a line between two nodes
                #we check first whether the lines goes right or left to add the yes/no label
                if e.start[0] < e.end[0]:
                    #going right, add "yes"
                    self.play(Create(e), Write(add_yes_no(e, "yes", font_size=10)))
                else:
                    #going left, add "no"
                    self.play(Create(e), Write(add_yes_no(e, "no", font_size=10)))