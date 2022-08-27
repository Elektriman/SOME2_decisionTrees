#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene19(MovingCameraScene):
    """
    this scene shows the confusion matrix and the result of our special case application
    """
    def construct(self):
        values = [14, 26, 2, 57] # values of the confusion matrix
        C = color_gradient([WHITE, rgb_to_color((0/256, 50/256, 103/256))], 58) # blue color gradient
        colors = [C[v] for v in values] # get the color corresponding to the value

        R = [Rectangle(fill_color=c,
                       fill_opacity=1.,
                       stroke_width=0,
                       width=5,
                       height=4,
                       z_index=1) for c in colors] # colored matrix cell

        matrix = VGroup(*R).arrange_in_grid(2, 2, buff=0) # matrix-like disposition
        # copy of the matrix with white rectangles for initialisation
        init = VGroup(*[r.copy().set(fill_color=WHITE) for r in R]).arrange_in_grid(2, 2, buff=0)

        # add disaplay of the value in each matrix cell, initialised at 0 and incremented afterwards
        trackers = [ValueTracker(0) for r in R] # track the value for each cell
        counts = [Integer(0).move_to(r).set_color(BLACK) for r in R] # display the value
        C = Circle(color=BLACK, stroke_width=0) # store the color for the last integer mobject that will become white

        # link the value tracker with its corresponding display mobject
        counts[0].add_updater(lambda m: m.set_value(trackers[0].get_value()).set_z_index(2, True))
        counts[1].add_updater(lambda m: m.set_value(trackers[1].get_value()).set_z_index(2, True))
        counts[2].add_updater(lambda m: m.set_value(trackers[2].get_value()).set_z_index(2, True))
        counts[3].add_updater(lambda m: m.set_value(trackers[3].get_value()).set_z_index(2, True).set_color(C.color))

        # add a set of axes
        axes = Axes(
            x_range = [0, 2],
            y_range = [0, 2],
            x_length = 10,
            y_length = 8,
            axis_config = {"include_tip":False, "include_ticks":False, "exclude_origin_tick":False},
            color=LIGHT_GREY
        ).set_z_index(0)

        # label the axis
        x_label = Text("Predicted values", font_size=30).next_to(axes[0], DOWN, buff=1.5)
        y_label = Text("Actual values", font_size=30).rotate(-90*DEGREES).next_to(axes[1], LEFT, buff=1.5)

        # add a legend for each row / column value
        x_fail = Text("FAIL", font_size=25).next_to(R[2], DOWN, buff=0.3)
        x_pass = Text("PASS", font_size=25).next_to(R[3], DOWN, buff=0.3)
        y_fail = Text("FAIL", font_size=25).next_to(R[0], LEFT, buff=0.1).rotate(-90*DEGREES)
        y_pass = Text("PASS", font_size=25).next_to(R[2], LEFT, buff=0.1).rotate(-90*DEGREES)

        # add a title
        title = Text("Confusion matrix", font_size=50).next_to(matrix, UP, buff=2)

        # adjust camera view
        view = Group(title, matrix, x_label)
        self.camera.frame.move_to(view).match_height(view).scale(1.1)

        # create the axes, show title, show labels, add the matrix cells
        self.play(LaggedStart(Write(title),
                              Create(axes),
                              AnimationGroup(*[Write(l) for l in [x_label, y_label, x_fail, x_pass, y_fail, y_pass]]),
                              AnimationGroup(*[DrawBorderThenFill(r) for r in init], group=init, lag_ratio=0.2),
                              lag_ratio=1))

        # write the values in the cells
        self.play(*[Write(count) for count in counts])
        self.wait()

        # increment each value untill the cell match the value in "values"
        for i in range(4):
            if i<3 :
                self.play(Transform(init[i], R[i]),
                          trackers[i].animate.set_value(values[i]),
                          rate_func=linear)
            else :
                # special case for the 4th cell that needs to change font color to WHITE because the cell color is too dark
                self.play(Transform(init[i], R[i]),
                          trackers[i].animate.set_value(values[i]),
                          C.animate.set_color(WHITE),
                          rate_func=linear)
            self.wait()

        # shift camera to the right to show a formula
        self.play(self.camera.frame.animate.shift(RIGHT*4))
        self.wait()

        # remove updaters, the numbers are frozen untill the end of scene
        for c in counts :
            c.clear_updaters()

        # formula for the computation of the precision of the model
        formula = MathTex(r"\text{true positive}", "+", r"\text{true negative}",
                          "\over",
                          r"\text{true positive}", "+", r"\text{true negative}", " + ", r"\text{false positive}", " + ", r"\text{false negative}")\
            .scale(0.7).next_to(matrix, RIGHT, buff=0.5).set_z_index(2, True)

        # color the elements of the formula
        f_color = [GREEN, WHITE, RED, WHITE, GREEN, WHITE, RED, WHITE, ORANGE, WHITE, ORANGE]
        for f,c in zip(formula, f_color):
            f.set_color(c)

        # each cell gives an element of the formula,
        # each element of the formula is transformed from its corresponding element in the matrix
        self.play(LaggedStart(TransformFromCopy(counts[0], formula[2]),
                              TransformFromCopy(counts[3], formula[0]),
                              TransformFromCopy(counts[0], formula[6]),
                              TransformFromCopy(counts[3], formula[4]),
                              TransformFromCopy(counts[1], formula[8]),
                              TransformFromCopy(counts[2], formula[10]),
                              *[Write(formula[i]) for i in [1,3,5,7,9]]),
                              lag_ratio=2)
        self.wait()

        # abreviation of the formula
        formula2 = MathTex(r"\text{TP}", " + ", r"\text{TN}",
                          "\over",
                          r"\text{TP}", " + ", r"\text{TN}", " + ", r"\text{FP}", " + ", r"\text{FN}") \
            .next_to(matrix, RIGHT, buff=0.5).set_z_index(2, True)
        # same coloring
        for f, c in zip(formula2, f_color):
            f.set_color(c)

        # transform the formula into its abreviation, reframe camera accordingly
        self.play(self.camera.frame.animate.shift(LEFT*1.5),
                  *[Transform(f, f2) for f,f2 in zip(formula, formula2)])
        self.wait()

        # write the evaluation for our special case
        result = MathTex(r"\approx ", "72", "\%").next_to(formula2, RIGHT)
        self.play(Write(result))

        # highlight the result in green
        result[1].set_color(GREEN)
        self.play(Flash(result[1], color=GREEN, flash_radius=result.width/3))
        self.wait()

        # fade out everything, end of scene
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()