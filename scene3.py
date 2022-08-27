#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import os

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene3(MovingCameraScene):
    """
    this scene shows the basics of what form takes the data we are using, aka what is a dataset
    """
    def construct(self):
        #recovering images from the 'img' folder
        """note that each image is a png of one line of the dataset displayed"""

        Rows = []
        path_of_the_directory = 'D:\Julien\Documents\projet vidéo maths 2022\code\img\dataset_parts'
        for filename in os.listdir(path_of_the_directory):
            f = os.path.join(path_of_the_directory, filename)
            if os.path.isfile(f):
                Rows.append(ImageMobject(f))

        ROW_HEIGHT = Rows[1].height
        ROW_WIDTH = Rows[1].width

        #creating the head
        head = Rows[0]
        self.camera.frame.move_to(head).match_width(head).scale(1.1).shift(5*ROW_HEIGHT * DOWN)
        self.play(FadeIn(head))
        self.wait(1)

        #moving the lines out of the camera frame before sliding them in
        for r in Rows[1:] :
            r.next_to(self.camera.frame, DOWN)
            self.add(r)

        #sliding the line one by one
        Anims = ()
        for i in range(1, len(Rows)) :
            Anims+=(Rows[i].animate.move_to(((i-1)*ROW_HEIGHT + head.height)*DOWN), )
        G = Group(*Rows)

        self.play(AnimationGroup(*Anims, group = G, lag_ratio=0.2))
        self.wait(2)

        #animation of the focus rectangle

        #rectangle parameters
        width = ValueTracker(0.6)
        height = ValueTracker(ROW_HEIGHT*10+head.height)
        x_coord = ValueTracker(-4.25)
        y_coord = ValueTracker(-1.6703703703703705)

        #using always redraw to keep the rectangle borders clean while resizing
        Focus = always_redraw(lambda: RoundedRectangle(width = width.get_value(),
                                                       height = height.get_value(),
                                                       corner_radius=0.05,
                                                       color=RED,
                                                       stroke_width=2).move_to([x_coord.get_value(), y_coord.get_value(), 0]))

        #creation of the focus
        self.play(Create(Focus))
        self.wait(2)

        #shifting to the family situation related columns
        self.play(x_coord.animate.increment_value(3.2), width.animate.set_value(4))
        self.wait(2)

        #shifting to the absences column
        self.play(x_coord.animate.increment_value(2.9), width.animate.set_value(1.75))
        self.wait(2)

        #shifting on the columns "mean grade" and "passed"
        self.play(x_coord.animate.increment_value(1.8), width.animate.set_value(1.9))
        self.wait(4)

        #shifting on the row of index Alice
        self.play(x_coord.animate.set_value(Rows[1].get_x()),
                  y_coord.animate.set_value(Rows[1].get_y()),
                  height.animate.set_value(ROW_HEIGHT),
                  width.animate.set_value(Rows[1].width))
        self.wait(2)

        #shifting on all the data
        self.play(x_coord.animate.increment_value(0.35),
                  y_coord.animate.set_value(Rows[1].get_y()-4.5*ROW_HEIGHT),
                  height.animate.set_value(ROW_HEIGHT*10),
                  width.animate.set_value(ROW_WIDTH-0.7))
        self.wait(2)

        #remove the figure, end of scene
        self.play(Uncreate(Focus))
        self.play(FadeOut(G))
        self.wait()