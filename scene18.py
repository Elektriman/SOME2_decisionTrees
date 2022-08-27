#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import random

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene18(MovingCameraScene):
    """
    this scene represents the process of separation of the data in two sets for training and testing the model
    """
    def construct(self):
        # create the data set as a rectangle with dots representing data
        main_set = Group(*[Dot(radius=0.5, color=LIGHTER_GREY, z_index=1) for i in range(64)])\
            .arrange_in_grid(4, 16, buff=0.5)\
            .add_background_rectangle(fill_color=rgb_to_color(3*(50/256,)), buff=0.3)
        # add a label
        main_label = Text("Data set", font_size=100).next_to(main_set, DOWN, buff=1)

        # create the training set
        training_set = Group(*[Dot(radius=0.5, color=LIGHTER_GREY) for i in range(42)]) \
            .arrange_in_grid(4, 11, buff=0.5) \
            .add_background_rectangle(fill_color=rgb_to_color(3 * (50 / 256,)), buff=0.3) \
            .next_to(main_set, DOWN, buff=5) \
            .shift(LEFT*7)
        # add a label
        training_label = Text("Training set", font_size=100).next_to(training_set, DOWN, buff=1)

        # create the testing set
        testing_set = Group(*[Dot(radius=0.5, color=LIGHTER_GREY) for i in range(22)]) \
            .arrange_in_grid(4, 6, buff=0.5) \
            .add_background_rectangle(fill_color=rgb_to_color(3 * (50 / 256,)), buff=0.3) \
            .next_to(main_set, DOWN, buff=5) \
            .shift(RIGHT*10)
        # add a label
        testing_label = Text("Testing set", font_size=100).next_to(testing_set, DOWN, buff=1)

        # camera setup
        view = Group(main_set, training_set, testing_set)
        self.camera.frame.move_to(view).match_width(view).scale(1.5)

        # create the rectangles representing the sets and show labels
        # show the data dots only on the main set
        self.wait()
        self.play(FadeIn(main_set), FadeIn(training_set[0]), FadeIn(testing_set[0]),
                  Write(main_label), Write(training_label), Write(testing_label))
        self.wait()

        # set random seed
        random.seed(69)
        distribution = [i+1 for i in range(64)] # make a list of the indices of the data dots in the main set
        random.shuffle(distribution) # mix the indices

        # give a part of the data to the training set, and the rest to the test set
        # proportions are approximately 63/35 % respectively
        Anims = []
        u,v = 1,1
        for i in range(len(main_set)-1):
            if distribution[i]<=42 :
                Anims.append(main_set[distribution[i]].animate.move_to(training_set[u]))
                u += 1
            else :
                Anims.append(main_set[distribution[i]].animate.move_to(testing_set[v]))
                v += 1

        # play the animation that will move the dots into their assigned set
        self.play(AnimationGroup(*Anims, group=main_set, lag_ratio=0.03))
        self.wait()

        # fade out everything, end of scene
        self.play(FadeOut(main_set), FadeOut(training_set), FadeOut(testing_set),
                  FadeOut(main_label), FadeOut(training_label), FadeOut(testing_label))
        self.wait()