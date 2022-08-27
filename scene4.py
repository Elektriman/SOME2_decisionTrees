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

# background color
config.background_color = rgb_to_color(3*(36/256,))

#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class Scene4(MovingCameraScene):
    """
    this scene shows the basics of what a model is, and introduces the concepts of overfitting and underfitting
    """
    def construct(self):
        #camera inital settings
        self.camera.frame.scale(1.1).shift(DOWN*0.3)
        self.camera.frame.save_state()

        #creating axis
        axes = Axes(
            x_range=[0, 20, 2.5],
            y_range=[0, 20, 2.5],
            x_length=6,
            y_length=6,
            axis_config={"color": LIGHT_GREY, "include_numbers": True, "include_tip":False},
        ).set_z_index(2, True)
        x_label = Text("first semester grade", font_size=25).next_to(axes[0], DOWN, buff=0.6).set_z_index(2, True).shift(0.5*LEFT)
        y_label = Text("final grade", font_size=25).next_to(axes[1], LEFT, buff=-0.2).rotate(90*DEGREES).set_z_index(2, True)

        #adding ticks at the origin
        axes[0].add_labels({0: "0.0"})
        axes[1].add_labels({0: "0.0"})
        x_origin_tick = axes[0].get_tick(0, 0.05).shift(DOWN * 0.04).set_z_index(2, True)
        y_origin_tick = axes[1].get_tick(0, 0.05).shift(LEFT * 0.04).set_z_index(2, True)
        
        #play creation animation
        Anims = (Create(axes), Create(x_origin_tick), Create(y_origin_tick), Create(x_label), Create(y_label))
        G = Group(axes, x_origin_tick, y_origin_tick, x_label, y_label)
        self.play(AnimationGroup(*Anims, group=G, lag_ratio=0.1))

        #importing the data points
        with open('.\imported_data\data', 'rb') as f:
            data = pickle.load(f)

        #scatter the data on the plot
        Anims=()
        G = ()
        for x, y in zip(data[0], data[1]):
            G += (Dot(axes.coords_to_point(x, y), z_index=2),)
            Anims += (GrowFromCenter(G[-1]),)

        self.play(AnimationGroup(*Anims, group=Group(*G), lag_ratio=0.15))

        #importing the model functions
        """
        the functions are in reality polynomials of degree n ranging from 0 to 9 that approximate best the data points
        """
        models = []
        for n in range(10):
            with open(f'.\imported_data\\func_{n}', 'rb') as f:
                models.append(pickle.load(f))

        #creating the curve object of the model function
        graph = axes.plot(models[1])

        #trick to prevent the curve to be displayed outside the plot on the up/down directions
        #I added two rectangles that will cover the curve if it exits the boundaries of the plot
        h=10
        R_bot = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                          fill_opacity=1.,
                          stroke_opacity=0,
                          width=axes.width,
                          height=h,
                          z_index=1).next_to(axes, DOWN, buff=-0.5)

        R_top = Rectangle(fill_color=rgb_to_color(3 * (36 / 256,)),
                          fill_opacity=1.,
                          stroke_opacity=0,
                          width=axes.width,
                          height=h,
                          z_index=1).next_to(axes, UP, buff=0)

        axes.set_z_index(2, True)
        self.add(R_bot, R_top)

        #creating the model curve
        self.play(Create(graph))

        #adding an indicater on the right to show the model complexity
        n_tracker = ValueTracker(1)
        indi_line = NumberLine(x_range=[0,10,1],
                               length = axes[1].height*0.9,
                               include_ticks = False,
                               include_tip = True,
                               color=LIGHT_GREY,
                               rotation=90*DEGREES).next_to(axes, RIGHT, buff=2)
        indi_label = Text("Model complexity", font_size=25).next_to(indi_line, DOWN)
        c = Mobject(color=WHITE)
        indi_dot = always_redraw(lambda : Dot(point = indi_line.n2p(n_tracker.get_value()), color=c.color))
        """
        indi_dot is defined with always_redraw so I can't use set_color to change its color because it will be redrawn.
        so I use another mobject as storage for indi_dot's color, here such mobject is c.
        """
        
        self.play(Create(indi_line), GrowFromCenter(indi_dot), Write(indi_label))
        self.wait(2)

        #examples of readings on the plot

        #creating lines from the axis 
        #(we change the start and end of the second line for the create animation to be correct)
        E1 = axes.get_lines_to_point(point=axes.c2p(5, models[1](5)), color=RED)
        E2 = axes.get_lines_to_point(point=axes.c2p(20, models[1](20)), color=RED)
        E1 = VGroup(E1[1], E1[0].put_start_and_end_on(E1[0].end, E1[0].start))
        E2 = VGroup(E2[1], E2[0].put_start_and_end_on(E2[0].end, E2[0].start))
        #creating labels
        L1 = MathTex(r"6.1", font_size=axes[0].font_size, color=RED).next_to(E1[1], LEFT, buff=1)
        L2 = MathTex(r"19.9", font_size=axes[0].font_size, color=RED).next_to(E2[1], LEFT, buff=1)

        #animation of the two examples for x=6.1 and x=19.9
        self.play(Create(E1))
        self.play(Write(L1))
        self.play(Create(E2))
        self.play(Write(L2))
        self.wait(2)
        self.play(Uncreate(E1), Unwrite(L1), Uncreate(E2), Unwrite(L2))
        self.wait(2)

        #highlight the points above then below the model
        lower = Group(*[G[i] for i in [0, 2, 4, 7, 9]])
        upper = Group(*[G[i] for i in [1, 3, 5, 6, 8]])
        self.play(Indicate(upper, scale_factor=1), run_time=1)
        self.wait()
        self.play(Indicate(lower, scale_factor=1), run_time=1)
        self.wait()

        #add error lines from data to model
        Err = []
        for i in range(len(G)):
            Err.append(DashedLine(dashed_ratio=0.6,
                                  color=YELLOW,
                                  stroke_width=2,
                                  z_index=0,
                                  start=axes.input_to_graph_point(data[0][i], graph),
                                  end=G[i].get_center()))
        Error_lines = Group(*Err)
        
        self.play(*[Create(e) for e in Err])
        self.wait()
        self.play(*[e.animate.set_color(LIGHT_GREY) for e in Err])
        self.wait(2)

        #evolution of the plot to a more complex model curve
        self.change_model(9, axes, graph, models, n_tracker, Error_lines)

        #creationg examples for the most complex model
        """ V1 and V3 should map to points out of the camera frame. we cut the lines near the frame border
        
        axes[0].n2p(4)[0] → 
            axes[0] : x axis, 
            .n2p(4) : maps a float (4) to the matching point on the axis,
            [0] : we keep only the x coordinate
        
        self.camera.frame.get_top()[1]+3, 0] →
            self.camera.frame : camera frame,
            .get_top() : get the point on the middle on the top segment,
            [1] : keep only the y coordinate,
            +10 : shift it because we will unzoom
        """
        #creating the lines
        V1 = axes.get_line_from_axis_to_point(index=0, point = [axes[0].n2p(4)[0], self.camera.frame.get_top()[1]+10, 0], color=RED)
        V2 = axes.get_lines_to_point(axes.c2p(14.7, models[-1](14.7)), color=RED)
        V3 = axes.get_line_from_axis_to_point(index=0, point = [axes[0].n2p(20)[0], self.camera.frame.get_bottom()[1]-10, 0], color=RED)
        
        #changing the order of some lines for the create function to animate correctly
        V1.set(z_index=2)
        V2 = VGroup(V2[1], V2[0].put_start_and_end_on(V2[0].end, V2[0].start)).set(z_index=2)
        V3.set(z_index=2)

        #create labels
        L1_x = MathTex(r"4", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V1[0], DOWN, buff=0.7)
        L2_x = MathTex(r"14.5", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V2[0], DOWN, buff=0.7)
        L2_y = MathTex(r"14.7", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V2[1], LEFT, buff=1)
        L3_x = MathTex(r"20", font_size=axes[0].font_size, color=RED, z_index=2).next_to(V3[0], UP, buff=0.5)

        #z_index behaviour wrong so I set it manually
        V1.set_z_index(1, True)
        V2.set_z_index(1, True)
        V3.set_z_index(1, True)
        L1_x.set_z_index(2, True)
        L2_x.set_z_index(2, True)
        L2_y.set_z_index(2, True)
        L3_x.set_z_index(2, True)

        #example for the value x=4
        self.play(Write(L1_x))
        self.play(Create(V1), R_top.animate.shift(10*UP), self.camera.frame.animate.scale(2).shift(UP*4), run_time=2)
        self.wait()
        self.play(Unwrite(L1_x), Uncreate(V1), R_top.animate.shift(10*DOWN), Restore(self.camera.frame))
        self.wait()

        #example for the value x=14.7
        self.play(Write(L2_x))
        self.play(Create(V2))
        self.play(Write(L2_y))
        self.wait()
        self.play(Unwrite(L2_x), Uncreate(V2), Unwrite(L2_y))
        self.wait()

        #example for the value x=20
        self.play(Write(L3_x))
        self.play(Create(V3), R_bot.animate.shift(10*DOWN), self.camera.frame.animate.scale(2).shift(DOWN*4), run_time=2)
        self.wait()
        self.play(Unwrite(L3_x), Uncreate(V3), R_bot.animate.shift(10*UP), Restore(self.camera.frame))
        self.wait(2)

        #adjusting the model's complexity
        self.change_model(2, axes, graph, models, n_tracker, Error_lines, wait_time=0)
        self.wait()
        self.change_model(5, axes, graph, models, n_tracker, Error_lines, wait_time=0)
        self.wait()
        self.change_model(3, axes, graph, models, n_tracker, Error_lines, wait_time=0)
        self.wait(2)
        self.play(Flash(indi_dot, color=GREEN), indi_dot.animate.set_color(GREEN), c.animate.set_color(GREEN))
        self.wait(3)

        #end of scene
        self.play(FadeOut(graph), FadeOut(Error_lines), Uncreate(indi_line), FadeOut(indi_dot), FadeOut(indi_label))
        self.remove(R_top, R_bot)
        self.play(*[FadeOut(g) for g in G])
        self.play(Uncreate(axes), Uncreate(x_origin_tick), Uncreate(y_origin_tick), FadeOut(x_label), FadeOut(y_label))
        self.wait(2)

    def change_model(self, n_target:int, axes:Axes, graph:Graph, models:list[function], n_tracker:ValueTracker, error_lines, wait_time=2):
        """animates the model to match the complexity identified with the n value

        Parameters
        ----------
        n_target : int
            target complexity
        axes : Axes
            axes mobject on which to plot the model
        graph : Graph
            the currently displayed curve
        models : list[function]
            the list of all the anonymous functions that represent the different models
        n_tracker : ValueTracker
            the value of the current model complexity displayed
        error_lines
            the Group mobject of all the error lines that need to be updated when the model changes
        wait_time
            additionnal parameter that allows the animation from a complexity value to another to go faster or slower
        """
        n = int(n_tracker.get_value())

        #decision about wether the direction must be toward the greater values or the lesser values
        #aka going from complexity 3 to 7 is going positive, 7 to 3 is negative
        if n<=n_target :
            dir = 1
        else :
            dir = -1

        for i in range(n, n_target+dir, dir):
            # replotting the curve
            to_plot = axes.plot(models[i])

            #redrawing the error lines
            err_line_anim = []
            for e in error_lines :
                err_line_anim.append(e.animate.become(DashedLine(dashed_ratio=e.dashed_ratio,
                                                                 stroke_width=1,
                                                                 z_index=0,
                                                                 color=e.color,
                                                                 start=axes.input_to_graph_point(axes.p2c(e.start)[0], to_plot),
                                                                 end=e.end)))

            #animating the transition
            self.play(graph.animate.become(to_plot), n_tracker.animate.set_value(i), *err_line_anim)
            self.wait(wait_time)