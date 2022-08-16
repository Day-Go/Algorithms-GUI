from collections import namedtuple


class StepGenerator:
    def __init__(self, sequence: list[int]) -> None:
        self.algorithms = {
            'Bubble sort': self.bubble_sort,
            'Insertion sort': self.insertion_sort,
            'Merge sort': self.run_merge_sort
        }

        self.sequence = sequence
        self.StepData = namedtuple('StepData', ['name', 'i1', 'i2'])


    def bubble_sort(self):
        swapped = False
        s = self.sequence

        for n in range(len(s)-1, 0, -1):
            for i in range(n):
                yield self.StepData(name='Compare', i1=i, i2=i+1) 
                if s[i] > s[i + 1]:
                    swapped = True
                    s[i], s[i+1] = s[i+1], s[i] 
                    yield self.StepData(name='GT', i1=i, i2=i+1)
                else:
                    yield self.StepData(name='LT', i1=i, i2=i+1)

            # if no swaps occur while passing over the list then it's sorted
            if not swapped:
                return

        yield self.StepData(name='End', i1=0, i2=0)

    def insertion_sort(self) -> None:
        s = self.sequence

        for step in range(1, len(s)):
            key = s[step]
            j = step - 1
                  
            while j >= 0 and key < s[j]:
                s[j + 1] = s[j]
                j = j - 1
                yield self.StepData(name='Shift Right', i1=step, i2=j)
            
            s[j + 1] = key
            yield self.StepData(name='Insert', i1=step, i2=j)


    def run_merge_sort(self):
        def merge_sort(sequence):
            
            if len(sequence) > 1:
                # Selecte sequence
                yield self.Operation(name='Select', data=sequence, indicies=1)

                #  r is the point where the sequence is divided into 
                # two subsequences
                r = len(sequence)//2
                L = sequence[:r]
                M = sequence[r:]

                # Sort the two halves
                yield from merge_sort(L)
                yield from merge_sort(M)

                i = j = k = 0

                # Until we reach either end of either L or M, pick larger among
                # elements L and M and place them in the correct 
                # position at A[p..r]
                while i < len(L) and j < len(M):
                    if L[i] < M[j]:
                        sequence[k] = L[i]
                        i += 1
                        # Comparison result: Left < Right -> Sorted
                        yield self.Operation(
                            name='Less',
                            data=sequence, 
                            indicies=2
                        )
                    else:
                        sequence[k] = M[j]
                        j += 1
                        # Comparison result: Left > Right
                        yield self.Operation(
                            name='Greater', 
                            data=sequence, 
                            indicies=3
                        )

                    k += 1

                # When we run out of elements in either L or M,
                # pick up the remaining elements and put in A[p..r]
                while i < len(L):
                    sequence[k] = L[i]
                    i += 1
                    k += 1

                    # Reorder
                    yield self.Operation(
                        name='Copy left', 
                        data=sequence, 
                        indicies=4
                    )


                while j < len(M):
                    sequence[k] = M[j]
                    j += 1
                    k += 1

                    # Perserve order

                    yield self.Operation(
                        name='Copy right', 
                        data=sequence, 
                        indicies=[]
                    )

            # Sorted array
            yield self.Operation(name='Sorted', data=sequence, indicies=6)
            

        generator = merge_sort(self.sequence)
        
        return generator

