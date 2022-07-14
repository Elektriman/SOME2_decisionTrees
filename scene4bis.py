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
config.background_color = rgb_to_color(3 * (36 / 256,))


#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene4bis(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1.3)
        self.camera.frame.save_state()

        # création des axes
        axes = Axes(
            x_range=[0, 11],
            y_range=[0, 7],
            x_length=12,
            y_length=7,
            axis_config={"color": WHITE, "include_numbers": False, "include_ticks":False}
        ).set_z_index(3, True)
        x_label = Text("Model complexity", font_size=30).next_to(axes[0], DOWN, buff=0).set_z_index(3, True)
        y_label = Text("Error", font_size=30).next_to(axes[1], LEFT, buff=-0.35).rotate(90 * DEGREES).set_z_index(3, True)

        #création des axes
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)

        #ajout d'un cache sur la droite
        cache = Rectangle(fill_opacity=1,
                          stroke_opacity=0,
                          height=axes.height*1.4,
                          width=6.5,
                          fill_color=GRIS,
                          z_index=2) \
            .next_to(axes, RIGHT, buff=-0.4)

        self.add(cache)

        """
        fonction qui sert à placer le nom d'une courbe le long de cette dernière
        """
        def name(curve, n, label, place=UP):
            xa, ya, xb, yb = curve.points[n-10][0], curve.points[n-10][1], curve.points[n+10][0], curve.points[n+10][1]
            return Text(label, color=curve.color, font_size=20, z_index=1)\
                        .next_to(curve.points[n], place)\
                        .rotate(np.arctan((yb-ya)/(xb-xa)))

        #création de la courbe d'erreur sur l'entrainement
        Training_error = lambda x: 5 * np.exp(-x / 4)
        Training_curve = axes.plot(Training_error).set(color=BLUE, z_index=1)
        Training_label = name(Training_curve, 350, "Training Error")

        Anims = (Create(Training_curve), Write(Training_label))
        G = Group(Training_curve, Training_label)

        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.4))
        self.wait(1)

        # création de la courbe de test
        Test_error = lambda x: 0.1 * (x - 5) ** 2 - 0.1 * x + 4
        Test_curve = axes.plot(Test_error).set(color=ORANGE, z_index=1)
        Test_label = name(Test_curve, 350, "Test Error", place=DOWN)

        Anims = (Create(Test_curve), Write(Test_label))
        G = Group(Test_curve, Test_label)

        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.4))
        self.wait(1)

        """#création de la courbe d'erreur totale
        Total_error = lambda x: Training_error(x) + Test_error(x)
        Total_curve = axes.plot(Total_error).set(color=GREEN, z_index=1)
        Total_label = name(Total_curve, 350, "Total Error")

        self.play(Create(Total_curve), Write(Total_label))
        self.wait(1)"""

        R_underfit = Rectangle(fill_opacity=0.2,
                               stroke_opacity=0,
                               height=axes.height-0.5,
                               width=6.75,
                               fill_color=color_gradient([RED, GRIS], 2),
                               sheen_direction=RIGHT)\
            .move_to([axes[0].n2p(3.125)[0], -0.2, 0])

        R_overfit = Rectangle(fill_opacity=0.2,
                              stroke_opacity=0,
                              height=axes.height-0.5,
                              width=6.5,
                              fill_color=color_gradient([RED, GRIS], 2),
                              sheen_direction=LEFT) \
            .move_to([axes[0].n2p(9.75)[0], -0.2, 0])

        underfit_label = Text("Underfitting", color=RED, font_size=25).next_to(R_underfit, UP).set_z_index(3, True)
        overfit_label = Text("Overfitting", color=RED, font_size=25).next_to(R_overfit, UP).shift(LEFT).set_z_index(3, True)

        # animation de la recherche d'optimal

        #création d'un traceur pour l'abscisse de la ligne
        e = ValueTracker(5)

        c = Square(color=YELLOW) #la couleur de la ligne est indirectement changée avec la couleur de ce mobject
        l = always_redraw(lambda : axes.get_line_from_axis_to_point(
            point=[axes[0].n2p(e.get_value())[0], axes.get_top()[1] - 0.4, 0],
            index=0,
            color=c.color))
        l.set_z_index(2, True)

        # création de la ligne du placement du modèle
        self.play(Create(l))
        self.wait(1)

        #montrer l'underfitting
        self.play(e.animate.set_value(2), FadeIn(R_underfit), run_time=3)
        self.wait(0.5)
        self.play(Write(underfit_label))
        self.wait(2)

        #montrer l'overfitting
        self.play(FadeIn(R_overfit), e.animate.set_value(9.5), run_time=4)
        self.wait(0.5)
        self.play(Write(overfit_label))
        self.wait(2)

        #mise de la ligne de fitting au niveau du sweet spot
        #animation via une fontion personnalisée
        def rate_f(t):
            if t > 0.3:
                return 0.3 + rate_functions.ease_out_elastic((t - 0.3) / 0.7) * 0.7
            else:
                return rate_functions.rush_into(t / 0.3) ** (4.8) * 0.3
        self.play(e.animate.set_value(6.5), rate_func=rate_f, run_time=3)

        #texte et mise en forme du best fit
        best_fit_label = Text("Best Fit",
                              color=GREEN,
                              font_size=25).next_to(l, UP, buff=0.35).set_z_index(3,True)
        c.set(color=GREEN)
        self.add(best_fit_label)
        self.play(Flash(best_fit_label, color=GREEN))
        self.wait(4)

        #fin de la scène
        self.play(FadeOut(R_overfit), Unwrite(overfit_label),
                  FadeOut(R_underfit),  Unwrite(underfit_label),
                  Uncreate(l), Unwrite(best_fit_label))
        self.play(Uncreate(Training_curve), Unwrite(Training_label),
                  Uncreate(Test_curve), Unwrite(Test_label),
                  Unwrite(x_label), Unwrite(y_label))
        self.play(Uncreate(axes))
        self.wait(1)