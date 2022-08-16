import json
import math
from manim import *
from inspect import isclass
from collections import namedtuple

from sort import StepGenerator
from manim.utils.color import int_to_color

# Class structure:
# 1. All animator classes will need to load in a sequence of data from
#    a json file. They will also need to know which algorithm they are running.
# 2. Some algorithms are better visualized with bars and others with nodes.
#    We will need two separate methods for initializing each.


class Animator(Scene):
    def __init__(self):
        super().__init__()

        # Format json data
        with open('cfg.json', 'r') as f:
            data = json.load(f)

        sequence = data['sequence'].replace('[','').replace(']','').split(',')
        sequence = [int(val) for val in sequence]

        # Animation params
        self.sequence = sequence
        self.algorithm = data['algorithm']
        self.obj_type = data['obj_type'].lower()
        self.vis_type = data['vis_type'].lower()
        print(f"{data['text_render']=}")
        print(f"{type(data['text_render'])=}")
        self.generator = StepGenerator(self.sequence)
    
        # Mobject config
        seq_max = max(sequence)
        self.heights = [val / seq_max * 5 for val in sequence]
        self.scaling_factor = 1 / (math.log10(len(sequence))+1)
        self.width = 14 / len(sequence) * self.scaling_factor
        self.radius = 6 / len(sequence) * self.scaling_factor
        self.spacing = self.width / (math.log10(len(sequence))+1)

        # Mobject data structure
        self.DataTuple = namedtuple('DataPoint', ['obj', 'vis', 'val'])

        if self.vis_type == 'color':
            old_range = (max(sequence) - min(sequence))  
            new_range = (41 - 0)
            self.rgb = [int((val - min(sequence)) * new_range / old_range)
                        for val in sequence] 


    def create_data_mobjects(self) -> None:
        """
            Create the mobjects needed for visualization.
            
            Each value in the sequence needs to be assigned a manim 
            mobjects and a Rectangle mobject which is always placed next
            to it via an updater.   
        """
        self.data_points = []

        # Hacky workaround to variable number of zip iterators being relevant
        if self.vis_type != 'color':
            self.rgb = [0] * len(self.heights)
            

        for value, height, cint in zip(self.sequence, self.heights, self.rgb):
            if self.obj_type == 'bar':
                vis_mobj = Rectangle(width=self.width, height=height)
                vis_mobj.stroke_width = self.scaling_factor * 2
            elif self.obj_type == 'node':
                if self.vis_type == 'size':
                    pass
                elif self.vis_type == 'color':
                    vis_mobj = Circle(radius=self.radius, color=int_to_color[cint])

            self.data_points.append(
                self.DataTuple(
                    Integer(value).scale(self.scaling_factor+0.1),
                    vis_mobj,
                    value
                )
            )

        # Use a VGroup to arrange & align objects conveniently
        obj_group = VGroup(*[point.obj for point in self.data_points]) 
        obj_group.arrange(buff=self.width)
        if self.obj_type == 'bar':
            obj_group.to_edge(DOWN)

        for i in range(len(self.data_points)):
            self.refresh_updater(i)

    def refresh_updater(self, idx: int) -> None:
        if self.data_points[idx].vis.get_updaters():
            self.data_points[idx].vis.remove_updater(
                self.data_points[idx].vis.get_updaters()
            )

        if self.obj_type == 'bar':
            self.data_points[idx].vis.add_updater(
                lambda mob,
                i=idx: mob.next_to(self.data_points[i].obj, UP)
            )
        elif self.obj_type == 'node':
            self.data_points[idx].vis.add_updater(
                lambda mob,
                i=idx: mob.move_to(self.data_points[i].obj.get_center())
            )

    def swap_datapoints_inplace(self, idx1: int, idx2: int) -> None:
        temp = self.data_points[idx1]
        self.data_points[idx1] = self.data_points[idx2]
        self.data_points[idx2] = temp



