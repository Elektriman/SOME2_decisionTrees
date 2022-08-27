#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *

#   _____ _
#  / ____| |
# | |    | | __ _ ___ ___  ___  ___
# | |    | |/ _` / __/ __|/ _ \/ __|
# | |____| | (_| \__ \__ \  __/\__ \
#  \_____|_|\__,_|___/___/\___||___/

class LabeledNode(Mobject):
    """
    Custom class to make tree nodes looking better
    """

    def __init__(self, text, cr=0.07, **kwargs):
        super().__init__(**kwargs)
        self.fill_rgbas = [0, 0, 0, 0]
        self.stroke_rgbas = [0, 0, 0, 0]
        self.background_stroke_rgbas = [0, 0, 0, 0]

        #adding text
        self.submobjects.append(text)

        #adding background rectangle manually
        shape = SurroundingRectangle(self.submobjects[0],
                                     corner_radius=cr,
                                     fill_color=WHITE,
                                     color=WHITE,
                                     fill_opacity=1.,
                                     z_index=text.z_index - 1)

        #adding rectangle to submobjects
        self.submobjects.append(shape)
        self.shape_updater()

    def shape_updater(self):
        """
        adding an updater for the size and position
        """
        #updating position
        self.submobjects[1].match_coord(self.submobjects[0], 0)
        self.submobjects[1].match_coord(self.submobjects[0], 1)
        #updating size
        self.submobjects[1].match_height(SurroundingRectangle(self.submobjects[0],corner_radius=0.07))
        self.submobjects[1].match_width(SurroundingRectangle(self.submobjects[0],corner_radius=0.07))
        #updating depth
        self.submobjects[1].set(z_index = self.submobjects[0].z_index -1)

    @override_animation(Create)
    def custom_create(self):
        """
        overriding the Create animation

        Returns
        -------
        AnimationGroup
            The animations to display on creation
        """
        anims = []#storage of animations
        anims.append(DrawBorderThenFill(self.submobjects[1])) #draw the background rectangle
        anims.append(Write(self.submobjects[0])) #write the text
        #custom timing to get the writing started right as the rectangle finishes being drawn
        return AnimationGroup(*anims, group=self, lag_ratio=0.9)#returning an Animation type object as specified in the Create function