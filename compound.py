#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Compound(MovingCameraScene):
    """
    this scene is used to create multiple small bits of animation used in the final project
    """
    def construct(self):

        #animation 1
        #display the texts 'Data', 'Model' and 'Prediction'

        data_text = Text("Data", font_size=40)
        model_text = Text("Model", font_size=40)
        prediction_text = Text("Prediction", font_size=40)

        def show(text):
            t = text.copy()
            self.play(Write(t))
            self.wait()
            self.play(Unwrite(t))
            self.wait()

        self.camera.frame.scale(0.3)
        self.wait()
        show(data_text)
        show(model_text)
        show(prediction_text)
        self.wait()

        #animation 1bis

        data_text.next_to(model_text, LEFT, buff=1)
        prediction_text.next_to(model_text, RIGHT, buff=1)
        T = [data_text, model_text, prediction_text]
        view = Group(*T)

        self.camera.frame.move_to(view).match_width(view).scale(1.2)

        for txt in T :
            self.play(Write(txt))
            self.wait()

        self.play(*[Unwrite(txt) for txt in T])
        self.wait()

        #animation 2
        #display 'f(individual characteristics) = final grade'

        formula = MathTex(r"f \phantom{.} ( \phantom{.} \text{individual ",
                          r"characteristics",
                          r"}) = ",
                          r"\text{final grade}")
        anchor = Rectangle().next_to(formula, LEFT)
        self.camera.frame.move_to(formula).match_width(formula).scale(1.7)
        self.play(Write(formula))
        self.wait()
        self.play(Circumscribe(formula[0][0]))
        self.wait()

        self.play(Circumscribe(formula[1]))
        self.play(FadeOut(formula[1], shift=UP))
        formula.become(MathTex(r"f \phantom{.} ( \phantom{.} \text{individual ",
                               r"\phantom{characteristics}",
                               r"}) = ",
                               r"\text{final grade}"))

        anchor.shift(LEFT*1.7)

        formula2 = MathTex(r"f \phantom{.} ( \phantom{.} \text{individual ",
                           r"\phantom{explanatory variables}",
                           r"}) = ",
                           r"\text{final grade}") \
            .next_to(anchor, RIGHT)

        enum1 = MathTex(r"&\text{explanatory variables}\\ &\text{covariates}\\ &\text{features}") \
            .next_to(formula2[0], RIGHT, buff=0.3) \
            .shift(DOWN * 0.7)
        bar1 = Line(start=enum1.get_corner(UP + LEFT), end=enum1.get_corner(DOWN + LEFT), color=LIGHT_GRAY,
                    fill_opacity=0.3) \
            .next_to(enum1, LEFT, buff=0.15)

        self.play(LaggedStart(TransformMatchingTex(formula, formula2), Create(bar1),
                              Write(enum1),
                              lag_ratio=0.8))
        self.wait()

        self.play(Circumscribe(formula2[3]))
        self.play(FadeOut(formula2[3], shift=UP))
        formula2.become(MathTex(r"f \phantom{.} ( \phantom{.} \text{individual ",
                                r"\phantom{explanatory variables}",
                                r"}) = ",
                                r"\phantom{\text{final grade}}")
                        .next_to(anchor, RIGHT))

        formula3 = MathTex(r"f \phantom{.} ( \phantom{.} \text{individual ",
                           r"\phantom{explanatory variables}",
                           r"}) = ",
                           r"\phantom{final grade}") \
            .next_to(anchor, RIGHT)

        enum2 = MathTex(r"&\text{target variables}\\ &\text{outcome}") \
            .next_to(formula2[2], RIGHT, buff=0.3) \
            .shift(DOWN * 0.35)
        bar2 = Line(start=enum2.get_corner(UP + LEFT), end=enum2.get_corner(DOWN + LEFT), color=LIGHT_GRAY,
                    fill_opacity=0.3) \
            .next_to(enum2, LEFT, buff=0.15)

        self.play(LaggedStart(TransformMatchingTex(formula2, formula3), Create(bar2), Write(enum2), lag_ratio=0.8))
        self.wait()
        self.play(*[FadeOut(m) for m in self.mobjects])


        #animation 3.1
        #diplay the formula for the Gini index
        
        self.wait()
        gini_formula = MathTex(r"\text{Gini} = 1-\sum_i \phantom{.} p_i^2")

        self.camera.frame.move_to(gini_formula).match_width(gini_formula).scale(1.7)

        self.play(Write(gini_formula, run_time=3))
        self.wait()
        self.play(FadeOut(gini_formula))
        self.wait()

        #animation 3.2
        #display the formula for the statistical entropy

        self.wait()
        entropy_formula = MathTex(r"\text{Entropy} = - \sum_{i} \phantom{.} p_i \phantom{.} log_2(p_i)")

        self.camera.frame.move_to(entropy_formula).match_width(entropy_formula).scale(1.7)

        self.play(Write(entropy_formula, run_time=3))
        self.wait()
        self.play(FadeOut(entropy_formula))
        self.wait()

        #animation 4
        #display a list of four items

        self.wait()
        txt_list = MathTex(r"&-\text{Random forest}\\", r"&-\text{Boosting}\\", r"&-\text{Survival trees}\\", r"&-\text{Longitudinal trees}")
        self.camera.frame.move_to(txt_list).match_width(txt_list).scale(1.5)
        self.play(AnimationGroup(*[Write(e) for e in txt_list], group=txt_list, lag_ratio=1))
        self.wait()
        self.play(FadeOut(txt_list))
        self.wait()

        #animation 5
        #display randomly organised texts

        self.wait()
        import random
        random.seed(69)
        texts = ["Bagging", "Random forest", "Boosting", "Adaboost", "XGBoost", "Catboost"]
        T = [Text(txt).scale(random.random()+0.5).shift((random.random()-0.5)*5*UP+(random.random()-0.5)*5*RIGHT) for txt in texts]
        T[0].scale(0.7)
        T[4].shift(LEFT * 2 + UP * 0.5)
        T[5].shift(LEFT * 3).scale(1.5)

        random.shuffle(T)

        G = VGroup(*T)
        self.camera.frame.move_to(G).match_width(G).scale(1.2)
        self.play(AnimationGroup(*[Write(g) for g in G], group=G, lag_ratio=0.7))
        self.wait()
        self.play(AnimationGroup(*[FadeOut(g) for g in G], group=G, lag_ratio=0.1))
        self.wait()


        #credits

        self.wait()
        thanks = Text("Thanks for watching !")
        credits_M = VGroup(Text("Text and voice : ", color=LIGHT_GREY), Text("Mathias Valla")).arrange_in_grid(1,2).scale(0.3)
        credits_F = VGroup(Text("Edition and equipment : ", color=LIGHT_GREY), Text("Fanny Gaucher")).arrange_in_grid(1,2).scale(0.3)
        credits_J = VGroup(Text("Animation : ", color=LIGHT_GREY), Text("Julien Crambes")).arrange_in_grid(1,2).scale(0.3)

        credits = VGroup(credits_M, credits_F, credits_J).arrange_in_grid(4, 1, cell_alignment=LEFT)
        view = VGroup(thanks, credits).arrange_in_grid(2, 1, buff=1)

        self.camera.frame.move_to(view).match_width(view).scale(1.2)

        self.play(Write(thanks), run_time=3)
        self.play(LaggedStart(*[Write(c) for c in credits], lag_ratio=0.5))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()
