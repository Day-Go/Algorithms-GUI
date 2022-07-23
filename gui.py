import random
from dearpypixl import Application, Viewport
from windows import SequenceGenerator, AlgorithmSelector, Display


class GUI(Application, Viewport):
    def __init__(self) -> None:
        self.maximize = True

        self.sequence_generator = SequenceGenerator()
        self.algorithm_selector = AlgorithmSelector()
        self.display = Display()

        @self.sequence_generator.btn_generate.events.on_click
        def generate_sequence() -> None:
            rng = random.Random(self.sequence_generator.inp_rng_seed.value)

            s_len = self.sequence_generator.inp_length.value
            v_max = self.sequence_generator.inp_max.value
            
            sequence = [rng.randint(-v_max, v_max) for _ in range(s_len)]

            order = self.sequence_generator.rad_order.value
            sign = self.sequence_generator.rad_sign.value

            if sign == 'Positive':
                sequence = [abs(v) for v in sequence]
            elif sign == 'Negative':
                sequence = [-abs(v) for v in sequence]

            if order == 'Ascending':
                sequence.sort()
            elif order == 'Descending':
                sequence.sort(reverse=True)

            print(sequence)

        self.start()