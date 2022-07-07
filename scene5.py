#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import manimpango

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene5(MovingCameraScene):
    def construct(self):

        #construction de la figure initiale
        Txt = Text("M", color=RED, z_index=0).move_to([0,0,0]) #lettre M
        #rectangle
        R = SurroundingRectangle(Txt,
                                 corner_radius=0.07,
                                 fill_color=WHITE,
                                 color=LIGHT_GRAY,
                                 fill_opacity=1.,
                                 z_index=-1)
        #flèche
        A = Arrow(start=2*LEFT, end=2*RIGHT, stroke_width=1,
                  max_tip_length_to_length_ratio=0.05,
                  color=LIGHT_GRAY,
                  z_index=-3)

        self.camera.frame.scale_to_fit_width(A.width*2) #zoom
        self.add_foreground_mobjects(Txt, R) #mise au premier plan de le boite

        #création de la figure initiale
        Fig = Group(Txt, R, A)
        self.play(AnimationGroup(DrawBorderThenFill(R),Write(Txt),Create(A), group=Fig, lag_ratio=0.5))
        self.wait(2)

        import random
        random.seed(2209)
        #création des points pseudo-aléatoires
        P = [Dot([random.normalvariate(0,1)*(1/8), random.normalvariate(0,1)*1, 0] + 3*LEFT, color=random_color(), z_index=-2) for i in range(10)]
        Points = Group(*P)
        #apparition des points
        self.play(AnimationGroup(*tuple(GrowFromCenter(p) for p in P), group = Points, lag_ratio=0.1))
        self.wait(2)

        end_anchor = R.get_center()
        end_handle = R.get_left()
        start_handle = 3*LEFT
        paths = [CubicBezier(p.get_center(), start_handle, end_handle, end_anchor) for p in P]
        #les points rentrent dans la boite en suivant une courbe de bézier
        self.play(AnimationGroup(*tuple(MoveAlongPath(P[i], paths[i]) for i in range(len(P))), group=Points, lag_ratio=0.05))
        self.wait(2)

        #transformation des points en carrés
        for p in P :
            p.become(Square(p.width, fill_color=p.color, color=p.color, fill_opacity=1.).move_to(p.center()))

        #fabrication des destinations en sortie
        random.seed(69)
        P2 = [Dot([random.normalvariate(0, 1) * (1 / 8), random.normalvariate(0, 1) +0.2, 0] + 3 * RIGHT, z_index=-2) for i in range(10)]
        start_anchor = R.get_center()
        start_handle = R.get_right()
        end_handle = 3*RIGHT
        paths2 = [CubicBezier(start_anchor, start_handle, end_handle, p.get_center()) for p in P2]
        #sortie des carrés selon une courbe de bézier
        self.play(AnimationGroup(*tuple(MoveAlongPath(P[i], paths2[i]) for i in range(len(P))), group=Points, lag_ratio=0.3))
        self.wait(2)

        #changement de la police d'écriture de la boite
        with register_font("Labajo.ttf"):
            new_txt = Text("M", font="Labajo", color=RED)
            self.play(FadeOut(Txt, run_time=2))
            self.play(Write(new_txt, rate_function="rush_into", run_time=2))
        self.wait(2)