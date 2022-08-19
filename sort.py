from collections import namedtuple


class StepGenerator:
    def __init__(self, sequence: list[int]) -> None:
        self.algorithms = {
            'Bubble sort': self.bubble_sort,
            'Insertion sort': self.insertion_sort,
            'Merge sort': self.run_merge_sort
        }

        self.sequence = sequence
        self.StepData = namedtuple('StepData', ['name', 'arg1', 'arg2'])
        # self.StepData = namedtuple('StepData', ['name', 'args'])


    def bubble_sort(self):
        swapped = False
        s = self.sequence

        for n in range(len(s)-1, 0, -1):
            for i in range(n):
                yield self.StepData(name='Compare', arg1=i, arg2=i+1) 
                if s[i] > s[i + 1]:
                    swapped = True
                    s[i], s[i+1] = s[i+1], s[i] 
                    yield self.StepData(name='Swap', arg1=i, arg2=i+1)
                else:
                    yield self.StepData(name='Continue', arg1=i, arg2=i+1)

            # if no swaps occur while passing over the list then it's sorted
            if not swapped:
                return

        yield self.StepData(name='End', arg1=0, arg2=0)

    def insertion_sort(self) -> None:
        s = self.sequence

        for step in range(1, len(s)):
            key = s[step]
            j = step - 1
                  
            # Add extra comparison & continue steps if we never enter 
            # the while loop
            if not (j >= 0 and key < s[j]):
                yield self.StepData(name='Compare', arg1=j, arg2=step) 
                yield self.StepData(name='Continue', arg1=j, arg2=step)

            while j >= 0 and key < s[j]:
                yield self.StepData(name='Compare', arg1=j, arg2=j+1) 
                s[j + 1] = s[j]
                yield self.StepData(name='Swap', arg1=j, arg2=j+1)
                j = j - 1
                yield self.StepData(name='Continue', arg1=j, arg2=step)
                
            s[j + 1] = key
            

        yield self.StepData(name='End', arg1=0, arg2=0)

    def run_merge_sort(self):
        def merge_sort(sequence: list, side: str):
            yield self.StepData(name='Group', arg1=sequence, arg2=side)

            if len(sequence) > 1:
                #  r is the point where the sequence is divided into 
                # two subsequences
                mid = len(sequence)//2
                left = sequence[:mid]
                right = sequence[mid:]

                yield self.StepData(name='Split', arg1=left, arg2=right)

                # yield self.StepData(name='Split', arg1=left, arg2='left')
                # yield self.StepData(name='Split', arg1=right, arg2='right')

                # Sort the two halves
                yield from merge_sort(left, 'left')
                yield from merge_sort(right, 'right')

                i = j = k = 0

                # Until we reach either end of either left or right, pick larger among
                # elements left and right and place them in the correct 
                # position at A[p..r]
                while i < len(left) and j < len(right):
                    if left[i] < right[j]:
                        sequence[k] = left[i]
                        i += 1
                    else:
                        sequence[k] = right[j]
                        j += 1

                    k += 1

                # When we run out of elements in either left or right,
                # pick up the remaining elements and put in A[p..r]
                while i < len(left):
                    sequence[k] = left[i]
                    i += 1
                    k += 1

                while j < len(right):
                    sequence[k] = right[j]
                    j += 1
                    k += 1

                yield self.StepData(name='ExitRecursion', arg1=None, arg2=None)
            

        generator = merge_sort(self.sequence, 0)
        
        return generator

