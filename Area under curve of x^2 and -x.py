from manimlib.imports import *
class V1(GraphScene,MovingCameraScene):
    CONFIG = {
        "camera_config": {"background_color":WHITE},
        "y_max": 0.5,
        "y_min": 0.001,
        "x_max": 4,
        "x_min": 0,
        "tick_size":0,
        "y_tick_frequency": 0.05,
        "x_tick_frequency": 2,
        "axes_color": BLACK,
        "graph_origin": ORIGIN,
        "y_axis_label": "$f(x)$",
        "x_axis_label": "$x$",
         "y_labeled_nums": np.array([]),
         "x_labeled_nums": np.array([]),
         "x_label_decimal": 0,
        "y_label_direction": LEFT,
        "x_label_direction": DOWN,
        "y_label_decimal": 2,
        "label_nums_color": BLACK,
        "x_label_color": RED,
        "y_label_color": BLUE,
    }
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)
    def get_dots(x, y, radius, color):
        return VGroup(*[Dot(radius=radius, color=color).move_to(self.coords_to_point(x[i], y[i]))
                        for i in range(x.size)
                        ])
    def get_lines(x, y, colors):
        return VGroup(*[Line(self.coords_to_point(x[i], y[i]), self.coords_to_point(x[i + 1], y[i + 1]),color=colors)
              for i in range(x.size - 1)
              ])
    def label_setups(self,x, y):
        self.x_max = np.amax(x) + 10 * np.amax(x) / 100
        self.y_max = np.amax(y) + 10 * np.amax(y) / 100
        self.x_min = np.amin(x) + 10 * np.amin(x) / 100
        self.y_min = np.amin(y) + 10 * np.amin(y) / 100
        self.y_labeled_nums = np.round(np.linspace(self.y_min, self.y_max, 5), 1)
        self.x_labeled_nums = np.round(np.linspace(self.x_min, self.x_max, 5), 0)
        self.setup_axes(animate=False)
        xx = VGroup(self.x_axis, self.y_axis)
        self.play(ShowCreation(xx),runtime = 4)

    def construct(self):

        def f(x):
            return -x
        def f2(x):
            return x**2
        min_x= 0
        max_x= 2
        self.graph_origin = ORIGIN + 1*DOWN + 2.5*LEFT
        self.label_setups(np.array([0, 2]), np.array([0, 4]))
        graph = self.get_graph(f,color=RED,x_min=min_x,x_max=max_x)
        graph_1 = self.get_graph(f2, color=RED, x_min=min_x, x_max=max_x)
        self.play(ShowCreation(graph),runtime= 3)
        self.wait(2)
        self.play(ShowCreation(graph_1))
        def get_rectangles(f,f_1,h,min_x,max_x,color):
            i= min_x
            line = Line(self.coords_to_point(i, f(i)), self.coords_to_point(i, 0), color=color)
            lines_1 = VGroup(*[Line(self.coords_to_point(i, f(i)), self.coords_to_point(i, f_1(i)), color=color)
                     for i in np.arange(min_x,max_x+h,h)
                     ])# Left line
            lines_4 = VGroup(*[Line(self.coords_to_point(i+h, f(i)), self.coords_to_point(i+h,  f_1(i)), color=color)
                               for i in np.arange(min_x, max_x, h)
                               ])#right line
            lines_2 = VGroup(*[Line(self.coords_to_point(i, f(i)), self.coords_to_point(i+h, f(i)), color=BLUE)
                               for i in np.arange(min_x,max_x,h)
                               ])#top line
            lines_3 = VGroup(*[Line(self.coords_to_point(i+h,  f_1(i)), self.coords_to_point(i,  f_1(i)), color=BLUE)
                               for i in np.arange(min_x,max_x, h)
                               ])#bottom line
            rectangles= VGroup(lines_1,lines_2,lines_3,lines_4)
            return rectangles
        k = 0.5
        rect= get_rectangles(f,f2,k,min_x,max_x,BLACK)
        self.play(ShowCreation(rect))
        i=0
        text = TextMobject("ss ", color=BLACK)
        while(i<5):
            k1=k
            k=k-k*0.5
            i=i+1
            print("The real value of k is: " + str(k))
            rect_1= get_rectangles(f,f2,k,min_x,max_x,BLACK)
            sum= 0
            x_1 = min_x
            while x_1 <= max_x:
                sum = sum + (f2(x_1) - f(x_1))*k
                x_1 = x_1 + k
            print(sum)
            self.remove((text))
            text = TextMobject(str(sum),color= BLACK).move_to(UP*3)
            self.play(ReplacementTransform(rect,rect_1),runtime = 3)
            self.play(Write(text))
            self.wait(2)
            rect=rect_1
        self.wait(3)
        integral_text = TexMobject(r"\int_0^2 x^2  - (-x) dx",color= BLACK).next_to(LEFT_SIDE + UP*3)
        t2= TexMobject(r"= [\frac{x^3}{3} + \frac{x^2}{2}]_0^2",color= BLACK).next_to(integral_text,DOWN,buff = MED_SMALL_BUFF)
        t3 = TexMobject(r"= [\frac{8}{3} + \frac{4}{2}]", color=BLACK).next_to(t2, DOWN,buff=MED_SMALL_BUFF)
        t4 = TexMobject(r"= [2.66... + 2]", color=BLACK).next_to(t3, DOWN, buff=MED_SMALL_BUFF)
        t5 = TexMobject(r"= 4.66....", color=BLACK).next_to(t4, DOWN, buff=MED_SMALL_BUFF)
        self.play(Write(integral_text))
        self.wait(2)
        self.play(Write(t2))
        self.wait(2)
        self.play(Write(t3))
        self.wait(2)
        self.play(Write(t4))
        self.wait(2)
        self.play(Write(t5))
        self.wait(2)
