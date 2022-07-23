from dearpypixl.items.containers import Window, ChildWindow, Group
from dearpypixl.items.basic import Text, InputInt, Button, RadioButton, Checkbox
from dearpypixl.items.misc import Spacer


class SequenceGenerator(Window):
    def __init__(self) -> None:
        self.cfg = {
            'label': 'Sequence generator',
            'min_size': [400, 200],
            'events': True
        }
        super().__init__(**self.cfg)

        self.sequence = None

        with self:
            self.inp_length = InputInt('Number of items', default_value=20)
            self.inp_max = InputInt('Maximum value', default_value=100)
            self.inp_rng_seed = InputInt('RNG seed', default_value=0)

            Text('Sequence config:')
            with Group(horizontal=True):
                self.rad_order = RadioButton(
                    items=['Random', 'Ascending', 'Descending'],
                    default_value='Random'
                )
                Spacer(width=30)
                self.rad_sign = RadioButton(
                    items=['Mixed', 'Positive', 'Negative'],
                    default_value='Mixed'
                )
            Spacer(height=8)
            self.btn_generate = Button('Generate sequence', events=True)
            self.btn_generate.width = 150


        @self.btn_generate.events.on_visible
        def position_button() -> None:
            btn_y = self.btn_generate.pos[1]
            btn_w = self.btn_generate.width
            self.btn_generate.pos = (self.width / 2 - btn_w / 2, btn_y)

            for child in self.btn_generate.events.children():
                if child.label == 'position_button':
                    child.show = False



class AlgorithmSelector(Window):
    def __init__(self) -> None:
        self.cfg = {
            'label': 'Algorithm selector',
            'min_size': [400, 600],
            'events': True
        }

class Display(Window):
    def __init__(self) -> None:
        self.cfg = {
            'label': 'Interactive display',
            'min_size': [800, 800],
            'no_collapse': True,
            'events': True
        }
        super().__init__(**self.cfg)

        with self:
            pass

    def clear(self):
        pass

    def update(self, sequence: list()) -> None:
        pass

    def draw(self):
        pass