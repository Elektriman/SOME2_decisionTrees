#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import pickle
import numpy as np

# configuration de la couleur d'arrière-plan
GRIS = rgb_to_color(3 * (36 / 256,))
config.background_color = rgb_to_color(GRIS)

#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def name(curve: ParametricFunction, n: int, label: str, place=UP) -> Text:
    """
    function that will return a label of the given function positionned along its curve
    the rotation is computed by taking two points : one before and one after the anchor
    the given points will give a line close to the derivative at the anchor
    the text will then be rotated to be aligned with that line

    Parameters
    ----------
    curve : ParametricFunction
        the curve next to which to display the label
    n : int
        the n-th point of the curve used as anchor to put the label next to it
    label : str
        the name of the curve that will be displayed
    place : np.ndarray
        the orientation on which shift the label to avoid the text overlapping the curve

    Returns
    -------
    Text
        the label to display
    """
    # taking the coordinates of two points before and after n
    xa, ya, xb, yb = curve.points[n - 10][0], curve.points[n - 10][1], curve.points[n + 10][0], curve.points[n + 10][1]

    return Text(label, color=curve.color, font_size=20, z_index=1) \
        .next_to(curve.points[n], place) \
        .rotate(np.arctan((yb - ya) / (xb - xa)))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene4bis(MovingCameraScene):
    """
    this scene shows the thought process of fitting a model to its data
    """
    def construct(self):
        #camera setup
        self.camera.frame.scale(1.3)
        self.camera.frame.save_state()

        #creating axes
        axes = Axes(
            x_range=[0, 11],
            y_range=[0, 7],
            x_length=12,
            y_length=7,
            axis_config={"color": WHITE, "include_numbers": False, "include_ticks":False}
        ).set_z_index(3, True)
        x_label = Text("Model complexity", font_size=30).next_to(axes[0], DOWN, buff=0).set_z_index(3, True)
        y_label = Text("Error", font_size=30).next_to(axes[1], LEFT, buff=-0.35).rotate(90 * DEGREES).set_z_index(3, True)

        self.play(GrowFromPoint(axes, axes.get_origin()), Write(x_label), Write(y_label))
        self.wait(1)

        #adding a rectangle to hide elements that are sticking out of the plot on the right
        cache = Rectangle(fill_opacity=1,
                          stroke_opacity=0,
                          height=axes.height*1.4,
                          width=6.5,
                          fill_color=GRIS,
                          z_index=2) \
            .next_to(axes, RIGHT, buff=-0.4)

        self.add(cache)

        #creating the curve of the training error
        Training_error = lambda x: 5 * np.exp(-x / 4)
        Training_curve = axes.plot(Training_error).set(color=BLUE, z_index=1)
        Training_label = name(Training_curve, 350, "Training Error")

        Anims = (Create(Training_curve), Write(Training_label))
        G = Group(Training_curve, Training_label)

        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.4))
        self.wait(1)

        #creating the curve of the text error
        Test_error = lambda x: 0.07 * (x - 5.5) ** 2 - 0.1 * x + 4
        Test_curve = axes.plot(Test_error).set(color=ORANGE, z_index=1)
        Test_label = name(Test_curve, 350, "Test Error", place=DOWN)

        Anims = (Create(Test_curve), Write(Test_label))
        G = Group(Test_curve, Test_label)

        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.4))
        self.wait(1)

        #creating gradients of red oritented left to right and right to left
        R_underfit = Rectangle(fill_opacity=0.2,
                               stroke_opacity=0,
                               height=axes.height-0.5,
                               width=87/14,
                               fill_color=color_gradient([RED, GRIS], 2),
                               sheen_direction=RIGHT)\
            .next_to([axes[0].n2p(87/14)[0], -0.2, 0], LEFT, buff=0.59)

        R_overfit = Rectangle(fill_opacity=0.2,
                              stroke_opacity=0,
                              height=axes.height-0.5,
                              width=R_underfit.width,
                              fill_color=color_gradient([RED, GRIS], 2),
                              sheen_direction=LEFT) \
            .next_to([axes[0].n2p(87/14)[0], -0.2, 0], RIGHT, buff=0.59)

        underfit_label = Text("Underfitting", color=RED, font_size=25).next_to(R_underfit, UP).set_z_index(3, True)
        overfit_label = Text("Overfitting", color=RED, font_size=25).next_to(R_overfit, UP).shift(LEFT).set_z_index(3, True)

        #animating the search for an optimal fit

        #tracking the x value where the line representing the current model is
        e = ValueTracker(5)

        c = Square(color=YELLOW) #the line mobject has its colour changed indirectly via this mobject
        l = always_redraw(lambda : axes.get_line_from_axis_to_point(
            point=[axes[0].n2p(e.get_value())[0], axes.get_top()[1] - 0.4, 0],
            index=0,
            color=c.color))
        l.set_z_index(2, True)

        #placing the cureent model in the plot
        self.play(Create(l))
        self.wait(1)

        #show the underfitting
        self.play(e.animate.set_value(2), FadeIn(R_underfit), run_time=3)
        self.wait(0.5)
        self.play(Write(underfit_label))
        self.wait(2)

        #show overfitting
        self.play(FadeIn(R_overfit), e.animate.set_value(9.5), run_time=4)
        self.wait(0.5)
        self.play(Write(overfit_label))
        self.wait(2)

        #putting the model line in the sweet spot

        """
        this is a custom rate function for the animation
        it starts easy and woobles around the target before stopping
        """
        def rate_f(t):
            if t > 0.3:
                return 0.3 + rate_functions.ease_out_elastic((t - 0.3) / 0.7) * 0.7
            else:
                return rate_functions.rush_into(t / 0.3) ** (4.8) * 0.3

        #set_value computed separately
        self.play(e.animate.set_value(87/14), rate_func=rate_f, run_time=3)

        #adding a leabel for the best fit
        best_fit_label = Text("Best Fit",
                              color=GREEN,
                              font_size=25).next_to(l, UP, buff=0.35).set_z_index(3,True)
        c.set(color=GREEN) #indirect colouring again

        self.add(best_fit_label)
        self.play(Flash(best_fit_label, color=GREEN))
        self.wait(4)

        #progressive fading out of everything on screen, end of scene 4bis
        self.play(FadeOut(R_overfit), Unwrite(overfit_label),
                  FadeOut(R_underfit),  Unwrite(underfit_label),
                  Uncreate(l), Unwrite(best_fit_label))
        self.play(Uncreate(Training_curve), Unwrite(Training_label),
                  Uncreate(Test_curve), Unwrite(Test_label),
                  Unwrite(x_label), Unwrite(y_label))
        self.play(GrowFromPoint(axes, axes.get_origin(),
                                rate_func=lambda x:1-rate_functions.ease_in_out_sine(x),
                                remover=True))
        self.wait(1)