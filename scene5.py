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

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene5(MovingCameraScene):
    def construct(self):

        #initial figure

        Txt = Text("M", color=BLACK, z_index=0).move_to([0,0,0]) #lettre M
        R = SurroundingRectangle(Txt,
                                 corner_radius=0.07,
                                 fill_color=WHITE,
                                 color=WHITE,
                                 fill_opacity=1.,
                                 z_index=-1)
        A = Arrow(start=2*LEFT, end=2*RIGHT, stroke_width=1,
                  max_tip_length_to_length_ratio=0.05,
                  color=LIGHT_GRAY,
                  z_index=-3)

        self.camera.frame.scale_to_fit_width(A.width*2)
        self.add_foreground_mobjects(Txt, R)

        #animating the creation of the initial figure
        Fig = Group(Txt, R, A)
        self.play(AnimationGroup(DrawBorderThenFill(R),Write(Txt),Create(A), group=Fig, lag_ratio=0.5))
        self.wait(2)

        #choosing random positions for the representation of the data points
        import random
        random.seed(2209)

        P = [Dot([random.normalvariate(0,1)*(1/8), random.normalvariate(0,1)*1, 0] + 3*LEFT, color=random_color(), z_index=-2) for i in range(10)]
        Points = Group(*P)

        #apparition of the points
        self.play(AnimationGroup(*tuple(GrowFromCenter(p) for p in P), group = Points, lag_ratio=0.1))
        self.wait(2)

        #making a smooth path to make the points slide into the rectangle
        end_anchor = R.get_center()
        end_handle = R.get_left()
        start_handle = 3*LEFT
        paths = [CubicBezier(p.get_center(), start_handle, end_handle, end_anchor) for p in P]

        self.play(AnimationGroup(*tuple(MoveAlongPath(P[i], paths[i]) for i in range(len(P))), group=Points, lag_ratio=0.05))
        self.wait(2)

        #transformation of the points into squares
        for p in P :
            p.become(Square(p.width, fill_color=p.color, color=p.color, fill_opacity=1.).move_to(p.center()))

        #choosing random positions for the points after exiting the rectangle
        random.seed(69)
        P2 = [Dot([random.normalvariate(0, 1) * (1 / 8), random.normalvariate(0, 1) +0.2, 0] + 3 * RIGHT, z_index=-2) for i in range(10)]

        #creating smooth paths to make the points go out of the rectangle
        start_anchor = R.get_center()
        start_handle = R.get_right()
        end_handle = 3*RIGHT
        paths2 = [CubicBezier(start_anchor, start_handle, end_handle, p.get_center()) for p in P2]

        #points exit the rectangle as squares
        self.play(AnimationGroup(*tuple(MoveAlongPath(P[i], paths2[i]) for i in range(len(P))), group=Points, lag_ratio=0.3))
        self.wait(2)

        #changin the color of the rectangle to illustrate the concept of "Blackbox"
        R2 = SurroundingRectangle(Txt,
                                 corner_radius=0.07,
                                 fill_color=BLACK,
                                 stroke_color=WHITE,
                                 stroke_width=3,
                                 fill_opacity=1.,
                                 z_index=-1)

        self.play(R.animate.become(R2), Txt.animate.set_color(WHITE))
        self.wait()
        self.play(R2.animate.become(R), Txt.animate.set_color(BLACK))

        #changing the font inside the box to show different types of models
        #font Montserrat
        with register_font("Montserrat.ttf"):
            Montserrat_txt = Text("M", font="Montserrat", weight="BOLD", color=WHITE)
            self.play(GrowFromCenter(Txt, reverse_rate_function=True, remover=True, rate_function=slow_into))
            self.play(GrowFromCenter(Montserrat_txt, rate_function=slow_into))
        self.wait(2)

        #font Courrier New
        with register_font("Courier_New.ttf"):
            Courier_txt = Text("M", font="Courier New", color=WHITE)
            self.play(GrowFromCenter(Montserrat_txt, reverse_rate_function=True, remover=True, rate_function=slow_into))
            self.play(GrowFromCenter(Courier_txt, rate_function=slow_into))
        self.wait(2)

        #font Arjona
        with register_font("Arjona.ttf"):
            Arjona_txt = Text("m", font="Arjona", color=WHITE)
            self.play(GrowFromCenter(Courier_txt, reverse_rate_function=True, remover=True, rate_function=slow_into))
            self.play(GrowFromCenter(Arjona_txt, rate_function=slow_into))
        self.wait(2)

        #font Didot regular
        with register_font("Didot Regular.ttf"):
            Didot_txt = Text("M", font="Didot", color=WHITE)
            self.play(GrowFromCenter(Arjona_txt, reverse_rate_function=True, remover=True, rate_function=slow_into))
            self.play(GrowFromCenter(Didot_txt, rate_function=slow_into))
        self.wait(2)

        #empying the box
        self.play(FadeOut(Didot_txt), run_time=2)
        self.wait(2)