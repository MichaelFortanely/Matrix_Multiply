# Created by Michael Fortanely on December 12, 2021
# Inspiration for this program provided by Abdul Bari
# 4.3 Matrix Chain Multiplication - Dynamic Programming: https://youtu.be/prx1psByp7U
import numpy
import numpy as np


class Matrix(object):

    def __init__(self, num_matrices):
        if num_matrices < 2:
            raise Exception('Must be at least two matrices')
        self.num_matrices = num_matrices
        self.dimensions = np.random.randint(1, 10, size=self.num_matrices + 1)
        self.matrices = self._gen_matrices()
        dim = []
        for i in range(1, len(self.dimensions)):
            if i == 1:
                dim = [(self.dimensions[i - 1], self.dimensions[i])]
            else:
                dim.append((self.dimensions[i - 1], self.dimensions[i]))
        self.dimensions = dim

    def _gen_matrices(self):
        # create a specified number of matrices with random dimensions that can be multiple together
        _list = list()
        for i in range(1, len(self.dimensions)):
            if i == 1:
                _list = [np.array(np.random.randint(1, 10, self.dimensions[i - 1] * self.dimensions[i]))]
            else:
                _list.append(np.random.randint(1, 10, self.dimensions[i - 1] * self.dimensions[i]))
            _list[len(_list) - 1] = np.reshape(_list[len(_list) - 1], (self.dimensions[i - 1], self.dimensions[i]))
        return _list

    def show_matrices(self):
        for dims, matrix in zip(self.dimensions, self.matrices):
            print('{}\n{}\n'.format(dims, matrix))

    def optimal_multiplication(self):
        # Use DP to calculate the optimal way to multiple them together
        ans = [[0 for x in range(self.num_matrices)] for y in range(self.num_matrices)]
        choices = [['None' for x in range(self.num_matrices)] for y in range(self.num_matrices)]
        for i in range(self.num_matrices - 1):
            for j in range(self.num_matrices - i - 1):
                if i == 0:
                    ans[j][i + j + 1] = self.dimensions[j][0] * self.dimensions[j + 1][0] * self.dimensions[j + 1][1]
                else:
                    # one to the left and then the one below
                    left = ans[j][i + j] + self.dimensions[j][0] * self.dimensions[i + j + 1][0] * \
                           self.dimensions[i + j + 1][1]
                    bottom = ans[j + 1][i + j + 1] + (
                                self.dimensions[j][0] * self.dimensions[j][1] * self.dimensions[i + j + 1][1])
                    if left <= bottom:
                        choice = 'Left'
                    else:
                        choice = 'Down'
                    ans[j][i + j + 1] = min(left, bottom)
                    choices[j][i + j + 1] = choice

        self.show_optimal(ans, choices)

    def show_optimal(self, ans, choices):
        self.pretty_print(ans)
        for choice in choices:
            print(choice)
        construct = ''
        i = 0
        j = self.num_matrices - 1
        offset = 0
        while True:
            word = choices[i][j]
            if word == 'Left':
                new_j = j - 1
                new_i = i
            elif word == 'Down':
                new_j = j
                new_i = i + 1
            else:
                if construct:
                    start, end = self._get_indices(construct, offset)
                    # base case 1 -> put last parentheses if there are > 2 matrices
                    construct = construct[0: start + 1] + '{}, {}'.format(str(i), str(j)) + construct[end:]
                else:
                    construct = '({}, {})'.format(i, j)
                    # base case 2 -> there are only two matrices to analyze
                break
            if construct:
                start, end = self._get_indices(construct, offset)
                if word == 'Left':
                    construct = construct[0: start + 1] + '(), {}'.format(j) + construct[end:]
                else:
                    construct = construct[0: start + 1] + '{}, ()'.format(i) + construct[end:]
            else:
                if word == 'Left':
                    construct = '(), {}'.format(j)
                    # starting case 1
                else:
                    construct = '{}, ()'.format(i)
                    # starting case 2
            offset += 1
            i = new_i
            j = new_j
        print('The optimal way to multiple the matrices is {}'.format(construct))


    def pretty_print(self, matrix):
        # Code for pretty printing an array from https://stackoverflow.com/questions/13214809/pretty-print-2d-list
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))

    def _get_indices(self, construct, offset):
        # start and end are the indices of the parentheses
        copy_offset = offset
        start, end = 0, len(construct) - 1
        while offset:
            if construct[start] == '(':
                offset -= 1
            start += 1
        while copy_offset:
            if construct[end] == ')':
                copy_offset -= 1
            end -= 1
        return start - 1, end + 1
