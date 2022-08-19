import json
import math
import pprint
from manim import *
from abc import ABC
from dataclasses import dataclass
from manim.utils.color import int_to_color
from collections import namedtuple, defaultdict

from sort import StepGenerator
# from bst import Node

@dataclass
class Node:
    data: Any
    parent: Any = None
    left: Any = None
    right: Any = None
    # def __init__(self, data: Any):
    #     self.data = data
    #     self.left = None
    #     self.right = None

class AnimationState(Scene):
    def __init__(self) -> None:
        super().__init__()

        with open('cfg.json', 'r') as f:
            data = json.load(f)

        self.sequence = data['sequence'] 
        self.scaling_coefficient = 1 / (math.log10(len(self.sequence)) + 1)

        # These generate the operations (algorithm steps)
        self.algorithm = data['algorithm']
        self.generator = StepGenerator(self.sequence)

        # These are needed for initializing mobjects
        self.obj_type = data['obj_type'].lower()
        self.vis_type = data['vis_type'].lower()
        
        self.create_data_mobjects()
        self.create_visualization_mobjects()
        self.add_updaters_to_visualization_mobjects()

        self.pp = pprint.PrettyPrinter()


    def create_data_mobjects(self):
        MobjectData = namedtuple('MobjectData', ['inst', 'val'])

        self.data = [MobjectData(inst=Integer(val), val=val) 
                     for val in self.sequence]

        inst_buffer = 14 / len(self.sequence) * self.scaling_coefficient

        temp = VGroup(*[data.inst for data in self.data])
        temp.arrange(buff=inst_buffer)
        
        if self.obj_type == 'bar': 
            temp.to_edge(DOWN)

    def create_visualization_mobjects(self):
        if self.obj_type == 'bar':
            width = 14 / len(self.sequence) * self.scaling_coefficient
            heights = [5 * data.val / max(self.sequence) for data in self.data]

            self.vis = [Rectangle(width=width, height=height) 
                        for height in heights]

        elif self.obj_type == 'node':
            radius = 6 / len(self.sequence) * self.scaling_coefficient
            self.vis = [Circle(radius=radius, color=WHITE) 
                        for _ in range(len(self.data))]

    def add_updaters_to_visualization_mobjects(self):
        if self.obj_type == 'bar':
            offset = 1
        elif self.obj_type == 'node':
            offset = 0

        for idx, vis in enumerate(self.vis):
            vis.add_updater(
                lambda mobj,
                i=idx: mobj.next_to(self.data[i].inst, offset*UP)
            )

    def reset_updaters(self)  -> None:
        for vis in self.vis:
            vis.remove_updater(vis.get_updaters())
        
        self.add_updaters_to_visualization_mobjects()

    def compare_data_values(self, idx1: int, idx2: int)  -> None:
        if self.obj_type == 'bar':
            self.indicator1 = SurroundingRectangle(
                self.data[idx1].inst,  color=YELLOW, buff=SMALL_BUFF
            )
            self.indicator2 = SurroundingRectangle(
                self.data[idx2].inst, color=YELLOW, buff=SMALL_BUFF
            )

            self.indicator1.add_updater(
                lambda mob: mob.move_to(self.data[idx1].inst.get_center())
            )
            self.indicator2.add_updater(
                lambda mob: mob.move_to(self.data[idx2].inst.get_center())
            )

            self.play(Create(self.indicator1), Create(self.indicator2))

        elif self.obj_type == 'node':
            self.indicator1, self.indicator2 = None, None 
            self.play(
                Indicate(self.vis[idx1]), 
                Indicate(self.vis[idx2])
            )

    def swap_data_positions(self, idx1: int, idx2: int) -> None:
        inst1 = self.data[idx1].inst
        inst2 = self.data[idx2].inst

        self.play(
            inst1.animate.move_to(inst2.get_center()),
            inst2.animate.move_to(inst1.get_center())
        )

        temp = self.data[idx1]
        self.data[idx1] = self.data[idx2]
        self.data[idx2] = temp

        temp = self.vis[idx1]
        self.vis[idx1] = self.vis[idx2]
        self.vis[idx2] = temp

        self.reset_updaters()

        if isinstance(self.indicator1, Mobject):
            self.uncreate_indicators()

    def get_subsequence_indexes(self, subsequence):
        first = [i for i, data in enumerate(self.data) if data.val == subsequence[0]]
        last = [i for i, data in enumerate(self.data) if data.val == subsequence[-1]]
        return first, last

    def group_subsequence(self, subsequence: list, side: str) -> None:
        print(side)
        if len(subsequence) > 1:
            if not side:
                self.bst = Node(self.data)
                self.head = self.bst
            elif side == 'left':
                self.head = self.head.left
            elif side == 'right':
                self.head = self.head.right

        print('')
        self.pp.pprint(self.bst) 
        print('')   
        self.pp.pprint(self.head)  

        print('')
        first, last = self.get_subsequence_indexes(subsequence)

        if self.head:
            mbjs = [vis for vis in self.vis[first[0]:last[-1]+1]] + \
                [data.inst for data in self.head.data[first[0]:last[-1]+1]]

            temp_group = VGroup(*mbjs)

            self.grouping_rect = SurroundingRectangle(
                temp_group, buff=MED_LARGE_BUFF
            )

            self.play(Create(self.grouping_rect))
        print('')

    def split_subseqeuence(self, left: list, right: list) -> None:
        lhi1, lhi2 = self.get_subsequence_indexes(left)
        rhi1, rhi2 = self.get_subsequence_indexes(right)
        
        self.head.left = Node(self.data[lhi1[0]:lhi2[-1]+1], parent=self.head)
        self.head.right = Node(self.data[rhi1[0]:rhi2[-1]+1], parent=self.head)

        
    def display_indicators(self, idx1: int, idx2: int) -> None:
        if isinstance(self.indicator1, Mobject):
            self.play(Create(self.indicator1), Create(self.indicator2))
        elif issubclass(self.indicator1, Transform):
            self.play(
                self.indicator1(self.vis[idx1]), 
                self.indicator2(self.vis[idx2])
            )

    def uncreate_indicators(self) -> None:
        self.play(Uncreate(self.indicator1), Uncreate(self.indicator2))

    def do_nothing(self, arg1: Any = None, arg2: Any = None) -> None:
        if isinstance(self.indicator1, Mobject):
            self.uncreate_indicators()

    def exit_recursion(self) -> None:
        if self.head and self.head.parent:
            self.head = self.head.parent
        self.pp.pprint(self.head)
        print('\n\n------------------ EXIT RECURSION -----------------------')

    def end(self, arg1: Any = None, arg2: Any = None) -> None:
        pass

    def construct(self):
        routines = {
            'Swap': self.swap_data_positions,
            'Compare': self.compare_data_values,
            'Group': self.group_subsequence,
            'Split': self.split_subseqeuence,
            'Continue': self.do_nothing,
            'ExitRecursion': self.exit_recursion,
            'End': self.end
        }

        self.play(*[Create(data.inst) for data in self.data],
                  *[Create(vis) for vis in self.vis])

        self.wait()
        
        for step in self.generator.algorithms[self.algorithm]():
            print(step)
            if step.arg1 is None and step.arg2 is None:
                routines[step.name]()
            elif step.arg1 is None or step.arg2 is None:
                routines[step.name](step.arg1)
            else:
                routines[step.name](step.arg1, step.arg2)
                
