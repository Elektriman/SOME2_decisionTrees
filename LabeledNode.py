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
    """Classe personnalisée pour afficher des noeuds d'arbre avec du contenu
    """

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.fill_rgbas = [0, 0, 0, 0]
        self.stroke_rgbas = [0, 0, 0, 0]
        self.background_stroke_rgbas = [0, 0, 0, 0]

        #ajout de la partie textuelle aux sous-mobjects
        self.submobjects.append(text)

        #création de la forme du noeud
        shape = SurroundingRectangle(self.submobjects[0],
                                     corner_radius=0.07,
                                     fill_color=WHITE,
                                     color=WHITE,
                                     fill_opacity=1.,
                                     z_index=text.z_index - 1)

        #ajout de la forme aux sous-mobjects
        self.submobjects.append(shape)
        self.shape_updater()

    #ajout d'un updater pour que la forme suive le texte (mvt + taille)
    def shape_updater(self):
        #mise à jour de la position
        self.submobjects[1].match_coord(self.submobjects[0], 0)
        self.submobjects[1].match_coord(self.submobjects[0], 1)
        self.submobjects[1].match_height(SurroundingRectangle(self.submobjects[0],corner_radius=0.07))
        self.submobjects[1].match_width(SurroundingRectangle(self.submobjects[0],corner_radius=0.07))
        self.submobjects[1].set(z_index = self.submobjects[0].z_index -1)

    @override_animation(Create)
    def custom_create(self):
        """Modification de l'animation create pour un meilleur rendu

        Returns
        -------
        AnimationGroup
            Le groupe des animations à jouer, dans l'ordre, pour créer l'objet
        """
        anims = []#stockage des animations
        anims.append(DrawBorderThenFill(self.submobjects[1])) #on dessine la forme en premier
        anims.append(Write(self.submobjects[0])) #on écrit le texte une fois la forme tracée
        # le timing est calibré pour avoir l'écriture et le remplissage de la forme synchrones
        return AnimationGroup(*anims, group = self, lag_ratio=0.9)#utilisation de AnimationGroup pour éviter les erreurs de la fonction Create