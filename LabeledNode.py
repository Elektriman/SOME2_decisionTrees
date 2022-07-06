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

        #ajout de la partie textuelle aux sous-mobjects
        self.submobjects.append(text)

        #création de la forme du noeud
        shape = RoundedRectangle(corner_radius=min(text.height, text.width)*0.2,
                                                 height=text.height*1.3,
                                                 width=text.width*1.3,
                                                 fill_color=WHITE,
                                                 fill_opacity=1.,
                                                 z_index=text.z_index - 1)

        #ajout de la forme aux sous-mobjects
        self.submobjects.append(shape)

        #ajout d'un updater pour que la forme suive le texte (mvt + taille)
        def shape_updater(shape):
            #mise à jour de la taille
            shape.set(height = self.submobjects[0].height*1.2)
            shape.set(width = self.submobjects[0].width*1.2)
            #mise à jour de la position
            shape.match_coord(self.submobjects[0], 0)
            shape.match_coord(self.submobjects[0], 1)

        self.submobjects[1].add_updater(shape_updater)
        self.submobjects[1].update()

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