class SortAnimation(Animator):
    def construct(self) -> None:
        self.create_data_mobjects()

        create_funcs = [[Create(point.obj), Create(point.vis)] 
                        for point in self.data_points]
   
        func_list = []
        for func in create_funcs:
            func_list.append(func[0])
            func_list.append(func[1])

        if self.obj_type == 'bar':
            self.b_size = 1
        elif self.obj_type == 'node':
            self.b_size = 2

        self.play(*func_list, run_time=1.2)
        self.wait()
        # Animation loop
        self.bubble_sort_animation()
        self.wait(2)

    def indicate_data_mobject(self, idx1: int, idx2: int) -> None: 
        if self.obj_type == 'bar':
            self.indicator1 = SurroundingRectangle(
                self.data_points[idx1].obj, 
                color=YELLOW, 
                buff=SMALL_BUFF
            )
            self.indicator2 = SurroundingRectangle(
                self.data_points[idx2].obj, 
                color=YELLOW, 
                buff=SMALL_BUFF
            )

            self.indicator1.add_updater(
                lambda mob: mob.move_to(
                    self.data_points[idx1].obj.get_center()
                )
            )
            self.indicator2.add_updater(
                lambda mob: mob.move_to(
                    self.data_points[idx2].obj.get_center()
                )
            )

        elif self.obj_type == 'node':
            self.indicator1 = Indicate
            self.indicator2 = Indicate

    # def 

    def bubble_sort_animation(self):
        def reset_frame(txt: Mobject):
            if isinstance(self.indicator1, Mobject):
                self.play(
                    Uncreate(txt), Uncreate(self.indicator1), 
                    Uncreate(self.indicator2), run_time=0.5    
                )
            else:
                self.play(Uncreate(txt), run_time=0.5)

            del self.indicator1
            del self.indicator2

        generator = self.generator.algorithms[self.algorithm]()

        for step in generator:
            self.indicators = []
            v1 = self.data_points[step.i1].val
            v2 = self.data_points[step.i2].val

            if step.name == 'Compare':
                t_str = f'{v1} < {v2} = ?'
                t = Text(t_str).scale(0.85)
                t.to_edge(self.b_size*UP)
                
                self.indicate_data_mobject(step.i1, step.i2)

                if isinstance(self.indicator1, Mobject):
                    self.play(
                        Create(t), Create(self.indicator1), 
                        Create(self.indicator2), run_time=0.5             
                    )
                elif isclass(self.indicator1):
                    self.play(
                        Create(t), 
                        self.indicator1(
                            self.data_points[step.i1].vis,
                            color=self.data_points[step.i1].vis.get_color()
                        ), 
                        self.indicator2(
                            self.data_points[step.i2].vis, 
                            color=self.data_points[step.i2].vis.get_color()), 
                        run_time=0.75             
                    )

                self.wait(0.5)
                
            if step.name == 'GT':
                t_str = f'{v1} < {v2} = False'
                t_res = Text(t_str).scale(0.85)
                t_res.to_edge(self.b_size*UP)
                self.play(ReplacementTransform(t,t_res))

                self.play(
                    self.data_points[step.i1].obj.animate.move_to(
                        self.data_points[step.i2].obj.get_center()
                    ),
                    self.data_points[step.i2].obj.animate.move_to(
                        self.data_points[step.i1].obj.get_center()
                    )    
                )

                self.swap_datapoints_inplace(step.i1, step.i2)
                self.refresh_updater(step.i1)
                self.refresh_updater(step.i2)

                reset_frame(t_res)
                            
            if step.name == 'LT':
                t_str = f'{v1} < {v2} = True'
                t_res = Text(t_str).scale(0.85)
                t_res.to_edge(self.b_size*UP)
                self.play(ReplacementTransform(t,t_res))

                reset_frame(t_res)

            if step.name == 'End':
                txt = 'Algorithm complete'
                t = Text(txt).scale(0.85)
                t.to_edge(self.b_size*UP)
                self.play(Create(t))

