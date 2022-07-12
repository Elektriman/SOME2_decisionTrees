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

#configuration de la couleur d'arrière-plan
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene3(MovingCameraScene):
    def construct(self):
        #récupération des images dans le dossier img
        Rows = []
        path_of_the_directory = 'D:\Julien\Documents\projet vidéo maths 2022\code\img\dataset_parts'
        for filename in os.listdir(path_of_the_directory):
            f = os.path.join(path_of_the_directory, filename)
            if os.path.isfile(f):
                Rows.append(ImageMobject(f))

        ROW_HEIGHT = Rows[1].height
        ROW_WIDTH = Rows[1].width

        #apparition de la tête
        head = Rows[0]
        self.camera.frame.move_to(head).match_width(head).scale(1.1).shift(5*ROW_HEIGHT * DOWN)
        self.play(FadeIn(head))
        self.wait(1)

        #déplacement des lignes hors du champ de la caméra
        for r in Rows[1:] :
            r.next_to(self.camera.frame, DOWN)
            self.add(r)

        #apparition des lignes une à une par le bas
        Anims = ()
        for i in range(1, len(Rows)) :
            Anims+=(Rows[i].animate.move_to(((i-1)*ROW_HEIGHT + head.height)*DOWN), )
        G = Group(*Rows)

        self.play(AnimationGroup(*Anims, group = G, lag_ratio=0.2))
        self.wait(2)

        #animation du rectangle d'attention

        #paramètres du rectangle
        width = ValueTracker(0.6)
        height = ValueTracker(ROW_HEIGHT*10+head.height)
        x_coord = ValueTracker(-4.25)
        y_coord = ValueTracker(-1.6703703703703705)

        #utilisation de always redraw pour que les coins arrondis ne soient pas déformés par l'étirement du rectangle
        Focus = always_redraw(lambda: RoundedRectangle(width = width.get_value(),
                                                       height = height.get_value(),
                                                       corner_radius=0.05,
                                                       color=RED,
                                                       stroke_width=2).move_to([x_coord.get_value(), y_coord.get_value(), 0]))

        #création du rectangle sur la colonne des indices
        self.play(Create(Focus))
        self.wait(2)

        #déplacement sur les paramètres liés à la situation familiale
        self.play(x_coord.animate.increment_value(3.2), width.animate.set_value(4))
        self.wait(2)

        #déplacement sur la colonne absences
        self.play(x_coord.animate.increment_value(2.45), width.animate.set_value(0.85))
        self.wait(2)

        #déplacement sur les colonnes "moyenne" et "Passage ?"
        self.play(x_coord.animate.increment_value(2.25), width.animate.set_value(1.9))
        self.wait(4)

        #déplacement sur la ligne Alice
        self.play(x_coord.animate.set_value(Rows[1].get_x()),
                  y_coord.animate.set_value(Rows[1].get_y()),
                  height.animate.set_value(ROW_HEIGHT),
                  width.animate.set_value(Rows[1].width))
        self.wait(2)

        #déplacement sur toutes les données hors index et en-tête
        self.play(x_coord.animate.increment_value(0.35),
                  y_coord.animate.set_value(Rows[1].get_y()-4.5*ROW_HEIGHT),
                  height.animate.set_value(ROW_HEIGHT*10),
                  width.animate.set_value(ROW_WIDTH-0.7))
        self.wait(2)

        #on retire le rectangle, puis le tableau
        self.play(Uncreate(Focus))
        self.play(FadeOut(G))

        #ici est l'animation de la régression linéaire
        self.wait(3)

        #retour au tableau de données
        self.play(FadeIn(G))
        self.wait(1)

        #séparation des trois dernières lignes
        self.play(G[:8].animate.shift(0.5*UP), G[8:].animate.shift(0.5*DOWN))
        self.wait(2)

        # encadrement de la partie haute
        width.set_value(ROW_WIDTH)
        height.set_value(head.height + 7 * ROW_HEIGHT)
        x_coord.increment_value(-0.35)
        y_coord.set_value(-0.66)

        #recréation du Focus
        Focus = always_redraw(lambda: RoundedRectangle(width=width.get_value(),
                                                       height=height.get_value(),
                                                       corner_radius=0.05,
                                                       color=RED,
                                                       stroke_width=2).move_to([x_coord.get_value(), y_coord.get_value(), 0]))

        self.play(Create(Focus))
        self.wait(2)

        #déplacement sur la partie basse
        self.play(y_coord.animate.increment_value(-1 - height.get_value()/2 - 1.5 * ROW_HEIGHT),
                  height.animate.set_value(3*ROW_HEIGHT))
        self.wait(2)

        #on enlève le Focus
        self.play(Uncreate(Focus))
        self.wait(1)

        #fin de la scène
        self.play(FadeOut(G))