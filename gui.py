import json
import random
import subprocess
from collections import namedtuple
from dearpypixl import Application, Viewport
from dearpypixl.items.containers import Window, ChildWindow, CollapsingHeader
from dearpypixl.items.basic import Text, Button, Combo, InputText, InputInt, InputIntMulti, Checkbox
from dearpypixl.items.misc import Spacer


class SortingConfig:
    def __init__(self, parent) -> None:
        self.qualities = {
            'Low': 'l',
            'Medium': 'm',
            'High': 'h',
            'Ultra': 'p',
            '4k': 'k',
        }
        self.cli_call = 'manim -pql animator.py SortAnimation'

        with parent:
            # Instructions heading
            cfg = {'label': 'Instructions', 'default_open': True}
            with CollapsingHeader(**cfg):
                # Instruction details
                instructions = (
                    '1. Choose a sorting algorithm from the dropdown box'
                    ' labelled "Algorithm"\n'
                    '2. Define a sequence that the algorithm will be applied to\n'
                    '\ta. Manually define the sequence by typing a comma separated '
                    'sequence of integers into the input field labelled '
                    '"Input sequence"\n'
                    '\tb. Randomly generate a sequence of length n using the '
                    ''
                )
                Text(instructions)

            cfg = {'label': 'Algorithms settings', 'default_open': True}
            with CollapsingHeader(**cfg):
                # Algorithm select dropdown menu
                cfg = {
                    'label': 'Algorithm',
                    'items': ['Bubble sort', 'Merge sort', 'Insertion sort'],
                }
                self.cmb_algo = Combo(**cfg)


                # Manual input box
                cfg = {
                    'label': 'Input sequence'
                }
                self.int_seq = InputText(**cfg)
                    
                # Random sequence generator controls
                # Sequence length
                cfg = {
                    'label': 'Sequence length',
                    'default_value': 3,
                    'min_value': 0,
                    'max_value': 999 
                }
                self.ini_seq_len = InputInt(**cfg)

                # Value range
                cfg = {
                    'label': 'Value range (min, max)',
                    'default_value': [1, 100],
                    'min_value': 0,
                    'max_value': 999,
                    'size': 2
                }
                self.iim_seq_range = InputIntMulti(**cfg)

                # Generate button
                cfg = {
                    'label': 'Generate sequence',
                    'callback': self.generate_sequence
                }
                self.btn_seq_gen = Button(**cfg)

            cfg = {'label': 'Animation settings', 'default_open': True}
            with CollapsingHeader(**cfg):
                cfg = {
                    'label': 'Video Quality',
                    'items': ['Low', 'Medium', 'High', 'Ultra', '4k'],
                    'default_value': 'Low',
                    'callback': self.update_cli_call
                }
                self.cmb_qual = Combo(**cfg)

                cfg = {
                    'label': 'Object type',
                    'items': ['Bar', 'Node'],
                    'default_value': 'Bar',
                    'callback': self.add_remove_vis_type
                }
                self.cmb_obj_type = Combo(**cfg)

                cfg = {
                    'label': 'Variable characteristic',
                    'items': ['Size', 'Color'],
                    'default_value': 'Size',
                    'show': False
                }
                self.cmb_vis_type = Combo(**cfg) 

                cfg = {
                    'label': 'Display step text',
                    'default_value': True
                }
                self.chk_disp_txt = Checkbox(**cfg)


    def generate_sequence(self) -> None:
        self.int_seq.value = [random.randint(*self.iim_seq_range.value[:2]) 
                              for _ in range(self.ini_seq_len.value)]
        
    def write_cfg_file(self) -> None:
        cfg = {
            'algorithm': self.cmb_algo.value,
            'sequence': self.int_seq.value,
            'obj_type': self.cmb_obj_type.value,
            'vis_type': self.cmb_vis_type.value,
            'text_render': self.chk_disp_txt.value
        }
        with open('cfg.json', 'w') as f:
            json.dump(cfg, f)

    def update_cli_call(self) -> None:
        quality = self.qualities[self.cmb_qual.value]

        self.cli_call = f'manim -pq{quality} animator.py SortAnimation'

    def add_remove_vis_type(self, sender) -> None:
        if self.cmb_obj_type.value == 'Bar':
            self.cmb_vis_type.show = False
            # if hasattr(self, 'cmb_vis_type'):
            #     self.cmb_vis_type.delete()
            #     del self.cmb_vis_type
        elif self.cmb_obj_type.value == 'Node':
            # cfg = {
            #     'label': 'Variable characteristic',
            #     'items': ['Size', 'Color'],
            #     'default_value': 'Size',
            # }
            # with sender.parent:
            self.cmb_vis_type.show = True 

class GUI(Application, Viewport):
    def __init__(self) -> None:
        self.w = {}
        with Window() as self.main_window:
            
            tasks = ['Sorting', 'String', 'Array']
            Combo(tasks, default_value=tasks[0], label='Task', 
                  callback=self.change_task)
            
            with ChildWindow(height=700) as self.config:
                pass

            Button('Create Animation', callback=self.animate)

        self.change_task(None, tasks[0])
        self.primary_window = self.main_window

    def animate(self) -> None:
        self.task_cfg.write_cfg_file()
        if self.task == 'Sorting':
            subprocess.run(self.task_cfg.cli_call)


    def change_task(self, sender, app_data) -> None:
        self.task = app_data 

        if self.task == 'Sorting':
            self.task_cfg = SortingConfig(parent=self.config)

    def update_animation_config(self) -> None:
        pass

if __name__ == '__main__':
    gui = GUI()
    gui.start()