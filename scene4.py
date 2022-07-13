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

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1.1)
        self.camera.frame.save_state()

        #création des axes
        axes = Axes(
            x_range=[0, 20, 2.5],
            y_range=[0, 20, 2.5],
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE, "include_numbers": True, "include_tip":False},
            z_index=2
        )

        # ajout des ticks et labels à l'origine
        axes[0].add_labels({0: "0.0"})
        axes[1].add_labels({0: "0.0"})
        x_origin_tick = axes[0].get_tick(0, 0.05).shift(DOWN * 0.04).set(z_index=2)
        y_origin_tick = axes[1].get_tick(0, 0.05).shift(LEFT * 0.04).set(z_index=2)
        Anims = (Create(axes), Create(x_origin_tick), Create(y_origin_tick))
        G = Group(axes, x_origin_tick, y_origin_tick)
        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.1))

        #extraction du tableau de points de données
        with open('.\imported_data\data', 'rb') as f:
            data = pickle.load(f)

        #ajout du tableau de données au schéma
        Anims=()
        G = ()
        X = np.linspace(0, 20, 100)
        for x, y in zip(data[0], data[1]):
            G += (Dot(axes.coords_to_point(x, y), z_index=2),)
            Anims += (GrowFromCenter(G[-1]),)
        self.play(AnimationGroup(*Anims, group=Group(*G), lag_ratio=0.15))

        #extraction des fonctions des models
        models = []
        for n in range(10):
            with open(f'.\imported_data\\func_{n}', 'rb') as f:
                models.append(pickle.load(f))

        #création de la courbe du modèle
        graph = axes.plot(models[1])

        #ajout de deux rectangles pour cacher les parties de la courbe qui dépassent du graphe
        h=10
        R_bot = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                          fill_opacity=1.,
                          color=rgb_to_color(3 * (36 / 256,)),
                          width=axes.width,
                          height=h,
                          z_index=1).next_to(axes, DOWN, buff=-0.5)

        R_bot_shadow = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                                 fill_opacity=0.6,
                                 color=rgb_to_color(3 * (36 / 256,)),
                                 width=axes.width,
                                 height=h,
                                 z_index=1).next_to(axes, DOWN, buff=-0.5)

        R_top = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                          fill_opacity=1.,
                          color=rgb_to_color(3 * (36 / 256,)),
                          width=axes.width,
                          height=h,
                          z_index=1).next_to(axes, UP, buff=0)

        R_top_shadow = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                                 fill_opacity=0.6,
                                 color=rgb_to_color(3 * (36 / 256,)),
                                 width=axes.width,
                                 height=h,
                                 z_index=1).next_to(axes, UP, buff=0)

        axes.set_z_index(2, True)
        self.add(R_bot, R_bot_shadow, R_top, R_top_shadow)

        #animation de la courbe du modèle et de l'indicateur
        self.play(Create(graph))
        n_tracker = ValueTracker(1)
        indi_line = NumberLine(x_range=[0,9,1],
                               length = axes[1].height*0.8,
                               rotation=90*DEGREES).next_to(axes, RIGHT, buff=1.5)
        indi_dot = always_redraw(lambda : Dot(point = indi_line.n2p(n_tracker.get_value())))
        indicateur_1 = always_redraw(lambda : MathTex(f'n = ').next_to(indi_dot, RIGHT))
        indicateur_2 = always_redraw(lambda: Integer(n_tracker.get_value()).next_to(indicateur_1, RIGHT))
        self.play(Create(indi_line), GrowFromCenter(indi_dot), Write(indicateur_1), Write(indicateur_2))
        self.wait(2)

        #exemple de lecture

        #création des lignes en inversant les lignes horizontales et en chngeant l'ordre des lignes pour l'animation de création
        E1 = axes.get_lines_to_point(point=axes.c2p(5, models[1](5)), color=RED)
        E2 = axes.get_lines_to_point(point=axes.c2p(20, models[1](20)), color=RED)
        E1 = VGroup(E1[1], E1[0].put_start_and_end_on(E1[0].end, E1[0].start))
        E2 = VGroup(E2[1], E2[0].put_start_and_end_on(E2[0].end, E2[0].start))
        #création des labels
        L1 = MathTex(r"6.5", font_size=axes[0].font_size, color=RED).next_to(E1[1], LEFT, buff=1)
        L2 = MathTex(r"19.9", font_size=axes[0].font_size, color=RED).next_to(E2[1], LEFT, buff=1)

        #animation des deux exemples en x=5 et x=20
        self.play(Create(E1))
        self.play(Write(L1))
        self.play(Create(E2))
        self.play(Write(L2))
        self.wait(2)
        self.play(Uncreate(E1), Unwrite(L1), Uncreate(E2), Unwrite(L2))
        self.wait(2)

        #évolution des modèles vers n=9
        self.change_model(9, axes, graph, models, n_tracker)

        #création des exemples pour le modèle n=9
        """V1 et V3 devraient aller à des points loin hors champ. On les coupe proche du cadre de la camera
        
        axes[0].n2p(4)[0] → 
            axes[0] : l'axe des x, 
            .n2p(4) : transforme un flottant (4) en le point sur correspondant sur l'axe,
            [0] : on ne garde que l'abscisse
        
        self.camera.frame.get_top()[1]+3, 0] →
            self.camera.frame : le rectangle de la camera,
            .get_top() : le point au millieu en haut du rectangle,
            [1] : on ne garde que l'ordonnée,
            +10 : on rejoute 10 de longueur pour un futur dézoom
        """
        V1 = axes.get_line_from_axis_to_point(index=0, point = [axes[0].n2p(4)[0], self.camera.frame.get_top()[1]+10, 0], color=RED)
        V2 = axes.get_lines_to_point(axes.c2p(14.7, models[-1](14.7)), color=RED)
        V3 = axes.get_line_from_axis_to_point(index=0, point = [axes[0].n2p(20)[0], self.camera.frame.get_bottom()[1]-10, 0], color=RED)

        V1.set(z_index=2)
        V2 = VGroup(V2[1], V2[0].put_start_and_end_on(V2[0].end, V2[0].start)).set(z_index=2)
        V3.set(z_index=2)

        #création des labels des axes
        L1_x = MathTex(r"4", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V1[0], DOWN, buff=0.7)
        L2_x = MathTex(r"14.5", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V2[0], DOWN, buff=0.7)
        L2_y = MathTex(r"14.7", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V2[1], LEFT, buff=1)
        L3_x = MathTex(r"20", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V3[0], DOWN+RIGHT, buff=0.5)

        #z_index bugué, il faut le reparamétrer manuellement
        V1.set_z_index(2, True)
        V2.set_z_index(2, True)
        V3.set_z_index(2, True)
        L1_x.set_z_index(2, True)
        L2_x.set_z_index(2, True)
        L2_y.set_z_index(2, True)
        L3_x.set_z_index(2, True)

        #exemple avec le modèle, pour la valeur 4
        self.play(Write(L1_x))
        self.play(Create(V1), R_top.animate.shift(10*UP), self.camera.frame.animate.scale(2).shift(UP*4), run_time=2)
        self.wait(1)
        self.play(Unwrite(L1_x), Uncreate(V1), R_top.animate.shift(10*DOWN), Restore(self.camera.frame))
        self.wait(1)

        # exemple avec le modèle, pour la valeur 14.7
        self.play(Write(L2_x))
        self.play(Create(V2))
        self.play(Write(L2_y))
        self.wait(1)
        self.play(Unwrite(L2_x), Uncreate(V2), Unwrite(L2_y))
        self.wait(1)

        # exemple avec le modèle, pour la valeur 20
        self.play(Write(L3_x))
        self.play(Create(V3), R_bot.animate.shift(10*DOWN), self.camera.frame.animate.scale(2).shift(DOWN*4), run_time=2)
        self.wait(2)

        #on retire les exemples
        self.play(Unwrite(L3_x), Uncreate(V3), R_bot.animate.shift(10*UP), Restore(self.camera.frame))
        self.wait(2)

        #ajustement de la valeur de n
        self.change_model(2, axes, graph, models, n_tracker, wait_time=0)
        self.wait(1)
        self.change_model(5, axes, graph, models, n_tracker, wait_time=0)
        self.wait(1)
        self.change_model(3, axes, graph, models, n_tracker, wait_time=0)
        self.wait(2)
        self.play(Flash(indi_dot, color=GREEN))
        self.wait(3)

        #fin de la scène
        self.play(FadeOut(graph),
                  FadeOut(indicateur_1), FadeOut(indicateur_2), Uncreate(indi_line), FadeOut(indi_dot))
        self.remove(R_top, R_top_shadow, R_bot, R_bot_shadow)
        self.play(*tuple(FadeOut(g) for g in G))
        self.play(Uncreate(axes), Uncreate(x_origin_tick), Uncreate(y_origin_tick))
        self.wait(2)

    def change_model(self, n_target:int, axes, graph, models, n_tracker, wait_time=2):
        n = int(n_tracker.get_value())
        if n<=n_target :
            dir = 1
        else :
            dir = -1
        for i in range(n, n_target+dir, dir):
            # évolution du modèle selon le degré max de la courbe "n"
            to_plot = axes.plot(models[i])
            self.play(graph.animate.become(to_plot), n_tracker.animate.set_value(i))
            self.wait(wait_time)